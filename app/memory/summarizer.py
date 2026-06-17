from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.conversation_repo import ConversationRepository
from app.database.repositories.summary_repo import SummaryRepository
from app.ai.client import openrouter_client
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class ConversationSummarizer:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.conv_repo = ConversationRepository(session)
        self.summary_repo = SummaryRepository(session)
    
    async def summarize_if_needed(self, user_id: int, force: bool = False) -> bool:
        msg_count = await self.conv_repo.get_message_count(user_id)
        
        if not force and msg_count % 20 != 0:
            return False
        
        if msg_count < 5:
            return False
        
        return await self.create_summary(user_id)
    
    async def create_summary(self, user_id: int) -> bool:
        try:
            latest_summary = await self.summary_repo.get_latest(user_id)
            since = latest_summary.created_at if latest_summary else None
            
            messages = await self.conv_repo.get_recent_for_summary(user_id, since)
            if len(messages) < 5:
                return False
            
            conversation_text = "\n".join([
                f"{'User' if m.role == 'user' else 'Assistant'}: {m.content}" 
                for m in messages
            ])
            
            prompt = f"""Analyze this conversation and create a concise summary. Include:
1. Main topics discussed
2. User's interests and needs
3. Information collected (name, level, goals, etc.)
4. Current status in the enrollment journey
5. Key points to remember for next conversation

Conversation:
{conversation_text}

Provide a structured summary:"""
            
            response = await openrouter_client.chat(
                [{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            # Extract key points
            key_points = {
                "topics": [],
                "collected_info": {},
                "status": "active",
                "next_steps": []
            }
            
            latest_memories = await self._get_user_info_from_messages(messages)
            key_points["collected_info"] = latest_memories
            
            await self.summary_repo.create(
                user_id=user_id,
                summary=response,
                key_points=json.dumps(key_points),
                message_count=len(messages)
            )
            
            logger.info(f"Created summary for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create summary for user {user_id}: {e}")
            return False
    
    async def _get_user_info_from_messages(self, messages) -> dict:
        info = {}
        for msg in messages:
            if msg.role == "user":
                text = msg.content.lower()
                if any(p in text for p in ["my name is", "меня зовут"]):
                    info["discussed_name"] = True
                if any(p in text for p in ["b1", "b2", "a1", "a2", "c1"]):
                    info["discussed_level"] = True
                if "ielts" in text:
                    info["interested_in_ielts"] = True
        return info
    
    async def get_context_summary(self, user_id: int) -> str:
        latest = await self.summary_repo.get_latest(user_id)
        if latest:
            return latest.summary
        return "No previous conversation summary available."
