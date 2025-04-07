# 9git-backend

## 0. 프로젝트 세팅

### 설치 및 실행

```bash
# 의존성 설치
poetry install --no-root

# 서버 실행
poetry run uvicorn app.main:app --reload
```

### 테스트

```bash
# 테스트 실행 기본
poetry run pytest
# 테스트 실행 커버리지 레포트 포함
poetry run pytest --cov=app
```

## 1. 폴더 구조 및 설명

```
├── app
│   ├── api       # API 라우터 및 엔드포인트가 위치
│   ├── core      # 프로젝트 핵심 설정 및 유틸리티 코드
│   ├── crud      # 데이터베이스 CRUD(생성, 조회, 수정, 삭제) 로직
│   ├── db        # DB 연결 및 세션 관리를 위한 코드
│   ├── models    # SQLAlchemy 모델 정의
│   ├── schemas   # Pydantic 스키마 정의
│   ├── services  # 비즈니스 로직 처리 (CRUD 외 추가적인 로직)
│   └── tests     # 테스트 코드
│   └── utils     # 유틸 코드
│   ├── main.py   # FastAPI 애플리케이션 진입점
├── migrations    # Alembic 마이그레이션 파일
│   └── env.py
├── poetry.lock
├── pyproject.toml
├── alembic.ini   # Alembic 설정
└── pytest.ini    # Pytest 관련 설정
```

## 2. 모델(DB) 수정 시 해야 할 것 (Alembic)

데이터베이스 모델을 수정한 후에는 다음 명령어로 마이그레이션을 생성하고 적용합니다:

```bash
# 모델 변경사항 자동 감지하여 마이그레이션 파일 생성
poetry run alembic revision --autogenerate -m "메시지"

# 마이그레이션 적용
poetry run alembic upgrade head
```

### 마이그레이션 과정

1. `app/models/` 디렉토리에서 모델 클래스를 추가하거나 수정합니다
2. 모델 클래스는 `Base` 클래스를 상속해야 합니다 (`from app.models.base import Base`)
3. `alembic revision` 명령어로 마이그레이션 파일을 생성합니다
4. `alembic upgrade` 명령어로 마이그레이션을 데이터베이스에 적용합니다

## 3. 환경 변수 추가하는 법

환경 변수는 `app/core/config.py` 파일의 `Settings` 클래스에 추가합니다:

```python
class Settings(BaseSettings):
    DB_ECHO_LOG: bool = False
    # 비동기 데이터베이스 연결 문자열
    ASYNC_DATABASE_URL: str
    # 동기 데이터베이스 연결 문자열 (Alembic 에서 사용)
    SYNC_DATABASE_URL: str

    # 새로운 환경 변수 추가 예시
    SECRET_KEY: str
    AZURE_KEY: str

    model_config = ConfigDict(env_file=".env", extra="allow")
```

그 후 `.env` 파일에 해당 환경 변수 값을 추가합니다:

## 4. 로깅 시스템

이 프로젝트는 `loguru`를 사용하여 로깅을 구현합니다:

- 터미널에 컬러 포맷으로 로그 출력
- `logs/app.log` 파일에 로그 저장
- 매일 자정에 새로운 로그 파일 생성 및 이전 파일 압축
- 30일간 로그 파일 보관 후 자동 삭제

로그 사용 예시:

```python
from loguru import logger

# 간단한 로그 출력
logger.info("정보 로그")
logger.debug("디버그 로그")
logger.warning("경고 로그")
logger.error("에러 로그")

# 예외 정보 포함
try:
    1/0
except Exception as e:
    logger.exception(f"예외 발생: {e}")
```
