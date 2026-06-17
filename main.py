"""
Main entry point for Render deployment.
Includes web server for health checks and bot polling.
"""
import asyncio
import logging
import os
import sys
from aiohttp import web

from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config.settings import settings
from app.database.engine import engine, async_session
from app.database.models import Base
from app.bot.middlewares.database import DatabaseMiddleware
from app.bot.middlewares.language import LanguageMiddleware
from app.bot.middlewares.rate_limit import RateLimitMiddleware
from app.bot.handlers import setup_handlers
from app.rag.chain import load_knowledge_base
from app.admin_panel.app import create_admin_app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    logger.info("Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")
    async with async_session() as session:
        count = await load_knowledge_base(session)
        logger.info(f"Knowledge base loaded: {count} chunks")
    logger.info("Startup complete")


async def on_shutdown(bot: Bot):
    logger.info("Shutting down...")
    await engine.dispose()
    logger.info("Shutdown complete")


async def health_handler(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok", "service": "edubot-ai"})


async def main():
    logger.info("Initializing bot...")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(LanguageMiddleware())
    dp.message.middleware(RateLimitMiddleware(limit=1, period=60))
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())

    router = Router()
    setup_handlers(router)
    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    admin_app = create_admin_app()
    admin_app.router.add_get("/", health_handler)
    admin_app.router.add_get("/health", health_handler)

    port = int(os.environ.get("PORT", 10000))

    runner = web.AppRunner(admin_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)

    logger.info(f"Starting web server on port {port}...")

    await site.start()

    logger.info(f"Web server running on port {port}. Starting bot polling...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
