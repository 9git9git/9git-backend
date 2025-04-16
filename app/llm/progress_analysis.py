from app.llm.llm_provider import get_agent
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
from app.core.config import settings
import json

# LLM & DB 연결
llm = get_agent()

db = SQLDatabase.from_uri(
    settings.SYNC_DATABASE_URL,
    include_tables=	["progresses", "todos", "categories"],
    sample_rows_in_table_info=2 # 테이블 구조 예시를 GPT가 이해하도록 제공
)

# 목표 한글 → DB ENUM 값 매핑
GOAL_TO_ENUM = {
    "영어": "ENGLISH",
    "코딩": "CODING",
    "운동": "EXERCISE",
}


# GPT 응답 JSON 파싱 유틸 함수
def extract_json(text: str, label: str):
    try:
        start = text.index('{')
        end = text.rindex('}') + 1
        return json.loads(text[start:end])
    except Exception as e:
        return {"error": f"{label} JSON parse 실패", "raw": text}



# 전체 목표 평균 달성률 요약
async def get_user_summary(user_id: str):
    query = f"""
    SELECT AVG(progress_rate) AS average_rate
    FROM progresses
    WHERE user_id = '{user_id}';
    """
    
    result = db.run(query)
    
    prompt = PromptTemplate.from_template("""
    당신은 목표 달성률을 기반으로 희망적인 복사정의 기준문장을 생성하는 AI입니다.

    - 평균 달성률 수치를 기반으로 하되, 사용자가 성취에 대한 자신감을 가질 수 있도록 유도해야함.
    - '사용자'는 표현은 제외하고 계속해서 자연스러운 문장으로 작성되어야함.
    - 달성률이 낮아도 격려하거나 앞으로의 가능성을 강조해 줘야함.
    - 문장은 따뜻하고 응원하는 톤으로, 반드시 존댓말로 작성할 것. 문장은 한 문장 이내, 70자 이내로 작성할 것.
    - 길이는 2줄 이내여야 하며, 아래 JSON 형식으로 응답해야 함.
    - 모든 응답은 반드시 **자연스러운 한국어**로 작성할 것. 영어나 외국어는 사용 금지.

    평균 달성률: {progress_data}

    아래 JSON 형식으로 출력하세요:
    ```json
    {{
      "summary": "..."
    }}
    """)
    formatted = prompt.format(progress_data=result)
    response = llm.invoke(formatted)
    return extract_json(response.content, "summary")



# 목표별 강점 & 개선점 분석
async def get_strength_weakness(user_id: str):
    query = f"""
    WITH ranked_goals AS (
      SELECT c.category_name AS goal, AVG(p.progress_rate) AS avg_rate
      FROM progresses p
      JOIN categories c ON p.category_id = c.id
      WHERE p.user_id = '{user_id}'
      GROUP BY c.category_name
    )
    SELECT * FROM ranked_goals ORDER BY avg_rate DESC;
    """
    
    results = db.run(query)
    
    prompt = PromptTemplate.from_template("""
    당신은 목표별 평균 달성률을 분석하고, 가장 높은 항목은 강점으로, 가장 낮은 항목은 감정점으로 표현하는 AI입니다.

    요약 문장은 반드시 짧고 간결하게 작성할 것:
    - 각 문장은 1줄, 70자 이내로 작성되어야 함.
    - '사용자'는 표현은 제외하고 자연스러운 일상 문장처럼 작성해야 함.
    - 강점은 격려 문장, 개선점은 실천을 유도하는 조언 문장으로 모두 존댓말로 작성할 것.
    - 모든 응답은 반드시 **자연스러운 한국어**로 작성되어야 함. 영어나 외국어는 사용하면 안됨.

    아래는 사용자의 목표별 평균 달성률임:
    {ranked_goals}

    아래 JSON 형식으로 출력하세요:
    ```json
    {{
      "strength": "...",
      "weakness": "..."
    }}
    """)
    formatted = prompt.format(ranked_goals=results)
    response = llm.invoke(formatted)
    return extract_json(response.content, "strength_weakness")




# 목표별 도전과제 추천
async def get_goal_challenges(user_id: str, goal: str):
    # 한글 목표명을 ENUM 값으로 매핑
    category_enum = GOAL_TO_ENUM.get(goal, None)
    if category_enum is None:
        return {"error": f"❌ goal '{goal}'은 지원되지 않음"}
    
    query = f"""
    SELECT t.content, t.is_completed, t.start_date, t.end_date
    FROM todos t
    JOIN categories c ON t.category_id = c.id
    WHERE t.user_id = '{user_id}' AND c.category_name = '{category_enum}'
      AND (t.start_date >= CURRENT_DATE - INTERVAL '6 months' OR t.end_date >= CURRENT_DATE - INTERVAL '6 months')
    ORDER BY t.start_date DESC;
    """
    
    results = db.run(query)
    
    prompt = PromptTemplate.from_template("""
    당신은 도전과제를 기획하는 전문가입니다.

    선택된 목표: '{goal}'
    최근 기록된 활동 내역(최대 6개월 기준, 실제 기록이 적을 수 있음):
    {todo_info}
    
    활동 내용을 기반으로 새로운 도전과제를 하나 추천할 것. 
    단, 기록이 부족한 경우에는 격려 문구를 포함한 실현 가능한 추천을 생성할 것.
    도전과제는 다음 기준을 충족해야 함:

    - 활동과 연관된 자격증, 시험, 수료증, 경진대회 등 실질적인 성취로 연결될 것
    - 사용자가 모르고 있을 수 있는 정보도 포함 가능
    - 예: 파이썬 → 정보처리기사, 크롤링 → 데이터 분석 전문가, 영어 회화 → OPIC, 운동 → 요가 지도자 수료증 등
    - 도전과제는 너무 거창하지 않으면서도 실현 가능하고, 자격증·공식 시험·현실성 있는 실습 챌린지 중심이어야 함.
    - 모든 응답은 반드시 **자연스러운 한국어**로 작성할것. 영어나 외국어는 절대 사용하면 안됨.
    - 아래 형식의 각 항목은 반드시 **간결하게**, 1~2문장 이내로 작성하며, 모든 문장은 존댓말로 작성할 것 (특히 reason과 motivation은 요점 중심으로 작성)

    아래 JSON 형식으로 출력하세요:
    ```json
    {{
      "title": "...",
      "reason": "...",   ← 배경 설명 없이 추천 이유만 간단히
      "motivation": "...",   ← 실천 유도 문장 위주, 핵심만 작성
      "duration": "...",
      "difficulty": "하/중/상"
    }}
    """)
    formatted = prompt.format(goal=goal, todo_info=results)
    response = llm.invoke(formatted)
    return extract_json(response.content, f"{goal}_challenge")