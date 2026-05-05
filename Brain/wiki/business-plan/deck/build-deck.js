#!/usr/bin/env node
// build-deck.js — Canary Retail pitch deck v1
// Generates both internal (named) and external (archetype) versions.
// Run: node build-deck.js
// Outputs: canary-retail-deck-v1-internal.pptx
//          canary-retail-deck-v1-external.pptx

const pptxgen = require("/opt/homebrew/lib/node_modules/pptxgenjs");
const fs = require("fs");
const path = require("path");

// ── Brand Constants ───────────────────────────────────────────────
const C = {
  NAVY:       "1C2951",
  NAVY_MID:   "2D4A8A",
  NAVY_LIGHT: "3B5998",
  YELLOW:     "F5C518",
  YELLOW_DARK:"C49B0C",
  WHITE:      "FFFFFF",
  OFF_WHITE:  "F7F8FA",
  LIGHT_BG:   "EEF2F7",
  TEXT:       "1A202C",
  TEXT_MID:   "4A5568",
  TEXT_LIGHT: "718096",
  BORDER:     "D1D9E6",
  GREEN:      "1A7A5E",
  RED_DARK:   "9B1C1C",
};

const LOGO_PATH = path.join(__dirname, "../../../../CanaryGo/internal/web/static/img/canary-icon-512.png");

const W = 10;    // slide width inches
const H = 5.625; // slide height inches

// ── Helpers ───────────────────────────────────────────────────────

function makeShadow() {
  return { type: "outer", color: "000000", blur: 5, offset: 2, angle: 135, opacity: 0.10 };
}

// Adds the standard header bar to a light slide (logo + brand name + slide title)
function addHeader(slide, title, opts = {}) {
  const { dark = false } = opts;
  const bg = dark ? C.NAVY : C.WHITE;
  const fg = dark ? C.WHITE : C.NAVY;
  // Left logo
  slide.addImage({ path: LOGO_PATH, x: 0.18, y: 0.10, w: 0.42, h: 0.42 });
  // Brand name
  slide.addText("CANARY RETAIL", {
    x: 0.68, y: 0.10, w: 2.8, h: 0.22,
    fontSize: 10, bold: true, color: dark ? C.YELLOW : C.NAVY,
    fontFace: "Calibri", charSpacing: 3, valign: "top", margin: 0,
  });
  // Slide title
  slide.addText(title, {
    x: 0.68, y: 0.32, w: 9.14, h: 0.38,
    fontSize: 20, bold: true, color: fg,
    fontFace: "Georgia", valign: "top", margin: 0,
  });
  // Thin yellow accent line under header
  slide.addShape(slide.pres.shapes.RECTANGLE, {
    x: 0.18, y: 0.72, w: 9.64, h: 0.025,
    fill: { color: C.YELLOW }, line: { color: C.YELLOW, width: 0 },
  });
}

// Standard footer
function addFooter(slide, opts = {}) {
  const { dark = false } = opts;
  const color = dark ? "9BACC8" : C.TEXT_LIGHT;
  slide.addText("GrowDirect LLC  ·  Strictly Confidential  ·  Not for External Distribution", {
    x: 0.18, y: 5.40, w: 8.5, h: 0.18,
    fontSize: 8, color, fontFace: "Calibri", valign: "bottom", margin: 0,
  });
  slide.addText("May 2026", {
    x: 8.68, y: 5.40, w: 1.15, h: 0.18,
    fontSize: 8, color, fontFace: "Calibri", align: "right", valign: "bottom", margin: 0,
  });
}

// Card: x, y, w, h, title, bullets[], accent color
function addCard(slide, x, y, w, h, titleText, bullets, opts = {}) {
  const { accentColor = C.NAVY_MID, dark = false, titleSize = 13, bodySize = 11 } = opts;
  const bgColor = dark ? C.NAVY : C.WHITE;
  const textColor = dark ? C.WHITE : C.TEXT;
  const mutedColor = dark ? "9BACC8" : C.TEXT_MID;

  // Card background
  slide.addShape(slide.pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: bgColor },
    line: { color: dark ? C.NAVY_MID : C.BORDER, width: 1 },
    shadow: makeShadow(),
  });
  // Left accent bar
  slide.addShape(slide.pres.shapes.RECTANGLE, {
    x, y, w: 0.06, h,
    fill: { color: accentColor }, line: { color: accentColor, width: 0 },
  });
  // Title
  slide.addText(titleText, {
    x: x + 0.14, y: y + 0.12, w: w - 0.22, h: 0.28,
    fontSize: titleSize, bold: true, color: dark ? C.YELLOW : accentColor,
    fontFace: "Calibri", valign: "top", margin: 0,
  });
  // Bullets
  if (bullets && bullets.length > 0) {
    const items = bullets.map((b, i) => ({
      text: b,
      options: { bullet: true, breakLine: i < bullets.length - 1, fontSize: bodySize, color: textColor, fontFace: "Calibri" },
    }));
    slide.addText(items, {
      x: x + 0.14, y: y + 0.44, w: w - 0.22, h: h - 0.54,
      valign: "top", margin: 0,
    });
  }
}

// ── Slide builders ────────────────────────────────────────────────

function buildSlide01_Cover(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.NAVY };

  // Large logo, centered
  slide.addImage({ path: LOGO_PATH, x: 4.2, y: 0.55, w: 1.6, h: 1.6 });

  // Main title
  slide.addText("CANARY RETAIL", {
    x: 0.5, y: 2.22, w: 9, h: 0.72,
    fontSize: 44, bold: true, color: C.YELLOW,
    fontFace: "Georgia", align: "center", charSpacing: 6, valign: "middle", margin: 0,
  });

  // Yellow divider
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 3.5, y: 3.02, w: 3.0, h: 0.03,
    fill: { color: C.YELLOW }, line: { color: C.YELLOW, width: 0 },
  });

  // Subtitle
  slide.addText("Building the Intelligence Layer for Independent Retail", {
    x: 0.5, y: 3.10, w: 9, h: 0.40,
    fontSize: 18, color: C.WHITE, fontFace: "Calibri", align: "center", valign: "middle", margin: 0,
  });

  // Deck type
  slide.addText("Partnership & Investment Overview", {
    x: 0.5, y: 3.56, w: 9, h: 0.28,
    fontSize: 13, color: "9BACC8", fontFace: "Calibri", align: "center", valign: "middle", margin: 0,
  });

  addFooter(slide, { dark: true });
}

function buildSlide02_StrategicPerspective(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "The Store Is the Agent's Environment");
  addFooter(slide);

  // Two column cards: Application Layer vs Operating Layer
  // Left: application layer (light bg, gray accent)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 0.88, w: 4.35, h: 2.60,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 },
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 0.88, w: 0.06, h: 2.60,
    fill: { color: C.TEXT_LIGHT }, line: { color: C.TEXT_LIGHT, width: 0 },
  });
  slide.addText("APPLICATION LAYER", {
    x: 0.32, y: 0.94, w: 4.14, h: 0.24,
    fontSize: 9, bold: true, color: C.TEXT_LIGHT, charSpacing: 2, fontFace: "Calibri", margin: 0,
  });
  slide.addText("Square · Clover · Toast · Lightspeed", {
    x: 0.32, y: 1.17, w: 4.14, h: 0.26,
    fontSize: 14, bold: true, color: C.TEXT, fontFace: "Georgia", margin: 0,
  });
  slide.addText([
    { text: "\"Log in to see what happened\"", options: { bold: true, italic: true, fontSize: 12, color: C.TEXT_MID, breakLine: true } },
    { text: "Retrospective  ·  Dashboard-mediated  ·  Data as destination", options: { fontSize: 11, color: C.TEXT_MID, breakLine: true } },
    { text: "Merchant goes TO the platform to learn what occurred after the fact. "
          + "Reports export data. Intelligence is asynchronous. The store operates independently of the platform.",
          options: { fontSize: 11, color: C.TEXT_MID } },
  ], { x: 0.32, y: 1.47, w: 4.14, h: 1.90, valign: "top", margin: 0 });

  // Right: operating layer (navy bg, yellow accent)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 4.73, y: 0.88, w: 4.91, h: 2.60,
    fill: { color: C.NAVY }, line: { color: C.NAVY_MID, width: 1 },
    shadow: makeShadow(),
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 4.73, y: 0.88, w: 0.06, h: 2.60,
    fill: { color: C.YELLOW }, line: { color: C.YELLOW, width: 0 },
  });
  slide.addText("OPERATING LAYER", {
    x: 4.88, y: 0.94, w: 4.68, h: 0.24,
    fontSize: 9, bold: true, color: C.YELLOW, charSpacing: 2, fontFace: "Calibri", margin: 0,
  });
  slide.addText("Canary Retail", {
    x: 4.88, y: 1.17, w: 4.68, h: 0.26,
    fontSize: 14, bold: true, color: C.WHITE, fontFace: "Georgia", margin: 0,
  });
  slide.addText([
    { text: "\"Agent in the store while it's happening\"", options: { bold: true, italic: true, fontSize: 12, color: C.YELLOW, breakLine: true } },
    { text: "Simultaneous  ·  Event-driven  ·  Data as operating infrastructure", options: { fontSize: 11, color: "9BACC8", breakLine: true } },
    { text: "The store IS the agent's environment. 166 MCP service junctions let agents reach "
          + "physical store operations at packet-layer speed. The platform operates — it doesn't observe.",
          options: { fontSize: 11, color: C.WHITE } },
  ], { x: 4.88, y: 1.47, w: 4.68, h: 1.90, valign: "top", margin: 0 });

  // Comparison table (3 rows)
  const rows = [
    [{ text: "", options: { bold: true } }, { text: "Application Layer", options: { bold: true } }, { text: "Canary Operating Layer", options: { bold: true } }],
    ["Timing",          "Retrospective — after events occur", "Simultaneous — at the speed of events"],
    ["Agent Role",      "Merchant reviews dashboards",        "Agent executes in the store"],
    ["Accountability",  "Reports show what happened",         "Four measurable rails (Ops · Financial · Evidentiary · Vendor)"],
    ["Commercial Model","$25/seat subscription",              "Satoshi per-junction — aligned with merchant value flow"],
  ];

  const headerOpts = { bold: true, color: C.WHITE, fill: { color: C.NAVY_MID } };
  const tableData = rows.map((row, ri) => row.map((cell, ci) => {
    const text = typeof cell === "string" ? cell : cell.text;
    const base = { text, options: { fontSize: 10, fontFace: "Calibri", fill: { color: ri === 0 ? C.NAVY : (ri % 2 === 0 ? C.OFF_WHITE : C.WHITE) } } };
    if (ri === 0) base.options = { ...base.options, bold: true, color: C.WHITE, fill: { color: C.NAVY } };
    else if (ci === 0) base.options = { ...base.options, bold: true };
    else if (ci === 2) base.options = { ...base.options, color: C.GREEN };
    return base;
  }));

  slide.addTable(tableData, {
    x: 0.18, y: 3.55, w: 9.46, h: 1.68,
    colW: [1.90, 3.56, 4.00],
    border: { pt: 0.5, color: C.BORDER },
    rowH: 0.28,
  });

  slide.addText("Source: Brain/wiki/cards/platform-thesis.md v3  ·  docs/sdds/go-handoff/mcp-service-junctions.md", {
    x: 0.18, y: 5.26, w: 8.5, h: 0.14,
    fontSize: 7.5, color: C.TEXT_LIGHT, fontFace: "Calibri", italic: true, margin: 0,
  });
}

function buildSlide03_WhoWeAre(pres, internal = true) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "Who We Are: Built at the Physical Layer Before It Was a Thesis");
  addFooter(slide);

  // Heritage statement
  slide.addText(
    "Quarter-century of canonical retail data model lineage, from global tier-1 production systems to today's SMB intelligence layer.",
    {
      x: 0.18, y: 0.82, w: 9.64, h: 0.46,
      fontSize: 13, color: C.TEXT_MID, fontFace: "Calibri", italic: true, valign: "top", margin: 0,
    }
  );

  // Timeline of credentials — horizontal cards
  const creds = internal ? [
    {
      period: "2007 – 2013",
      org:    "Tesco Fresh & Easy (US)  ·  Project Fireball",
      detail: "Architect of the in-store operating model: planogram, shelf edge, and back-end systems integrated as a single operating substrate inside production US grocery stores. Physical-layer-meets-backend at tier-1 grocery scale.",
    },
    {
      period: "2009",
      org:    "Walmart International  ·  GSLM",
      detail: "Defined the Global Store Logical Model — canonical retail data model rolled out across Walmart's international acquired banners (ASDA UK, Walmex, Brazil, China). Nine-domain completeness framework still used as a completeness checklist in Canary Go's 13-module spine.",
    },
    {
      period: "2023",
      org:    "Dollar Tree  ·  Integration Design",
      detail: "Applied the GSLM framework as the canonical-model exemplar for the Dollar Tree integration team. Domain continuity across 20 years and three tier-1 retailers.",
    },
    {
      period: "2026 →",
      org:    "Canary Retail  ·  RapidPOS Proof Case",
      detail: "Applied to SMB: 13-module retail spine, 65-entity canonical data model, 166-junction MCP service architecture. Channel delivery via RapidPOS VAR ecosystem. First customer proof case in progress.",
    },
  ] : [
    {
      period: "2007 – 2013",
      org:    "Tier-1 US Specialty Grocer  ·  In-Store Operating Model",
      detail: "Architect of the in-store operating model: planogram, shelf edge, and back-end systems integrated as a single operating substrate inside production grocery stores. Physical-layer-meets-backend at tier-1 scale.",
    },
    {
      period: "2009",
      org:    "Global Tier-1 Retailer  ·  Canonical Data Model (GSLM)",
      detail: "Defined the canonical retail data model rolled out across multiple acquired international banners. Nine-domain completeness framework reused as the completeness checklist in Canary Go's 13-module spine.",
    },
    {
      period: "2023",
      org:    "National Specialty Retailer  ·  Data Integration",
      detail: "Applied the canonical model framework for a national specialty retailer's integration program. Domain continuity across 20 years and three tier-1 retail engagements.",
    },
    {
      period: "2026 →",
      org:    "Canary Retail  ·  RapidPOS Proof Case",
      detail: "Applied to SMB: 13-module retail spine, 65-entity canonical data model, 166-junction MCP service architecture. Channel delivery via RapidPOS VAR ecosystem. First customer proof case in progress.",
    },
  ];

  const cardW = 2.32;
  const cardH = 3.26;
  const startX = 0.18;
  const startY = 1.30;
  const gap = 0.12;

  creds.forEach((c, i) => {
    const x = startX + i * (cardW + gap);
    // Card bg
    const isLast = i === 3;
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: startY, w: cardW, h: cardH,
      fill: { color: isLast ? C.NAVY : C.OFF_WHITE },
      line: { color: isLast ? C.NAVY_MID : C.BORDER, width: 1 },
      shadow: makeShadow(),
    });
    // Top accent
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: startY, w: cardW, h: 0.06,
      fill: { color: isLast ? C.YELLOW : C.NAVY_MID }, 
    });
    // Period
    slide.addText(c.period, {
      x: x + 0.12, y: startY + 0.12, w: cardW - 0.22, h: 0.22,
      fontSize: 10, bold: true, color: isLast ? C.YELLOW : C.NAVY_MID, fontFace: "Calibri", margin: 0,
    });
    // Org name
    slide.addText(c.org, {
      x: x + 0.12, y: startY + 0.36, w: cardW - 0.22, h: 0.58,
      fontSize: 11, bold: true, color: isLast ? C.WHITE : C.TEXT, fontFace: "Calibri", margin: 0,
    });
    // Detail
    slide.addText(c.detail, {
      x: x + 0.12, y: startY + 0.98, w: cardW - 0.22, h: 2.14,
      fontSize: 10, color: isLast ? "9BACC8" : C.TEXT_MID, fontFace: "Calibri", valign: "top", margin: 0,
    });
  });

  // One-line thesis
  slide.addText(
    "Built the physical operating layer at tier-1 scale. Now applying that model at SMB scale, agent-native and cost-transparent.",
    {
      x: 0.18, y: 4.66, w: 9.64, h: 0.38,
      fontSize: 12, bold: true, color: C.NAVY, fontFace: "Georgia", italic: true, valign: "top", margin: 0,
    }
  );
}

function buildSlide04_CategoryDifference(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "Application Layer vs. Operating Layer");
  addFooter(slide);

  // Left column: them (gray)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 0.85, w: 4.60, h: 4.30,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 },
  });
  slide.addText("APPLICATION LAYER", {
    x: 0.28, y: 0.92, w: 4.40, h: 0.20,
    fontSize: 9, bold: true, color: C.TEXT_LIGHT, charSpacing: 2, fontFace: "Calibri", margin: 0,
  });
  slide.addText("Square  ·  Clover  ·  Toast  ·  Lightspeed", {
    x: 0.28, y: 1.13, w: 4.40, h: 0.32,
    fontSize: 16, bold: true, color: C.TEXT, fontFace: "Georgia", margin: 0,
  });

  const leftItems = [
    ["Timing",        "Retrospective — reports generated after events"],
    ["Agent Role",    "None — merchant pulls data on demand"],
    ["Data Model",    "POS transaction log; no canonical domain coverage"],
    ["Billing",       "$25–$200/seat/month — flat, regardless of value delivered"],
    ["Accountability","Dashboard shows what happened — no rails, no enforcement"],
    ["LP",            "Add-on module or separate vendor"],
    ["Evidence",      "Exportable CSV — no cryptographic chain"],
    ["Vendor SLA",    "No measurement, no recourse"],
    ["Long Arc",      "POS vendor with analytics add-on — ecosystem closed"],
  ];
  leftItems.forEach(([label, value], i) => {
    const y = 1.50 + i * 0.30;
    slide.addText(label + ":", {
      x: 0.28, y, w: 1.20, h: 0.26,
      fontSize: 10, bold: true, color: C.TEXT_MID, fontFace: "Calibri", margin: 0,
    });
    slide.addText(value, {
      x: 1.50, y, w: 3.18, h: 0.26,
      fontSize: 10, color: C.TEXT_MID, fontFace: "Calibri", margin: 0,
    });
  });

  // Right column: Canary (navy)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.05, y: 0.85, w: 4.77, h: 4.30,
    fill: { color: C.NAVY }, line: { color: C.NAVY_MID, width: 1 },
    shadow: makeShadow(),
  });
  slide.addText("OPERATING LAYER", {
    x: 5.15, y: 0.92, w: 4.57, h: 0.20,
    fontSize: 9, bold: true, color: C.YELLOW, charSpacing: 2, fontFace: "Calibri", margin: 0,
  });
  slide.addText("Canary Retail", {
    x: 5.15, y: 1.13, w: 4.57, h: 0.32,
    fontSize: 16, bold: true, color: C.WHITE, fontFace: "Georgia", margin: 0,
  });

  const rightItems = [
    ["Timing",        "Simultaneous — agent operates at the speed of events"],
    ["Agent Role",    "Agents are participants — they observe AND operate"],
    ["Data Model",    "65-entity canonical model, 13 modules, 9 domains"],
    ["Billing",       "Satoshi per-junction — aligned with actual value delivered"],
    ["Accountability","Four rails: Ops / Financial / Evidentiary / Vendor — all measurable"],
    ["LP",            "Rail 1 — built into the spine, not bolted on"],
    ["Evidence",      "L2 blockchain hash per event — public, non-repudiable"],
    ["Vendor SLA",    "OpenTelemetry-measured, disputed automatically"],
    ["Long Arc",      "Phase 1→4: intelligence layer → full POS replacement"],
  ];
  rightItems.forEach(([label, value], i) => {
    const y = 1.50 + i * 0.30;
    slide.addText(label + ":", {
      x: 5.15, y, w: 1.20, h: 0.26,
      fontSize: 10, bold: true, color: C.YELLOW, fontFace: "Calibri", margin: 0,
    });
    slide.addText(value, {
      x: 6.37, y, w: 3.36, h: 0.26,
      fontSize: 10, color: C.WHITE, fontFace: "Calibri", margin: 0,
    });
  });

  // Divider arrow in middle
  slide.addText("vs", {
    x: 4.52, y: 2.75, w: 0.55, h: 0.55,
    fontSize: 18, bold: true, color: C.TEXT_LIGHT, fontFace: "Georgia", align: "center", valign: "middle", margin: 0,
  });
}

function buildSlide05_FourRails(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "Four Accountability Rails: The Graph Is Closed");
  addFooter(slide);

  slide.addText(
    "Every escape route retailers have relied on — unknown loss, unauthorized spend, contested evidence, unmet SLA — is structurally closed.",
    { x: 0.18, y: 0.82, w: 9.64, h: 0.36, fontSize: 12, color: C.TEXT_MID, fontFace: "Calibri", italic: true, valign: "top", margin: 0 }
  );

  const rails = [
    {
      num: "01", title: "Operational", subtitle: "No Unknown Loss",
      body: "The 13-module spine is a closed graph. Every unit of inventory, labor, price, space, and transaction has a measurement contract. Shrink has a Fox case, a forecast variance, or a receiving discrepancy — or the absence is itself a signal. The local market layer eliminates the last external alibi.",
      close: "If it happened in the store, it is in the model. If it is in the model, someone is accountable for it.",
      color: C.NAVY_MID,
    },
    {
      num: "02", title: "Financial", subtitle: "No Unauthorized Spend",
      body: "OTB is not a number in a spreadsheet — it is a funded Lightning wallet. A commercial agent commits spend by calling an L402-gated MCP tool. The payment is the authorization. The agent cannot overspend because it cannot pay for the tool call that would authorize it.",
      close: "Every spend is a settled payment. Every approval is a funded wallet. Every variance is owned.",
      color: C.GREEN,
    },
    {
      num: "03", title: "Evidentiary", subtitle: "No Unanchored Record",
      body: "Every Fox case card generation and status transition publishes a cryptographic hash to a public L2 blockchain. The record is timestamped and non-repudiable — not by GrowDirect, not by the retailer, not by the VAR. A court, an insurer, or a regulatory auditor can verify the chain of custody without trusting any party.",
      close: "The evidence chain is public. The timeline is immutable. LP is provable to anyone.",
      color: C.NAVY,
    },
    {
      num: "04", title: "Vendor", subtitle: "No Unmet SLA Paid",
      body: "Cloud providers oversell capacity structurally — power generation is the binding constraint. SMB workloads get throttled first. Every MCP junction is OpenTelemetry-instrumented against published SLAs. Variances accumulate in an append-only ledger, anchored on L2 alongside LP evidence. Dispute automation files SLA credits automatically.",
      close: "Every dollar paid to a cloud provider is paid for SLA-met service. Migration capability is real, not theoretical.",
      color: "8B3A3A",
    },
  ];

  rails.forEach((rail, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.18 + col * 4.92;
    const y = 1.24 + row * 2.08;
    const w = 4.72;
    const h = 1.96;

    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w, h,
      fill: { color: C.WHITE }, line: { color: C.BORDER, width: 1 },
      shadow: makeShadow(),
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w, h: 0.06,
      fill: { color: rail.color }, 
    });

    // Number + title
    slide.addText(`${rail.num}  ${rail.title.toUpperCase()}`, {
      x: x + 0.12, y: y + 0.10, w: w - 0.22, h: 0.20,
      fontSize: 9, bold: true, color: rail.color, charSpacing: 1, fontFace: "Calibri", margin: 0,
    });
    slide.addText(rail.subtitle, {
      x: x + 0.12, y: y + 0.30, w: w - 0.22, h: 0.24,
      fontSize: 14, bold: true, color: C.TEXT, fontFace: "Georgia", margin: 0,
    });
    slide.addText(rail.body, {
      x: x + 0.12, y: y + 0.58, w: w - 0.22, h: 0.94,
      fontSize: 9.5, color: C.TEXT_MID, fontFace: "Calibri", valign: "top", margin: 0,
    });
    slide.addText(rail.close, {
      x: x + 0.12, y: y + 1.56, w: w - 0.22, h: 0.32,
      fontSize: 9.5, bold: true, italic: true, color: rail.color, fontFace: "Calibri", valign: "top", margin: 0,
    });
  });

  slide.addText("Source: Brain/wiki/cards/platform-thesis.md v3  ·  project_cloud_provider_accountability_stance", {
    x: 0.18, y: 5.26, w: 8.5, h: 0.14,
    fontSize: 7.5, color: C.TEXT_LIGHT, fontFace: "Calibri", italic: true, margin: 0,
  });
}

function buildSlide06_MCPJunctional(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "The Virtual USB-C Plug: 166 Junctions, 13 Spine Modules");
  addFooter(slide);

  // Left column: USB-C analogy table
  slide.addText("What USB-C did in hardware — Canary does for retail ops:", {
    x: 0.18, y: 0.82, w: 5.20, h: 0.28,
    fontSize: 12, bold: true, color: C.NAVY, fontFace: "Calibri", valign: "top", margin: 0,
  });

  const analogy = [
    ["USB-C in Hardware",                         "MCP-Native in Retail"],
    ["One port: power + data + display + periph.", "One junction: query + write + event + decision"],
    ["Replaces 6 different connectors",           "Replaces REST + webhook + ETL + dashboard + report + review"],
    ["Bidirectional — power flows either way",    "Bidirectional — agent observes AND operates"],
    ["Standard — every vendor speaks it",         "ARTS-compliant + open MCP — every POS can plug in"],
    ["Invisible to user — just plug in",          "Invisible to operator — platform tracks, decides, acts"],
  ];

  const tableData = analogy.map((row, ri) => row.map((cell, ci) => ({
    text: cell,
    options: {
      fontSize: 10, fontFace: "Calibri",
      bold: ri === 0,
      color: ri === 0 ? C.WHITE : (ci === 1 ? C.TEXT : C.TEXT_MID),
      fill: { color: ri === 0 ? C.NAVY : (ri % 2 === 0 ? C.OFF_WHITE : C.WHITE) },
    },
  })));

  slide.addTable(tableData, {
    x: 0.18, y: 1.14, w: 5.30, h: 2.88,
    colW: [2.65, 2.65],
    border: { pt: 0.5, color: C.BORDER },
    rowH: 0.40,
  });

  // Right column: plug visual (shapes-based USB-C metaphor)
  // Outer cable plug body (navy rectangle)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 6.10, y: 1.20, w: 3.50, h: 2.50,
    fill: { color: C.NAVY }, line: { color: C.NAVY_MID, width: 1 },
    shadow: makeShadow(),
  });
  // Inner connector port
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 6.42, y: 1.60, w: 2.86, h: 1.72,
    fill: { color: "162140" }, line: { color: C.NAVY_MID, width: 1 },
  });
  // Junction pins (horizontal colored bars)
  const pinColors = [C.YELLOW, "3B82F6", C.GREEN, "E84393", "8B5CF6", "F97316"];
  const pinLabels = ["Inventory", "Sales", "Labor", "Finance", "Ordering", "Evidence"];
  pinColors.forEach((pc, i) => {
    const py = 1.68 + i * 0.24;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 6.54, y: py, w: 2.62, h: 0.16,
      fill: { color: pc }, line: { color: pc, width: 0 },
    });
    slide.addText(pinLabels[i], {
      x: 6.57, y: py + 0.01, w: 2.56, h: 0.14,
      fontSize: 7.5, bold: true, color: C.NAVY, fontFace: "Calibri", valign: "middle", margin: 0,
    });
  });

  // Label: "MCP Junction"
  slide.addText("MCP Service Junction", {
    x: 6.10, y: 3.74, w: 3.50, h: 0.24,
    fontSize: 10, bold: true, color: C.NAVY_MID, fontFace: "Calibri", align: "center", margin: 0,
  });

  // Key stat
  slide.addText("166 junctions across 10 archetypes", {
    x: 0.18, y: 4.08, w: 5.30, h: 0.28,
    fontSize: 13, bold: true, color: C.NAVY, fontFace: "Georgia", margin: 0,
  });
  slide.addText(
    "Each junction is the billing record and the evidentiary record — the satoshi toll IS the audit entry. "
    + "No separate billing system. No separate compliance module.",
    { x: 0.18, y: 4.38, w: 5.30, h: 0.76, fontSize: 11, color: C.TEXT_MID, fontFace: "Calibri", valign: "top", margin: 0 }
  );

  slide.addText("Source: docs/sdds/go-handoff/mcp-service-junctions.md  ·  project_mcp_native_virtual_usbc_plug", {
    x: 0.18, y: 5.26, w: 8.5, h: 0.14,
    fontSize: 7.5, color: C.TEXT_LIGHT, fontFace: "Calibri", italic: true, margin: 0,
  });
}

function buildSlide07_PhasedTrajectory(pres, internal = true) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "Phased Trajectory: Intelligence Layer → Full POS");
  addFooter(slide);

  slide.addText(
    "Canary earns the right to replace Counterpoint by proving value at each phase, not by demanding rip-and-replace.",
    { x: 0.18, y: 0.82, w: 9.64, h: 0.30, fontSize: 12, color: C.TEXT_MID, fontFace: "Calibri", italic: true, valign: "top", margin: 0 }
  );

  const phases = [
    {
      num: "1", period: "Now → 2027",
      title: "Intelligence Layer",
      desc: "Canary runs alongside Counterpoint/RapidPOS. 13-module spine, 166-junction MCP architecture, four accountability rails. Sells on operational + financial + evidentiary value.",
      channels: "Channel: RapidPOS VAR ecosystem",
      current: true,
    },
    {
      num: "2", period: "2027 – 2028",
      title: "Workflow Absorption",
      desc: "Canary absorbs workflows Counterpoint does badly or not at all — LP, OTB, distribution, multi-tier assortment, labor, advanced merchandising. Counterpoint usage narrows.",
      channels: "Channel: Expanded VAR + direct enterprise",
    },
    {
      num: "3", period: "2029",
      title: "Register-Adjacent",
      desc: "Canary runs the register-adjacent experience (companion tablet, capture-augmented register, or full register). Counterpoint becomes a back-office residual.",
      channels: "Channel: Platform-native + POS hardware partnerships",
    },
    {
      num: "4", period: "2029 – 30+",
      title: "Full POS",
      desc: "Canary IS the POS. Counterpoint can be turned off. Merchant runs on Canary end-to-end. The merchant data asset is fully owned by the platform.",
      channels: "The POS vendor of choice for SMB retail",
    },
  ];

  // Timeline bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 1.22, w: 9.64, h: 0.06,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 0 },
  });

  // Phase dots on timeline
  const dotPositions = [0.18, 2.64, 5.10, 7.56];
  const phaseW = 2.30;

  phases.forEach((ph, i) => {
    const x = dotPositions[i];

    // Dot on timeline — all phases use visible colors
    slide.addShape(pres.shapes.OVAL, {
      x: x + (phaseW / 2) - 0.14, y: 1.06, w: 0.28, h: 0.28,
      fill: { color: ph.current ? C.YELLOW : C.NAVY }, line: { color: ph.current ? C.YELLOW_DARK : C.NAVY_MID, width: 1 },
    });

    // Phase card
    const cardBg = ph.current ? C.NAVY : C.OFF_WHITE;
    const textClr = ph.current ? C.WHITE : C.TEXT;
    const mutedClr = ph.current ? "9BACC8" : C.TEXT_MID;

    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.44, w: phaseW, h: 3.60,
      fill: { color: cardBg }, line: { color: ph.current ? C.NAVY_MID : C.BORDER, width: 1 },
      shadow: ph.current ? makeShadow() : undefined,
    });
    // Top accent
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.44, w: phaseW, h: 0.05,
      fill: { color: ph.current ? C.YELLOW : C.NAVY_MID }, 
    });

    slide.addText(`PHASE ${ph.num}`, {
      x: x + 0.10, y: 1.52, w: phaseW - 0.18, h: 0.20,
      fontSize: 9, bold: true, charSpacing: 2,
      color: ph.current ? C.YELLOW : C.NAVY_MID, fontFace: "Calibri", margin: 0,
    });
    slide.addText(ph.period, {
      x: x + 0.10, y: 1.73, w: phaseW - 0.18, h: 0.20,
      fontSize: 9.5, color: mutedClr, fontFace: "Calibri", margin: 0,
    });
    slide.addText(ph.title, {
      x: x + 0.10, y: 1.95, w: phaseW - 0.18, h: 0.40,
      fontSize: 14, bold: true, color: textClr, fontFace: "Georgia", margin: 0,
    });
    slide.addText(ph.desc, {
      x: x + 0.10, y: 2.38, w: phaseW - 0.18, h: 2.00,
      fontSize: 10, color: mutedClr, fontFace: "Calibri", valign: "top", margin: 0,
    });
    slide.addText(ph.channels, {
      x: x + 0.10, y: 4.42, w: phaseW - 0.18, h: 0.44,
      fontSize: 9.5, bold: true, italic: true,
      color: ph.current ? C.YELLOW : C.NAVY_MID, fontFace: "Calibri", valign: "top", margin: 0,
    });

    // Current indicator — inside card
    if (ph.current) {
      slide.addText("◀  TODAY", {
        x: x + 0.10, y: 4.74, w: phaseW - 0.18, h: 0.22,
        fontSize: 9, bold: true, color: C.YELLOW, fontFace: "Calibri", align: "center", margin: 0,
      });
    }
  });

  if (!internal) {
    slide.addText("External framing: Phase 1 only — intelligence layer alongside existing POS. Phases 2–4 are internal roadmap only.", {
      x: 0.18, y: 5.26, w: 9.64, h: 0.14,
      fontSize: 7.5, color: C.TEXT_LIGHT, fontFace: "Calibri", italic: true, margin: 0,
    });
  } else {
    slide.addText("Source: project_canary_replaces_counterpoint_long_arc  ·  Internal roadmap — not for external distribution", {
      x: 0.18, y: 5.26, w: 9.64, h: 0.14,
      fontSize: 7.5, color: C.TEXT_LIGHT, fontFace: "Calibri", italic: true, margin: 0,
    });
  }
}

function buildSlide08_SMBDataAsset(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "The ICP: SMB Retailer Wearing Every Hat");
  addFooter(slide);

  slide.addText("Private retail, $10M–$50M revenue, one to a few people making every decision simultaneously.", {
    x: 0.18, y: 0.82, w: 9.64, h: 0.30,
    fontSize: 12, color: C.TEXT_MID, fontFace: "Calibri", italic: true, valign: "top", margin: 0,
  });

  // Left: infrastructure displacement
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 1.18, w: 4.70, h: 3.80,
    fill: { color: C.OFF_WHITE }, line: { color: C.BORDER, width: 1 },
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 1.18, w: 4.70, h: 0.05,
    fill: { color: C.NAVY_MID }, 
  });
  slide.addText("THE INFRASTRUCTURE DISPLACEMENT", {
    x: 0.30, y: 1.26, w: 4.48, h: 0.20,
    fontSize: 9, bold: true, color: C.NAVY_MID, charSpacing: 1, fontFace: "Calibri", margin: 0,
  });
  slide.addText("The $10M–$50M retailer is almost always running a server room nobody talks about.", {
    x: 0.30, y: 1.50, w: 4.48, h: 0.42,
    fontSize: 11, bold: true, color: C.TEXT, fontFace: "Calibri", margin: 0,
  });

  const dispItems = [
    "Backoffice server eliminated — event log lives in the platform",
    "SQL Server license eliminated — cloud-native append-only event storage",
    "MSP contract scope reduced — the complexity that required managed IT no longer exists on-premise",
    "Hardware refresh cycle ends — POS endpoint becomes a thin client",
    "Single point of failure eliminated — no 'guy who knows how it works'",
  ];
  const dispBullets = dispItems.map((t, i) => ({
    text: t, options: { bullet: true, breakLine: i < dispItems.length - 1, fontSize: 10.5, color: C.TEXT, fontFace: "Calibri" },
  }));
  slide.addText(dispBullets, { x: 0.30, y: 1.96, w: 4.48, h: 2.88, valign: "top", margin: 0 });

  // Right: four beats
  const beats = [
    { num: "1", title: "Keeps you on track", body: "Meter model provides accountability without overhead. Every entity operates under a performance contract that runs without anyone watching it." },
    { num: "2", title: "Meets your customers where they're going", body: "Local market intelligence layer: seasonality curves, weather shifts, community events — same signals you sense, now confirmed and quantified." },
    { num: "3", title: "Operates above your weight class", body: "LP monitoring, forecast adjustment, commercial signal surfacing, compliance tracking, evidence anchoring — agents handle these continuously." },
    { num: "4", title: "Gives you back the power to serve", body: "When agents carry the operational weight, you walk the floor instead of running reports. You're a merchant again." },
  ];

  beats.forEach((beat, i) => {
    const by = 1.18 + i * 0.96;
    slide.addShape(pres.shapes.OVAL, {
      x: 5.10, y: by + 0.22, w: 0.38, h: 0.38,
      fill: { color: C.YELLOW }, line: { color: C.YELLOW_DARK, width: 1 },
    });
    slide.addText(beat.num, {
      x: 5.10, y: by + 0.22, w: 0.38, h: 0.38,
      fontSize: 12, bold: true, color: C.NAVY, fontFace: "Georgia", align: "center", valign: "middle", margin: 0,
    });
    slide.addText(beat.title, {
      x: 5.58, y: by + 0.18, w: 4.24, h: 0.26,
      fontSize: 11.5, bold: true, color: C.NAVY, fontFace: "Calibri", margin: 0,
    });
    slide.addText(beat.body, {
      x: 5.58, y: by + 0.46, w: 4.24, h: 0.42,
      fontSize: 10, color: C.TEXT_MID, fontFace: "Calibri", valign: "top", margin: 0,
    });
  });

  slide.addText(
    "\"This model keeps you on track, meets your customers where they're going, and gives you back the power to actually serve them.\"",
    {
      x: 0.18, y: 5.05, w: 9.64, h: 0.26,
      fontSize: 11, bold: true, italic: true, color: C.NAVY, fontFace: "Georgia", align: "center", margin: 0,
    }
  );
}

function buildSlide09_BusinessModel(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "Business Model: Satoshi Cost-to-Serve Replaces $25/Seat");
  addFooter(slide);

  slide.addText(
    "Pricing is denominated in satoshis — transparent, per-junction, aligned with merchant value. No seat, no retainer, no scope creep.",
    { x: 0.18, y: 0.82, w: 9.64, h: 0.30, fontSize: 12, color: C.TEXT_MID, fontFace: "Calibri", italic: true, valign: "top", margin: 0 }
  );

  // Left: mechanism
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 1.18, w: 4.50, h: 3.96,
    fill: { color: C.NAVY }, line: { color: C.NAVY_MID, width: 1 },
    shadow: makeShadow(),
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 1.18, w: 4.50, h: 0.05,
    fill: { color: C.YELLOW }, 
  });
  slide.addText("THE MECHANISM", {
    x: 0.30, y: 1.26, w: 4.28, h: 0.20,
    fontSize: 9, bold: true, color: C.YELLOW, charSpacing: 2, fontFace: "Calibri", margin: 0,
  });

  const mechItems = [
    "Events × tier_weight × service_cost + storage + decisions + passthroughs + anchor share + floor",
    "Tier weights: stream 10× · change-feed 4× · daily-batch 1.5× · reference 0.2×",
    "Patent-protected services (ILDWAC, L402-OTB, blockchain-anchor) charge moat premium",
    "Settlement: pre-funded OTB → per-call gating → period-end with L2 anchor",
    "Channel rev-share by SourceCode — RapidPOS/NCR VARs earn proportional to data flow, settled via Lightning",
  ];
  const mechBullets = mechItems.map((t, i) => ({
    text: t, options: { bullet: true, breakLine: i < mechItems.length - 1, fontSize: 10.5, color: C.WHITE, fontFace: "Calibri" },
  }));
  slide.addText(mechBullets, { x: 0.30, y: 1.52, w: 4.28, h: 2.20, valign: "top", margin: 0 });

  slide.addText("THE MOAT", {
    x: 0.30, y: 3.80, w: 4.28, h: 0.20,
    fontSize: 9, bold: true, color: C.YELLOW, charSpacing: 2, fontFace: "Calibri", margin: 0,
  });
  const moatItems = [
    "Verifiable billing against Bitcoin L2 — no competitor can claim this",
    "Microservice-level cost transparency — Square/Lightspeed/Toast hide cost-to-serve",
    "Channel rev-share as architecture, not contract — settled in Lightning",
  ];
  const moatBullets = moatItems.map((t, i) => ({
    text: t, options: { bullet: true, breakLine: i < moatItems.length - 1, fontSize: 10.5, color: C.WHITE, fontFace: "Calibri" },
  }));
  slide.addText(moatBullets, { x: 0.30, y: 4.02, w: 4.28, h: 1.00, valign: "top", margin: 0 });

  // Right: comparison table
  slide.addText("vs Competitor Pricing Models", {
    x: 4.94, y: 1.14, w: 4.88, h: 0.26,
    fontSize: 13, bold: true, color: C.NAVY, fontFace: "Georgia", margin: 0,
  });

  const compRows = [
    [{ text: "Dimension", options: { bold: true } }, { text: "Square / Toast / Lightspeed", options: { bold: true } }, { text: "Canary Retail", options: { bold: true } }],
    ["Unit",          "$25–200/seat/month",                    "Satoshi per-junction"],
    ["Alignment",     "Flat — no value linkage",               "Aligned with actual data + decision flow"],
    ["Transparency",  "Opaque cost-to-serve",                  "Microservice-level cost breakdown"],
    ["Audit",         "Export to CSV — no chain",              "L2 blockchain anchor — non-repudiable"],
    ["Channel",       "Quota-based VAR contract",              "Rev-share by SourceCode, Lightning-settled"],
    ["High volume",   "Same cost regardless of efficiency",    "5–10× cheaper as merchant efficiency improves"],
  ];
  const compData = compRows.map((row, ri) => row.map((cell, ci) => {
    const text = typeof cell === "string" ? cell : cell.text;
    const base = { text, options: { fontSize: 10, fontFace: "Calibri" } };
    if (ri === 0) { base.options.bold = true; base.options.color = C.WHITE; base.options.fill = { color: C.NAVY }; }
    else if (ci === 0) { base.options.bold = true; base.options.fill = { color: ri % 2 === 0 ? C.OFF_WHITE : C.WHITE }; }
    else if (ci === 1) { base.options.color = C.TEXT_MID; base.options.fill = { color: ri % 2 === 0 ? C.OFF_WHITE : C.WHITE }; }
    else { base.options.color = C.GREEN; base.options.bold = true; base.options.fill = { color: ri % 2 === 0 ? C.OFF_WHITE : C.WHITE }; }
    return base;
  }));

  slide.addTable(compData, {
    x: 4.94, y: 1.44, w: 4.88, h: 3.60,
    colW: [1.36, 1.76, 1.76],
    border: { pt: 0.5, color: C.BORDER },
    rowH: 0.44,
  });

  slide.addText("Source: project_satoshi_cost_model  ·  Brain/wiki/canary-go-satoshi-cost-model.md  ·  docs/sdds/go-handoff/satoshi-cost-rollup.md", {
    x: 0.18, y: 5.26, w: 9.64, h: 0.14,
    fontSize: 7.5, color: C.TEXT_LIGHT, fontFace: "Calibri", italic: true, margin: 0,
  });
}

function buildSlide10_NewCoStructure(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "Two Divisions, One Thesis: Services Dissolution at Every Layer");
  addFooter(slide);

  slide.addText(
    "AI agents structurally close the four gaps that justify professional services firms. NewCo proves this at the application layer (Canary) and the infrastructure layer (CompanyX Division).",
    { x: 0.18, y: 0.82, w: 9.64, h: 0.36, fontSize: 12, color: C.TEXT_MID, fontFace: "Calibri", italic: true, valign: "top", margin: 0 }
  );

  // Two division cards
  // Canary Division (left)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 1.28, w: 4.40, h: 3.66,
    fill: { color: C.NAVY }, line: { color: C.NAVY_MID, width: 1 }, shadow: makeShadow(),
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 1.28, w: 4.40, h: 0.05,
    fill: { color: C.YELLOW }, 
  });
  slide.addText("DIVISION A", { x: 0.30, y: 1.35, w: 4.18, h: 0.20, fontSize: 9, bold: true, color: C.YELLOW, charSpacing: 2, fontFace: "Calibri", margin: 0 });
  slide.addText("Canary Retail", { x: 0.30, y: 1.57, w: 4.18, h: 0.34, fontSize: 18, bold: true, color: C.WHITE, fontFace: "Georgia", margin: 0 });
  slide.addText("Application Layer", { x: 0.30, y: 1.93, w: 4.18, h: 0.22, fontSize: 11, color: "9BACC8", fontFace: "Calibri", margin: 0 });

  const canaryItems = [
    "13-module retail spine (inventory, labor, LP, merchandising, ordering, etc.)",
    "65-entity canonical data model — ARTS-native",
    "166-junction MCP service architecture",
    "Four accountability rails: Ops / Financial / Evidentiary / Vendor",
    "Satoshi per-junction billing — verifiable against Bitcoin L2",
    "ICP: SMB private retail, $10M–$50M, wearing every hat",
    "Channel: RapidPOS VAR ecosystem + direct",
  ];
  const canaryBullets = canaryItems.map((t, i) => ({
    text: t, options: { bullet: true, breakLine: i < canaryItems.length - 1, fontSize: 10.5, color: C.WHITE, fontFace: "Calibri" },
  }));
  slide.addText(canaryBullets, { x: 0.30, y: 2.18, w: 4.18, h: 2.64, valign: "top", margin: 0 });

  // CompanyX Division (right)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 4.78, y: 1.28, w: 5.04, h: 3.66,
    fill: { color: C.OFF_WHITE }, line: { color: C.BORDER, width: 1 }, shadow: makeShadow(),
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 4.78, y: 1.28, w: 5.04, h: 0.05,
    fill: { color: C.NAVY_MID }, 
  });
  slide.addText("DIVISION B", { x: 4.90, y: 1.35, w: 4.82, h: 0.20, fontSize: 9, bold: true, color: C.NAVY_MID, charSpacing: 2, fontFace: "Calibri", margin: 0 });
  slide.addText("CompanyX Cloud", { x: 4.90, y: 1.57, w: 4.82, h: 0.34, fontSize: 18, bold: true, color: C.TEXT, fontFace: "Georgia", margin: 0 });
  slide.addText("Infrastructure Layer (Partner-Contributed)", { x: 4.90, y: 1.93, w: 4.82, h: 0.22, fontSize: 11, color: C.TEXT_MID, fontFace: "Calibri", margin: 0 });

  const cx_items = [
    "Terraform-as-code, drift detection, cost optimization, SRE automation",
    "Multi-cloud orchestration with vendor SLA accountability",
    "Agent-native infrastructure management (parallel canonical spec exercise)",
    "Per-tenant cost-to-serve in satoshis — same billing substrate as Canary",
    "ICP: SMB and lower mid-market (existing install base from partner)",
    "Proves services dissolution at the infrastructure layer below applications",
    "Partner profile: existing cloud/devops/MSP book of business to modernize",
  ];
  const cx_bullets = cx_items.map((t, i) => ({
    text: t, options: { bullet: true, breakLine: i < cx_items.length - 1, fontSize: 10.5, color: C.TEXT, fontFace: "Calibri" },
  }));
  slide.addText(cx_bullets, { x: 4.90, y: 2.18, w: 4.82, h: 2.64, valign: "top", margin: 0 });

  // Shared substrate bar at bottom
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.18, y: 5.01, w: 9.64, h: 0.28,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 },
  });
  slide.addText(
    "SHARED SUBSTRATE  ·  Agent runtime  ·  MCP service framework  ·  Satoshi billing (ILDWAC)  ·  L402 settlement  ·  Blockchain anchoring  ·  Vendor SLA ledger",
    { x: 0.28, y: 5.04, w: 9.40, h: 0.22, fontSize: 9.5, bold: true, color: C.NAVY, fontFace: "Calibri", valign: "middle", margin: 0 }
  );
}

function buildSlide11_Risks(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.WHITE };
  addHeader(slide, "Honest Framing: Risks & Open Questions");
  addFooter(slide);

  slide.addText("We are pre-revenue, pre-formation. These are the real open questions — not glossed over.", {
    x: 0.18, y: 0.82, w: 9.64, h: 0.28,
    fontSize: 12, color: C.TEXT_MID, fontFace: "Calibri", italic: true, valign: "top", margin: 0,
  });

  const risks = [
    {
      title: "Who is CompanyX?",
      body: "The NewCo thesis requires a cloud/devops partner with an existing install base. Profile: devops consultancy, infrastructure platform, cloud cost-optimization firm, or modernizing MSP. Partner selection is the critical path item for Division B. Not yet identified.",
    },
    {
      title: "Regulatory exposure for agentic services",
      body: "Agents executing on behalf of merchants (financial commitments, LP evidence, vendor disputes) enters novel legal territory, especially when PE portfolio companies are involved. Fiduciary implications unclear at scale. SOC 2 / ISO 27001 scope is pre-Phase 4 delivery — see GRO-686–699.",
    },
    {
      title: "PCI scope at Phase 4",
      body: "Phase 4 (full POS) brings PCI Service Provider scope. Card data flows pinpad→processor, never through Canary. Architecture must honor this boundary from Phase 3. ~$500K–$1M launch investment when scope opens.",
    },
    {
      title: "Brand strategy",
      body: "Is NewCo a single brand (one holding company) or two operating brands under a holding entity? The Canary brand is already in motion. CompanyX brand is the founder's or partner's call. Not resolved.",
    },
    {
      title: "Talent: who needs to be on the team",
      body: "Solo-founder + AI agent delivery works through proof-of-concept phase. Phase 2 forward requires at minimum a VP Sales / channel lead and a compliance officer. Capital requirements are modest (low headcount, agent-driven) but Phase 3 register-side has hardware dependencies.",
    },
    {
      title: "Incumbent defense",
      body: "NCR Counterpoint / RapidPOS are upstream data sources in Phase 1. Phase 2+ narrowing of their workflow surface will trigger incumbent defense. Canary must be deeply installed and evidence-rich before Phase 2 begins. The CATz method (channel-friendly, cross-vendor) is the shield.",
    },
  ];

  risks.forEach((risk, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.18 + col * 4.92;
    const y = 1.16 + row * 1.34;

    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.72, h: 1.24,
      fill: { color: C.OFF_WHITE }, line: { color: C.BORDER, width: 1 },
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.05, h: 1.24,
      fill: { color: "E53E3E" }, 
    });
    slide.addText(risk.title, {
      x: x + 0.12, y: y + 0.08, w: 4.50, h: 0.22,
      fontSize: 11, bold: true, color: C.TEXT, fontFace: "Calibri", margin: 0,
    });
    slide.addText(risk.body, {
      x: x + 0.12, y: y + 0.32, w: 4.50, h: 0.84,
      fontSize: 9.5, color: C.TEXT_MID, fontFace: "Calibri", valign: "top", margin: 0,
    });
  });
}

function buildSlide12_Close(pres) {
  const slide = pres.addSlide();
  slide.background = { color: C.NAVY };
  addFooter(slide, { dark: true });

  slide.addImage({ path: LOGO_PATH, x: 4.2, y: 0.42, w: 1.6, h: 1.6 });

  slide.addText("THREE PATHS FORWARD", {
    x: 0.5, y: 2.12, w: 9, h: 0.28,
    fontSize: 11, bold: true, color: C.YELLOW, charSpacing: 3, fontFace: "Calibri", align: "center", margin: 0,
  });

  // Three columns
  const paths = [
    { title: "Partner", body: "You have an install base of retailers or SMB clients. Canary's intelligence layer and channel rev-share model makes your product more valuable without replacing it. The CATz method is the delivery vehicle." },
    { title: "Invest", body: "Pre-revenue, self-funding through proof-of-concept. Seeking strategic capital aligned with the agentic-services thesis — not PE management fees, but growth capital that accelerates Phase 2 channel expansion." },
    { title: "Use Canary", body: "You are a $10M–$50M independent retailer on NCR Counterpoint or RapidPOS. You are wearing every hat. The first customer proof case is the most important conversation we are having right now." },
  ];

  paths.forEach((p, i) => {
    const x = 0.68 + i * 2.98;
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 2.52, w: 2.70, h: 2.56,
      fill: { color: "162140" }, line: { color: C.NAVY_MID, width: 1 },
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 2.52, w: 2.70, h: 0.05,
      fill: { color: C.YELLOW }, 
    });
    slide.addText(p.title, {
      x: x + 0.14, y: 2.62, w: 2.42, h: 0.30,
      fontSize: 16, bold: true, color: C.YELLOW, fontFace: "Georgia", margin: 0,
    });
    slide.addText(p.body, {
      x: x + 0.14, y: 2.96, w: 2.42, h: 2.00,
      fontSize: 10.5, color: C.WHITE, fontFace: "Calibri", valign: "top", margin: 0,
    });
  });

  slide.addText("Contact: GrowDirect LLC  ·  hello@growdirect.io", {
    x: 0.5, y: 5.18, w: 9, h: 0.18,
    fontSize: 9, color: "9BACC8", fontFace: "Calibri", align: "center", margin: 0,
  });
}

// ── Main: build both versions ─────────────────────────────────────

async function buildVersion(outputPath, internal) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "GrowDirect LLC";
  pres.title = internal
    ? "Canary Retail — Partnership & Investment Overview (Internal)"
    : "Canary Retail — Partnership & Investment Overview";

  // Attach pres reference for shapes in helpers
  // (PptxGenJS exposes pres.shapes on slides, but we need it in helpers — attach via closure)
  const originalAddSlide = pres.addSlide.bind(pres);
  pres.addSlide = function(...args) {
    const slide = originalAddSlide(...args);
    slide.pres = pres;
    return slide;
  };

  buildSlide01_Cover(pres);
  buildSlide02_StrategicPerspective(pres);
  buildSlide03_WhoWeAre(pres, internal);
  buildSlide04_CategoryDifference(pres);
  buildSlide05_FourRails(pres);
  buildSlide06_MCPJunctional(pres);
  buildSlide07_PhasedTrajectory(pres, internal);
  buildSlide08_SMBDataAsset(pres);
  buildSlide09_BusinessModel(pres);
  buildSlide10_NewCoStructure(pres);
  buildSlide11_Risks(pres);
  buildSlide12_Close(pres);

  await pres.writeFile({ fileName: outputPath });
  console.log(`✓  ${outputPath}`);
}

(async () => {
  const outDir = __dirname;
  await buildVersion(path.join(outDir, "canary-retail-deck-v1-internal.pptx"), true);
  await buildVersion(path.join(outDir, "canary-retail-deck-v1-external.pptx"), false);
  console.log("Done.");
})();
