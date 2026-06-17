"""
Vercel serverless function entry point for the admin panel.
Delegates to the aiohttp admin app.
"""
import os
import sys
import json
import asyncio
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from dotenv import load_dotenv
load_dotenv()

from aiohttp import web
from app.admin_panel.app import create_admin_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the aiohttp app once (reused across warm starts)
_app = None


def get_app() -> web.Application:
    global _app
    if _app is None:
        _app = create_admin_app()
    return _app


app = get_app()


# Vercel uses the ASGI/WSGI interface or handler class
# For aiohttp, we use the app as a handler
handler = app
