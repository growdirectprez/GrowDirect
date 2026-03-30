---
name: file-guardian
description: |
  Protected file modification gate. Use before modifying any file listed as
  protected in the app's CLAUDE.md. Enforces approval, pre/post-flight
  validation, and manifest tracking. Agents MUST use this skill — direct
  edits to protected files are not allowed.
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
---

# File Guardian — Protected File Gate

You are about to modify a protected file. This skill enforces an approval gate with
validation. Follow every step. Do not skip steps. Do not modify protected files
outside of this skill.

## Protected Files

Each app defines its own protected file list in its CLAUDE.md. Common protected files:

| File Pattern | Typical Validation |
|---|---|
| `.env` | Env validation script + health check |
| `wsgi.py` | Health endpoint returns 200 |
| `*/session_factory.py` or `*/extensions.py` | Health check + DB connection test |
| `Dockerfile` | `docker build --check .` or syntax validation |
| `docker-compose*.yml` | `docker compose -f <file> config --quiet` |

**Check your app's CLAUDE.md** for the exact list and validation commands.

## Step 1: Identify the file

Which protected file are you modifying? If the file is not in the app's protected
file list, this skill does not apply — proceed normally.

If you are modifying multiple protected files, run this skill once per file.

## Step 2: Pre-flight — snapshot and integrity check

```bash
# Compute current hash
FILE="<path-to-file>"
CURRENT_HASH=$(shasum -a 256 "$FILE" | awk '{print $1}')
echo "Current SHA256: $CURRENT_HASH"

# Check manifest if it exists
MANIFEST_DIR=$(dirname "$FILE")
if [ -f "$MANIFEST_DIR/.guardian-manifest" ]; then
  cat "$MANIFEST_DIR/.guardian-manifest" | python3 -c "
import sys, json
m = json.load(sys.stdin)
f = m.get('files', {}).get('$FILE', {})
print(f'Manifest SHA256: {f.get(\"sha256\", \"(not in manifest)\")}')
print(f'Last edit: {f.get(\"last_guardian_edit\", \"unknown\")}')
print(f'Reason: {f.get(\"reason\", \"unknown\")}')
"
fi
```

**If hash matches manifest:** Proceed to Step 3.

**If hash does NOT match manifest:** STOP. The file was modified outside the
guardian process. Show the diff and ask the user whether to accept the current
state as baseline or investigate.

## Step 3: Present the change

Tell the user:

1. **Which file** you need to modify
2. **Why** — what problem this solves or what GRO issue this serves
3. **What changes** — specific lines, vars, or blocks being added/removed/changed
4. **For `.env`:** mask any secret values (show `SECRET_KEY=EAAAl...***`)

Then ask: **"Approve this change?"**

**Do not proceed without explicit approval.**

## Step 4: Save a backup

```bash
cp "$FILE" "$FILE.guardian-backup"
```

## Step 5: Make the edit

Apply the approved change using the Edit or Write tool.

## Step 6: Post-flight validation

Run the validation command from the app's CLAUDE.md for this file.

**If validation passes:** Proceed to Step 7.

**If validation fails:** Revert immediately:

```bash
cp "$FILE.guardian-backup" "$FILE"
rm "$FILE.guardian-backup"
```

Report what failed. Do not retry without presenting a revised change.

## Step 7: Update manifest (if applicable)

```bash
NEW_HASH=$(shasum -a 256 "$FILE" | awk '{print $1}')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

python3 -c "
import json, os
manifest_path = '.guardian-manifest'
if os.path.exists(manifest_path):
    with open(manifest_path, 'r') as f:
        m = json.load(f)
else:
    m = {'files': {}}
m['files']['$FILE'] = {
    'sha256': '$NEW_HASH',
    'last_guardian_edit': '$TIMESTAMP',
    'reason': '<REASON>'
}
m['updated_at'] = '$TIMESTAMP'
m['gro_issue'] = '<GRO-XXX>'
with open(manifest_path, 'w') as f:
    json.dump(m, f, indent=2)
    f.write('\n')
print('Manifest updated.')
"
```

## Step 8: Cleanup

```bash
rm -f "$FILE.guardian-backup"
```

## Reminders

- **One file per invocation.** If you need to edit `.env` and `wsgi.py`, run this
  skill twice.
- **No batching approvals.** Each file gets its own approval.
- **Revert on failure.** If validation fails, restore the backup. No exceptions.
- **Mask secrets.** Never show full values of TOKEN, SECRET, KEY, PASSWORD vars.
- **This skill is mandatory.** CLAUDE.md requires it. Skipping it is a violation.
