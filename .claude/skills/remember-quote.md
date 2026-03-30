---
name: remember-quote
description: |
  Capture CEO quotes and strategic insights from Jeffe for press releases,
  marketing, and public communications. Use whenever Jeffe says "remember that",
  "quote this", "log that quote", or makes a particularly quotable statement
  about strategy, mission, product vision, or Bitcoin philosophy.
allowed-tools:
  - Read
  - Edit
---

# Remember Quote

## Overview

Captures quotable moments from Jeffe (CEO) and logs them to
`~/GrowDirect/IP/Team/Jeffe_Quotes.md` with proper formatting, context, and
status tracking. Part of PR/communications responsibilities to curate CEO quotes
for press releases, investor materials, and marketing content.

## When to Use This Skill

**Explicit triggers:**
- "remember that", "quote this", "log that quote"
- "add that to my quotes"

**Proactive triggers** (use even without explicit request):
- Jeffe makes a statement about strategic positioning or competitive advantage
- Jeffe articulates mission, vision, or core principles
- Jeffe explains product philosophy or Bitcoin-native infrastructure
- Jeffe references a book, study, or external source worth tracking
- Jeffe makes an ethical or moral statement about data integrity
- Any statement that sounds like it belongs in a press release or investor deck

## Workflow

### Step 1: Identify the Quote

Extract the exact quote. Prefer direct quotes with quotation marks.

**Rules:**
- Capture 1-3 sentences (the quotable core)
- Remove verbal filler ("like", "you know", "um")
- Preserve Jeffe's authentic voice and tone

### Step 2: Determine Quote Type

**Regular Quote** → "Strategic Vision & Product Philosophy" section
**Book/Study Reference** → "Book & Study References" section

### Step 3: Gather Context

1. **Context**: What was being discussed? (1-2 sentences)
2. **Source**: Which document or conversation?
3. **Use Case**: Where could this quote be used?
4. **Keywords**: 3-5 key terms for searchability

### Step 4: Set Status

Default to **NEEDS POLISHING** unless:
- Jeffe explicitly says "use this as-is" → APPROVED
- Quote contains confidential strategy → CONFIDENTIAL
- Quote is a book/study citation → REFERENCE

### Step 5: Format and Append

**For regular quotes:**

```markdown
### [Date] — [Topic/Context Title]

> "[The actual quote]"

**Context:** [1-2 sentence description]
**Source:** [Document name or "Current conversation" + date]
**Use Case:** [Where this could be used]
**Keywords:** [keyword1, keyword2, keyword3]
**Status:** NEEDS POLISHING

---
```

**For book/study references:**

```markdown
### [Book/Study Title] — [Author/Source]
- **Quote Context:** "[The quote or concept]"
- **Source:** [Where Jeffe mentioned this]
- **Use Case:** [How this could be used]
- **Status:** REFERENCE

---
```

### Step 6: Append to File

**Critical**: Always APPEND to the quotes file, never overwrite.

**File location:** `~/GrowDirect/IP/Team/Jeffe_Quotes.md`

Use Edit tool to append (NOT Write tool which would overwrite).

### Step 7: Confirm

After appending: "Quote logged to Jeffe_Quotes.md" + show the formatted quote briefly.

## Important Rules

1. **Never overwrite the file** — Always append
2. **Default to NEEDS POLISHING** — Protect from unpolished quotes going public
3. **Preserve voice** — Don't over-edit when capturing
4. **Be proactive** — Don't wait for "quote this" if obviously quotable
5. **Date everything** — Use current date
6. **Check for duplicates** — Don't log the same quote twice
