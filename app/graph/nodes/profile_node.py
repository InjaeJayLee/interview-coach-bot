from app.config import client, DEFAULT_MODEL
from app.graph.state import InterviewState
from app.prompts.profile_prompts import PROFILE_SUMMARY_SYSTEM_PROMPT, build_profile_user_prompt


def _parse_profile_output(raw: str) -> tuple[str, list[str]]:
    """
    LLM이 생성한 텍스트에서
    - profile_summary (문단)
    - focus_areas (bullet list)
    를 분리해서 뽑아내는 헬퍼.

    프롬프트에서 [1] profile_summary, [2] focus_areas 구조 형태로 리턴하며 "[2]" 기준으로 자름.
    bullet(-, •) 줄들을 focus_areas로 간주.
    """

    text = raw.strip()
    focus_areas = []
    
    if "[2]" in text:
        before, after = text.split("[2]", 1)
        profile_summary = before.strip()
        focus_block = after
    else:
        # 혹시 "[2]"를 안 지켰으면 그냥 전체를 summary로 쓰고 끝
        return profile_summary, focus_areas

    # focus_block에서 bullet line들만 추출
    for line in focus_block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("-") or stripped.startswith("•"):
            # 맨 앞 bullet 기호 제거
            item = stripped.lstrip("-•").strip()
            if item:
                focus_areas.append(item)

    return profile_summary, focus_areas


def profile_nodes(state: InterviewState) -> InterviewState:
    """
    이력서/경력기술서 + JD + career_note(optional)를 기반으로
    - profile_summary
    - focus_areas
    를 생성해서 state에 채워넣는 노드.
    """
    resume_text = state.get("resume_text", "") or ""
    job_description = state.get("job_description", "") or ""
    career_note = state.get("career_note", "") or ""

    if not resume_text.strip():
        raise ValueError("resume_text가 비어 있습니다. 이력서/경력기술서를 입력해 주세요.")
    if not job_description.strip():
        raise ValueError("job_description이 비어 있습니다. JD 텍스트를 입력해 주세요.")

    user_prompt = build_profile_user_prompt(
        resume_text=resume_text,
        job_description=job_description,
        career_note=career_note or None,
    )

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": PROFILE_SUMMARY_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    raw_output = response.choices[0].message.content or ""
    profile_summary, focus_areas = _parse_profile_output(raw_output)

    new_state: InterviewState = {
        **state,
        "profile_summary": profile_summary,
        "focus_areas": focus_areas,
    }
    return new_state
