from typing import TypedDict


class PipelineState(TypedDict):
    task: str              # human-provided task description
    service: str           # Cloud Run service name / output subdirectory
    artifacts: dict[str, str]   # relative-path → file content
    review_result: str     # "approved" | "needs_revision" | ""
    revision_count: int    # guard: abort after 3 revisions
    deploy_status: str     # "ok" | "failed" | ""
    error: str             # last error message, empty if none
    output_dir: str        # emit destination, default: out/<service>
