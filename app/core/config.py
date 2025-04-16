from pydantic_settings import BaseSettings
from pydantic import ConfigDict


# 환경 변수 설정
class Settings(BaseSettings):
    DB_ECHO_LOG: bool = False
    # 비동기 데이터베이스 연결 문자열
    ASYNC_DATABASE_URL: str
    # 동기 데이터베이스 연결 문자열 (Alembic 에서 사용)
    SYNC_DATABASE_URL: str
    # 서버 시크릿 키
    SECRET_KEY: str
    # 쿠키 보안 설정
    IS_SECURE: bool

    # Azure OpenAI API 설정
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_VERSION: str

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


settings = Settings()
