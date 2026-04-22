---
name: factory-linear
roles-primary:[ALX]
roles-assist:[ProgramManager]
description: |
  Standardized Linear integration at factory stage boundaries. Handles issue
  reads at preflight, status transitions at blueprint/ship, document attachment,
  and comment posting at close. All Linear MCP calls go through this skill.
allowed-tools:
  - Read
  - Bash
  - mcp__a018de2b-6aea-4cf1-aa2a-20375d7d8e69__get_issue
  - mcp__a018de2b-6aea-4cf1-aa2a-20375d7d8e69__save_issue
  - mcp__a018de2b-6aea-4cf1-aa2a-20375d7d8e69__save_comment
  - mcp__a018de2b-6aea-4cf1-aa2a-20375d7d8e69__create_document
  - mcp__a018de2b-6aea-4cf1-aa2a-20375d7d8e69__get_issue_status
  - mcp__a018de2b-6aea-4cf1-aa2a-20375d7d8e69__list_issue_statuses
---

# factory-linear — Linear Integration

Standardizes all Linear read/write operations at factory stage boundaries.

## Usage

This skill is invoked by other factory skills at stage transitions. It is not
typically invoked directly.

## Stage: Preflight

**Action:** Read and validate the GRO issue.

1. Use `get_issue` with the GRO identifier
2. Extract: title, description, status, labels, project, attachments
3. Validate the issue exists and is not completed/cancelled
4. Return issue data to preflight for context loading

## Stage: Blueprint

**Action:** Transition issue and attach plan.

1. Use `list_issue_statuses` to find the "In Progress" status ID for the team
2. Use `save_issue` to move the issue to "In Progress"
3. Use `create_document` to attach the implementation plan as a Linear document
4. Link the document to the issue

## Stage: Ship

**Action:** Post results and close.

1. Use `save_comment` to post verify/QA results summary:
   ```
   ## Ship Report
   - Tests: X passed, 0 failed
   - Migrations: applied / not needed
   - Branch: [branch name]
   - Commits: [count]
   ```
2. Use `list_issue_statuses` to find the "Done" status ID
3. Use `save_issue` to move to "Done"

## Stage: Close

**Action:** Post session summary.

1. Use `save_comment` to post:
   ```
   ## Session Summary
   **Completed:** [list of deliverables]
   **Pending:** [list or "none"]
   **New Issues:** [GRO numbers or "none"]
   ```

## Error Handling

If Linear MCP is unreachable at any stage:
- Log a warning: "Linear MCP unreachable — skipping [action]"
- Continue the pipeline — Linear integration is important but not blocking
- Note the skipped action in the session summary for manual follow-up
