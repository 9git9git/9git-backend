# app/core/logging.py
import logging  # 기본 Python 로깅 모듈
import sys
from loguru import logger  # loguru 라이브러리


# 📌 기존 Python logging 모듈과 loguru를 연결하는 핸들러
class InterceptHandler(logging.Handler):
    """기존 logging 모듈을 loguru로 라우팅하는 핸들러"""

    def emit(self, record):
        try:
            # 기존 logging 레벨을 loguru의 레벨로 변환
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno  # 변환이 불가능하면 기본 logging 레벨 사용

        # 📌 로그를 호출한 코드 위치를 추적하여 loguru에서 정확한 위치를 출력할 수 있도록 설정
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # 한 단계 위의 프레임을 가져옴
            depth += 1

        # 📌 loguru의 logger를 사용하여 로그 출력
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# 📌 로깅 시스템을 설정하는 함수
def setup_logging():
    """Python 기본 logging을 loguru 기반으로 설정"""

    # 1️⃣ 기본 logging 핸들러를 InterceptHandler()로 교체하여 loguru로 로그를 전송
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)  # 기본 로그 레벨을 INFO로 설정

    # 2️⃣ 기존 로거 설정 제거 (loguru를 사용하도록 변경)
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []  # 기존 핸들러 제거
        logging.getLogger(name).propagate = True  # 상위 로거로 전파 활성화

    # 3️⃣ loguru 설정 적용 (콘솔 출력 + 파일 로깅)
    logger.configure(
        handlers=[
            {
                # ✅ 터미널에 컬러 포맷으로 로그 출력
                "sink": sys.stdout,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>",
            },
            {
                # ✅ 로그를 파일(`logs/app.log`)에 저장
                "sink": "logs/app.log",
                "rotation": "00:00",  # 매일 자정에 새로운 로그 파일 생성
                "compression": "zip",  # 이전 로그 파일을 zip으로 압축
                "retention": "30 days",  # 30일 동안 로그 보관 후 자동 삭제
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
                "{level: <8} | {name}:{function}:{line} - {message}",
            },
        ]
    )
