# utils/main.py

from app.gpt.handlers import category_router
from app.enum.category import CategoryNameEnum


def main():
    selected_category = CategoryNameEnum.CODING.value

    greetings = {
        CategoryNameEnum.ENGLISH.value: "실전형 영어 코치",
        CategoryNameEnum.CODING.value: "상위 1% 개발자 멘토",
        CategoryNameEnum.EXERCISE.value: "국가대표 피지컬 코치",
    }

    print(f"🔹 {selected_category.upper()} 챗봇 활성화")
    print(f"📢 {greetings.get(selected_category)}\n")
    print("'/exit' 입력 시 종료됩니다.\n")

    # 대화 루프
    while True:
        user_input = input("사용자: ").strip()
        if user_input.lower() == "/exit":
            print("챗봇을 종료합니다.")
            break
        if not user_input:
            print("⚠️ 입력이 비어있습니다.\n")
            continue

        response = category_router.handle_tutor(user_input, selected_category)
        print(f"\n💬 GPT 응답:\n{response}\n")


if __name__ == "__main__":
    main()
