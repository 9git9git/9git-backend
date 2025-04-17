# utils/prompts_loader.py

import os
from app.enum.category import CategoryNameEnum


# ✅ 카테고리별 프롬프트 파일 불러오기
def load_combined_prompt(category_enum: CategoryNameEnum) -> tuple[str, str]:
    """
    prompts/{category}.txt 파일을 읽어
    '### SYSTEM'과 '### USER' 구분자를 기준으로 나눠 반환합니다.

    반환 형식: (system_prompt, user_template)
    """
    filename = category_enum.name + ".txt"  # CODING.txt
    prompt_path = f"app/gpt/prompts/{filename}"

    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"❌ 프롬프트 파일이 없습니다: {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        content = f.read()

    parts = content.split("###")
    system_prompt, user_template = "", ""

    for part in parts:
        if part.strip().startswith("SYSTEM"):
            system_prompt = part.replace("SYSTEM", "").strip()
        elif part.strip().startswith("USER"):
            user_template = part.replace("USER", "").strip()

    if not system_prompt or not user_template:
        raise ValueError("❌ '### SYSTEM' 또는 '### USER' 구분자가 없습니다.")

    return system_prompt, user_template


# ✅ 프롬프트에 context와 question 삽입
def format_prompt(template: str, context: str, question: str) -> str:
    """
    템플릿 문자열에 context와 question을 삽입하여
    최종 user 메시지를 생성합니다.

    템플릿 내에는 {context}, {question} 이 두 개의 포맷팅 키워드가 있어야 합니다.
    """
    return template.format(context=context.strip(), question=question.strip())
