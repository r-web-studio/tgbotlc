from aiogram import Router
from app.bot.handlers.start import router as start_router
from app.bot.handlers.menu import router as menu_router
from app.bot.handlers.enrollment import router as enrollment_router
from app.bot.handlers.admin import router as admin_router
from app.bot.handlers.chat import router as chat_router

def setup_handlers(main_router: Router):
    main_router.include_router(start_router)
    main_router.include_router(menu_router)
    main_router.include_router(enrollment_router)
    main_router.include_router(admin_router)
    main_router.include_router(chat_router)
