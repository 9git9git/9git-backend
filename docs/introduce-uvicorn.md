## Uvicorn 가이드라인 (Poetry, FastAPI와 함께 사용)

Uvicorn은 ASGI (Asynchronous Server Gateway Interface) 표준을 구현한 빠른 ASGI 서버입니다. FastAPI는 ASGI를 기반으로 구축되었으므로 Uvicorn은 FastAPI 애플리케이션을 실행하는 데 권장되는 서버입니다. Poetry는 Python 프로젝트의 종속성 관리 및 패키징 도구로, Uvicorn과 FastAPI를 함께 사용하는 프로젝트를 관리하는 데 유용합니다.

이 가이드라인에서는 Poetry와 FastAPI를 함께 사용하는 환경에서 Uvicorn을 효과적으로 사용하는 방법에 대해 설명합니다.

### 1. Uvicorn 설치

Poetry를 사용하여 Uvicorn을 프로젝트의 종속성으로 추가합니다. 프로젝트 루트 디렉토리에서 다음 명령을 실행합니다.

```bash
poetry add uvicorn
```

이 명령은 `pyproject.toml` 파일에 `uvicorn`을 추가하고 `poetry.lock` 파일을 업데이트합니다.

### 2. FastAPI 애플리케이션 정의

FastAPI 애플리케이션을 만듭니다. 예를 들어, `main.py` 파일에 다음과 같이 정의할 수 있습니다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### 3. Uvicorn으로 FastAPI 애플리케이션 실행

Uvicorn을 사용하여 FastAPI 애플리케이션을 실행하는 가장 기본적인 방법은 터미널에서 직접 명령을 실행하는 것입니다.

```bash
uvicorn main:app --reload
```

각 옵션의 의미는 다음과 같습니다.

* `main`: FastAPI 애플리케이션이 정의된 Python 파일 (`main.py`).
* `app`: FastAPI 애플리케이션 인스턴스 (`main.py`에서 `app = FastAPI()`로 정의).
* `--reload`: 코드 변경 시 서버를 자동으로 재시작합니다. 개발 환경에서 유용합니다.

### 4. 실행 옵션

Uvicorn은 다양한 실행 옵션을 제공합니다. 주요 옵션은 다음과 같습니다.

* `--host`: 서버가 바인딩될 IP 주소 (기본값: `127.0.0.1`).
* `--port`: 서버가 리스닝할 포트 번호 (기본값: `8000`).
* `--workers`: 실행할 워커 프로세스 수. CPU 코어 수에 맞춰 설정하는 것이 일반적입니다. 프로덕션 환경에서 성능 향상을 위해 사용됩니다.
* `--log-level`: 로깅 수준 설정 (`debug`, `info`, `warning`, `error`, `critical`).
* `--ssl-keyfile`, `--ssl-certfile`: HTTPS 설정을 위한 키 파일 및 인증서 파일 경로.
* `--proxy-headers`: 프록시 서버 뒤에서 실행될 때 필요한 헤더 처리 활성화.
* `--forwarded-allow-ips`: `X-Forwarded-For` 헤더를 신뢰할 수 있는 IP 주소 목록.

Poetry 스크립트를 사용하여 이러한 옵션을 편리하게 관리할 수 있습니다. `pyproject.toml` 파일의 `[tool.poetry.scripts]` 섹션에 다음과 같이 추가합니다.

```toml
[tool.poetry.scripts]
start = "uvicorn main:app --reload"
start-prod = "uvicorn main:app --workers 4 --host 0.0.0.0 --port 80"
```

이제 다음 명령으로 애플리케이션을 실행할 수 있습니다.

```bash
poetry run start        # 개발 모드 (자동 재시작)
poetry run start-prod   # 프로덕션 모드 (4개의 워커, 모든 IP, 80번 포트)
```

### 5. Poetry 환경 내에서 Uvicorn 실행

Poetry 환경 내에서 Uvicorn을 직접 실행할 수도 있습니다. 먼저 Poetry 셸을 활성화합니다.

```bash
poetry shell
```

활성화된 셸에서 `uvicorn` 명령을 직접 실행합니다.

```bash
uvicorn main:app --reload
```

### 6. 프로덕션 환경 설정

프로덕션 환경에서는 다음과 같은 사항을 고려해야 합니다.

* **자동 재시작 비활성화 (`--reload` 옵션 제거):** 프로덕션 환경에서는 코드 변경 시 자동으로 서버가 재시작되는 것을 방지해야 합니다.
* **워커 프로세스 설정 (`--workers`):** CPU 코어 수에 맞춰 적절한 워커 수를 설정하여 성능을 최적화합니다. 일반적으로 CPU 코어 수만큼 또는 2배수로 설정합니다.
* **호스트 및 포트 설정 (`--host 0.0.0.0`, `--port 80 또는 443`):** 외부 접근이 가능하도록 호스트를 `0.0.0.0`으로 설정하고, HTTP(80) 또는 HTTPS(443) 포트를 사용합니다.
* **로깅 설정 (`--log-level`):** 적절한 로깅 수준을 설정하여 서버 상태를 모니터링합니다.
* **HTTPS 설정 (`--ssl-keyfile`, `--ssl-certfile`):** 보안을 위해 HTTPS를 구성합니다. SSL 인증서 및 키 파일을 지정해야 합니다.
* **시스템 관리자 도구 활용 (systemd, Supervisor 등):** 서버 프로세스를 안정적으로 관리하고 자동 재시작, 로깅 등을 설정합니다.
* **로드 밸런서 및 프록시 설정:** 여러 Uvicorn 인스턴스를 로드 밸런서 뒤에 배치하여 트래픽을 분산하고 가용성을 높입니다. 프록시 서버를 사용하는 경우 `--proxy-headers` 및 `--forwarded-allow-ips` 옵션을 적절히 설정합니다.

### 7. 추가 고려 사항

* **`.env` 파일:** 환경 변수를 사용하여 Uvicorn 설정을 관리하는 것이 좋습니다. Python의 `dotenv` 라이브러리를 사용하여 `.env` 파일을 로드할 수 있습니다.
* **설정 파일:** 복잡한 설정의 경우 별도의 설정 파일을 (예: YAML, TOML) 사용하여 Uvicorn 옵션을 관리하는 것을 고려해볼 수 있습니다.
* **모니터링:** Prometheus, Grafana 등의 도구를 사용하여 Uvicorn 서버의 성능 지표를 모니터링하는 것이 중요합니다.

이 가이드라인을 통해 Poetry와 FastAPI를 함께 사용하는 환경에서 Uvicorn을 효과적으로 관리하고 실행하는 데 도움이 되기를 바랍니다. Uvicorn의 공식 문서를 참조하여 더 많은 고급 기능과 설정을 확인하는 것을 추천합니다.