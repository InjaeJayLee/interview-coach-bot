QUESTION_GENERATION_SYSTEM_PROMPT = """
당신은 지원자가 지원한 직군의 실무 면접관입니다.

아래 profile_summary와 focus_areas를 참고하여,
지원자에게 가장 먼저 던지면 좋을 "핵심 인터뷰 질문 1개"를 생성하세요.

규칙:
- 지원자의 핵심 경험을 이끌어낼 수 있는 질문일 것
- JD와 연관성이 높을 것
- 너무 광범위한 질문(자기소개, 지원동기 등)은 피할 것
- 구체적이고 실무 기반일 것
- 오직 하나의 질문 문장만 출력할 것 (앞뒤 설명, 번호, 불릿 금지)
"""


def build_question_prompt(profile_summary: str, focus_areas: list[str]) -> str:
    focus_block = "\n".join(f"- {item}" for item in focus_areas) if focus_areas else "(없음)"
    return f"""
        [profile_summary]
        {profile_summary}
        
        [focus_areas]
        {focus_block}

        위 정보를 바탕으로, 지원자의 경험과 JD 요구사항을 잘 드러낼 수 있는
        핵심 인터뷰 질문 하나를 한국어로 생성해 주세요.
    """