# handlers/category_router.py

from app.gpt.handlers.english_tutor import handle_english_tutor
from app.gpt.handlers.coding_tutor import handle_coding_tutor
from app.gpt.handlers.exercise_tutor import handle_exercise_tutor
from app.enum.category import CategoryNameEnum


def handle_tutor(user_input: str, category: str) -> str:
    category_enum = CategoryNameEnum[category.upper()]

    if category_enum == CategoryNameEnum.ENGLISH:
        return handle_english_tutor(user_input)
    elif category_enum == CategoryNameEnum.CODING:
        return handle_coding_tutor(user_input)
    elif category_enum == CategoryNameEnum.EXERCISE:
        return handle_exercise_tutor(user_input)
    else:
        raise ValueError(f"[❌] 지원하지 않는 category: {category}")


def handle_tutor(user_input: str, category: str) -> str:
    if category == CategoryNameEnum.ENGLISH.value:
        return handle_english_tutor(user_input)
    elif category == CategoryNameEnum.CODING.value:
        return handle_coding_tutor(user_input)
    elif category == CategoryNameEnum.EXERCISE.value:
        return handle_exercise_tutor(user_input)
    else:
        raise ValueError(f"[❌] 지원하지 않는 category: {category}")
