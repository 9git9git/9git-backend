from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from loguru import logger
from app.core.logging import setup_logging
from app.db.base import init_db
from app.api.v1.router import router as api_router
import asyncio
from fastapi.middleware.cors import CORSMiddleware


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
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

allow_origins = [
    "http://localhost:3000",
    "https://gugit-frontend-test-aca.calmforest-521dd431.eastus.azurecontainerapps.io",
    "https://9git-frontend.vercel.app",
    # TODO: 추후 프론트 배포 url 추가 필요
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # 모든 출처 허용 (배포 환경에서는 특정 도메인으로 제한하는 것이 좋습니다)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


@app.get("/")
async def health_check():
    return {"message": "OK"}


app.include_router(api_router, prefix="/api/v1")
