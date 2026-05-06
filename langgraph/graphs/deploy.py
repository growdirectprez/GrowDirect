from langgraph.graph import StateGraph, END
from graphs.state import PipelineState
from graphs.nodes.deploy_run import deploy_run_node


def route_after_deploy(state: PipelineState):
    if state.get("deploy_status") == "ok":
        return END
    return "interrupt_on_failure"


def build_graph(checkpointer=None):
    builder = StateGraph(PipelineState)
    builder.add_node("deploy_run", deploy_run_node)
    builder.set_entry_point("deploy_run")
    builder.add_conditional_edges("deploy_run", route_after_deploy, {
        END: END,
        "interrupt_on_failure": END,  # interrupt_after handles the pause
    })

    # langgraph dev injects its own checkpointer — don't provide one at module level
    return builder.compile(checkpointer=checkpointer, interrupt_after=["deploy_run"])


graph = build_graph()
