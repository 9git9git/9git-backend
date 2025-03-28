from sqlalchemy.orm import DeclarativeBase


# Base 클래스는 SQLAlchemy의 모든 ORM 모델 클래스가 상속받는 기본 클래스입니다.
# 이 클래스는 데이터베이스 테이블과 매핑되는 ORM 모델을 정의하는 데 사용됩니다.
class Base(DeclarativeBase):
    pass  # 이 클래스 자체는 비어 있지만, 상속받는 클래스들이 테이블을 정의하게 됩니다.
