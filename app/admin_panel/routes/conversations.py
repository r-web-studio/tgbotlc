from aiohttp import web
from aiohttp_jinja2 import render_template
from app.database.engine import async_session
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.conversation_repo import ConversationRepository
from app.admin_panel.auth import require_auth
from sqlalchemy import select
from app.database.models.user import User
import logging

logger = logging.getLogger(__name__)


@require_auth
async def conversations_page(request: web.Request) -> web.Response:
    async with async_session() as session:
        user_repo = UserRepository(session)
        conv_repo = ConversationRepository(session)

        users = await user_repo.get_all(limit=100)
        user_conversations = []

        for user in users:
            msgs = await conv_repo.get_history(user.id, limit=1)
            last_msg = msgs[0] if msgs else None
            user_conversations.append({
                "user": user,
                "last_message": last_msg,
            })

        return render_template("conversations.html", request, {
            "admin": request["admin"],
            "conversations": user_conversations,
        })


@require_auth
async def conversation_detail(request: web.Request) -> web.Response:
    user_id = int(request.match_info["user_id"])

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise web.HTTPNotFound()

        conv_repo = ConversationRepository(session)
        history = await conv_repo.get_full_history(user.id)

        return render_template("conversation_detail.html", request, {
            "admin": request["admin"],
            "user": user,
            "history": history,
        })
