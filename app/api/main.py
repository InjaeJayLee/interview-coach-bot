from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from app.graph.graph_builder import build_profile_question_graph
from app.graph.nodes.coaching_node import coaching_node
from app.graph.state import InterviewState


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
