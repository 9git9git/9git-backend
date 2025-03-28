from fastapi import FastAPI

app = FastAPI(
    title="9git-backend API",
    description="9git-backend API",
    version="0.1.0",
)


@app.get("/")
async def health_check():
    return {"message": "OK"}
