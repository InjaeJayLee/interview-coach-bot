from app.llm.client import llm
from app.graph.state import InterviewState
from app.prompts.question_prompts import QUESTION_GENERATION_SYSTEM_PROMPT, build_question_prompt


def question_node(state: InterviewState) -> InterviewState:
    """
    profile_summary + focus_areas → question
    """

    profile_summary = state.get("profile_summary", "")
    focus_areas = state.get("focus_areas", [])
    previous_questions = state.get("previous_questions", [])

    if not profile_summary.strip():
        raise ValueError("profile_summary가 비어 있어 질문을 생성할 수 없습니다.")
    
    question_prompt = build_question_prompt(profile_summary, focus_areas, previous_questions)

    content = llm.chat(
        messages=[
            {"role": "system", "content": QUESTION_GENERATION_SYSTEM_PROMPT},
            {"role": "user", "content": question_prompt}
        ],
        temperature=0.4,
    )

    new_state: InterviewState = {
        **state,
        "question": content,
    }
    return new_state
