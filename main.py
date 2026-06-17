"""
Main entry point for Render deployment.
Web server binds FIRST, then bot starts up in background.
"""
import asyncio
import logging
import os
import sys
from aiohttp import web
import sqlalchemy

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

    for attempt in range(1, 6):
        try:
            async with engine.begin() as conn:
                try:
                    await conn.execute(sqlalchemy.text(
                        "CREATE EXTENSION IF NOT EXISTS vector"
                    ))
                    logger.info("pgvector extension enabled")
                    has_pgvector = True
                except Exception:
                    logger.warning("pgvector not available - embedding search disabled")
                    has_pgvector = False

                if has_pgvector:
                    await conn.run_sync(Base.metadata.create_all)
                    logger.info("All tables created")
                else:
                    non_embed = [t for t in Base.metadata.sorted_tables if t.name != "embeddings"]
                    for t in non_embed:
                        await conn.run_sync(t.create, checkfirst=True)
                    logger.info("Tables created (embeddings skipped)")
            break
        except Exception as e:
            if attempt < 5:
                logger.warning(f"DB attempt {attempt}/5: {e}")
                await asyncio.sleep(5 * attempt)
            else:
                logger.error(f"DB failed: {e}")
                return

    try:
        async with async_session() as session:
            count = await load_knowledge_base(session)
            logger.info(f"Knowledge base loaded: {count} chunks")
    except Exception as e:
        logger.warning(f"Knowledge base skipped: {e}")

    logger.info("Startup complete")


async def on_shutdown(bot: Bot):
    logger.info("Shutting down...")
    await engine.dispose()


async def health_handler(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok", "service": "edubot-ai"})


async def start_bot():
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

    await dp.start_polling(bot)


async def main():
    admin_app = create_admin_app()
    admin_app.router.add_get("/", health_handler)
    admin_app.router.add_get("/health", health_handler)

    port = int(os.environ.get("PORT", 10000))

    runner = web.AppRunner(admin_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()
    logger.info(f"Web server on port {port}")

    try:
        await start_bot()
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        await asyncio.sleep(3600)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
