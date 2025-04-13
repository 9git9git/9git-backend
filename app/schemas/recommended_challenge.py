from uuid import UUID
from typing import Optional
from app.schemas.base import BaseModel
from app.enum.category import CategoryNameEnum


# 생성
class RecommendedChallengeCreate(BaseModel):
    progressRate: float
    challengeTask: str
    challengeDuration: str
    challengeDifficulty: str
    challengeSuggestion: str


# 응답
class RecommendedChallengeResponse(BaseModel):
    id: UUID
    progress_id: UUID
    challenge_task: str
    challenge_duration: str
    challenge_difficulty: str
    challenge_suggestion: str


# 업데이트
class RecommendedChallengeUpdate(BaseModel):
    progressRate: Optional[float] = None
    challengeTask: Optional[str] = None
    challengeDuration: Optional[str] = None
    challengeDifficulty: Optional[str] = None
    challengeSuggestion: Optional[str] = None
