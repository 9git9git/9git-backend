# services/ai_search.py

import os
import requests
import json
from datetime import datetime, timezone
from uuid import uuid4
from app.enum.category import CategoryNameEnum
from dotenv import load_dotenv

load_dotenv()

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_api_version = os.getenv("AZURE_SEARCH_API_VERSION")
admin_key = os.getenv("AZURE_SEARCH_ADMIN_KEY")


# 요청 헤더 설정 (API 인증 및 Content-Type 명시)
HEADERS = {"Content-Type": "application/json", "api-key": admin_key}


def get_notice_index(category_enum: CategoryNameEnum) -> str:
    return {
        CategoryNameEnum.ENGLISH.name: os.getenv("AZURE_SEARCH_INDEX_NOTICE_ENGLISH"),
        CategoryNameEnum.CODING.name: os.getenv("AZURE_SEARCH_INDEX_NOTICE_CODING"),
        CategoryNameEnum.EXERCISE.name: os.getenv("AZURE_SEARCH_INDEX_NOTICE_EXERCISE"),
    }.get(category_enum.name)


# Azure AI Search에서 검색 (RAG)
def search_notice(query: str, category_enum: CategoryNameEnum, top_k: int = 3) -> str:
    """
    사용자 질문(query)에 대해 Azure AI Search에서
    카테고리별 정보('category'noticeindex) 인덱스를 조회하고,
    summary 필드의 텍스트를 정리하여 반환합니다.
    """
    index = get_notice_index(category_enum)
    if not index:
        return ""

    # url = f"{search_endpoint}/indexes/{index}/docs/search?api-version={search_api_version}"
    url = (
        f"{search_endpoint}/indexes/{index}/docs/search?api-version=2023-07-01-preview"
    )
    payload = {"search": query, "top": top_k, "select": "summary"}

    res = requests.post(url, headers=HEADERS, json=payload)

    if res.status_code == 200:
        results = res.json().get("value", [])
        return "\n---\n".join([r["summary"] for r in results if "summary" in r])
    else:
        print(f"❌ 검색 실패 {res.status_code}: {res.text}")
        return ""


# 💾 GPT 응답을 Azure Search에 저장하는 함수
def upload_to_index(index_name: str, data: dict):
    """
    GPT가 생성한 응답 요약 데이터를 지정한 인덱스(englishtutorindex)에 업로드합니다.
    Azure AI Search의 index API를 사용하여 데이터 삽입을 수행합니다.
    """

    now = datetime.now(timezone.utc).isoformat()
    doc = {
        "value": [
            {
                "@search.action": "upload",
                "id": data.get("id", str(uuid4())),
                "mode": data.get("mode", "summary"),
                "category": data.get("category", "general"),
                "original": data.get("original", ""),
                "summary": data.get("summary", ""),
                "created_at": data.get("created_at", now),
                "user_choice": data.get("user_choice", ""),
            }
        ]
    }

    # url = f"{search_endpoint}/indexes/{index_name}/docs/index?api-version={search_api_version}"
    url = f"{search_endpoint}/indexes/{index_name}/docs/search?api-version=2023-07-01-preview"
    res = requests.post(url, headers=HEADERS, json=doc)

    # 결과 확인 및 출력
    if res.status_code == 200:
        print(f"✅ 저장 성공: {index_name}")
    else:
        print(f"❌ 저장 실패 {res.status_code}: {res.text}")
