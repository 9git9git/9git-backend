## FastAPI 가이드라인

FastAPI는 현대적이고 빠르며 (고성능), Python 3.8+ 기반의 웹 API를 구축하기 위한 웹 프레임워크입니다. 개발자가 쉽고 빠르게 API를 개발할 수 있도록 다양한 기능을 제공하며, 자동 데이터 유효성 검사, 직렬화, API 문서 자동 생성 등의 장점을 가지고 있습니다.

이 가이드라인에서는 FastAPI를 효과적으로 사용하기 위한 기본적인 방법과 권장 사항을 다룹니다.

### 1. FastAPI 설치

Poetry를 사용하여 FastAPI를 프로젝트의 종속성으로 추가합니다. 프로젝트 루트 디렉토리에서 다음 명령을 실행합니다.

```bash
poetry add fastapi
```

FastAPI는 ASGI 서버가 필요하므로 Uvicorn 또는 Hypercorn 중 하나를 함께 설치하는 것이 일반적입니다. Uvicorn을 권장합니다.

```bash
poetry add uvicorn
```

### 2. 기본적인 FastAPI 애플리케이션 구조

FastAPI 애플리케이션은 일반적으로 다음과 같은 구조를 가집니다.

- **`main.py` (또는 애플리케이션 진입점 파일):** FastAPI 애플리케이션 인스턴스를 생성하고 API 엔드포인트를 정의합니다.
- **`models.py` (선택 사항):** Pydantic 모델을 정의하여 요청 및 응답 데이터의 구조와 유효성 검사를 관리합니다.
- **`schemas.py` (선택 사항):** 데이터 직렬화 및 API 문서 생성을 위한 Pydantic 스키마를 정의합니다.
- **`routers/` (선택 사항):** API 엔드포인트를 논리적인 그룹으로 분리하기 위한 디렉토리입니다.

### 3. FastAPI 애플리케이션 인스턴스 생성

`main.py` 파일에서 FastAPI 애플리케이션 인스턴스를 생성합니다.

```python
from fastapi import FastAPI

app = FastAPI()
```

### 4. API 엔드포인트 정의 (경로 및 HTTP 메서드)

`@app` 데코레이터를 사용하여 API 엔드포인트를 정의합니다. 각 데코레이터는 특정 HTTP 메서드와 경로를 매핑합니다.

- `@app.get(path)`: GET 요청 처리
- `@app.post(path)`: POST 요청 처리
- `@app.put(path)`: PUT 요청 처리
- `@app.delete(path)`: DELETE 요청 처리
- `@app.patch(path)`: PATCH 요청 처리

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: dict):
    return {"item": item}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

- 경로는 `/` 와 같이 고정된 값일 수도 있고, `/items/{item_id}` 와 같이 경로 매개변수 (`item_id`)를 포함할 수도 있습니다. 경로 매개변수는 함수 인자로 전달됩니다.
- 쿼리 매개변수 (`q=None`)는 함수 인자의 기본값을 설정하여 정의할 수 있습니다.

### 5. Pydantic 모델을 이용한 데이터 유효성 검사 및 직렬화

Pydantic은 Python 타입 힌트를 사용하여 데이터 유효성 검사, 직렬화 및 API 문서 생성을 자동화하는 데 사용됩니다. 요청 및 응답 데이터를 위한 Pydantic 모델을 정의하는 것이 좋습니다.

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

- `Item` 클래스는 Pydantic 모델로, 요청 본문의 데이터 구조와 각 필드의 타입을 정의합니다.
- FastAPI는 함수 인자로 선언된 Pydantic 모델을 자동으로 유효성 검사하고, 유효하지 않은 경우 적절한 HTTP 오류 응답을 반환합니다.
- Pydantic 모델은 응답 데이터를 직렬화하는 데에도 사용됩니다.

### 6. API 문서 자동 생성

FastAPI는 OpenAPI 및 Swagger UI (또는 Redoc)를 기반으로 API 문서를 자동으로 생성합니다. 별도의 문서 작성 없이 API를 쉽게 탐색하고 테스트할 수 있습니다.

- **/docs:** Swagger UI를 통해 API 문서를 확인할 수 있습니다.
- **/redoc:** Redoc을 통해 API 문서를 확인할 수 있습니다.

Uvicorn을 사용하여 애플리케이션을 실행한 후 (예: `uvicorn main:app --reload`), 웹 브라우저에서 `http://localhost:8000/docs` 또는 `http://localhost:8000/redoc` 에 접속하여 API 문서를 확인하십시오.

### 7. 의존성 주입

FastAPI의 강력한 기능 중 하나는 의존성 주입 시스템입니다. 함수 인자로 타입을 선언하여 의존성을 정의하고, FastAPI가 자동으로 해당 의존성을 해결하여 함수에 주입합니다.

```python
from fastapi import FastAPI, Header, Depends

app = FastAPI()

async def get_token_header(x_token: str = Header()):
    return {"X-Token": x_token}

@app.get("/items/", dependencies=[Depends(get_token_header)])
async def read_items():
    return [{"name": "Foo", "price": 42}]
```

- `Depends()` 를 사용하여 의존성 함수를 선언합니다.
- `Header()` 는 HTTP 헤더를 의존성으로 주입받는 데 사용됩니다.
- `dependencies` 매개변수를 사용하여 특정 경로 작업 함수에 의존성을 추가할 수 있습니다.

### 8. 라우터 (API 엔드포인트 분리)

API 엔드포인트가 많아질 경우, 라우터를 사용하여 논리적인 그룹으로 분리하는 것이 좋습니다.

```python
# routers/items.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[/* 전역 의존성 */],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_item(item: Item):
    return {"item": item}

@router.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# main.py
from fastapi import FastAPI
from .routers import items

app = FastAPI()
app.include_router(items.router)
```

- `APIRouter` 를 사용하여 라우터 인스턴스를 생성하고, 경로 접두사 (`prefix`), 태그 (`tags`), 의존성 (`dependencies`), 응답 (`responses`) 등을 설정할 수 있습니다.
- `app.include_router()` 를 사용하여 라우터를 FastAPI 애플리케이션에 포함시킵니다.

### 9. 미들웨어

미들웨어는 요청 처리 전후에 특정 로직을 실행하는 데 사용됩니다. 로깅, 인증, CORS (Cross-Origin Resource Sharing) 처리 등에 유용합니다.

```python
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

* `app.add_middleware()` 를 사용하여 미들웨어를 추가합니다.
* `starlette.middleware` 모듈에서 다양한 미들웨어를 사용할 수 있습니다.

### 10. 예외 처리

FastAPI는 표준 Python 예외와 HTTP 예외를 쉽게 처리할 수 있도록 지원합니다.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

* `HTTPException` 을 발생시켜 특정 HTTP 상태 코드와 상세 메시지를 포함한 오류 응답을 반환할 수 있습니다.

### 권장 사항

- **Pydantic 모델 적극 활용:** 데이터 유효성 검사, 직렬화, API 문서 자동 생성을 위해 Pydantic 모델을 적극적으로 사용하는 것이 좋습니다.
- **명확한 타입 힌트 사용:** 타입 힌트는 코드의 가독성을 높이고, 정적 분석 도구의 활용을 용이하게 하며, FastAPI의 자동 기능들을 효과적으로 사용할 수 있도록 합니다.
- **API 엔드포인트 설계:** RESTful API 디자인 원칙을 따르고, 명확하고 일관된 API 엔드포인트를 설계하는 것이 중요합니다.
- **라우터 활용:** API 규모가 커질수록 라우터를 사용하여 엔드포인트를 논리적으로 분리하고 관리하는 것이 좋습니다.
- **적절한 예외 처리:** 예상되는 오류 상황에 대해 적절한 예외 처리를 구현하여 사용자에게 유용한 오류 메시지를 제공해야 합니다.
- **테스트:** Pytest와 같은 테스트 프레임워크를 사용하여 API 엔드포인트를 철저히 테스트하는 것이 중요합니다. FastAPI는 테스트를 위한 편리한 `TestClient` 를 제공합니다.

이 가이드라인은 FastAPI의 기본적인 사용법과 권장 사항을 다루고 있습니다. FastAPI의 더 많은 기능과 고급 사용법은 [공식 문서](https://fastapi.tiangolo.com/ko/)를 참고하시기 바랍니다.