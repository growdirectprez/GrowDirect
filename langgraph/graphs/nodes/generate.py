import os
from langchain_core.language_models import BaseChatModel
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from graphs.state import PipelineState

SYSTEM_PROMPT = """You are an expert Go engineer working on the Canary Go platform.
Module: github.com/growdirect-llc/rapidpos
Stack: Go 1.22+, Chi v5, pgx/v5, PostgreSQL 17, Valkey 8
Conventions: UUID PKs, created_at/updated_at on all tables, Chi handlers, pgx direct for simple queries.

When given a task, produce Go source files needed to implement it.
Format your response as a sequence of files, each preceded by a line:
FILE: <relative/path/from/repo/root.go>
followed by the complete file content, then END_FILE.
Produce only files that need to change. Be complete — no placeholders."""


def _default_llm() -> BaseChatModel:
    return ChatAnthropic(
        model=os.getenv("LLM_MODEL", "claude-sonnet-4-5"),
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )


def _parse_artifacts(text: str) -> dict[str, str]:
    artifacts: dict[str, str] = {}
    parts = text.split("FILE: ")
    for part in parts[1:]:
        lines = part.split("\n", 1)
        if len(lines) < 2:
            continue
        path = lines[0].strip()
        content = lines[1].split("END_FILE")[0].strip()
        artifacts[path] = content
    return artifacts


def generate_node(state: PipelineState, llm: BaseChatModel | None = None) -> dict:
    if llm is None:
        llm = _default_llm()

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Task: {state['task']}\n\nService: {state['service']}"),
    ]
    response = llm.invoke(messages)
    artifacts = _parse_artifacts(response.content)

    # Fallback: if LLM didn't use FILE: format, store raw as a note
    if not artifacts:
        artifacts["_llm_output.txt"] = response.content

    return {
        "artifacts": artifacts,
        "revision_count": state.get("revision_count", 0),
    }
