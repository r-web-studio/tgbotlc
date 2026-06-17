from aiohttp import web
import aiohttp_jinja2
import jinja2
from app.admin_panel.routes import setup_routes
from app.admin_panel.auth import setup_session_middleware
import logging
import os

logger = logging.getLogger(__name__)


def create_admin_app() -> web.Application:
    app = web.Application()

    setup_session_middleware(app)

    # Setup Jinja2 template loader
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(templates_dir)
    )

    setup_routes(app)

    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.makedirs(static_dir, exist_ok=True)
    app.router.add_static("/static/", static_dir, name="static")

    logger.info("Admin panel app created")
    return app
