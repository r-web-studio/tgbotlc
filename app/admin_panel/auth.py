from aiohttp import web
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.config.settings import settings
import hashlib
import logging

logger = logging.getLogger(__name__)

serializer = URLSafeTimedSerializer(settings.SESSION_SECRET)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


def create_session_token(admin_id: str) -> str:
    return serializer.dumps({"admin_id": admin_id})


def validate_session_token(token: str) -> dict | None:
    try:
        data = serializer.loads(token, max_age=86400 * 7)
        return data
    except (BadSignature, SignatureExpired):
        return None


def setup_session_middleware(app: web.Application):
    @web.middleware
    async def session_middleware(request: web.Request, handler):
        token = request.cookies.get("admin_session")
        request["admin"] = None

        if token:
            data = validate_session_token(token)
            if data:
                request["admin"] = data["admin_id"]

        response = await handler(request)
        return response

    app.middlewares.append(session_middleware)


def require_auth(handler):
    async def wrapped(request: web.Request):
        if not request.get("admin"):
            raise web.HTTPFound("/login")
        return await handler(request)
    return wrapped
