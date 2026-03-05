from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from awesomeapp.config import settings

# Create SQLAlchemy async engine
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession
)

# Dependency injection for FastAPI routes
async def get_db():
    async with SessionLocal() as session:
        yield session
