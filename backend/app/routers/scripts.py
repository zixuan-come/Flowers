from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Script
from app.schemas import ScriptCreate, ScriptOut
from app.dependencies import require_admin

router = APIRouter()


@router.get("/scripts", response_model=list[ScriptOut])
async def list_scripts(category_id: int | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Script).order_by(Script.created_at.desc())
    if category_id is not None:
        stmt = stmt.where(Script.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/scripts/{script_id}", response_model=ScriptOut)
async def get_script(script_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Script).where(Script.id == script_id))
    script = result.scalar_one_or_none()
    if not script:
        from fastapi import HTTPException
        raise HTTPException(404, "脚本不存在")
    return script


@router.post("/scripts", response_model=ScriptOut, dependencies=[Depends(require_admin)])
async def create(data: ScriptCreate, db: AsyncSession = Depends(get_db)):
    script = Script(**data.model_dump())
    db.add(script)
    await db.commit()
    await db.refresh(script)
    return script


@router.put("/scripts/{script_id}", response_model=ScriptOut, dependencies=[Depends(require_admin)])
async def update(script_id: int, data: ScriptCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Script).where(Script.id == script_id))
    script = result.scalar_one_or_none()
    if not script:
        from fastapi import HTTPException
        raise HTTPException(404, "脚本不存在")
    for k, v in data.model_dump().items():
        setattr(script, k, v)
    await db.commit()
    await db.refresh(script)
    return script


@router.delete("/scripts/{script_id}", dependencies=[Depends(require_admin)])
async def delete(script_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Script).where(Script.id == script_id))
    script = result.scalar_one_or_none()
    if not script:
        from fastapi import HTTPException
        raise HTTPException(404, "脚本不存在")
    await db.delete(script)
    await db.commit()
    return {"ok": True}
