import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel


def make_mock_llm(responses: list[str]) -> FakeListChatModel:
    """Returns a FakeListChatModel that cycles through the given string responses."""
    return FakeListChatModel(responses=responses)


@pytest.fixture
def llm_approved():
    """LLM that always returns an approved review."""
    return make_mock_llm(["APPROVED"])


@pytest.fixture
def llm_needs_revision():
    """LLM that returns needs-revision once, then approves."""
    return make_mock_llm(["NEEDS_REVISION: missing error handling", "APPROVED"])


@pytest.fixture
def base_state() -> dict:
    return {
        "task": "add a health check endpoint to the hawk service",
        "service": "canary-hawk",
        "artifacts": {},
        "review_result": "",
        "revision_count": 0,
        "deploy_status": "",
        "error": "",
        "output_dir": "out/canary-hawk",
    }
