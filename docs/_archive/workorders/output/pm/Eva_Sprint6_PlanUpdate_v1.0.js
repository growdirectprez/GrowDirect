const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, LevelFormat
} = require("docx");

// Brand colors
const SIGNAL_YELLOW = "FBBF24";
const DEEP_BLUE = "1F4D78";
const DARK_BG = "1A1A2E";
const GREEN = "22C55E";
const RED = "EF4444";
const ORANGE = "F97316";
const GRAY = "6B7280";
const LIGHT_GRAY = "F3F4F6";
const WHITE = "FFFFFF";

const border = { style: BorderStyle.SINGLE, size: 1, color: "D1D5DB" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

// Page constants
const PAGE_WIDTH = 12240;
const MARGIN = 1440;
const CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN); // 9360

function headerCell(text, width) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: DEEP_BLUE, type: ShadingType.CLEAR },
    margins: cellMargins,
    children: [new Paragraph({ children: [new TextRun({ text, bold: true, color: WHITE, font: "Calibri", size: 20 })] })]
  });
}

function cell(text, width, opts = {}) {
  const runs = Array.isArray(text)
    ? text
    : [new TextRun({ text, font: "Calibri", size: 20, bold: opts.bold || false, color: opts.color || "000000" })];
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
    margins: cellMargins,
    children: [new Paragraph({ children: runs })]
  });
}

function statusRun(status) {
  const map = {
    "DONE": { text: "DONE", color: GREEN },
    "DELIVERED": { text: "DELIVERED", color: GREEN },
    "RESOLVED": { text: "RESOLVED", color: GREEN },
    "IN PROGRESS": { text: "IN PROGRESS", color: ORANGE },
    "ACTIVE": { text: "ACTIVE", color: ORANGE },
    "BLOCKED": { text: "BLOCKED", color: RED },
    "WAITING": { text: "WAITING", color: GRAY },
    "PENDING": { text: "PENDING", color: GRAY },
    "PARKED": { text: "PARKED", color: GRAY },
  };
  const s = map[status] || { text: status, color: "000000" };
  return new TextRun({ text: s.text, bold: true, color: s.color, font: "Calibri", size: 20 });
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Calibri", color: DEEP_BLUE },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Calibri", color: DEEP_BLUE },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 }
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: "Calibri", color: DARK_BG },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
      },
    ]
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_WIDTH, height: 15840 },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: SIGNAL_YELLOW, space: 1 } },
          spacing: { after: 120 },
          children: [
            new TextRun({ text: "GrowDirect", bold: true, font: "Calibri", size: 18, color: DEEP_BLUE }),
            new TextRun({ text: "  |  Sprint 6 Plan Update  |  February 28, 2026", font: "Calibri", size: 18, color: GRAY }),
          ]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: SIGNAL_YELLOW, space: 1 } },
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "INTERNAL \u2014 ", font: "Calibri", size: 16, color: GRAY }),
            new TextRun({ text: "Page ", font: "Calibri", size: 16, color: GRAY }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Calibri", size: 16, color: GRAY }),
          ]
        })]
      })
    },
    children: [
      // ===== TITLE =====
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({ text: "Sprint 6 Plan Update", bold: true, font: "Calibri", size: 48, color: DEEP_BLUE })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({ text: "Eva \u2014 Program Manager  |  February 28, 2026", font: "Calibri", size: 22, color: GRAY })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 300 },
        children: [new TextRun({ text: "Classification: INTERNAL", font: "Calibri", size: 20, italics: true, color: GRAY })]
      }),

      // ===== EXECUTIVE SUMMARY =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Executive Summary")] }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "Sprint 5 is COMPLETE. Sprint 6 scope was locked February 27 with two parallel tracks: Track 1 (Protocol Pipe) and Track 2 (Canary Slim). The Heartbeat pipeline code is built (21 new files, 7/7 smoke tests), and the sandbox integration gate has been cleared \u2014 26 real Square webhooks received and processed with HMAC signature verification passing. The Foundation Layer (B-068) is fully delivered across all five lanes. The single gate to production heartbeat is Jeffe providing production Square credentials. We are at a natural code branch point \u2014 Sprint 5 baseline is clean, Sprint 6 TSP code is a significant new layer that should be committed to a dedicated branch.", font: "Calibri", size: 22 })]
      }),

      // ===== SPRINT 5 CLOSEOUT =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Sprint 5 Closeout")] }),
      new Paragraph({
        spacing: { after: 160 },
        children: [new TextRun({ text: "Sprint 5 (Integration Validation) is fully complete. All five phases delivered:", font: "Calibri", size: 22 })]
      }),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [1200, 4160, 1500, 2500],
        rows: [
          new TableRow({ children: [
            headerCell("Phase", 1200), headerCell("Deliverable", 4160), headerCell("Status", 1500), headerCell("Verified", 2500)
          ]}),
          new TableRow({ children: [
            cell("Phase 1", 1200), cell("Stack: Docker, Flask, PostgreSQL, migrations", 4160),
            cell([statusRun("DONE")], 1500), cell("iMac + Mac Mini", 2500)
          ]}),
          new TableRow({ children: [
            cell("Phase 2", 1200), cell("Schema: Alembic on real PostgreSQL, 22 triggers, hash chain", 4160),
            cell([statusRun("DONE")], 1500), cell("Commit 5effb5e", 2500)
          ]}),
          new TableRow({ children: [
            cell("Phase 3", 1200), cell("Data: Seed script, Level B demo data loaded", 4160),
            cell([statusRun("DONE")], 1500), cell("Offset Coffee data", 2500)
          ]}),
          new TableRow({ children: [
            cell("Phase 4", 1200), cell("Tests: 541 pass / 0 fail / 0 errors / 216 skipped", 4160),
            cell([statusRun("DONE")], 1500), cell("Dev loop CLEAN", 2500)
          ]}),
          new TableRow({ children: [
            cell("Phase 5", 1200), cell("Clickthrough: Today\u2019s View, Process 4 wizard, role gating", 4160),
            cell([statusRun("DONE")], 1500), cell("QA stack live", 2500)
          ]}),
        ]
      }),

      new Paragraph({ spacing: { before: 160, after: 200 }, children: [
        new TextRun({ text: "Test baseline at Sprint 5 close: ", font: "Calibri", size: 22 }),
        new TextRun({ text: "541 pass / 0 fail / 0 errors / 216 skipped", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: ". Last commit: ", font: "Calibri", size: 22 }),
        new TextRun({ text: "72d0082", bold: true, font: "Calibri", size: 22, color: DEEP_BLUE }),
        new TextRun({ text: " (Level B demo stack). Branch: ", font: "Calibri", size: 22 }),
        new TextRun({ text: "alpha-clean", bold: true, font: "Calibri", size: 22, color: DEEP_BLUE }),
        new TextRun({ text: ".", font: "Calibri", size: 22 }),
      ]}),

      // ===== SPRINT 6 STATUS =====
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Sprint 6 Status \u2014 Two Parallel Tracks")] }),

      // Track 1
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Track 1: Protocol Pipe (End-to-End Evidence on Chain)")] }),
      new Paragraph({ spacing: { after: 160 }, children: [
        new TextRun({ text: "Objective: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "One Square event \u2192 Canary catches \u2192 seals \u2192 inscribes \u2192 receipt. The full vertical slice that proves the protocol.", font: "Calibri", size: 22 }),
      ]}),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [600, 2600, 1200, 1500, 1200, 2260],
        rows: [
          new TableRow({ children: [
            headerCell("#", 600), headerCell("Component", 2600), headerCell("Existed?", 1200),
            headerCell("Status", 1500), headerCell("Owner", 1200), headerCell("Notes", 2260)
          ]}),
          new TableRow({ children: [
            cell("1", 600), cell("Square OAuth 2.0 flow", 2600), cell("No", 1200),
            cell([statusRun("DONE")], 1500, { fill: "DCFCE7" }), cell("Jeremy", 1200),
            cell("Self-auth for Phase 1 \u2014 working", 2260)
          ]}),
          new TableRow({ children: [
            cell("2", 600), cell("Webhook receiver + HMAC verification", 2600), cell("Partial", 1200),
            cell([statusRun("DONE")], 1500, { fill: "DCFCE7" }), cell("Jeremy", 1200),
            cell("26 real webhooks, all 200 OK", 2260)
          ]}),
          new TableRow({ children: [
            cell("3", 600), cell("Chirp rule: refund > $10", 2600), cell("Yes", 1200),
            cell([statusRun("DONE")], 1500, { fill: "DCFCE7" }), cell("\u2014", 1200),
            cell("Sprint 5 rule engine", 2260)
          ]}),
          new TableRow({ children: [
            cell("4", 600), cell("Evidence seal (Sub 1 \u2014 PostgreSQL)", 2600), cell("Yes", 1200),
            cell([statusRun("DONE")], 1500, { fill: "DCFCE7" }), cell("\u2014", 1200),
            cell("Sprint 5: 22 triggers + hash chain", 2260)
          ]}),
          new TableRow({ children: [
            cell("5", 600), cell("TSP-01 Webhook blueprint + stream publisher", 2600), cell("No", 1200),
            cell([statusRun("DONE")], 1500, { fill: "DCFCE7" }), cell("Jeremy", 1200),
            cell("XADD to Valkey Streams", 2260)
          ]}),
          new TableRow({ children: [
            cell("6", 600), cell("TSP-03 Sub 1 consumer (seal worker)", 2600), cell("No", 1200),
            cell([statusRun("DONE")], 1500, { fill: "DCFCE7" }), cell("Jeremy", 1200),
            cell("BYTEA chain hash, advisory locks", 2260)
          ]}),
          new TableRow({ children: [
            cell("7", 600), cell("TSP-05 Sub 3 Merkle batch + mock inscription", 2600), cell("No", 1200),
            cell([statusRun("DONE")], 1500, { fill: "DCFCE7" }), cell("Jeremy", 1200),
            cell("100-event or 10-min batch", 2260)
          ]}),
          new TableRow({ children: [
            cell("8", 600), cell("TSP-07 Receipt endpoint", 2600), cell("No", 1200),
            cell([statusRun("DONE")], 1500, { fill: "DCFCE7" }), cell("Jeremy", 1200),
            cell("Query by hash or event_id", 2260)
          ]}),
          new TableRow({ children: [
            cell("9", 600), cell("Inscription bridge (OrdinalsBot API)", 2600), cell("No", 1200),
            cell([statusRun("PENDING")], 1500, { fill: "FEF3C7" }), cell("Jeremy", 1200),
            cell("Mock in place \u2014 live API Sprint 7", 2260)
          ]}),
          new TableRow({ children: [
            cell("10", 600), cell("Production webhook subscription", 2600), cell("No", 1200),
            cell([statusRun("WAITING")], 1500, { fill: "FEF3C7" }), cell("Jeffe", 1200),
            cell("Needs production credentials", 2260)
          ]}),
        ]
      }),

      new Paragraph({ spacing: { before: 200, after: 200 }, children: [
        new TextRun({ text: "Track 1 Assessment: ", bold: true, font: "Calibri", size: 22, color: DEEP_BLUE }),
        new TextRun({ text: "8 of 10 components built. Sandbox integration validated end-to-end. The pipe works. Two items remain: (1) production credentials from Jeffe (15-minute action), and (2) live inscription bridge swap from mock to OrdinalsBot API (Sprint 7 scope). ", font: "Calibri", size: 22 }),
        new TextRun({ text: "Track 1 is effectively done for Sprint 6.", bold: true, font: "Calibri", size: 22 }),
      ]}),

      // Track 2
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Track 2: Canary Slim (Beachhead Momentum)")] }),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [600, 3500, 1500, 1500, 2260],
        rows: [
          new TableRow({ children: [
            headerCell("#", 600), headerCell("Deliverable", 3500), headerCell("Status", 1500),
            headerCell("Owner", 1500), headerCell("Notes", 2260)
          ]}),
          new TableRow({ children: [
            cell("1", 600), cell("B-032: Square Developer + Merchant accounts", 3500),
            cell([statusRun("RESOLVED")], 1500), cell("Jeffe", 1500),
            cell("Canary authorized as marketplace app", 2260)
          ]}),
          new TableRow({ children: [
            cell("2", 600), cell("B-065-A: Square SDK repos cloned + indexed", 3500),
            cell([statusRun("RESOLVED")], 1500), cell("Jeremy", 1500),
            cell("4 repos, 5,539 files, v44.0.1", 2260)
          ]}),
          new TableRow({ children: [
            cell("3", 600), cell("B-065-B: Webhook subscription automation", 3500),
            cell([statusRun("RESOLVED")], 1500), cell("Jeremy", 1500),
            cell("Full SDK CLI built", 2260)
          ]}),
          new TableRow({ children: [
            cell("4", 600), cell("B-036: Square SDK \u2192 CRDM alignment audit", 3500),
            cell([statusRun("WAITING")], 1500), cell("Jeremy", 1500),
            cell("Gates Tom B-035 DDL", 2260)
          ]}),
          new TableRow({ children: [
            cell("5", 600), cell("B-066: Condor SDK review + TSP coding standards", 3500),
            cell([statusRun("IN PROGRESS")], 1500), cell("Condor", 1500),
            cell("Gates Jeremy next TSP session", 2260)
          ]}),
          new TableRow({ children: [
            cell("6", 600), cell("B-067: Square Capability Dashboard", 3500),
            cell([statusRun("IN PROGRESS")], 1500), cell("Condor+Jeremy+Qwen", 1500),
            cell("3-lane parallel build", 2260)
          ]}),
          new TableRow({ children: [
            cell("7", 600), cell("Chirp Config MVP (1 page, 1 merchant)", 3500),
            cell([statusRun("PENDING")], 1500), cell("Art + Jeremy", 1500),
            cell("After B-066 + B-067", 2260)
          ]}),
        ]
      }),

      // ===== FOUNDATION LAYER =====
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Foundation Layer (B-068) \u2014 ALL FIVE LANES COMPLETE")] }),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [1000, 3500, 1500, 1500, 1860],
        rows: [
          new TableRow({ children: [
            headerCell("Lane", 1000), headerCell("Deliverable", 3500), headerCell("Owner", 1500),
            headerCell("Status", 1500), headerCell("Key Output", 1860)
          ]}),
          new TableRow({ children: [
            cell("A", 1000), cell("Partition architecture", 3500), cell("Tom", 1500),
            cell([statusRun("DELIVERED")], 1500), cell("DDL templates", 1860)
          ]}),
          new TableRow({ children: [
            cell("B", 1000), cell("Blueprint v2.0 tokenization", 3500), cell("Condor", 1500),
            cell([statusRun("DELIVERED")], 1500), cell("178 tokens", 1860)
          ]}),
          new TableRow({ children: [
            cell("C", 1000), cell("Locale + vocabulary JSON packs", 3500), cell("Condor", 1500),
            cell([statusRun("DELIVERED")], 1500), cell("3 JSON files", 1860)
          ]}),
          new TableRow({ children: [
            cell("D", 1000), cell("Vocabulary schema (merchant_vocabulary)", 3500), cell("Tom", 1500),
            cell([statusRun("DELIVERED")], 1500), cell("DB schema", 1860)
          ]}),
          new TableRow({ children: [
            cell("E", 1000), cell("White paper", 3500), cell("PhD", 1500),
            cell([statusRun("DELIVERED")], 1500), cell("Thesis document", 1860)
          ]}),
        ]
      }),

      new Paragraph({ spacing: { before: 160, after: 200 }, children: [
        new TextRun({ text: "Minor remaining step: ", font: "Calibri", size: 22 }),
        new TextRun({ text: "Tom confirms Lane D schema accommodates full 32-token vocabulary set from Condor\u2019s Token Registry. One-session reconciliation.", font: "Calibri", size: 22 }),
      ]}),

      // ===== RESOLVED SINCE LAST UPDATE =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Resolved Since Last Eva Update (Feb 26)")] }),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [1200, 5000, 1500, 1660],
        rows: [
          new TableRow({ children: [
            headerCell("ID", 1200), headerCell("Blocker", 5000), headerCell("Resolved By", 1500), headerCell("Date", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-028", 1200), cell("GrowDirect company website", 5000), cell("Jeffe", 1500), cell("Feb 27", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-032", 1200), cell("Square Developer + Merchant accounts", 5000), cell("Jeffe", 1500), cell("Feb 27", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-046", 1200), cell("elJeffe business model documentation", 5000), cell("ALX", 1500), cell("Feb 27", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-048", 1200), cell("card_fingerprint scope (network-universal)", 5000), cell("Jeffe directive", 1500), cell("Feb 27", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-052", 1200), cell("MVP rethink \u2014 parallel tracks locked", 5000), cell("Jeffe + ALX", 1500), cell("Feb 27", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-059", 1200), cell("TSP PRD revision cycle (21 issues, 6 passes)", 5000), cell("Condor + PhD", 1500), cell("Feb 27", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-060", 1200), cell("TSP Consolidated Review v1.0", 5000), cell("ALX", 1500), cell("Feb 27", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-061", 1200), cell("Key Custody \u2014 Lightning only via Strike", 5000), cell("Jeffe", 1500), cell("Feb 27", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-065-A", 1200), cell("Square GitHub repo scan", 5000), cell("Jeremy", 1500), cell("Feb 28", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-065-B", 1200), cell("Square webhook subscription automation", 5000), cell("Jeremy", 1500), cell("Feb 28", 1660)
          ]}),
          new TableRow({ children: [
            cell("B-068", 1200), cell("Foundation Layer \u2014 all 5 lanes", 5000), cell("Tom + Condor", 1500), cell("Feb 28", 1660)
          ]}),
        ]
      }),

      new Paragraph({ spacing: { before: 160, after: 100 }, children: [
        new TextRun({ text: "12 blockers resolved in 48 hours.", bold: true, font: "Calibri", size: 22, color: GREEN }),
        new TextRun({ text: " This is the most productive stretch since project start.", font: "Calibri", size: 22 }),
      ]}),

      // ===== CODE BRANCH ASSESSMENT =====
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Code Branch + New Baseline Assessment")] }),
      new Paragraph({ spacing: { after: 160 }, children: [
        new TextRun({ text: "Current Git state on ", font: "Calibri", size: 22 }),
        new TextRun({ text: "alpha-clean", bold: true, font: "Calibri", size: 22, color: DEEP_BLUE }),
        new TextRun({ text: " branch:", font: "Calibri", size: 22 }),
      ]}),

      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "Last commit: ", font: "Calibri", size: 22 }),
        new TextRun({ text: "72d0082", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: " \u2014 Level B demo stack (Today\u2019s View + Process 4 wizard + seed script)", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "Uncommitted modified files: ", font: "Calibri", size: 22 }),
        new TextRun({ text: "13 files", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: " (registry.py, session_factory.py, models, compose files, requirements.txt, valkey.conf, wsgi)", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "Untracked new files: ", font: "Calibri", size: 22 }),
        new TextRun({ text: "~15 files", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: " (TSP blueprints, consumers, migrations 004\u2013006, models, evidence_chain, webhook manager, smoke tests, entry points)", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun({ text: "Square SDK repos: ", font: "Calibri", size: 22 }),
        new TextRun({ text: "square/", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: " directory (4 repos, 5,539 files) \u2014 should be .gitignored, not committed", font: "Calibri", size: 22 }),
      ]}),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Recommendation: Branch + Commit + Tag")] }),

      new Paragraph({ numbering: { reference: "numbers", level: 0 }, children: [
        new TextRun({ text: "Tag current HEAD as Sprint 5 baseline: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "git tag sprint-5-baseline 72d0082", font: "Calibri", size: 22, color: DEEP_BLUE }),
        new TextRun({ text: " \u2014 marks the clean Sprint 5 state. This is the rollback point.", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "numbers", level: 0 }, children: [
        new TextRun({ text: "Add square/ to .gitignore: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "SDK reference repos don\u2019t belong in the Canary codebase. 5,539 files of vendor code.", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "numbers", level: 0 }, children: [
        new TextRun({ text: "Create Sprint 6 branch: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "git checkout -b sprint-6-tsp", font: "Calibri", size: 22, color: DEEP_BLUE }),
        new TextRun({ text: " \u2014 all TSP pipeline work goes here. Isolates Sprint 6 changes from the proven Sprint 5 base.", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "numbers", level: 0 }, children: [
        new TextRun({ text: "Commit TSP pipeline code: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "Stage all 28 files (13 modified + 15 new). Single commit: ", font: "Calibri", size: 22 }),
        new TextRun({ text: "feat(sprint6): TSP heartbeat pipeline \u2014 webhook, seal, Merkle, receipt", font: "Calibri", size: 22, italics: true, color: DEEP_BLUE }),
      ]}),
      new Paragraph({ numbering: { reference: "numbers", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun({ text: "Push to origin: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "Both the tag and the new branch. Remote state matches local.", font: "Calibri", size: 22 }),
      ]}),

      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun({ text: "Why now: ", bold: true, font: "Calibri", size: 22, color: DEEP_BLUE }),
        new TextRun({ text: "The TSP pipeline is a significant architectural layer (21 new files, 3 new migrations, new Valkey Streams config, new model package). It\u2019s validated (7/7 smoke, 26 real webhooks) but not yet integration-tested against the full Docker stack. Branching now gives us a clean rollback to Sprint 5 if integration surfaces issues, while preserving all Sprint 6 work. This is textbook branch hygiene.", font: "Calibri", size: 22 }),
      ]}),

      // ===== FACTORY PROCESS GATE STATUS =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Factory Process Gate Status")] }),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [2500, 2000, 1500, 1500, 1860],
        rows: [
          new TableRow({ children: [
            headerCell("Deliverable", 2500), headerCell("Current Gate", 2000), headerCell("Status", 1500),
            headerCell("Owner", 1500), headerCell("Blocker", 1860)
          ]}),
          new TableRow({ children: [
            cell("TSP Heartbeat Pipeline", 2500), cell("ASSEMBLY (Stage 3)", 2000),
            cell([statusRun("IN PROGRESS")], 1500), cell("Jeremy", 1500),
            cell("Production creds", 1860)
          ]}),
          new TableRow({ children: [
            cell("Square Capability Dashboard", 2500), cell("PARTS (Stage 2)", 2000),
            cell([statusRun("IN PROGRESS")], 1500), cell("Condor+Jeremy+Qwen", 1500),
            cell("None", 1860)
          ]}),
          new TableRow({ children: [
            cell("Foundation Layer (B-068)", 2500), cell("QC (Stage 4)", 2000),
            cell([statusRun("DELIVERED")], 1500), cell("Tom reconciliation", 1500),
            cell("Minor", 1860)
          ]}),
          new TableRow({ children: [
            cell("War Chest / Investor Site", 2500), cell("QC (Stage 4)", 2000),
            cell([statusRun("WAITING")], 1500), cell("Syd sign-off", 1500),
            cell("Syd availability", 1860)
          ]}),
          new TableRow({ children: [
            cell("Chirp Config MVP", 2500), cell("BLUEPRINT (Stage 1)", 2000),
            cell([statusRun("PENDING")], 1500), cell("Art + Jeremy", 1500),
            cell("B-066 + B-067 first", 1860)
          ]}),
        ]
      }),

      // ===== TIMELINE ESTIMATE =====
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Sprint 6 Timeline Estimate")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Track 1: Protocol Pipe")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "Production heartbeat: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "1\u20132 days after Jeffe provides production credentials. Jeremy has all tooling ready.", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "Docker integration test: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "1 day. Run Alembic migrations 004\u2013006, start Flask + Sub 1 + Sub 3 workers, verify full pipe in Docker.", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "End-to-end proof with real TX: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "Same day as production heartbeat. Jeffe\u2019s phone triggers transaction \u2192 webhook \u2192 seal \u2192 mock inscription \u2192 receipt.", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun({ text: "Estimated delivery: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "March 3\u20134, 2026", bold: true, font: "Calibri", size: 22, color: GREEN }),
        new TextRun({ text: " (contingent on production credentials this weekend)", font: "Calibri", size: 22 }),
      ]}),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Track 2: Canary Slim")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "B-066 (Condor SDK review): ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "1 session, dispatched. Delivers TSP Coding Standards for Jeremy.", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "B-067 (Capability Dashboard): ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "3 parallel lanes (Condor map, Jeremy API module, Qwen dashboard). 2\u20133 sessions total.", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun({ text: "Chirp Config MVP: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "Follows B-066/B-067. Art (design) + Jeremy (build). 1 week after dependencies clear.", font: "Calibri", size: 22 }),
      ]}),

      // ===== TOP 3 RISKS =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Top 3 Risks to Sprint 6 Delivery")] }),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [600, 3000, 1500, 1500, 2760],
        rows: [
          new TableRow({ children: [
            headerCell("#", 600), headerCell("Risk", 3000), headerCell("Likelihood", 1500),
            headerCell("Impact", 1500), headerCell("Mitigation", 2760)
          ]}),
          new TableRow({ children: [
            cell("1", 600), cell("Production credentials delayed", 3000), cell("MEDIUM", 1500),
            cell("HIGH", 1500, { color: RED }), cell("Jeffe action \u2014 15 min in Square Dashboard. ALX to surface.", 2760)
          ]}),
          new TableRow({ children: [
            cell("2", 600), cell("Docker integration uncovers issues in TSP migrations", 3000), cell("MEDIUM", 1500),
            cell("MEDIUM", 1500, { color: ORANGE }), cell("Sprint 5 baseline tag = clean rollback. Jeremy fixes forward on sprint-6-tsp branch.", 2760)
          ]}),
          new TableRow({ children: [
            cell("3", 600), cell("Context window costs escalating on multi-session builds", 3000), cell("HIGH", 1500),
            cell("MEDIUM", 1500, { color: ORANGE }), cell("Consolidate sessions. Avoid compaction-driven re-hydration. Feb 27 s5 cost $130 on context replay alone.", 2760)
          ]}),
        ]
      }),

      // ===== TIMELOG ENFORCEMENT =====
      new Paragraph({ spacing: { before: 400 }, heading: HeadingLevel.HEADING_1, children: [new TextRun("Timelog Enforcement Check")] }),
      new Paragraph({ spacing: { after: 160 }, children: [
        new TextRun({ text: "Checked ", font: "Calibri", size: 22 }),
        new TextRun({ text: "Documents/timelogs/2026/02-February/daily/", font: "Calibri", size: 22, color: DEEP_BLUE }),
        new TextRun({ text: ":", font: "Calibri", size: 22 }),
      ]}),

      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "Feb 28: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "2 entries (Jeremy B-065, Condor B-068 Lanes B+C) \u2014 ", font: "Calibri", size: 22 }),
        new TextRun({ text: "LOGGED", bold: true, color: GREEN, font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun({ text: "Feb 27: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "6 entries (Syd/PhD dispatch, B-058 War Chest, War Chest v2.5 build, TSP PRD review, B-059 work order, Jeremy Heartbeat build) \u2014 ", font: "Calibri", size: 22 }),
        new TextRun({ text: "LOGGED", bold: true, color: GREEN, font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun({ text: "Assessment: ", bold: true, font: "Calibri", size: 22 }),
        new TextRun({ text: "All sessions since Feb 27 have timelog entries. No gaps detected. B-026 (skill port to Cowork) still open but manual process is working.", font: "Calibri", size: 22 }),
      ]}),

      // ===== BOTTOM LINE =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Bottom Line")] }),
      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun({ text: "Sprint 6 is ahead of schedule. Track 1 is functionally complete pending one 15-minute Jeffe action. Track 2 is in active build with no blockers. The Foundation Layer is done. The War Chest is built and awaiting legal sign-off. This is the right moment to cut a code branch, tag the Sprint 5 baseline, and commit the TSP pipeline to a clean Sprint 6 branch. The team has earned a new baseline.", font: "Calibri", size: 22 }),
      ]}),
      new Paragraph({
        spacing: { after: 100 },
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: SIGNAL_YELLOW, space: 4 } },
        children: [
          new TextRun({ text: "\nPrepared by ALX (Chief of Staff) on behalf of Eva (Program Manager)", font: "Calibri", size: 20, italics: true, color: GRAY }),
        ]
      }),
      new Paragraph({ children: [
        new TextRun({ text: "February 28, 2026", font: "Calibri", size: 20, italics: true, color: GRAY }),
      ]}),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/sessions/busy-happy-lovelace/mnt/GrowDirect/_ALX/WorkOrders/output/Eva/Eva_Sprint6_PlanUpdate_v1.0.docx", buffer);
  console.log("DONE — Eva_Sprint6_PlanUpdate_v1.0.docx written");
});
