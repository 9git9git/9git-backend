from fastapi import APIRouter
from app.api.v1.endpoints import auth, user, category_progress, monthly_achievement

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(
    category_progress.router, prefix="/category-progresses", tags=["categoryProgress"]
)
router.include_router(
    monthly_achievement.router,
    prefix="/monthly-achievements",
    tags=["monthlyAchievement"],
)
