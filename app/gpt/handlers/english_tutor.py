# handlers/english_tutor.py

import os
from uuid import uuid4
from datetime import datetime, timezone

from app.gpt.services.gpt_client import call_gpt
from app.gpt.services.ai_search import upload_to_index, search_notice
from app.gpt.utils.prompts_loader import load_combined_prompt, format_prompt
from app.enum.category import CategoryNameEnum


# ✅ 영어 튜터 전용 핸들러
def handle_english_tutor(user_input: str) -> str:
    category = CategoryNameEnum.ENGLISH.value
    index_name = os.getenv("AZURE_SEARCH_INDEX_ENGLISH")

    # 1. 사용자 입력 수신
    question = user_input.strip()

    # 2. Notice 인덱스에서 관련 정보 검색 (시험 정보 등)
    rag_context = search_notice(query=question, category=category)
    print("🧾 검색 결과 (RAG):", rag_context)
    # 3. 프롬프트 로딩 및 메시지 생성
    system_prompt, user_template = load_combined_prompt(category)
    user_message = format_prompt(
        template=user_template, context=rag_context, question=question
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    # 4. GPT 응답 생성
    result = call_gpt(messages=messages, category=category)

    # 5. 응답 요약 후 AI Search 저장
    summary_prompt = [
        {
            "role": "system",
            "content": "다음 응답을 한 문장으로 요약해 주세요. 반드시 한국어로.",
        },
        {"role": "user", "content": result},
    ]
    summary = call_gpt(summary_prompt, category=category)

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
