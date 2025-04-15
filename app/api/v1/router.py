from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    user,
    character,
    user_character,
    comprehensive_evaluation,
    memo,
    category,
    storage,
    recommended_challenge,
    week,
    chat,
    progress,
)

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(character.router, prefix="/characters", tags=["characters"])
router.include_router(
    user_character.router, prefix="/user_characters", tags=["user_characters"]
)
router.include_router(
    comprehensive_evaluation.router,
    prefix="/users/{user_id}/comprehensive_evaluations",
    tags=["comprehensive_evaluations"],
)
router.include_router(
    memo.router,
    prefix="/users/{user_id}/categories/{category_id}/memos",
    tags=["memos"],
)
router.include_router(category.router, prefix="/categories", tags=["Category"])
router.include_router(
    storage.router,
    prefix="/users/{user_id}/categories/{category_id}/storages",
    tags=["storages"],
)

router.include_router(
    recommended_challenge.router,
    prefix="/users/{user_id}/categories/{category_id}/recommend-challenges",
    tags=["RecommendedChallenges"],
)

router.include_router(
    week.router,
    prefix="/users/{user_id}/categories/{category_id}/todos/{todo_id}/weeks",
    tags=["weeks"],
)
router.include_router(
    chat.router,
    prefix="/users/{user_id}",
    tags=["chats"],
)
router.include_router(
    progress.router, prefix="/ users/{user_id}/progresses", tags=["Progress"]
)
