from aiohttp import web
from aiohttp_jinja2 import render_template
from app.database.engine import async_session
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.conversation_repo import ConversationRepository
from app.database.repositories.memory_repo import MemoryRepository
from app.database.repositories.summary_repo import SummaryRepository
from app.admin_panel.auth import require_auth
from sqlalchemy import select
from app.database.models.user import User
import logging

logger = logging.getLogger(__name__)


@require_auth
async def users_page(request: web.Request) -> web.Response:
    search = request.query.get("search", "")
    page = int(request.query.get("page", 1))
    per_page = 20
    offset = (page - 1) * per_page

    async with async_session() as session:
        user_repo = UserRepository(session)

        if search:
            users = await user_repo.search(search)
        else:
            users = await user_repo.get_all(offset=offset, limit=per_page)

        return render_template("users.html", request, {
            "admin": request["admin"],
            "users": users,
            "search": search,
            "page": page,
        })


@require_auth
async def user_detail_page(request: web.Request) -> web.Response:
    user_id = int(request.match_info["user_id"])

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise web.HTTPNotFound()

        memory_repo = MemoryRepository(session)
        conv_repo = ConversationRepository(session)
        summary_repo = SummaryRepository(session)

        memories = await memory_repo.get_by_user(user.id)
        history = await conv_repo.get_history(user.id, limit=50)
        summaries = await summary_repo.get_all_for_user(user.id)

        return render_template("user_detail.html", request, {
            "admin": request["admin"],
            "user": user,
            "memories": memories,
            "history": history,
            "summaries": summaries,
        })


@require_auth
async def delete_user(request: web.Request) -> web.Response:
    user_id = int(request.match_info["user_id"])

    async with async_session() as session:
        user_repo = UserRepository(session)
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if user:
            await user_repo.soft_delete(user)

    raise web.HTTPFound("/users")
