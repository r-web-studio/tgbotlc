from aiohttp import web
from aiohttp_jinja2 import render_template
from app.database.engine import async_session
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.lead_repo import LeadRepository
from app.admin_panel.auth import require_auth
import logging

logger = logging.getLogger(__name__)


@require_auth
async def leads_page(request: web.Request) -> web.Response:
    async with async_session() as session:
        user_repo = UserRepository(session)

        all_users = await user_repo.get_all(limit=100)
        hot_users = [u for u in all_users if u.lead_status == "hot"]
        warm_users = [u for u in all_users if u.lead_status == "warm"]
        cold_users = [u for u in all_users if u.lead_status == "cold"]
        enrolled_users = [u for u in all_users if u.lead_status == "enrolled"]

        return render_template("leads.html", request, {
            "admin": request["admin"],
            "hot_users": hot_users,
            "warm_users": warm_users,
            "cold_users": cold_users,
            "enrolled_users": enrolled_users,
        })


@require_auth
async def update_lead_status(request: web.Request) -> web.Response:
    user_id = int(request.match_info["user_id"])
    data = await request.post()
    new_status = data.get("status", "cold")

    async with async_session() as session:
        lead_repo = LeadRepository(session)
        await lead_repo.update_status(user_id, new_status, "Updated via admin panel")

    raise web.HTTPFound("/leads")
