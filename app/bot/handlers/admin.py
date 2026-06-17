from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config.settings import settings
from app.database.engine import async_session
from app.database.models.user import User
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.conversation_repo import ConversationRepository
from app.database.repositories.memory_repo import MemoryRepository
from app.database.repositories.lead_repo import LeadRepository
from app.database.repositories.enrollment_repo import EnrollmentRepository
import logging

logger = logging.getLogger(__name__)
router = Router()
PAGE_SIZE = 5


def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


async def admin_check(message: Message) -> bool:
    if not is_admin(message.from_user.id):
        await message.answer("Access denied.")
        return False
    return True


async def admin_check_cb(callback: CallbackQuery) -> bool:
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied.", show_alert=True)
        return False
    return True


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not await admin_check(message):
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Dashboard", callback_data="adm:dashboard")],
        [InlineKeyboardButton(text="Users", callback_data="adm:users:0")],
        [InlineKeyboardButton(text="Conversations", callback_data="adm:convs")],
        [InlineKeyboardButton(text="Leads", callback_data="adm:leads")],
        [InlineKeyboardButton(text="Search User", callback_data="adm:search")],
    ])
    await message.answer("Admin Panel", reply_markup=kb)


@router.callback_query(F.data.startswith("adm:dashboard"))
async def cb_dashboard(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()

    async with async_session() as session:
        user_repo = UserRepository(session)
        enroll_repo = EnrollmentRepository(session)

        total = await user_repo.count_all()
        enrolled = await enroll_repo.count()
        hot = await user_repo.count_by_lead_status("hot")
        warm = await user_repo.count_by_lead_status("warm")
        cold = await user_repo.count_by_lead_status("cold")

    text = (
        f"Dashboard\n"
        f"Total Users: {total}\n"
        f"Enrolled: {enrolled}\n"
        f"Hot Leads: {hot}\n"
        f"Warm Leads: {warm}\n"
        f"Cold Leads: {cold}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data="adm:back")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data.startswith("adm:users:"))
async def cb_users(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()

    page = int(callback.data.split(":")[2])
    offset = page * PAGE_SIZE

    async with async_session() as session:
        user_repo = UserRepository(session)
        users = await user_repo.get_all(offset=offset, limit=PAGE_SIZE)
        total = await user_repo.count_all()

    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    if not users:
        text = "No users found."
    else:
        lines = []
        for u in users:
            name = u.full_name or u.username or str(u.telegram_id)
            status = "active" if u.is_active else "inactive"
            lines.append(f"[{u.id}] {name} ({u.lead_status}, {status})")
        text = f"Users (page {page + 1}/{total_pages}):\n\n" + "\n".join(lines)

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="Prev", callback_data=f"adm:users:{page - 1}"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton(text="Next", callback_data=f"adm:users:{page + 1}"))

    kb_buttons = []
    if nav:
        kb_buttons.append(nav)
    if users:
        for u in users:
            name = u.full_name or u.username or str(u.telegram_id)
            kb_buttons.append([InlineKeyboardButton(text=f"View {name}", callback_data=f"adm:user:{u.id}")])
    kb_buttons.append([InlineKeyboardButton(text="Back", callback_data="adm:back")])

    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb_buttons))


@router.callback_query(F.data.startswith("adm:user:"))
async def cb_user_detail(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()

    user_id = int(callback.data.split(":")[2])

    async with async_session() as session:
        user_repo = UserRepository(session)
        memory_repo = MemoryRepository(session)
        conv_repo = ConversationRepository(session)
        enroll_repo = EnrollmentRepository(session)
        lead_repo = LeadRepository(session)

        user = await user_repo.get_by_id(user_id)
        if not user:
            await callback.message.edit_text("User not found.")
            return

        memories = await memory_repo.get_by_user(user.id)
        history = await conv_repo.get_history(user.id, limit=5)
        enrollment = await enroll_repo.get_by_user(user.id)

    text = (
        f"User #{user.id}\n"
        f"Name: {user.full_name or 'N/A'}\n"
        f"Username: @{user.username or 'N/A'}\n"
        f"Telegram ID: {user.telegram_id}\n"
        f"Phone: {user.phone or 'N/A'}\n"
        f"Age: {user.age or 'N/A'}\n"
        f"English Level: {user.english_level or 'N/A'}\n"
        f"Goal: {user.goal or 'N/A'}\n"
        f"Lead Status: {user.lead_status}\n"
        f"Enrolled: {'Yes' if user.is_enrolled else 'No'}\n"
        f"Active: {'Yes' if user.is_active else 'No'}\n"
        f"Language: {user.language}\n"
        f"Last Interaction: {user.last_interaction.strftime('%Y-%m-%d %H:%M') if user.last_interaction else 'N/A'}\n"
        f"Created: {user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'N/A'}"
    )

    if enrollment:
        text += (
            f"\n\nEnrollment:\n"
            f"  Status: {enrollment.status}\n"
            f"  Name: {enrollment.full_name}\n"
            f"  Phone: {enrollment.phone}\n"
            f"  Level: {enrollment.english_level}\n"
            f"  Goal: {enrollment.goal}\n"
            f"  Time: {enrollment.preferred_time}"
        )

    if memories:
        text += "\n\nMemories:\n"
        for m in memories:
            text += f"  {m.key}: {m.value[:50]}\n"

    if history:
        text += "\nLast Messages:\n"
        for msg in history:
            prefix = "User" if msg.role == "user" else "Bot"
            text += f"  {prefix}: {msg.content[:80]}\n"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="History", callback_data=f"adm:userhist:{user.id}"),
            InlineKeyboardButton(text="Conversations", callback_data=f"adm:userconv:{user.id}"),
        ],
        [
            InlineKeyboardButton(text="Set Hot", callback_data=f"adm:setlead:{user.id}:hot"),
            InlineKeyboardButton(text="Set Warm", callback_data=f"adm:setlead:{user.id}:warm"),
            InlineKeyboardButton(text="Set Cold", callback_data=f"adm:setlead:{user.id}:cold"),
        ],
        [
            InlineKeyboardButton(text="Deactivate", callback_data=f"adm:deactivate:{user.id}"),
        ],
        [InlineKeyboardButton(text="Back to Users", callback_data="adm:users:0")],
    ])
    await callback.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data.startswith("adm:userhist:"))
async def cb_user_history(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()

    user_id = int(callback.data.split(":")[2])

    async with async_session() as session:
        conv_repo = ConversationRepository(session)
        history = await conv_repo.get_full_history(user_id)

    if not history:
        text = "No message history."
    else:
        lines = []
        for msg in history[-30:]:
            prefix = "User" if msg.role == "user" else "Bot"
            lines.append(f"{prefix}: {msg.content[:100]}")
        text = f"Message History ({len(history)} total):\n\n" + "\n".join(lines)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data=f"adm:user:{user_id}")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data.startswith("adm:userconv:"))
async def cb_user_conv(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()

    user_id = int(callback.data.split(":")[2])

    async with async_session() as session:
        conv_repo = ConversationRepository(session)
        history = await conv_repo.get_history(user_id, limit=10)

    if not history:
        text = "No recent messages."
    else:
        lines = []
        for msg in history:
            prefix = "User" if msg.role == "user" else "Bot"
            lines.append(f"{prefix}: {msg.content[:120]}")
        text = f"Recent Messages:\n\n" + "\n".join(lines)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data=f"adm:user:{user_id}")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data.startswith("adm:setlead:"))
async def cb_set_lead(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer("Status updated")

    parts = callback.data.split(":")
    user_id = int(parts[2])
    new_status = parts[3]

    async with async_session() as session:
        lead_repo = LeadRepository(session)
        await lead_repo.update_status(user_id, new_status, f"Updated by admin {callback.from_user.id}")

    await callback.message.edit_text(f"Lead status updated to {new_status}")


@router.callback_query(F.data.startswith("adm:deactivate:"))
async def cb_deactivate(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer("User deactivated")

    user_id = int(callback.data.split(":")[2])

    async with async_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_id(user_id)
        if user:
            await user_repo.soft_delete(user)

    await callback.message.edit_text(f"User #{user_id} deactivated")


@router.callback_query(F.data == "adm:convs")
async def cb_conversations(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()

    async with async_session() as session:
        user_repo = UserRepository(session)
        conv_repo = ConversationRepository(session)
        users = await user_repo.get_all(limit=10)

    if not users:
        text = "No users."
    else:
        lines = []
        for u in users:
            msgs = await conv_repo.get_history(u.id, limit=1)
            last = msgs[0].content[:50] if msgs else "No messages"
            name = u.full_name or u.username or str(u.telegram_id)
            lines.append(f"[{u.id}] {name}: {last}")
        text = "Conversations:\n\n" + "\n".join(lines)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data="adm:back")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data == "adm:leads")
async def cb_leads(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()

    async with async_session() as session:
        user_repo = UserRepository(session)
        hot = await user_repo.count_by_lead_status("hot")
        warm = await user_repo.count_by_lead_status("warm")
        cold = await user_repo.count_by_lead_status("cold")
        enrolled = await user_repo.count_by_lead_status("enrolled")

    text = (
        f"Lead Overview:\n\n"
        f"Hot: {hot}\n"
        f"Warm: {warm}\n"
        f"Cold: {cold}\n"
        f"Enrolled: {enrolled}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="View Hot Leads", callback_data="adm:leadsby:hot")],
        [InlineKeyboardButton(text="View Warm Leads", callback_data="adm:leadsby:warm")],
        [InlineKeyboardButton(text="Back", callback_data="adm:back")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data.startswith("adm:leadsby:"))
async def cb_leads_by(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()

    status = callback.data.split(":")[2]

    async with async_session() as session:
        user_repo = UserRepository(session)
        users = await user_repo.get_all(limit=100)
        filtered = [u for u in users if u.lead_status == status]

    if not filtered:
        text = f"No {status} leads."
    else:
        lines = []
        for u in filtered[:20]:
            name = u.full_name or u.username or str(u.telegram_id)
            lines.append(f"[{u.id}] {name}")
        text = f"{status.title()} Leads ({len(filtered)}):\n\n" + "\n".join(lines)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data="adm:leads")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data == "adm:search")
async def cb_search(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()
    await callback.message.edit_text(
        "Send the search query (name, username, or phone):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Cancel", callback_data="adm:back")]
        ])
    )


@router.callback_query(F.data == "adm:back")
async def cb_back(callback: CallbackQuery):
    if not await admin_check_cb(callback):
        return
    await callback.answer()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Dashboard", callback_data="adm:dashboard")],
        [InlineKeyboardButton(text="Users", callback_data="adm:users:0")],
        [InlineKeyboardButton(text="Conversations", callback_data="adm:convs")],
        [InlineKeyboardButton(text="Leads", callback_data="adm:leads")],
        [InlineKeyboardButton(text="Search User", callback_data="adm:search")],
    ])
    await callback.message.edit_text("Admin Panel", reply_markup=kb)


@router.message(F.text & ~F.command, F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_search_handler(message: Message):
    if not await admin_check(message):
        return

    async with async_session() as session:
        user_repo = UserRepository(session)
        users = await user_repo.search(message.text)

    if not users:
        await message.answer("No users found.")
        return

    kb = []
    for u in users[:10]:
        name = u.full_name or u.username or str(u.telegram_id)
        kb.append([InlineKeyboardButton(text=f"[{u.id}] {name}", callback_data=f"adm:user:{u.id}")])
    kb.append([InlineKeyboardButton(text="Back", callback_data="adm:back")])

    await message.answer(f"Found {len(users)} users:", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
