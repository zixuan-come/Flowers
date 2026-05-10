from fastapi import Header, HTTPException
from app.config import ADMIN_PASSWORD


async def require_admin(x_admin_password: str = Header(None)):
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="密码错误")

