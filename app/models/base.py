# `func`을 추가하여 SQL 기본 함수 활용
from sqlalchemy import DateTime, func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime
import pytz

# 한국 시간대 설정
kst = pytz.timezone("Asia/Seoul")


# 공통된 칼럼을 상속받는 Base 클래스
class Base(DeclarativeBase):
    """Base class which provides automated table name
    and surrogate primary key column.
    """

    metadata = MetaData()

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
