from app.graph.graph_builder import build_graph
from app.graph.state import InterviewState


def main():
    graph_app = build_graph()

    # 테스트용
    sample_resume = """
    - 데이터 분석가로 3년간 커머스/여행 도메인에서 근무
    - Python, SQL, Airflow 기반으로 ETL 및 분석 파이프라인 구축
    - 검색 랭킹 모델, 항공권 판매 실적 예측 모델 개발
    - Superset 대시보드 구축 자동화
    """
    sample_jd = """
    [주요 업무]
    - 데이터 분석 및 실험 설계를 통해 서비스 개선 기회를 발굴
    - SQL, Python을 활용한 데이터 파이프라인 및 분석 자동화
    - 비즈니스 의사결정을 지원하는 핵심 지표 정의 및 대시보드 구축

    [자격 요건]
    - 데이터 분석 혹은 관련 분야 3년 이상 경력
    - SQL 숙련자, Python을 활용한 분석 경험
    - A/B 테스트, 코호트 분석 등 실무 경험
    """

    sample_answer = """
    이전 회사에서 항공권 월별 판매 실적 예측 모델을 고도화한 경험이 있습니다.
    기존에는 단순히 리드타임별 과거 평균 CDF를 사용해서 예측했지만,
    명절/휴가철, 항공사별 프로모션, 취소율 같은 요인이 제대로 반영되지 않아 정확도가 낮았습니다.
    모든 요소를 한꺼번에 반영하기에는 시간이 부족했기 때문에,
    제가 취했던 방법은 임팩트가 큰 부분부터 우선순위를 정해 순차적으로 반영하는 것이었습니다.
    그 중 단기간에 가장 큰 영향을 줄 수 있다고 판단한 연휴 효과를 먼저 반영했고,
    나머지 요소들은 마일스톤을 세워 단계적으로 반영하기로 했습니다.
    그 결과, 연휴 효과만 우선 반영했음에도 실적 예측 정확도가 약 15~20% 개선되었습니다.
    이후 취소율과 계절성, 항공사 프로모션 효과 등을 순차적으로 반영하면서 모델 성능을 점진적으로 고도화할 수 있었습니다.
    """

    init_state: InterviewState = {
        "resume_text": sample_resume,
        "job_description": sample_jd,
        "answer": sample_answer,
    }

    final_state = graph_app.invoke(init_state)

    print("===== [PROFILE SUMMARY] =====")
    print(final_state.get("profile_summary", "").strip())
    print()

    print("===== [FOCUS AREAS] =====")
    focus_areas = final_state.get("focus_areas", [])
    for i, item in enumerate(focus_areas, start=1):
        print(f"{i}. {item}")
    print()

    print("===== [GENERATED QUESTION] =====")
    print(final_state.get("question", "").strip())
    print()

    print("===== [COACHING FEEDBACK] =====")
    print(final_state.get("feedback", "").strip())


if __name__ == "__main__":
    main()
