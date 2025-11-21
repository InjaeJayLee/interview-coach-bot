from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal
from uuid import uuid4

from app.graph.graph_builder import build_profile_question_graph
from app.graph.nodes.coaching_node import coaching_node
from app.graph.nodes.question_node import question_node
from app.graph.nodes.summary_node import summary_node
from app.graph.state import InterviewState


MAX_QUESTIONS_PER_SESSION = 5

class QAHistoryItem(BaseModel):
    question: str
    answer: str
    feedback: str = ""


class SessionData(BaseModel):
    session_id: str
    profile_summary: str
    focus_areas: list[str]
    previous_questions: list[str]
    history: list[QAHistoryItem]
    mode: Literal["practice", "mock"] = "practice"


SESSIONS: dict[str, SessionData] = {}

# FastAPI 인스턴스 생성
app = FastAPI(
    title="Interview Coaching Bot API",
    version="0.1.0",
)

graph = build_profile_question_graph()


class InitInterviewRequest(BaseModel):
    resume_text: str
    job_description: str
    career_note: Optional[str] = None


class InitInterviewResponse(BaseModel):
    profile_summary: str
    focus_areas: list[str]
    question: str


class CoachingRequest(BaseModel):
    question: str
    answer: str
    profile_summary: Optional[str] = None


class CoachingResponse(BaseModel):
    feedback: str


# 세션용
class SessionInitRequest(BaseModel):
    resume_text: str
    job_description: str
    career_note: Optional[str] = None
    mode: Literal["practice", "mock"] = "practice"


class SessionInitResponse(BaseModel):
    session_id: str
    profile_summary: str
    focus_areas: list[str]
    question: str


class SessionAnswerRequest(BaseModel):
    session_id: str
    answer: str


class SessionAnswerResponse(BaseModel):
    question: str       
    answer: str
    feedback: str
    next_question: Optional[str] = None
    finished: bool


class SessionSummaryRequest(BaseModel):
    session_id: str


class SessionSummaryResponse(BaseModel):
    overall_feedback: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/v1/interview/init", response_model=InitInterviewResponse)
def init_interview(req: InitInterviewRequest):
    init_state: InterviewState = {
        "resume_text": req.resume_text,
        "job_description": req.job_description,
    }
    if req.career_note:
        init_state["career_note"] = req.career_note

    final_state = graph.invoke(init_state)

    profile_summary = final_state.get("profile_summary", "").strip()
    focus_areas = final_state.get("focus_areas", [])
    question = final_state.get("question", "").strip()

    return InitInterviewResponse(
        profile_summary=profile_summary,
        focus_areas=focus_areas,
        question=question,
    )


@app.post("/api/v1/interview/coach", response_model=CoachingResponse)
def coach_answer(req: CoachingRequest):
    state: InterviewState = {
        "question": req.question,
        "answer": req.answer,
    }
    if req.profile_summary:
        state["profile_summary"] = req.profile_summary

    final_state = coaching_node(state)
    feedback = final_state.get("feedback", "").strip()

    return CoachingResponse(feedback=feedback)


@app.post("/api/v1/interview/session/init", response_model=SessionInitResponse)
def session_init(req: SessionInitRequest):
    init_state: InterviewState = {
        "resume_text": req.resume_text,
        "job_description": req.job_description,
    }
    if req.career_note:
        init_state["career_note"] = req.career_note

    final_state = graph.invoke(init_state)

    profile_summary = final_state.get("profile_summary", "").strip()
    focus_areas = final_state.get("focus_areas", [])
    question = final_state.get("question", "").strip()

    if not question:
        raise HTTPException(status_code=500, detail="질문 생성에 실패했습니다.")

    session_id = str(uuid4())

    session = SessionData(
        session_id=session_id,
        profile_summary=profile_summary,
        focus_areas=focus_areas,
        previous_questions=[question],
        history=[],
        mode=req.mode,
    )
    SESSIONS[session_id] = session

    return SessionInitResponse(
        session_id=session_id,
        profile_summary=profile_summary,
        focus_areas=focus_areas,
        question=question,
    )


@app.post("/api/v1/interview/session/answer", response_model=SessionAnswerResponse)
def session_answer(req: SessionAnswerRequest):
    session = SESSIONS.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")

    return _handle_session_answer(session, req.answer)


@app.post("/api/v1/interview/session/summary", response_model=SessionSummaryResponse)
def session_summary(req: SessionSummaryRequest):
    session = SESSIONS.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")

    if not session.history:
        raise HTTPException(status_code=400, detail="아직 답변 기록이 없습니다.")

    qa_history = [
        {
            "question": item.question,
            "answer": item.answer,
            "feedback": item.feedback,
        }
        for item in session.history
    ]

    state_for_summary: InterviewState = {
        "profile_summary": session.profile_summary,
        "focus_areas": session.focus_areas,
        "qa_history": qa_history,
    }

    final_state = summary_node(state_for_summary)
    overall_feedback = final_state.get("overall_feedback", "").strip()

    return SessionSummaryResponse(
        overall_feedback=overall_feedback,
    )


def _handle_session_answer(session: SessionData, answer_text: str) -> SessionAnswerResponse:
    if not session.previous_questions:
        raise HTTPException(status_code=400, detail="세션에 질문이 없습니다.")

    current_question = session.previous_questions[-1]

    feedback = ""  # mock일 경우 비어있는 string
    if session.mode == "practice":
        state_for_coaching: InterviewState = {
            "question": current_question,
            "answer": answer_text,
            "profile_summary": session.profile_summary,
        }
        coached_state = coaching_node(state_for_coaching)
        feedback = coached_state.get("feedback", "").strip()

    session.history.append(
        QAHistoryItem(
            question=current_question,
            answer=answer_text,
            feedback=feedback,
        )
    )

    next_question: Optional[str] = None
    finished = False

    if len(session.previous_questions) >= MAX_QUESTIONS_PER_SESSION:
        finished = True
    else:
        state_for_question: InterviewState = {
            "profile_summary": session.profile_summary,
            "focus_areas": session.focus_areas,
            "previous_questions": session.previous_questions,
        }
        q_state = question_node(state_for_question)
        candidate = q_state.get("question", "").strip()

        if candidate:
            next_question = candidate
            session.previous_questions.append(candidate)
        else:
            finished = True

    return SessionAnswerResponse(
        question=current_question,
        answer=answer_text,
        feedback=feedback,
        next_question=next_question,
        finished=finished,
    )
