# factory-assembly — Implementation

## Precondition

All blueprint tasks are defined. All tests are written and failing. Do not start assembly until TDD is complete.

## Task loop

For each task in the blueprint, in order:

1. **Read the task** from the plan — understand what it requires before touching any file.

2. **Execute the step** — make the specific change described. One task at a time.

3. **Run the test for this task**
   ```bash
   python3 -m pytest tests/path/test_file.py::test_name -v
   ```
   If it fails: stop. Diagnose the failure. Fix the implementation. Re-run. Do not move on with a red test.

4. **Run smoke tests**
   ```bash
   python3 -m pytest tests/ -k smoke -v
   ```
   If smoke breaks: you introduced a regression. Fix it before continuing.

5. **Commit**
   ```bash
   git add <specific files>
   git commit -m "feat: <task description> (GRO-XXX)"
   ```
   Commit after each task — not at the end of all tasks. Granular commits make regressions easy to isolate.

## Failure protocol

If a step fails:
- Stop immediately
- Read the error in full
- Check the relevant model/service/route for the cause
- Fix and re-run — do not skip or work around
- If the fix is outside scope: create a new Linear issue, note it, and return to the original task

## Scope control

If you notice a bug or missing feature outside the current GRO issue: note it, create a new Linear issue, and do not fix it inline. Scope creep is a defect.

## Assembly is done when

All tests from the TDD phase are green. Smoke tests pass. Every task has a commit.
