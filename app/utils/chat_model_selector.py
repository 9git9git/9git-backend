from app.gpt.handlers.coding_tutor import handle_coding_tutor
from app.gpt.handlers.english_tutor import handle_english_tutor
from app.gpt.handlers.exercise_tutor import handle_exercise_tutor
from app.enum.category import CategoryNameEnum


def route_to_model(category_enum: CategoryNameEnum):
    if category_enum == CategoryNameEnum.CODING:
        return handle_coding_tutor
    elif category_enum == CategoryNameEnum.ENGLISH:
        return handle_english_tutor
    elif category_enum == CategoryNameEnum.EXERCISE:
        return handle_exercise_tutor
    else:
        raise ValueError("지원되지 않는 카테고리입니다.")
