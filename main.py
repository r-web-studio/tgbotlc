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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    """Initialize database and knowledge base on startup."""
    logger.info("Starting up...")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")

    # Load knowledge base
    async with async_session() as session:
        count = await load_knowledge_base(session)
        logger.info(f"Knowledge base loaded: {count} chunks")

    logger.info("Startup complete")


async def on_shutdown(bot: Bot):
    """Cleanup on shutdown."""
    logger.info("Shutting down...")
    await engine.dispose()
    logger.info("Shutdown complete")


async def health_handler(request: web.Request) -> web.Response:
    """Health check endpoint for Render."""
    return web.json_response({
        "status": "ok",
        "service": "edubot-ai",
        "version": "1.0.0"
    })


async def main():
    """Main function - runs bot polling and web server concurrently."""
    logger.info("Initializing bot...")

    # Create bot
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Create dispatcher
    dp = Dispatcher()

    # Setup middlewares
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(LanguageMiddleware())
    dp.message.middleware(RateLimitMiddleware(limit=1, period=60))
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())

    # Setup handlers
    router = Router()
    setup_handlers(router)
    dp.include_router(router)

    # Startup/shutdown
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Create admin panel app
    admin_app = create_admin_app()

    # Add health check route
    admin_app.router.add_get("/", health_handler)
    admin_app.router.add_get("/health", health_handler)

    # Get port from environment (Render provides this)
    port = int(os.environ.get("PORT", 8080))

    logger.info(f"Bot initialized, starting on port {port}...")

    # Create web runner
    runner = web.AppRunner(admin_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)

    try:
        # Run bot polling and web server concurrently
        await asyncio.gather(
            dp.start_polling(bot),
            site.start(),
        )
    except KeyboardInterrupt:
        pass
    finally:
        await runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
