from langchain.prompts import PromptTemplate
from app.llm.llm_provider import get_agent

llm = get_agent()


# 통합 프롬프트 템플릿


general_prompt = PromptTemplate.from_template(
    """
당신은 {goal} 분야의 따뜻하고 실용적인 전문가입니다.

[사용자 요청]
"{user_input}"

[사용자의 현재 상태]
요청 유형: {intent}

{extra_instruction}
"""
)


# 일반 응답 (피드백, 로드맵)
def get_response(goal: str, user_input: str, intent: str) -> str:
    instruction = (
        "사용자의 질문에 전문가로서 조언이나 피드백을 제공해주세요."
        if intent == "피드백"
        else (
            "사용자의 목표에 맞는 단계별 학습 로드맵이나 실천 계획을 제시해주세요."
            if intent == "로드맵"
            else "질문에 대해 상황을 이해하고 적절한 조언을 제공해주세요."
        )
    )

    return llm.invoke(
        general_prompt.format(
            goal=goal,
            user_input=user_input,
            intent=intent,
            extra_instruction=instruction,
        )
    ).content.strip()


get_english_response = lambda u, i: get_response("영어", u, i)
get_coding_response = lambda u, i: get_response("코딩", u, i)
get_fitness_response = lambda u, i: get_response("운동", u, i)


# 문제 생성
def get_question(goal: str, user_input: str) -> str:
    instruction = f"{goal} 분야의 간단한 퀴즈나 연습 문제를 생성해주세요. 상황이나 감정도 반영해주세요."
    return llm.invoke(
        general_prompt.format(
            goal=goal,
            user_input=user_input,
            intent="문제 생성",
            extra_instruction=instruction,
        )
    ).content.strip()


get_english_question = lambda u: get_question("영어", u)
get_coding_question = lambda u: get_question("코딩", u)


# 정보 제공
def get_info(goal: str, user_input: str) -> str:
    instruction = f"{goal}과 관련된 시험, 자격증, 학습 팁, 활동 정보 등을 전문가 입장에서 자세히 제공해주세요."
    return llm.invoke(
        general_prompt.format(
            goal=goal,
            user_input=user_input,
            intent="정보 제공",
            extra_instruction=instruction,
        )
    ).content.strip()


get_english_info = lambda u: get_info("영어", u)
get_coding_info = lambda u: get_info("코딩", u)
get_fitness_info = lambda u: get_info("운동", u)


# 멘탈케어 응답
def get_mentalcare(goal: str, user_input: str) -> str:
    instruction = f"""
당신은 {goal} 분야의 학습이나 실천 과정에서 지친 사람에게
공감과 위로, 회복을 돕는 따뜻한 메시지를 전달하는 전문가입니다.
현재 감정과 상황을 고려하여 부담스럽지 않게 응원해주세요.
"""
    return llm.invoke(
        general_prompt.format(
            goal=goal,
            user_input=user_input,
            intent="멘탈케어",
            extra_instruction=instruction,
        )
    ).content.strip()


get_english_mentalcare = lambda u: get_mentalcare("영어", u)
get_coding_mentalcare = lambda u: get_mentalcare("코딩", u)
get_fitness_mentalcare = lambda u: get_mentalcare("운동", u)
