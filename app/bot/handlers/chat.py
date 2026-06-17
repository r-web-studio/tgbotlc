import re
import logging
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.conversation_repo import ConversationRepository
from app.database.repositories.memory_repo import MemoryRepository
from app.database.repositories.summary_repo import SummaryRepository
from app.rag.retriever import RAGRetriever
from app.ai.client import openrouter_client
from app.ai.prompts import SYSTEM_PROMPT
from app.ai.detector import IntentDetector
from app.utils.language import TRANSLATIONS

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text)
async def chat_handler(message: Message, session: AsyncSession, language: str = "en"):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(message.from_user.id)

    if not user:
        user = await user_repo.create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language=language
        )

    await user_repo.update_last_interaction(user)

    user_text = message.text.strip()

    conv_repo = ConversationRepository(session)
    await conv_repo.add_message(user.id, "user", user_text, language)

    intent = IntentDetector.detect_intent(user_text)
    lead_signal = IntentDetector.detect_lead_signal(user_text)

    if lead_signal and user.lead_status != "enrolled":
        from app.database.repositories.lead_repo import LeadRepository
        lead_repo = LeadRepository(session)
        await lead_repo.update_status(user.id, lead_signal, f"Detected signal: {intent}")

    memory_repo = MemoryRepository(session)
    user_memories = await memory_repo.get_all_by_user_as_dict(user.id)
    user_info_str = "\n".join([f"- {k}: {v}" for k, v in user_memories.items()]) if user_memories else "No information collected yet."

    summary_repo = SummaryRepository(session)
    latest_summary = await summary_repo.get_latest(user.id)
    conversation_summary = latest_summary.summary if latest_summary else "No previous conversation summary."

    rag_retriever = RAGRetriever(session)
    context = await rag_retriever.retrieve_context(user_text)
    if not context:
        context = "No specific information found in knowledge base for this query."

    system_prompt = SYSTEM_PROMPT.format(
        user_info=user_info_str,
        conversation_summary=conversation_summary,
        context=context
    )

    history = await conv_repo.get_history(user.id, limit=10)
    messages = [{"role": "system", "content": system_prompt}]

    for h in history:
        messages.append({"role": h.role, "content": h.content})

    messages.append({"role": "user", "content": user_text})

    try:
        response = await openrouter_client.chat(messages)
        logger.info(f"AI response for user {message.from_user.id}: {response[:100]}")
    except Exception as e:
        logger.error(f"AI error for user {message.from_user.id}: {e}")
        t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
        response = t.get("error", "I'm sorry, something went wrong. Please try again.")

    await conv_repo.add_message(user.id, "assistant", response, language)

    await _extract_info(session, user.id, user_text, response)

    msg_count = await conv_repo.get_message_count(user.id)
    if msg_count > 0 and msg_count % 20 == 0:
        await _create_summary(session, user.id, conv_repo, summary_repo)

    await message.answer(response)

async def _extract_info(session: AsyncSession, user_id: int, user_text: str, ai_response: str):
    memory_repo = MemoryRepository(session)
    text_lower = user_text.lower()

    name_patterns = ["my name is", "i'm", "i am", "меня зовут", "мени исмим"]
    for pattern in name_patterns:
        if pattern in text_lower:
            idx = text_lower.index(pattern) + len(pattern)
            name = user_text[idx:].strip().split(".")[0].split(",")[0].strip()
            if name and len(name) < 100:
                await memory_repo.upsert(user_id, "full_name", name, "info")

    phone_match = re.search(r'\+?\d{10,15}', user_text)
    if phone_match:
        await memory_repo.upsert(user_id, "phone", phone_match.group(), "info")

    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    for level in levels:
        if level.lower() in text_lower:
            await memory_repo.upsert(user_id, "english_level", level, "info")

    goals = ["ielts", "toefl", "business", "travel", "work", "study", "general"]
    for goal in goals:
        if goal in text_lower:
            await memory_repo.upsert(user_id, "goal", goal, "preference")

async def _create_summary(session: AsyncSession, user_id: int, conv_repo, summary_repo):
    history = await conv_repo.get_full_history(user_id)
    if not history:
        return

    conversation_text = "\n".join([f"{h.role}: {h.content}" for h in history[-20:]])

    try:
        summary_prompt = f"Summarize this conversation concisely, noting key user information, interests, and next steps:\n\n{conversation_text}"
        summary = await openrouter_client.chat([{"role": "user", "content": summary_prompt}], max_tokens=300)
        await summary_repo.create(user_id, summary, message_count=len(history))
    except Exception:
        pass
