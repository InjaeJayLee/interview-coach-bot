from app.config import client, DEFAULT_MODEL
from app.graph.state import InterviewState
from app.prompts.coaching_prompts import INTERVIEW_COACH_SYSTEM_PROMPT, build_coaching_prompt


def coaching_node(state: InterviewState) -> InterviewState:
    """
    question + answer (+ profile_summary) → feedback 생성
    """

    question = state.get("question", "").strip()
    answer = state.get("answer", "").strip()
    profile_summary = state.get("profile_summary", "").strip()

    if not question:
        raise ValueError("question이 비어 있어 코칭을 수행할 수 없습니다.")
    if not answer:
        raise ValueError("answer가 비어 있어 코칭을 수행할 수 없습니다.")
    
    coaching_prompt = build_coaching_prompt(
        question=question,
        answer=answer,
        profile_summary=profile_summary or None,
    )

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": INTERVIEW_COACH_SYSTEM_PROMPT},
            {"role": "user", "content": coaching_prompt}
        ],
        temperature=0.4,
    )

    feedback = (response.choices[0].message.content or "").strip()

    new_state: InterviewState = {
        **state,
        "feedback": feedback,
    }
    return new_state
