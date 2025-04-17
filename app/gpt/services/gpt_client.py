# services/gpt_client.py - Azure OpenAI

import os
import requests
from app.enum.category import CategoryNameEnum
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AZURE_OAI_KEY")
api_version = os.getenv("AZURE_OAI_API_VERSION")


# ✅ 카테고리별 endpoint + deployment 동시 불러오기
def get_model_config(category: CategoryNameEnum) -> tuple[str, str]:
    endpoint = {
        CategoryNameEnum.ENGLISH.name: os.getenv("AZURE_OAI_ENDPOINT_ENGLISH"),
        CategoryNameEnum.CODING.name: os.getenv("AZURE_OAI_ENDPOINT_CODING"),
        CategoryNameEnum.EXERCISE.name: os.getenv("AZURE_OAI_ENDPOINT_EXERCISE"),
    }.get(category.name)

    deployment = {
        CategoryNameEnum.ENGLISH.name: os.getenv("AZURE_OAI_DEPLOYMENT_ENGLISH"),
        CategoryNameEnum.CODING.name: os.getenv("AZURE_OAI_DEPLOYMENT_CODING"),
        CategoryNameEnum.EXERCISE.name: os.getenv("AZURE_OAI_DEPLOYMENT_EXERCISE"),
    }.get(category.name)

    if not endpoint or not deployment:
        raise ValueError(f"❌ '{category}'에 대한 설정이 .env에 누락되었습니다.")

    return endpoint, deployment


# ✅ GPT 호출
def call_gpt(
    messages, category: CategoryNameEnum, temperature=0.7, max_tokens=1000
) -> str:
    """
    GPT 모델에 메시지 리스트를 전달하여 응답을 받아옵니다.
    - messages: 시스템/사용자 대화 이력 (list of dict)
    - temperature: 창의성 조절 파라미터 (기본 0.7)
    - max_tokens: 최대 토큰 수 (기본 1000)
    """

    endpoint, deployment = get_model_config(category)

    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    print(f"📡 호출 URL: {url}")
    headers = {"Content-Type": "application/json", "api-key": api_key}

    # GPT API 요청 페이로드 구성
    payload = {
        "messages": messages,  # 메시지 리스트
        "temperature": temperature,
        "top_p": 0.95,
        "max_tokens": max_tokens,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("❌ GPT 응답 파싱 오류:", e)
            print("📨 응답 원문:", response.json())
            raise

    # 실패한 경우 상세 로그 출력 후 예외 발생
    else:
        print(f"❌ GPT 호출 실패 {response.status_code}")
        print("📤 요청:", messages)
        print("📨 응답:", response.text)
        raise Exception("GPT 요청 실패")
