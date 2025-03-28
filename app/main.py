from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title="9git-backend API",
    description="9git-backend API",
    version="0.1.0",
    debug=settings.DB_ECHO_LOG,
)


@app.get("/")
async def health_check():
    return {"message": "OK"}
