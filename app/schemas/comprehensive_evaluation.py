from app.schemas.base import BaseModel
from uuid import UUID
from typing import Optional


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
    evaluation_text: Optional[str] = None
    strength_achievement_rate: float
    strength_text: Optional[str] = None
    improvement_achievement_rate: float
    improvementText: Optional[str] = None


class ComprehensiveEvaluationUpdate(BaseModel):
    overallAchievementRate: float
    evaluationText: str
    strengthAchievementRate: float
    strengthText: str
    improvementAchievementRate: float
    improvementText: str
