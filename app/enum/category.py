from enum import Enum


class CategoryNameEnum(Enum):
    CODING = "코딩"
    ENGLISH = "영어"
    EXERCISE = "운동"


# CategoryColorEnum 클래스 정의
class CategoryColorEnum(Enum):
    CODING = "#6C88C4"  # 인디고 블루
    ENGLISH = "#FDA63A"  # 호박색
    EXERCISE = "#556B2F"  # 올리브 그린
