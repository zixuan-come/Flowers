from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import PasswordIn
from app.config import ADMIN_PASSWORD
from app.routers import scripts, categories

app = FastAPI(title="Flowers API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scripts.router, prefix="/api")
app.include_router(categories.router, prefix="/api")


@app.post("/api/verify-password")
async def verify_password(data: PasswordIn):
    if data.password != ADMIN_PASSWORD:
        from fastapi import HTTPException
        raise HTTPException(403, "密码错误")
    return {"ok": True}