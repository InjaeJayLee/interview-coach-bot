SESSION_SUMMARY_SYSTEM_PROMPT = """
당신은 해당 면접 포지션의 실무 경험이 풍부한 면접 코치입니다.

아래에 주어지는 정보는 한 번의 모의 면접 세션에서 오간
지원자의 프로필 요약([profile_summary])과 면접에서 중점적으로 확인한 목록([focus_areas]), 그리고 질문/답변각 답변에 대한 개별 피드백 목록([qa_history])입니다.

이를 바탕으로 인터뷰 전체에 대한 종합 피드백을 작성하세요.

출력 형식:
1. 전체 총평 (짧은 문단 2~3개)
2. 강점 (불릿 포인트 3~5개)
3. 개선이 필요한 부분 (불릿 포인트 3~5개)
4. 앞으로의 연습 가이드 (우선순위 3가지 정도, 번호 매기기)

반드시 한국어로 작성해 주세요.
"""


def build_session_summary_prompt(profile_summary: str, focus_areas: list[str], qa_history: list[dict[str, str]]) -> str:
    focus_text = (
        "\n".join(f"- {f}" for f in focus_areas) if focus_areas else "(없음)"
    )

    history_lines: list[str] = []
    for idx, item in enumerate(qa_history, start=1):
        q = item.get("question", "").strip()
        a = item.get("answer", "").strip()
        fb = item.get("feedback", "").strip()

        if not q and not a:
            continue

        history_lines.append(f"Q{idx}: {q}")
        history_lines.append(f"A{idx}: {a}")
        if fb:
            history_lines.append(f"Per-question feedback{idx}: {fb}")
        history_lines.append("")

    history_text = "\n".join(history_lines).strip() or "(아직 Q/A 기록이 없습니다.)"

    return f"""
        [profile_summary]
        {profile_summary}

        [focus_areas]
        {focus_text}

        [qa_history]
        {history_text}

        위 정보를 바탕으로, 이 모의 면접 세션 전체에 대한 종합 피드백을 작성해 주세요.
    """