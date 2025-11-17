from typing import TypedDict, Optional


class InterviewState(TypedDict, total=False):
    """인터뷰 코칭 그래프에서 사용하는 상태 정의"""

    # 사전 정보
    resume_text: str
    career_note: str
    job_description: str

    # 사전 정보 기반 요약/해석 결과
    profile_summary: str
    focus_area: list[str]

    # 현재 인터뷰 Q&A
    question: str
    answer: str
    feedback: str
    