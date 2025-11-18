from app.config import client, DEFAULT_MODEL
from app.graph.state import InterviewState
from app.prompts.question_prompts import QUESTION_GENERATION_SYSTEM_PROMPT, build_question_prompt


def question_node(state: InterviewState) -> InterviewState:
    """
    profile_summary + focus_areas → question
    """

    profile_summary = state.get("profile_summary", "")
    focus_areas = state.get("focus_areas", [])

    if not profile_summary.strip():
        raise ValueError("profile_summary가 비어 있어 질문을 생성할 수 없습니다.")
    
    question_prompt = build_question_prompt(profile_summary, focus_areas)

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": QUESTION_GENERATION_SYSTEM_PROMPT},
            {"role": "user", "content": question_prompt}
        ],
        temperature=0.4,
    )

    content = (response.choices[0].message.content or "").strip()
    # if content.startswith(("1.", "1)", "- ")):
    #     parts = content.split(maxsplit=1)
    #     if len(parts) == 2:
    #         content = parts[1].strip()

    new_state: InterviewState = {
        **state,
        "question": content,
    }
    return new_state
