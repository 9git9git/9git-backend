from langchain.schema import HumanMessage
from app.llm.llm_provider import get_agent


# 프롬프트 템플릿
# 사용자 입력을 4가지 유형 중 하나로 분류하기 위한 가이드
INTENT_GUIDANCE = """
다음은 사용자의 요청 유형을 분류하는 기준이야야. 분류는 반드시 다음 4개 중 하나로만 해줘줘:

1. 피드백: 사용자의 활동이나 학습 결과에 대한 평가, 코칭, 잘하고 있는지 질문하는 경우
2. 로드맵: 앞으로 무엇을 해야 할지, 계획/단계 추천을 요청하는 경우
3. 멘탈케어: 감정적 표현이 포함된 경우 (예: 지쳤다, 힘들다, 위로받고 싶다)
4. 확장 요청: 문제를 만들어달라, 예시 보여달라, 시험/정보를 요청하는 등의 경우

사용자의 입력을 기반으로 위 4가지 중 가장 적절한 하나를 골라. 단어 그대로 "피드백", "로드맵", "멘탈케어", "확장 요청" 중 하나만 답변하도록 해.
"""

# 목표(goal)에 따라 입력 요청을 분류하기 위한 템플릿 (문제 생성 / 정보 제공 / 일반 요청)
GOAL_FUNCTION_GUIDANCE_TEMPLATE = """
너는 '{goal}' 분야의 전문 AI 코치야.
사용자의 요청이 아래 유형 중 하나인지 판단해줘:

- 문제 생성: 퀴즈, 예시 문제, 테스트 요청
- 정보 제공: 자격증, 시험, 실습, 동작 등에 대한 구체적인 정보 요청
- 일반 요청: 일상 대화, 피드백, 코칭 등 자유로운 조언

반드시 다음 중 하나로만 응답해: 문제 생성 / 정보 제공 / 일반 요청
"""



# Intent 분석 함수 (대화 목적 분류)
"""
사용자의 입력 문장을 기반으로 '의도(intent)'를 분류함.
'피드백', '로드맵', '멘탈케어', '확장 요청' 중 하나로 분류됨
"""
def detect_intent(user_input: str) -> str:
    llm = get_agent()
    response = llm.invoke([
        HumanMessage(content=INTENT_GUIDANCE),
        HumanMessage(content=user_input)
    ])
    return response.content.strip()



# Goal Function 분석 함수 (특수 요청 분류)
"""
사용자의 입력 문장을 기반으로 목표(goal)에 맞는 요청의 유형을 분류
'문제 생성', '정보 제공', '일반 요청' 중 하나로 응답
"""
def detect_goal_function(user_input: str, goal: str) -> str:
    llm = get_agent()
    guidance = GOAL_FUNCTION_GUIDANCE_TEMPLATE.format(goal=goal)
    response = llm.invoke([
        HumanMessage(content=guidance),
        HumanMessage(content=user_input)
    ])
    return response.content.strip()
