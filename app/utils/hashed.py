from passlib.context import CryptContext

# 비밀번호 해싱에 사용할 알고리즘 설정
# schemes 목록에서 첫 번째 항목이 기본 해싱 알고리즘으로 사용됨
pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12  # 보안 수준 (기본값은 12)
)


def get_password_hash(password: str) -> str:
    """
    비밀번호를 해시합니다.

    Args:
        password: 해시할 비밀번호

    Returns:
        str: 해시된 비밀번호
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:

        # 에러가 발생하면 로그 기록 후 예외 재발생
        raise ValueError(f"비밀번호 해싱 중 오류가 발생했습니다: {str(e)}")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    일반 텍스트 비밀번호와 해시된 비밀번호를 비교합니다.

    Args:
        plain_password: 일반 텍스트 비밀번호
        hashed_password: 해시된 비밀번호

    Returns:
        bool: 비밀번호가 일치하면 True, 그렇지 않으면 False
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:

        # 검증 중 오류 발생 시 보안상 False 반환
        return False
