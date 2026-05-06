from langgraph.graph import StateGraph, END
from graphs.state import PipelineState
from graphs.nodes.generate import generate_node
from graphs.nodes.review import review_node, route_after_review
from graphs.nodes.emit import emit_node


def build_graph(checkpointer=None):
    builder = StateGraph(PipelineState)

    builder.add_node("generate", generate_node)
    builder.add_node("review", review_node)
    builder.add_node("emit", emit_node)

    builder.set_entry_point("generate")
    builder.add_edge("generate", "review")
    builder.add_conditional_edges("review", route_after_review, {
        "emit": "emit",
        "generate": "generate",
    })
    builder.add_edge("emit", END)

    # langgraph dev injects its own checkpointer at runtime — don't provide one
    # at module level. Tests pass MemorySaver() explicitly.
    return builder.compile(checkpointer=checkpointer, interrupt_after=["emit"])


# Module-level graph instance for langgraph.json — no custom checkpointer;
# the langgraph dev server / Cloud Run runtime injects persistence automatically.
graph = build_graph()
