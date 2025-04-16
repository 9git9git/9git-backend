from app.llm.progress_analysis import (
    get_user_summary,
    get_strength_weakness,
    get_goal_challenges,
)


async def get_ai_analysis(user_id: str):
    # 전체 요약 가져오기
    summary_result = await get_user_summary(user_id)

    # 강점과 개선점 분석
    strength_result = await get_strength_weakness(user_id)

    return {
        "overall_achievement_rate": summary_result["overall_achievement_rate"],
        "evaluation_text": summary_result["summary"],
        "strength_achievement_rate": strength_result["strength_rate"],
        "strength_text": strength_result["strength"],
        "improvement_achievement_rate": strength_result["weakness_rate"],
        "improvement_text": strength_result["weakness"],
    }


async def get_goal_challenges_analysis(user_id: str):
    """
    모든 목표에 대한 도전과제 추천을 가져옵니다.
    """
    challenges = {}
    for goal in ["영어", "코딩", "운동"]:
        challenge_result = await get_goal_challenges(user_id, goal)
        challenges[goal] = challenge_result

    return challenges
