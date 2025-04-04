from sqlalchemy import String, DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime, timezone
import pytz

# 한국 시간대 설정
kst = pytz.timezone("Asia/Seoul")


# 3개 다 필요함 공통된 칼럼을 상속받는 Base
class Base(DeclarativeBase):

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(kst)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(kst)
    )
