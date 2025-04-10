from uuid import UUID
from decimal import Decimal
from typing import Optional
from app.schemas.base import BaseModel
from app.enum.category import CategoryNameEnum



# 생성 
class RecommendedChallengeCreate(BaseModel):
    progress_id: UUID
    user_id: UUID
    category_name: CategoryNameEnum
    challenge_task: str
    challenge_duration: str
    challenge_difficulty: str
    challenge_suggestion: str
    
    
# 응답 
class RecommendedChallengeResponse(BaseModel):
    id: UUID
    progress_id: UUID
    user_id: UUID
    category_name: CategoryNameEnum
    challenge_task: str
    challenge_duration: str
    challenge_difficulty: str
    challenge_suggestion: str


# 업데이트 
class RecommendedChallengeUpdate(BaseModel):
    challenge_task: Optional[str] = None 
    challenge_duration: Optional[str] = None  
    challenge_difficulty: Optional[str] = None 
    challenge_suggestion: Optional[str] = None  

# 카테고리 하나당 진행률
class GoalProgressItem(BaseModel):
    category_name: CategoryNameEnum  # 예: 영어, 코딩, 운동
    progress_rate: float


# class RecommendedChallengeRead(RecommendedChallengeCreate):
#     id: UUID

        
    

