from typing import TypedDict, Optional


class InterviewState(TypedDict, total=False):
    """인터뷰 코칭 그래프에서 사용하는 상태 정의"""

    # 사전 정보
    resume_text: str                    # 이력서/경력기술서 전체 텍스트
    career_note: str                    # 추가 자기소개/포트폴리오 설명 등 (선택)
    job_description: str                # 지원 포지션 JD 텍스트

    # 사전 정보 기반 요약/해석 결과
    profile_summary: str                # 이력서 + JD 기반으로 정리한 요약 프로필
    focus_areas: list[str]              # 면접에서 중점적으로 파고들 포인트 리스트

    # 개별 Q&A + feedback
    question: str                       # 현재 질문
    answer: str                         # 사용자가 입력한 답변
    feedback: str                       # 코칭 결과 (피드백 + 개선 답변)

    # 세션 요약
    qa_history: list[dict[str, str]]    # {"question", "answer", "feedback"} dict 리스트
    overall_feedback: str               # 세션 종합 피드백
    