from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, func
from sqlalchemy.orm import selectinload
from app.models.category import Todo, Category
from app.schemas.chart import DailyAchievementResponse
from collections import defaultdict
from typing import List


async def get_daily_achievement(
    db: AsyncSession, user_id: UUID, year: int
) -> List[DailyAchievementResponse]:
    # 해당 연도의 투두 불러오기
    result = await db.execute(
        select(Todo)
        .join(Category)
        .options(selectinload(Todo.category))
        .where(Todo.user_id == user_id, extract("year", Todo.start_date) == year)
    )
    todos = result.scalars().all()

    # 일자별 → 카테고리별 → [완료된 수, 전체 수] 누적
    data = defaultdict(
        lambda: {"english": [0, 0], "exercise": [0, 0], "coding": [0, 0]}
    )

    for todo in todos:
        key_date = todo.start_date
        category = todo.category.category_name.value  # "영어", "운동", "코딩"

        if category == "영어":
            key = "english"
        elif category == "운동":
            key = "exercise"
        elif category == "코딩":
            key = "coding"
        else:
            continue  # 혹시 모를 예외

        data[key_date][key][1] += 1  # 전체 수
        if todo.is_completed:
            data[key_date][key][0] += 1  # 완료 수

    # 응답 데이터 구성
    responses: List[DailyAchievementResponse] = []

    for date_key in sorted(data.keys()):
        entry = data[date_key]
        responses.append(
            DailyAchievementResponse(
                date=date_key,
                english=(
                    round((entry["english"][0] / entry["english"][1] * 100), 2)
                    if entry["english"][1]
                    else 0
                ),
                exercise=(
                    round((entry["exercise"][0] / entry["exercise"][1] * 100), 2)
                    if entry["exercise"][1]
                    else 0
                ),
                coding=(
                    round((entry["coding"][0] / entry["coding"][1] * 100), 2)
                    if entry["coding"][1]
                    else 0
                ),
            )
        )

    return responses


from app.models.category import Todo, Category
from app.schemas.chart import MonthlyAchievementResponse
from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from collections import defaultdict
from typing import List


async def get_monthly_achievement(
    db: AsyncSession, user_id: UUID, year: int
) -> List[MonthlyAchievementResponse]:
    # 1. 연도에 해당하는 Todo 불러오기 (Category 조인 포함)
    result = await db.execute(
        select(Todo)
        .join(Category)
        .options(selectinload(Todo.category))
        .where(Todo.user_id == user_id, extract("year", Todo.start_date) == year)
    )
    todos = result.scalars().all()

    # 2. 월별 데이터 누적용 딕셔너리 초기화
    data = defaultdict(
        lambda: {
            "english": [0, 0],
            "exercise": [0, 0],
            "coding": [0, 0],
        }
    )

    # 3. 데이터 누적
    for todo in todos:
        month_str = todo.start_date.strftime("%Y-%m")  # 예: "2025-01"
        category = todo.category.category_name.value  # "코딩", "영어", "운동"

        if category == "영어":
            key = "english"
        elif category == "운동":
            key = "exercise"
        elif category == "코딩":
            key = "coding"
        else:
            continue

        data[month_str][key][1] += 1  # 전체 수 증가
        if todo.is_completed:
            data[month_str][key][0] += 1  # 완료 수 증가

    # 4. 응답 스키마에 맞게 가공
    responses: List[MonthlyAchievementResponse] = []
    for month_key in sorted(data.keys()):
        entry = data[month_key]
        responses.append(
            MonthlyAchievementResponse(
                month=month_key,
                english=(
                    round((entry["english"][0] / entry["english"][1] * 100), 2)
                    if entry["english"][1]
                    else 0
                ),
                exercise=(
                    round((entry["exercise"][0] / entry["exercise"][1] * 100), 2)
                    if entry["exercise"][1]
                    else 0
                ),
                coding=(
                    round((entry["coding"][0] / entry["coding"][1] * 100), 2)
                    if entry["coding"][1]
                    else 0
                ),
            )
        )

    return responses
