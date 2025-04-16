from app.llm.tools import detect_intent, detect_goal_function
from app.llm.goal_agents import (
    get_english_response,
    get_coding_response,
    get_fitness_response,
    get_english_question,
    get_coding_question,
    get_english_info,
    get_coding_info,
    get_fitness_info,
    get_english_mentalcare,
    get_coding_mentalcare,
    get_fitness_mentalcare,
)

VALID_GOALS = ["영어", "코딩", "운동"]

# goal 별 응답 함수 매핑
RESPONSE_FUNCS = {
    "영어": get_english_response,
    "코딩": get_coding_response,
    "운동": get_fitness_response,
}

QUESTION_FUNCS = {
    "영어": get_english_question,
    "코딩": get_coding_question,
}

INFO_FUNCS = {
    "영어": get_english_info,
    "코딩": get_coding_info,
    "운동": get_fitness_info,
}

MENTAL_FUNCS = {
    "영어": get_english_mentalcare,
    "코딩": get_coding_mentalcare,
    "운동": get_fitness_mentalcare,
}


# 에이전트 선택을 제어하는 핵심 로직
def route_to_agent(user_input: str, context: dict) -> str:
    goal = context.get("goal")
    if goal not in VALID_GOALS:
        return "목표는 영어, 코딩, 운동 중 하나여야 합니다."

    # intent와 goal_function_type 분석
    intent = detect_intent(user_input)
    goal_func_type = detect_goal_function(user_input, goal)

    # 멘탈케어는 intent 기준으로 분기
    if intent == "멘탈케어" and goal in MENTAL_FUNCS:
        return MENTAL_FUNCS[goal](user_input)

    # 특수 요청: 문제 생성
    if goal_func_type == "문제 생성" and goal in QUESTION_FUNCS:
        return QUESTION_FUNCS[goal](user_input)

    # 특수 요청: 정보 제공
    if goal_func_type == "정보 제공" and goal in INFO_FUNCS:
        return INFO_FUNCS[goal](user_input)

    # 일반 응답 (피드백, 로드맵)
    response_func = RESPONSE_FUNCS.get(goal)
    if response_func:
        return response_func(user_input, intent)

    return "알 수 없는 목표나 요청이에요."
