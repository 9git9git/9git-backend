# handlers/coding_tutor.py

import os
from uuid import uuid4
from datetime import datetime, timezone

from app.gpt.services.gpt_client import call_gpt
from app.gpt.services.ai_search import upload_to_index  # Notice 검색은 구조만 있음
from app.gpt.utils.prompts_loader import load_combined_prompt, format_prompt
from app.enum.category import CategoryNameEnum


# ✅ 코딩 튜터 전용 핸들러
def handle_coding_tutor(user_input: str) -> str:
    category = CategoryNameEnum.CODING.value
    index_name = os.getenv("AZURE_SEARCH_INDEX_CODING")
    question = user_input.strip()

    # 🔹 Notice 기반 RAG 검색 (향후 codingnoticeindex 연동 예정)
    rag_context = ""  # 검색 구조만 유지

    # 🔹 프롬프트 로딩 및 메시지 구성
    system_prompt, user_template = load_combined_prompt(category)
    user_message = format_prompt(user_template, rag_context, question)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    # 🔹 GPT 호출
    result = call_gpt(messages, category)

    # 🔹 요약 생성 및 저장
    summary_prompt = [
        {
            "role": "system",
            "content": "다음 응답을 한 문장으로 요약해 주세요. 반드시 한국어로.",
        },
        {"role": "user", "content": result},
    ]
    summary = call_gpt(summary_prompt, category)

    upload_to_index(
        index_name,
        {
            "id": f"{category}-{str(uuid4())}",
            "mode": "summary",
            "category": category,
            "original": question,
            "summary": summary,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "user_choice": "",
        },
    )

    return result
