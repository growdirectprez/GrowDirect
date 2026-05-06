import os
from typing import Literal
from langchain_core.language_models import BaseChatModel
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from graphs.state import PipelineState

REVIEW_PROMPT = """You are reviewing Go code for the Canary Go platform.
Check for: correct package declarations, missing error handling, missing defer rows.Close(),
missing context propagation, hardcoded credentials, or obvious logic errors.

Respond with exactly one of:
- APPROVED  (if the code is acceptable)
- NEEDS_REVISION: <one-line reason>  (if there are issues)

Do not include any other text."""

MAX_REVISIONS = 3


def _default_llm() -> BaseChatModel:
    return ChatAnthropic(
        model=os.getenv("LLM_MODEL", "claude-sonnet-4-5"),
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )


def review_node(state: PipelineState, llm: BaseChatModel | None = None) -> dict:
    if llm is None:
        llm = _default_llm()

    artifacts_text = "\n\n".join(
        f"// FILE: {path}\n{content}"
        for path, content in state["artifacts"].items()
    )
    messages = [
        SystemMessage(content=REVIEW_PROMPT),
        HumanMessage(content=f"Task: {state['task']}\n\nCode:\n{artifacts_text}"),
    ]
    response = llm.invoke(messages)
    text = response.content.strip()

    if text.startswith("APPROVED"):
        return {"review_result": "approved"}
    return {"review_result": "needs_revision"}


def route_after_review(state: PipelineState) -> Literal["emit", "generate"]:
    if state["review_result"] == "approved":
        return "emit"
    if state.get("revision_count", 0) >= MAX_REVISIONS:
        return "emit"  # force emit with what we have; human reviews in portal
    return "generate"
