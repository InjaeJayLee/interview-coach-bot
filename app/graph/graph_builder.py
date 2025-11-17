from langgraph.graph import StateGraph, END

from app.graph.state import InterviewState
from app.graph.nodes.profile_node import profile_node


def build_profile_graph():
    graph = StateGraph(InterviewState)

    graph.add_node("profile", profile_node)
    
    graph.set_entry_point("profile")

    graph.add_edge("profile", END)

    app = graph.compile()
    return app
