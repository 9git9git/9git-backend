# 분석 AI TEST CODE

import asyncio
import nest_asyncio
from app.llm.progress_analysis import get_user_summary, get_strength_weakness, get_goal_challenges


# 테스트할 user_id
user_id = "user_id"

async def test_summary():
    result = await get_user_summary(user_id)
    print("🎯 GPT 요약 결과:")
    print(result)

async def test_strength():
    result = await get_strength_weakness(user_id)
    print("✅ 강점 & 개선점 분석 결과:")
    print(result)

async def test_goal_challenge():
    for goal in ["영어", "코딩", "운동"]:
        print(f"\n🎯 {goal} 도전과제 추천:")
        result = await get_goal_challenges(user_id, goal)
        print(result)


if __name__ == "__main__":
    async def run_all():
        await test_summary()
        await test_strength()
        await test_goal_challenge()

    asyncio.run(run_all())