from uuid import main
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
    todo,
    main,
    analyze,
    chart,
)

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
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
    prefix="/users/{user_id}/categories/{category_id}/chats",
    tags=["chats"],
)
router.include_router(
    progress.router, prefix="/users/{user_id}/progresses", tags=["Progress"]
)

router.include_router(
    todo.router,
    prefix="/users/{user_id}/categories/{category_id}/todos",
    tags=["todos"],
)
router.include_router(main.router, prefix="/users/{user_id}", tags=["main"])

# 일반 캐릭터 CRUD
router.include_router(character.router, prefix="/characters", tags=["characters"])

# 유저 도감 전용 API (GET /users/{user_id}/characters)
router.include_router(
    character.router,
    prefix="/users/{user_id}",
    tags=["user_characters"],  # or "characters" if you want to group together
)
router.include_router(
    analyze.router,
    prefix="/users/{user_id}/analyze",
    tags=["analyze"],
)

router.include_router(
    chart.router,
    prefix="/users/{user_id}",
    tags=["Chart"],
)
