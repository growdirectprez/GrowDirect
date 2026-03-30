---
type: workorder
domain: infra
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy — Test & Debug `canary-deploy` Skill
*Issued by ALX · February 26, 2026 · Priority: 🟡 HIGH — QA pipeline enabler*

---

## Context

ALX just scaffolded the `canary-deploy` Claude Code skill. It lives at:
```
Canary/.claude/skills/canary-deploy/SKILL.md
```

This skill defines the 7-step dev→QA deployment pipeline as discrete, verifiable steps
with gate checks. It's a scaffold — the logic is correct but it hasn't been run against
real infrastructure yet. Your job is to test it end-to-end in Claude Code, find where
it breaks, and fix it.

The goal: one session where you read the skill, run the pipeline against real machines,
and come out the other end with QA (`192.168.10.117`) running a clean Docker stack
pulled from a verified GitHub push.

---

## What You're Testing

The pipeline is 7 steps:

```
STEP 1: DEV GATE CHECK        — Branch, working tree, tests passing
STEP 2: GIT PUSH              — Push alpha-clean to GitHub
STEP 3: QA CONNECTIVITY       — Ping + SSH to iMac (192.168.10.117)
STEP 4: QA STACK TEARDOWN     — Kill running containers on iMac
STEP 5: GIT PULL (on iMac)    — Pull latest, verify commit hashes match
STEP 6: DOCKER BUILD + UP     — Run canary_deploy.sh --full on iMac
STEP 7: VERIFY                — /health 200, /companion/demo 200
```

---

## Session Instructions (read these first)

### Step 1: Read the skill

Before running anything:
```
read Canary/.claude/skills/canary-deploy/SKILL.md
read Canary/.claude/skills/canary-deploy/references/environment.md
```

Understand what each step does, what each gate checks, and what the expected output is.

### Step 2: Run each step in sequence

Execute each step exactly as written in the skill. At each step, report:
```
[STEP N/7] <NAME>
  Before check: PASS / FAIL / SKIP (reason)
  Action: <what you ran>
  Output: <actual output, abbreviated>
  After verify: PASS / FAIL
  Gate: GREEN / RED
  → <next action>
```

Do not skip steps. If a step fails, stop and diagnose before proceeding.

### Step 3: Verify SSH key situation

Before Step 3, check which SSH key is actually configured for the iMac:
```bash
cat ~/.ssh/config | grep -A3 "192.168.10.117"
ssh-add -l
```

The skill references `~/.ssh/id_canary` but the active key may be different.
Update `Canary/.claude/skills/canary-deploy/references/environment.md` with the
correct key name if it differs.

### Step 4: Test `imac_deploy.sh` directly

After Steps 1–5 are green, run:
```bash
cd /Users/geofflyle/GrowDirect/Canary
./devops/imac_deploy.sh --status
```

If `--status` works, then run the full deploy:
```bash
./devops/imac_deploy.sh
```

Stream the output. Report the full `CANARY DEPLOYMENT REPORT` block at the end.

### Step 5: Document every deviation

The skill will have gaps. Every place where:
- The skill said "run X" but X didn't work
- A gate check produced unexpected output
- A step required a manual intervention not in the skill
- An error message wasn't covered in `references/troubleshooting.md`

...write it down. You'll fix these at the end.

---

## Acceptance Criteria

| # | Criterion | How to verify |
|---|---|---|
| AC-1 | Steps 1–5 pass cleanly from Mac Mini | All gate checks GREEN |
| AC-2 | Dev and QA commit hashes match after Step 5 | `IN SYNC` output from hash compare |
| AC-3 | `./devops/imac_deploy.sh` runs without intervention | Script exits 0 |
| AC-4 | Deploy report shows 0 failed tests | Report block at end |
| AC-5 | `/health` returns 200 from Mac Mini | `curl http://192.168.10.117:5001/health` |
| AC-6 | `/companion/demo` returns 200 | `curl` check |
| AC-7 | Any skill gap found is fixed in SKILL.md or references/ | Updated files committed |

---

## Fixes to Make During Session

As you hit issues, fix them directly:

1. **Wrong SSH key path** → Update `references/environment.md`
2. **Missing troubleshooting entry** → Add row to `references/troubleshooting.md`
3. **Command in skill doesn't work as written** → Fix the command in `SKILL.md`
4. **Fallback needed that isn't documented** → Add to `references/fallback-deploy.md`
5. **Step sequence wrong** → Reorder in `SKILL.md` with a comment explaining why

Do not create new files. Edit the existing skill files only.

---

## Known Issue to Investigate

**SSH key for iMac:** The skill currently says `~/.ssh/id_canary` but this may not
be correct. The Mac Mini's GitHub key is `id_github_growdirect`. The iMac SSH key
may be different. Verify and correct before anything else — it blocks Step 3.

---

## Output Expected at Session Close

1. **QA stack running** at `http://192.168.10.117:5002/companion/demo`
2. **Updated skill files** with any fixes applied
3. **Session report** (one paragraph): what worked, what needed fixing, what's still rough
4. **TRIAGE update** if any new blockers discovered

---

## Files

| File | Path |
|---|---|
| Skill (main) | `Canary/.claude/skills/canary-deploy/SKILL.md` |
| Environment ref | `Canary/.claude/skills/canary-deploy/references/environment.md` |
| Troubleshooting ref | `Canary/.claude/skills/canary-deploy/references/troubleshooting.md` |
| Fallback ref | `Canary/.claude/skills/canary-deploy/references/fallback-deploy.md` |
| Deploy script (local) | `Canary/devops/canary_deploy.sh` |
| Deploy script (remote) | `Canary/devops/imac_deploy.sh` |
| Deploy reports output | `Canary/devops/deploy_reports/` |

---

## Standing Rule

If you get to Step 6 and the Docker build fails: do not retry more than twice before
stopping and reporting. Build failures that repeat are a signal, not bad luck.
Surface the exact error and wait for direction.

---

*Issued by ALX. This is a single-session deliverable. AC-6 is the finish line.*
