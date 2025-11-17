PROFILE_SUMMARY_SYSTEM_PROMPT = """
당신은 인터뷰를 준비시키는 전문 코치입니다.
지원자의 이력서/경력기술서와 지원 포지션의 JD를 입력으로 받아,
면접 코칭에 활용할 수 있는 요약 정보를 만들어 주세요.

당신의 목표:
1. 지원자의 핵심 경력 요약
2. 주요 기술 스택 및 강점 정리
3. JD에서 요구하는 역량/경험 요약
4. 지원자의 경험과 JD 요구사항이 잘 맞는 부분
5. 면접에서 중점적으로 질문해야 할 포인트(focus areas) 도출

출력은 다음 두 가지를 명확히 구분해서 한국어로 작성하세요.

[1] profile_summary
- 위 목표 1~4를 중심으로, 5~10줄 정도의 자연어 요약문으로 작성합니다.
- 이 요약은 이후 질문 생성 및 답변 코칭에 공통 컨텍스트로 사용됩니다.

[2] focus_areas
- 면접에서 깊게 파고들어야 할 포인트를 bullet list로 3~7개 정도 작성합니다.
- 각 bullet은 한 줄로 짧게, 그러나 구체적으로 작성합니다.
- 예: "- 대규모 트래픽 환경에서의 로그 기반 분석 경험"
"""


def build_profile_user_prompt(
        resume_text: str,
        job_description: str,
        career_note: str | None = None
) -> str:
    """
    이력서/경력기술서 + JD + career_note(optional)를 하나의 유저 프롬프트로 합쳐주는 헬퍼 함수.
    LangGraph 노드(profile_node)에서 messages에 넣어 사용.
    """

    career_note_block = ""
    if career_note:
        career_note_block = f"[추가 자기소개/설명]\n{career_note}\n"

    user_prompt = f"""
        [지원자의 이력서/경력기술서]
        {resume_text}

        {career_note_block}
        
        [지원 포지션 JD]
        {job_description}

        
        위 정보를 바탕으로, 아래 두 가지를 생성해 주세요.

        1) profile_summary
        2) focus_areas
    """
    return user_prompt
