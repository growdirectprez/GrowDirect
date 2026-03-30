---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Cowork Session: Fix Companion Guide Brand Template Problem

## Context for All Agents

Jess produced two Companion Guides (Functional v1.0 and Technical v1.0). The content is excellent — reviewed, complete, compliant. But the documents are NOT using the correct Canary Document Template formatting. We ran the docs three times and attempted an ALX XML-level font swap — the output still doesn't match the brand template.

**The root cause is in Jess's profile.** Her Agentic Rule #1 says "reference `brand/BRAND_GUIDE_v3.html`" for typography. That HTML file specifies **Inter** (body) and **Space Grotesk** (headings) — those are WEB fonts for screen rendering. The actual Word document template at `Canary/brand/Canary_Document_Template.docx` uses **Calibri** throughout with specific heading sizes, colors, spacing, and branded header/footer.

Jess's profile has no explicit instruction to use `Canary_Document_Template.docx` as the **style source** for .docx output. She references "templates in `brand/`" generically but the font instruction overrides that with the HTML brand guide.

---

## What Needs to Happen This Session

### 1. EVA — Gate Enforcement (you own delivery quality)

- Review the current Canary Document Template: `/Users/geofflyle/GrowDirect/Canary/brand/Canary_Document_Template.docx`
- Confirm these are the brand-correct styles for Word output:
  - **Font:** Calibri throughout (body 11pt #333333, H1 18pt bold #0D1117, H2 14pt bold #161B22, H3 12pt bold #6B7280)
  - **Header:** Two-column table — "CANARY" in Signal Yellow (#FBBF24) left, doc title in gray (#6B7280) right, thin dark border bottom
  - **Footer:** Two-column table — "Confidential" italic gray left, "Page [N]" gray right, thin dark border top
  - **Page:** US Letter, 1" margins
- Add this as a Factory Process gate: **No .docx deliverable ships without matching `Canary_Document_Template.docx` styles.** This is a QC check, same as Jim's test gate.

### 2. JESS — Rebuild Both Guides on the Correct Template

**Critical instruction:** When producing .docx files, you MUST use the `docx` skill (read `/mnt/skills/public/docx/SKILL.md` FIRST). The approach:

**Option A (Preferred — rebuild from template):**
1. Read the SKILL.md for docx creation
2. Unpack `Canary/brand/Canary_Document_Template.docx` to examine its exact XML styles, header, and footer
3. Extract content from the existing guides using pandoc: 
   - `pandoc Canary_Functional_Companion_Guide_v1.0.docx -o functional.md`
   - `pandoc Canary_Technical_Companion_Guide_v1.0.docx -o technical.md`
4. Rebuild each document using the `docx-js` approach from the skill, applying the EXACT styles from the template:
   - Calibri font family throughout (NOT Inter, NOT Space Grotesk)
   - Heading styles matching the template XML exactly
   - Header and footer matching the template XML exactly
5. Validate with `python scripts/office/validate.py`

**Option B (XML surgery):**
1. Unpack each guide with `python scripts/office/unpack.py`
2. Replace `word/styles.xml` with the template's `styles.xml`
3. Replace `word/header1.xml` with the template's `header1.xml` (update doc title text)
4. Replace `word/footer1.xml` with the template's `footer1.xml`
5. Search ALL XML files for any remaining "Inter" or "Space Grotesk" references and replace with "Calibri"
6. Repack with `python scripts/office/pack.py`
7. Validate

**For BOTH approaches:** The final test is visual. Convert to PDF (`python scripts/office/soffice.py --headless --convert-to pdf`) and verify headings are Calibri, header shows "CANARY" in yellow, footer shows "Confidential" + page number.

**Source files:**
- Template: `/Users/geofflyle/GrowDirect/Canary/brand/Canary_Document_Template.docx`
- Functional Guide: `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Jess/Canary_Functional_Companion_Guide_v1.0.docx`
- Technical Guide: `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Jess/Canary_Technical_Companion_Guide_v1.0.docx`

### 3. ALX — Profile Fix + Process Fix

After Jess delivers corrected docs, ALX will:

1. **Update Jess's profile** (`Company/Team/Jess.md`) to add a standing instruction:

   In Agentic Rule #1, change from:
   > "Always check the brand guide first. Before producing or reviewing any document, reference `brand/BRAND_GUIDE_v3.html`"
   
   To:
   > "Always check the brand guide AND the document template first. For .docx output, the style source is `Canary/brand/Canary_Document_Template.docx` (Calibri fonts, branded header/footer). For web/screen output, reference `brand/BRAND_GUIDE_v3.html` (Inter + Space Grotesk). The HTML brand guide defines the visual identity. The .docx template defines how that identity renders in Word documents. They are not interchangeable."

2. **Add to Core Principle #2** a clarification:
   > "Typography varies by medium: Word documents use Calibri (per `Canary_Document_Template.docx`). Web and screen use Inter + Space Grotesk (per `BRAND_GUIDE_v3.html`). Both are correct for their medium."

3. **Update TRIAGE.md** with resolution

---

## Acceptance Criteria

- [ ] Both guides open in Word/Pages/LibreOffice showing Calibri fonts throughout
- [ ] Headers show "CANARY" in Signal Yellow + doc title in gray
- [ ] Footers show "Confidential" + page numbers
- [ ] All content from v1.0 preserved — zero content loss
- [ ] Jess's profile updated to prevent recurrence
- [ ] Eva confirms this is now a Factory Process QC check

---

## File Locations Reference

| What | Path |
|------|------|
| Document template | `/Users/geofflyle/GrowDirect/Canary/brand/Canary_Document_Template.docx` |
| Presentation template | `/Users/geofflyle/GrowDirect/Canary/brand/Canary_Presentation_Template.pptx` |
| HTML Brand Guide | `/Users/geofflyle/GrowDirect/Canary/brand/BRAND_GUIDE_v3.html` |
| Functional Guide (current) | `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Jess/Canary_Functional_Companion_Guide_v1.0.docx` |
| Technical Guide (current) | `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Jess/Canary_Technical_Companion_Guide_v1.0.docx` |
| Jess profile | `/Users/geofflyle/GrowDirect/Company/Team/Jess.md` |
| DOCX Skill | `/mnt/skills/public/docx/SKILL.md` |
