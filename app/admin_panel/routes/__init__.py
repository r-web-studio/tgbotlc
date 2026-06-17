from aiohttp import web
from app.admin_panel.routes import dashboard, users, conversations, leads, export


def setup_routes(app: web.Application):
    app.router.add_get("/login", dashboard.login_page, name="login")
    app.router.add_post("/login", dashboard.login_handler, name="login_post")
    app.router.add_get("/logout", dashboard.logout_handler, name="logout")
    app.router.add_get("/", dashboard.dashboard_page, name="dashboard")
    app.router.add_get("/users", users.users_page, name="users")
    app.router.add_get("/users/{user_id}", users.user_detail_page, name="user_detail")
    app.router.add_get("/users/{user_id}/delete", users.delete_user, name="delete_user")
    app.router.add_get("/conversations", conversations.conversations_page, name="conversations")
    app.router.add_get("/conversations/{user_id}", conversations.conversation_detail, name="conversation_detail")
    app.router.add_get("/leads", leads.leads_page, name="leads")
    app.router.add_post("/leads/{user_id}/update", leads.update_lead_status, name="update_lead")
    app.router.add_get("/export/users", export.export_users, name="export_users")
