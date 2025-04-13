from app.schemas.base import BaseModel
from uuid import UUID


class ComprehensiveEvaluationCreate(BaseModel):
    overallAchievementRate: float
    evaluationText: str
    strengthAchievementRate: float
    strengthText: str
    improvementAchievementRate: float
    improvementText: str


class ComprehensiveEvaluationResponse(BaseModel):
    id: UUID
    user_id: UUID
    overall_achievement_rate: float
    evaluation_text: str
    strength_achievement_rate: float
    strength_text: str
    improvement_achievement_rate: float


class ComprehensiveEvaluationUpdate(BaseModel):
    overallAchievementRate: float
    evaluationText: str
    strengthAchievementRate: float
    strengthText: str
    improvementAchievementRate: float
