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

    init_state: InterviewState = {
        "resume_text": sample_resume,
        "job_description": sample_jd,
        # "career_note": "추가로 어필하고 싶은 내용이 있다면 여기에.",
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


if __name__ == "__main__":
    main()
