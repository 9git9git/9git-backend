from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from loguru import logger
from app.core.logging import setup_logging
from app.db.base import init_db
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행
    setup_logging()
    logger.info("Application starting up...")
    try:
        await init_db()
        yield
    except asyncio.CancelledError:
        logger.warning("Lifespan tasks cancelled")
    finally:
        logger.info("Application shutting down...")


app = FastAPI(
    title="9git-backend API",
    description="9git-backend API",
    version="0.0.1",
    debug=settings.DB_ECHO_LOG,
    lifespan=lifespan,
)


@app.get("/")
async def health_check():
    return {"message": "OK"}
