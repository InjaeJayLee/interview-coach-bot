from app.llm.client import llm
from app.graph.state import InterviewState
from app.prompts.summary_prompts import SESSION_SUMMARY_SYSTEM_PROMPT, build_session_summary_prompt


def summary_node(state: InterviewState) -> InterviewState:
    """
    세션 전체 Q/A 기록을 기반으로 종합 피드백(overall_feedback)을 생성하는 노드.
    """
    profile_summary = state.get("profile_summary", "").strip()
    focus_areas = state.get("focus_areas", [])
    qa_history = state.get("qa_history", [])

    if not profile_summary:
        raise ValueError("profile_summary가 비어 있어 세션 요약을 생성할 수 없습니다.")
    if not qa_history:
        raise ValueError("qa_history가 비어 있어 세션 요약을 생성할 수 없습니다.")

    summary_prompt = build_session_summary_prompt(
        profile_summary=profile_summary,
        focus_areas=focus_areas,
        qa_history=qa_history,
    )

    content = llm.chat(
        messages=[
            {"role": "system", "content": SESSION_SUMMARY_SYSTEM_PROMPT},
            {"role": "user", "content": summary_prompt},
        ],
        temperature=0.4,
    )

    overall_feedback = (content or "").strip()

    new_state: InterviewState = {
        **state,
        "overall_feedback": overall_feedback,
    }
    return new_state
