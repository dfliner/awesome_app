
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from awesomeapp.database import get_db
from awesomeapp.models import User

router = APIRouter()

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {"users": users}

@router.post("/users")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"user": user}
