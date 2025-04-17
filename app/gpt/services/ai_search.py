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

HEADERS = {"Content-Type": "application/json", "api-key": admin_key}


def get_notice_index(category: str) -> str:
    return {
        CategoryNameEnum.ENGLISH.name: os.getenv("AZURE_SEARCH_INDEX_NOTICE_ENGLISH"),
        CategoryNameEnum.CODING.name: os.getenv("AZURE_SEARCH_INDEX_NOTICE_CODING"),
        CategoryNameEnum.EXERCISE.name: os.getenv("AZURE_SEARCH_INDEX_NOTICE_EXERCISE"),
    }.get(category)


def search_notice(query: str, category: str, top_k: int = 3) -> str:
    index = get_notice_index(category)
    if not index:
        return ""

    url = f"{search_endpoint}/indexes/{index}/docs/search?api-version={search_api_version}"
    payload = {"search": query, "top": top_k, "select": "summary"}

    res = requests.post(url, headers=HEADERS, json=payload)
    if res.status_code == 200:
        results = res.json().get("value", [])
        return "\n---\n".join([r["summary"] for r in results if "summary" in r])
    else:
        print(f"❌ 검색 실패 {res.status_code}: {res.text}")
        return ""


def upload_to_index(index_name: str, data: dict):
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

    url = f"{search_endpoint}/indexes/{index_name}/docs/index?api-version={search_api_version}"
    res = requests.post(url, headers=HEADERS, json=doc)
    if res.status_code == 200:
        print(f"✅ 저장 성공: {index_name}")
    else:
        print(f"❌ 저장 실패 {res.status_code}: {res.text}")
