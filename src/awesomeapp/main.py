from fastapi import FastAPI
from awesomeapp.config import settings
from awesomeapp.database import engine
from awesomeapp.models import Base
from awesomeapp.routes import router
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown code (if any)

app = FastAPI(title="AwesomeApp", debug=settings.DEBUG, lifespan=lifespan)

@app.on_event("startup")
async def on_startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Include routes
app.include_router(router)
