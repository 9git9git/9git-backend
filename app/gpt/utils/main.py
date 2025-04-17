# utils/main.py
from app.gpt.handlers import category_router
from app.enum.category import CategoryNameEnum


def main():
    greetings = {
        CategoryNameEnum.ENGLISH: "실전형 영어 코치",
        CategoryNameEnum.CODING: "상위 1% 개발자 멘토",
        CategoryNameEnum.EXERCISE: "국가대표 피지컬 코치",
    }

    # 카테고리 선택
    print("🔷 테스트할 카테고리를 선택하세요:")
    for i, category_enum in enumerate(CategoryNameEnum, start=1):
        print(f"{i}. {category_enum.name} - {greetings[category_enum]}")

    try:
        selected_index = int(input("번호 입력: ").strip()) - 1
        selected_enum = list(CategoryNameEnum)[selected_index]
    except (IndexError, ValueError):
        print("❌ 유효하지 않은 선택입니다.")
        return

    print(f"\n🔹 선택된 챗봇: {selected_enum.name}")
    print(f"📢 {greetings[selected_enum]}\n")
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

        # ✅ Enum.name을 string으로 전달
        response = category_router.handle_tutor(user_input, selected_enum.name)
        print(f"\n💬 GPT 응답:\n{response}\n")


if __name__ == "__main__":
    main()
