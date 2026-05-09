from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryOut
from app.dependencies import require_admin

router = APIRouter()


@router.get("/categories", response_model=list[CategoryOut])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.sort_order))
    return result.scalars().all()


@router.post("/categories", response_model=CategoryOut, dependencies=[Depends(require_admin)])
async def create(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    cat = Category(**data.model_dump())
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


@router.put("/categories/{cat_id}", response_model=CategoryOut, dependencies=[Depends(require_admin)])
async def update(cat_id: int, data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        from fastapi import HTTPException
        raise HTTPException(404, "分类不存在")
    cat.name = data.name
    cat.icon = data.icon
    await db.commit()
    await db.refresh(cat)
    return cat


@router.delete("/categories/{cat_id}", dependencies=[Depends(require_admin)])
async def delete(cat_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        from fastapi import HTTPException
        raise HTTPException(404, "分类不存在")
    await db.delete(cat)
    await db.commit()
    return {"ok": True}