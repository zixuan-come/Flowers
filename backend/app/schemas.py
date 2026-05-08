from pydantic import BaseModel
from datetime import datetime


# --- 分类 ---
class CategoryCreate(BaseModel):
    name: str
    icon: str = "📁"


class CategoryOut(BaseModel):
    id: int
    name: str
    icon: str
    sort_order: int
    created_at: datetime | None = None


# --- 脚本 ---
class ScriptCreate(BaseModel):
    title: str
    description: str | None = ""
    language: str = "Python"
    code: str
    category_id: int | None = None
    tags: str | None = ""


class ScriptOut(ScriptCreate):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


# --- 密码验证 ---
class PasswordIn(BaseModel):
    password: str