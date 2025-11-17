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
