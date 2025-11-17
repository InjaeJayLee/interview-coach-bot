from langgraph.graph import StateGraph, END

from app.graph.state import InterviewState
from app.graph.nodes.profile_node import profile_node
from app.graph.nodes.question_node import question_node


def build_graph():
    graph = StateGraph(InterviewState)

    graph.add_node("profile_node", profile_node)
    graph.add_node("question_node", question_node)
    
    graph.set_entry_point("profile_node")

    graph.add_edge("profile_node", "question_node")
    graph.add_edge("question_node", END)

    app = graph.compile()
    return app
