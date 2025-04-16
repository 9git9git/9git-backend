
from functools import lru_cache
from langchain_community.chat_models import AzureChatOpenAI
from app.core.config import settings

@lru_cache()
def get_agent():
    return AzureChatOpenAI(
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        openai_api_key=settings.AZURE_OPENAI_API_KEY,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=0.5
    )

