from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.comprehensive_evaluation import (
    ComprehensiveEvaluationCreate,
    ComprehensiveEvaluationResponse,
    ComprehensiveEvaluationUpdate,
)
from app.schemas.recommended_challenge import (
    RecommendedChallengeResponse,
    RecommendedChallengeCreate,
)
from app.services.comprehensive_evaluation import (
    select_comprehensive_evaluations,
    add_comprehensive_evaluation,
    update_comprehensive_evaluation_service,
)
from app.services.recommended_challenge import (
    select_recommended_challenges,
    add_recommended_challenge,
    update_recommended_challenge_service,
)
from app.services.ai import get_ai_analysis, get_goal_challenges_analysis


async def get_or_create_today_comprehensive_evaluation(
    db: AsyncSession, user_id: UUID
) -> ComprehensiveEvaluationResponse:
    """
    오늘 생성된 종합 평가가 있는지 확인하고,
    없으면 새로 생성하여 AI 분석을 받아 업데이트합니다.
    """
    # 1. 오늘 생성된 평가 확인
    evaluations = await select_comprehensive_evaluations(db, user_id)
    today = datetime.now(timezone.utc).date()

    today_evaluation = next(
        (eval for eval in evaluations if eval.created_at.date() == today), None
    )

    if today_evaluation:
        # 2. 오늘 생성된 평가가 있으면 반환
        return today_evaluation

    # 3. 오늘 생성된 평가가 없으면 새로 생성
    new_evaluation = ComprehensiveEvaluationCreate(
        overallAchievementRate=0.0,
        evaluationText="",
        strengthAchievementRate=0.0,
        strengthText="",
        improvementAchievementRate=0.0,
        improvementText="",
    )
    created_evaluation = await add_comprehensive_evaluation(db, user_id, new_evaluation)

    # 4. AI 분석 요청 및 업데이트
    ai_analysis = await get_ai_analysis(str(user_id))

    update_data = ComprehensiveEvaluationUpdate(
        overallAchievementRate=ai_analysis["overall_achievement_rate"],
        evaluationText=ai_analysis["evaluation_text"],
        strengthAchievementRate=ai_analysis["strength_achievement_rate"],
        strengthText=ai_analysis["strength_text"],
        improvementAchievementRate=ai_analysis["improvement_achievement_rate"],
        improvementText=ai_analysis["improvement_text"],
    )

    # 5. AI 분석 결과로 업데이트
    updated_evaluation = await update_comprehensive_evaluation_service(
        db, user_id, created_evaluation.id, update_data
    )

    return updated_evaluation


async def get_or_create_today_recommended_challenges(
    db: AsyncSession, user_id: UUID
) -> list[RecommendedChallengeResponse]:
    """
    오늘 생성된 추천 도전과제가 있는지 확인하고,
    없으면 새로 생성하여 AI 분석을 받아 업데이트합니다.
    """
    # 1. 오늘 생성된 추천 도전과제 확인
    challenges = await select_recommended_challenges(db, user_id)
    today = datetime.now(timezone.utc).date()

    today_challenges = [
        challenge for challenge in challenges if challenge.created_at.date() == today
    ]

    if today_challenges:
        # 2. 오늘 생성된 추천 도전과제가 있으면 반환
        return today_challenges

    # 3. AI 분석 요청
    challenges_data = await get_goal_challenges_analysis(str(user_id))

    # 4. 각 목표별로 추천 도전과제 생성
    created_challenges = []
    for goal, challenge_data in challenges_data.items():
        new_challenge = RecommendedChallengeCreate(
            progressRate=0.0,
            challengeTask=challenge_data["title"],
            challengeDuration=challenge_data["duration"],
            challengeDifficulty=challenge_data["difficulty"],
            challengeSuggestion=f"{challenge_data['reason']}\n{challenge_data['motivation']}",
        )

        # AI 분석 결과에서 받은 ID 사용
        try:
            category_id = UUID(str(challenge_data.get("category_id", "")))
        except (ValueError, TypeError):
            category_id = None

        created_challenge = await add_recommended_challenge(
            db, user_id, category_id, new_challenge
        )
        created_challenges.append(created_challenge)

    return created_challenges
