from aiohttp import web
from app.database.engine import async_session
from app.database.repositories.user_repo import UserRepository
from app.admin_panel.auth import require_auth
import io
from openpyxl import Workbook
from datetime import datetime


@require_auth
async def export_users(request: web.Request) -> web.Response:
    async with async_session() as session:
        user_repo = UserRepository(session)
        users = await user_repo.get_all(limit=10000)

        wb = Workbook()
        ws = wb.active
        ws.title = "Users"

        headers = [
            "ID", "Telegram ID", "Username", "Full Name", "Age", "Phone",
            "English Level", "Goal", "Lead Status", "Enrolled", "Created At",
        ]
        ws.append(headers)

        for user in users:
            ws.append([
                user.id,
                user.telegram_id,
                user.username or "",
                user.full_name or "",
                user.age or "",
                user.phone or "",
                user.english_level or "",
                user.goal or "",
                user.lead_status,
                "Yes" if user.is_enrolled else "No",
                user.created_at.strftime("%Y-%m-%d %H:%M") if user.created_at else "",
            ])

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return web.Response(
            body=output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            },
        )
