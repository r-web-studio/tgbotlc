from aiohttp import web
from aiohttp_jinja2 import render_template
from app.admin_panel.auth import create_session_token, verify_password, hash_password
from app.config.settings import settings
from app.database.engine import async_session
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.enrollment_repo import EnrollmentRepository
import logging

logger = logging.getLogger(__name__)


async def login_page(request: web.Request) -> web.Response:
    if request.get("admin"):
        raise web.HTTPFound("/")
    return render_template("login.html", request, {"error": None})


async def login_handler(request: web.Request) -> web.Response:
    data = await request.post()
    username = data.get("username", "")
    password = data.get("password", "")

    if username == settings.ADMIN_USERNAME and verify_password(password, hash_password(settings.ADMIN_PASSWORD)):
        token = create_session_token(username)
        resp = web.Response(status=302, headers={"Location": "/"})
        resp.set_cookie("admin_session", token, max_age=86400 * 7, httponly=True)
        raise resp

    return render_template("login.html", request, {"error": "Invalid credentials"})


async def logout_handler(request: web.Request) -> web.Response:
    resp = web.Response(status=302, headers={"Location": "/login"})
    resp.del_cookie("admin_session")
    raise resp


async def dashboard_page(request: web.Request) -> web.Response:
    if not request.get("admin"):
        raise web.HTTPFound("/login")

    async with async_session() as session:
        user_repo = UserRepository(session)
        enrollment_repo = EnrollmentRepository(session)

        total_users = await user_repo.count_all()
        enrolled = await enrollment_repo.count()
        hot_leads = await user_repo.count_by_lead_status("hot")
        warm_leads = await user_repo.count_by_lead_status("warm")
        cold_leads = await user_repo.count_by_lead_status("cold")

        return render_template("dashboard.html", request, {
            "admin": request["admin"],
            "total_users": total_users,
            "enrolled": enrolled,
            "hot_leads": hot_leads,
            "warm_leads": warm_leads,
            "cold_leads": cold_leads,
        })
