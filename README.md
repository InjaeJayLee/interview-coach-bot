# AI Interview Coach 
음성 기반 실시간 모의 면접 · STT · TTS · 자동 질문 생성 · 피드백 요약 · 종합 리뷰 기능을 포함한 인터뷰 코칭 웹 애플리케이션

---

## 🎯 프로젝트 개요

**AI Interview Coach**은 지원자의 이력서·JD 기반으로 **자동 질문 생성**을 수행하고,  
사용자는 브라우저에서 **음성으로 답변 → 음성 인식(STT) → 텍스트 수정 → 전송**하는 방식으로  
실제 면접과 거의 동일한 흐름을 경험할 수 있는 웹 애플리케이션입니다.

각 질문에 대한 짧고 핵심적인 피드백과, 세션 종료 후의 **종합 피드백 리포트**까지 제공하여  
면접 대비에 큰 도움을 줄 수 있습니다.


---

## ✨ 주요 기능

### ✔ 1. 이력서 & JD 기반 질문 생성
- 이력서와 JD, career note(선택)를 기반으로 사용자 Profile Summary 생성하고 Focus Area를 도출
- 첫 질문 자동 생성
- TTS로 질문 자동 읽기

### ✔ 2. 음성 기반 답변 → STT 변환
- 음성으로 답변 후 텍스트로 변환
- 인식된 텍스트가 올바른지 확인 후 필요하다면 사용자가 직접 수정 가능

### ✔ 3. 질문별 피드백
- 답변 평가
    1. 질문에 대한 답변 적절성
    2. 답변이 STAR(상황, 과제, 행동, 결과) 구조를 잘 따르는지
- 데이터/지표/비즈니스 임팩트 관점에서 답변의 강점과 보완점을 피드백
- 면접 태도, 커뮤니케이션 관점(논리 흐름, 길이, 표현, 집중도)에서 피드백

### ✔ 4. 자연스러운 모의 면접 흐름
- 답변 전송 → 다음 질문 자동 생성
- TTS로 자동 재생

### ✔ 5. 세션 종료 후 종합 피드백 리포트
- 전체 총평
- 강점
- 개선점
- 연습 가이드


---

## 🏗 아키텍처

```bash
.
├─ app/
│  ├─ api/
│  │  └─ main.py                  # FastAPI 엔트리 포인트 (라우터, 세션/엔드포인트 정의)
│  │
│  ├─ audio/
│  │  └─ transcriber.py           # STT 래퍼 모듈 (Whisper/Faster-Whisper로 음성 → 텍스트 변환)
│  │
│  ├─ graph/
│  │  ├─ graph_builder.py         # 인터뷰 플로우(Graph) 구성 (프로필 요약 → 질문 생성 파이프라인) [테스트용]
│  │  ├─ state.py                 # InterviewState 등 그래프에서 공유하는 상태 타입 정의
│  │  └─ nodes/
│  │      ├─ profile_node.py      # 이력서 + JD 기반 profile_summary / focus_areas 생성 노드
│  │      ├─ question_node.py     # 질문 생성 노드
│  │      ├─ coaching_node.py     # 개별 답변에 대한 피드백 생성 노드
│  │      └─ summary_node.py      # 세션 전체 종합 피드백 생성 노드
│  │
│  ├─ llm/
│  │  └─ client.py                # OpenAI, Anthropic LLM 호출 래퍼
│  │
│  └─ prompts/
│      ├─ profile_prompts.py      # 프로필 요약과 질문 기반이 될 포인트 요약용 프롬프트
│      ├─ question_prompts.py     # 질문 생성용 프롬프트
│      ├─ coaching_prompts.py     # 개별 답변 코칭용 프롬프트
│      └─ summary_prompts.py      # 세션 종합 피드백용 프롬프트
│
├─ static/
│  └─ interview.html               # 브라우저용 프론트엔드 (TTS, 녹음, STT, 피드백/요약 UI)
│
├─ requirements.txt                
└─ README.md                       
```

---

## ⚙️ 기술 스택

- OpenAI GPT
- Anthropic Claude
- LangGraph
- edge-tts (TTS)  
- Whisper / Faster-Whisper (STT) 
- FastAPI  
- Pydantic 

---

## 🚀 사용법 (Usage)

이 섹션은 **환경 변수 설정 → 서버 실행 → 웹 인터페이스 이용 방법**까지  
모든 절차를 순서대로 정리했습니다.

---

### 1. 사전 요구사항 (Prerequisites)

다음 환경이 필요합니다:

- Python 3.11  
- FFmpeg (Whisper/Faster-Whisper, MediaRecorder WebM 변환용)
- GPU 사용 시: CUDA 환경(optional)
- OpenAI API Key  
- Anthropic API Key  

---

### 2. .env 파일 생성

git clone 실행 후 프로젝트 루트에 존재하는 **.dummy_env** 파일명을 **.env**로 변경한 뒤 각 API KEY 값을 입력

```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

---

### 3. FastAPI 서버 실행

터미널에서 아래 명령어 실행
```
uvicorn app.api.main:app --reload
```

---

### 4. 웹 인터페이스 접속

브라우저에서 아래 URL 열기
```
http://localhost:8000/static/interview.html
```