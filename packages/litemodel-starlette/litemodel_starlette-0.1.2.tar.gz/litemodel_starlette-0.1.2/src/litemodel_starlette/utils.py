
from litemodel_starlette.models import AdminUser
from starlette.requests import Request

def tables() -> str:
    return """SELECT name FROM sqlite_master where type='table' order by name GLOB '[A-Za-z]*' DESC, name;"""

async def get_by_admin_user_id(request: Request, user_id: str) -> AdminUser | None:
    return await AdminUser.find(user_id)
