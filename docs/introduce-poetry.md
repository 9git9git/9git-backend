# Poetry 상세 가이드라인

### 1. Poetry 소개

Poetry는 파이썬 프로젝트의 의존성 관리, 가상 환경 관리, 빌드, 패키징 및 배포를 위한 통합 도구입니다. `venv`와 같은 기본적인 가상 환경 관리 도구를 넘어, 프로젝트의 전체 라이프사이클을 효율적으로 관리할 수 있도록 지원합니다.

### 1.1. Poetry와 venv 비교

| 기능 | venv | Poetry |
|---|---|---|
| **주요 목적** | 파이썬 패키지 격리를 위한 가상 환경 생성 및 관리 | 파이썬 프로젝트의 의존성 관리, 가상 환경 관리, 빌드, 패키징, 배포 등 **종합적인 프로젝트 관리** |
| **의존성 관리** | `requirements.txt` 파일을 수동으로 관리 (생성, 편집) 또는 `pip freeze` 사용 | `pyproject.toml` 파일을 통해 중앙 집중식으로 관리, `poetry add/remove` 명령어로 자동 업데이트, `poetry.lock` 파일로 정확한 의존성 버전 고정 |
| **가상 환경 관리** | 직접 생성 (`python -m venv <venv_이름>`) 및 활성화/비활성화 필요 | 프로젝트별로 자동 생성 및 관리, 사용자는 Poetry 명령어만 사용 |
| **의존성 해결** | 순차적 설치, 충돌 가능성 존재 | 정교한 의존성 해결 알고리즘으로 호환 가능한 조합 탐색 |
| **패키징 및 배포** | 별도의 도구 (예: setuptools) 및 설정 필요 (`setup.py`) | `pyproject.toml` 기반으로 빌드 및 패키징 자동화, PyPI 배포 용이 |
| **개발 의존성 관리** | 일반 의존성과 명확히 구분하기 어려움 (일반적으로 `requirements-dev.txt` 등으로 관리) | `--dev` 옵션을 사용하여 개발에만 필요한 의존성 분리 관리 |
| **설정 파일** | 표준화된 설정 파일 없음 (`requirements.txt`, `setup.py` 등 여러 파일 관리 필요) | PEP 518 표준을 따르는 `pyproject.toml` 파일 하나로 프로젝트 설정 통합 관리 |
| **사용 편의성** | 비교적 단순하지만, 의존성 관리를 수동으로 해야 하는 번거로움 존재 | 자동화된 기능과 명확한 명령어를 통해 프로젝트 관리 편의성 높음 |
| **학습 곡선** | 비교적 낮음 | 처음에는 약간의 학습 필요 |
| **프로젝트 규모** | 간단한 프로젝트에 적합 | 중대형 프로젝트 및 팀 협업에 더욱 효과적 |

### 2. Poetry 설치

터미널 또는 명령 프롬프트에서 다음 명령어를 실행하여 Poetry를 설치합니다.

#### 2.1. macOS, Linux, WSL

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### 2.2. Windows

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

설치 후, 다음 명령어로 Poetry 버전을 확인하여 설치를 검증합니다.

```bash
poetry --version
```

### 3. 새로운 프로젝트 시작

새로운 파이썬 프로젝트를 시작하고 Poetry를 초기화합니다.

```bash
cd <프로젝트_디렉토리>
poetry new
```

이 명령어는 기본적인 프로젝트 구조 (`pyproject.toml`, `README.rst`, 프로젝트 패키지 디렉토리, 테스트 디렉토리)를 생성합니다.

기본 구조 없이 `pyproject.toml` 파일만 생성하려면 다음 명령어를 사용합니다.

#### 3.1. `poetry init`과 `poetry new`의 차이점

* **`poetry new <프로젝트_이름>`**: 새로운 프로젝트 디렉토리를 생성하고 기본적인 프로젝트 구조 (소스 코드 디렉토리, 테스트 디렉토리, `pyproject.toml`, `README.rst`)를 자동으로 구성합니다. 처음부터 새로운 프로젝트를 시작할 때 유용합니다.
* **`poetry init`**: **기존 프로젝트**를 Poetry로 관리하도록 초기화하는 명령어입니다. 현재 디렉토리에 `pyproject.toml` 파일을 생성하는 과정을 대화형으로 안내합니다. 이미 코드가 있는 프로젝트에 Poetry를 적용할 때 사용합니다.

```bash
poetry init --no-interaction
```

### 4. 의존성 관리

#### 4.1. 새로운 의존성 추가

프로젝트에 필요한 새로운 패키지를 추가합니다.

```bash
poetry add <패키지_이름>         # 일반 의존성 추가
poetry add <패키지_이름1> <패키지_이름2> ... # 여러 패키지 한 번에 추가
poetry add --dev <개발_의존성_이름> # 개발에만 필요한 의존성 추가 (예: 테스트 도구)
```

**예시:**

```bash
poetry add requests
poetry add numpy pandas
poetry add --dev pytest
```

특정 버전을 지정하여 추가할 수도 있습니다.

```bash
poetry add requests==2.25.1
poetry add "flask>=2.0,<3.0"
```

#### 4.2. 의존성 제거

더 이상 필요 없는 패키지를 제거합니다.

```bash
poetry remove <패키지_이름>
poetry remove --dev <개발_의존성_이름>
```

**예시:**

```bash
poetry remove requests
poetry remove --dev pytest
```

#### 4.3. 의존성 업데이트

`pyproject.toml` 파일에 명시된 버전 제약 조건에 따라 의존성을 최신 버전으로 업데이트합니다.

```bash
poetry update             # 모든 의존성 업데이트
poetry update <패키지_이름> # 특정 패키지만 업데이트
```

#### 4.4. 의존성 설치

프로젝트의 모든 의존성을 설치합니다. 이는 다른 환경에서 프로젝트를 처음 설정할 때 사용합니다.

```bash
poetry install
```

이 명령어는 `poetry.lock` 파일에 기록된 정확한 버전의 의존성들을 설치합니다. `poetry.lock` 파일이 없다면 `pyproject.toml` 파일을 기반으로 의존성을 해결하고 `poetry.lock` 파일을 생성합니다.

#### 4.5. `poetry install --no-root` 설명

`poetry install` 명령어는 기본적으로 현재 프로젝트를 "root 패키지"로 간주하고, `pyproject.toml` 파일의 `[tool.poetry]` 섹션에 정의된 프로젝트 자체 정보와 의존성을 함께 설치하려고 시도합니다.

`poetry install --no-root` 옵션은 **현재 프로젝트 자체는 설치하지 않고**, `pyproject.toml` 파일에 정의된 의존성들만 가상 환경에 설치하도록 지시하는 명령어입니다.

**이 옵션이 유용한 경우는 다음과 같습니다:**

- **라이브러리 개발:** 여러분이 재사용 가능한 라이브러리를 개발하고 있을 때, 최종 사용자는 여러분의 라이브러리 코드를 직접 `pip install` 할 것입니다. 개발 과정에서 여러분은 해당 라이브러리가 의존하는 다른 패키지들만 가상 환경에 설치하여 테스트하고 싶을 수 있습니다. 이 때 `--no-root` 옵션을 사용하면 라이브러리 자신의 패키지 설치 없이 의존성만 설치하여 개발 환경을 구성할 수 있습니다.
- **플러그인 개발:** 특정 애플리케이션의 플러그인을 개발할 때, 플러그인 자체는 해당 애플리케이션의 환경 내에서 실행됩니다. 플러그인이 필요로 하는 추가적인 의존성만 격리된 가상 환경에 설치하고 싶을 때 유용합니다.
- **테스트 환경 구성:** 때로는 프로젝트의 의존성만 격리된 환경에서 테스트하고 싶을 수 있습니다. `--no-root` 옵션을 사용하면 프로젝트 코드는 설치하지 않고 의존성만 설치하여 테스트 환경을 빠르게 구성할 수 있습니다.

**일반적인 프로젝트와의 차이점:**

일반적인 애플리케이션 프로젝트에서는 `poetry install` 명령어를 실행하면 프로젝트 자체도 가상 환경에 설치되어 `import <프로젝트_이름>` 형태로 접근할 수 있게 됩니다. 하지만 `--no-root` 옵션을 사용하면 프로젝트의 소스 코드는 가상 환경에 설치되지 않으므로 직접적인 import는 불가능합니다. 대신, 설치된 의존성들의 기능을 활용하여 개발 및 테스트를 진행하게 됩니다.

**요약:**

`poetry install --no-root`는 현재 프로젝트 자체를 가상 환경에 설치하지 않고, `pyproject.toml` 파일에 정의된 의존성만을 설치하는 옵션입니다. 주로 라이브러리 개발, 플러그인 개발, 또는 프로젝트 의존성만 격리하여 테스트하고 싶을 때 유용하게 사용됩니다.

### 5. 가상 환경 관리

Poetry는 프로젝트별로 자동으로 가상 환경을 생성하고 관리합니다.

#### 5.1. 가상 환경 활성화

Poetry가 관리하는 가상 환경을 활성화합니다.

```bash
poetry shell
```

활성화되면 터미널 프롬프트 앞에 가상 환경 이름이 표시됩니다.

#### 5.2. 가상 환경 정보 확인

현재 Poetry 프로젝트의 가상 환경 정보를 확인합니다.

```bash
poetry env info
```

#### 5.3. 가상 환경 삭제

Poetry가 관리하는 가상 환경을 삭제합니다.

```bash
poetry env remove python<버전>  # 특정 파이썬 버전의 가상 환경 삭제 (예: python3.9)
poetry env remove --all      # 모든 가상 환경 삭제 (주의!)
```

### 6. 빌드 및 패키징

Poetry를 사용하여 프로젝트를 배포 가능한 형태로 빌드합니다.

```bash
poetry build
```

빌드 결과물 (`.whl`, `.tar.gz`)은 프로젝트 루트 디렉토리의 `dist` 폴더에 저장됩니다.

### 7. 배포

Poetry를 사용하여 빌드된 패키지를 PyPI 또는 다른 저장소에 배포합니다.

#### 7.1. 저장소 설정

배포할 저장소를 설정합니다. 기본적으로 PyPI가 설정되어 있습니다. 다른 저장소를 사용하려면 `poetry config` 명령어를 사용합니다.

```bash
poetry config repositories.<저장소_이름> <저장소_URL>
poetry config pypi-token.<저장소_이름> <API_토큰>
```

#### 7.2. 배포 실행

빌드된 패키지를 설정된 저장소에 배포합니다. 배포 전에 반드시 빌드를 먼저 실행해야 합니다.

```bash
poetry publish
```

### 8. 주요 설정 파일

#### 8.1. `pyproject.toml`

Poetry 프로젝트의 핵심 설정 파일입니다. 프로젝트 정보, 의존성, 빌드 설정 등을 정의합니다.

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "My awesome Python project"
authors = ["Your Name <you@example.com>"]
license = "MIT"
readme = "README.rst"

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.25.1"
numpy = "^1.21.0"

[tool.poetry.dev-dependencies]
pytest = "^6.2.4"
flake8 = "^3.9.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

#### 8.2. `poetry.lock`

프로젝트에 설치된 모든 의존성의 정확한 버전 정보를 담고 있는 파일입니다. 이 파일을 통해 다른 환경에서도 동일한 의존성 환경을 재현할 수 있습니다. 버전 관리 시스템에 반드시 포함해야 합니다.

### 9. 기타 유용한 명령어

* **프로젝트 정보 확인:**
    ```bash
    poetry show             # 설치된 패키지 목록 확인
    poetry show <패키지_이름> # 특정 패키지 정보 확인
    poetry show --tree       # 의존성 트리 구조 확인
    poetry show -v           # 상세 정보 출력
    ```

* **lock 파일 관리:**
    ```bash
    poetry lock             # pyproject.toml 기반으로 lock 파일 업데이트
    poetry lock --check       # lock 파일이 최신 상태인지 확인
    ```

* **설정 관리:**
    ```bash
    poetry config --list      # Poetry 설정 목록 확인
    poetry config <설정_이름> <설정_값> # 특정 설정 값 변경
    ```

### 10. 결론

Poetry는 파이썬 프로젝트 관리를 위한 강력하고 효율적인 도구입니다. 의존성 관리의 편의성, 자동화된 가상 환경 관리, 간편한 빌드 및 배포 기능을 통해 개발 생산성을 향상시키고 프로젝트의 안정성을 높일 수 있습니다. 본 가이드라인을 통해 Poetry의 기본적인 사용법을 익히고, 실제 프로젝트에 적용하여 효율적인 개발 워크플로우를 구축하시기 바랍니다.
