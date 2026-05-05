const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, HeadingLevel,
  VerticalAlign, PageOrientation, Header, ImageRun, LevelFormat
} = require('/opt/homebrew/lib/node_modules/docx');
const fs = require('fs');
const path = require('path');

// Brand colors
const DEEP_INK   = '0F1729';
const SLATE      = '1F2D4A';
const CYAN       = '4FC3DC';
const SIGNAL     = 'F2C94C';
const IVORY      = 'F4F1EA';
const STONE      = 'DDD8CD';

// Page: US Letter, 1" margins
const PAGE = { width: 12240, height: 15840 };
const MARGIN = 1440;
const CONTENT_W = PAGE.width - MARGIN * 2; // 9360

function labelRun(text) {
  return new TextRun({ text, font: 'Arial', size: 20, bold: true, color: CYAN, allCaps: true, characterSpacing: 30 });
}

function bodyRun(text, opts = {}) {
  return new TextRun({ text, font: 'Arial', size: 20, color: IVORY, ...opts });
}

function heroRun(text) {
  return new TextRun({ text, font: 'Arial', size: 22, color: IVORY });
}

function labelPara(text) {
  return new Paragraph({
    spacing: { before: 320, after: 80 },
    children: [labelRun(text)]
  });
}

function bodyPara(text, opts = {}) {
  return new Paragraph({
    spacing: { before: 0, after: 160 },
    children: [bodyRun(text, opts)]
  });
}

function divider() {
  return new Paragraph({
    spacing: { before: 240, after: 240 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: SLATE, space: 1 } },
    children: []
  });
}

function cellBorders(color = SLATE) {
  const b = { style: BorderStyle.SINGLE, size: 1, color };
  return { top: b, bottom: b, left: b, right: b };
}

// Header row for tables
function headerCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    borders: cellBorders(SLATE),
    shading: { fill: SLATE, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text, font: 'Arial', size: 18, bold: true, color: CYAN, allCaps: true, characterSpacing: 20 })] })]
  });
}

function dataCell(text, width, highlight = false) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    borders: cellBorders(SLATE),
    shading: { fill: highlight ? SLATE : DEEP_INK, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text, font: 'Arial', size: 18, color: highlight ? SIGNAL : IVORY })] })]
  });
}

// --- TABLES ---

// Claims table
const claimsTable = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: [3600, 5760],
  rows: [
    new TableRow({ children: [headerCell('BRAND CLAIM', 3600), headerCell('WHAT IT REQUIRES', 5760)] }),
    new TableRow({ children: [
      dataCell('"Listening Systems that keep the operating model intelligent"', 3600, true),
      dataCell('Compute that runs continuously. A scheduler, a data store, a wire substrate. Not a spreadsheet.', 5760)
    ]}),
    new TableRow({ children: [
      dataCell('"We invoice when the cost line moves"', 3600, true),
      dataCell('A baseline captured before work starts. A diff engine comparing after. An audit trail that survives the engagement.', 5760)
    ]}),
    new TableRow({ children: [
      dataCell('"We agree the baseline before any work starts"', 3600, true),
      dataCell('A structured artifact stored, versioned, and queryable. A schema-fragment in AlloyDB, not a slide.', 5760)
    ]}),
  ]
});

// Deployment options table
const optionsTable = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: [1560, 2400, 2400, 3000],
  rows: [
    new TableRow({ children: [
      headerCell('OPTION', 1560),
      headerCell('WHAT IT IS', 2400),
      headerCell('PROS', 2400),
      headerCell('CONS', 3000)
    ]}),
    new TableRow({ children: [
      dataCell('A — GCP Shared', 1560, true),
      dataCell('Shared GCP project; all engagements on a single AlloyDB + Cloud Run stack', 2400),
      dataCell('Cheapest to operate. Patterns index compounds. Fastest to deploy.', 2400),
      dataCell('Carries the security posture. Data co-mingled (schema isolation). Procurement friction at enterprise clients.', 3000)
    ]}),
    new TableRow({ children: [
      dataCell('B — Customer GCP', 1560, true),
      dataCell('Deploy Atlas View into the client\'s own GCP project per engagement', 2400),
      dataCell('Clean data residency. No infra costs. Enterprise-friendly.', 2400),
      dataCell('Patterns index breaks. Each engagement is an island. Deployment overhead per client.', 3000)
    ]}),
    new TableRow({ children: [
      dataCell('C — Workstation', 1560, true),
      dataCell('Postgres + pgvector on MacBook Pro; no cloud', 2400),
      dataCell('Zero cloud spend. Works air-gapped. Fully portable.', 2400),
      dataCell('No Listening System heartbeat without laptop open. No cross-engagement index. Data requires explicit sync.', 3000)
    ]}),
  ]
});

// Decision table
const decisionTable = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: [2000, 3000, 4360],
  rows: [
    new TableRow({ children: [
      headerCell('TIER', 2000),
      headerCell('WHERE IT LIVES', 3000),
      headerCell('WHAT IT HOLDS', 4360)
    ]}),
    new TableRow({ children: [
      dataCell('Control Plane', 2000, true),
      dataCell('GCP shared — always-on', 3000),
      dataCell('Patterns index only. Cross-engagement synthesis. Imprint registry. No raw engagement data.', 4360)
    ]}),
    new TableRow({ children: [
      dataCell('Execution Tier', 2000, true),
      dataCell('Per-engagement: customer GCP preferred, workstation fallback', 3000),
      dataCell('Fragment store. Vault. Listening System heartbeats. Transcript and schema-fragment records for that engagement.', 4360)
    ]}),
  ]
});

// Architecture layers table
const archTable = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: [2400, 3760, 3200],
  rows: [
    new TableRow({ children: [
      headerCell('LAYER', 2400),
      headerCell('WHAT IT IS', 3760),
      headerCell('WHERE IT LIVES', 3200)
    ]}),
    new TableRow({ children: [
      dataCell('Atlas View substrate', 2400, true),
      dataCell('AlloyDB schema, Cloud Run services, imprint format', 3760),
      dataCell('GCP control plane', 3200)
    ]}),
    new TableRow({ children: [
      dataCell('Patterns index', 2400, true),
      dataCell('Cross-engagement synthesis. The compounding surface.', 3760),
      dataCell('GCP control plane — persistent', 3200)
    ]}),
    new TableRow({ children: [
      dataCell('Engagement execution', 2400, true),
      dataCell('Fragment store, vault, Listening System heartbeats', 3760),
      dataCell('Client perimeter — per engagement', 3200)
    ]}),
    new TableRow({ children: [
      dataCell('Method layer', 2400, true),
      dataCell('Five-D System, Sparring Partner definitions, Listening System logic', 3760),
      dataCell('Delivered as imprints at engagement start', 3200)
    ]}),
    new TableRow({ children: [
      dataCell('Brand surface', 2400, true),
      dataCell('Atlas View UI, Sparring Partner cards', 3760),
      dataCell('Deep Ink ground. Signal Yellow active nodes.', 3200)
    ]}),
  ]
});

// --- DOCUMENT ---

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: PAGE.width, height: PAGE.height },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }
      }
    },
    children: [
      // Document label
      new Paragraph({
        spacing: { before: 0, after: 80 },
        children: [new TextRun({ text: 'INTERNAL BRIEF  ·  2026-05-05', font: 'Arial', size: 18, bold: true, color: STONE, allCaps: true, characterSpacing: 20 })]
      }),

      // Title
      new Paragraph({
        spacing: { before: 160, after: 80 },
        children: [new TextRun({ text: 'Atlas View', font: 'Arial', size: 52, color: IVORY })]
      }),
      new Paragraph({
        spacing: { before: 0, after: 320 },
        children: [new TextRun({ text: 'Deployment Posture', font: 'Arial', size: 44, color: STONE })]
      }),

      // Governing claim
      new Paragraph({
        spacing: { before: 0, after: 400 },
        border: { left: { style: BorderStyle.SINGLE, size: 12, color: SIGNAL, space: 12 } },
        indent: { left: 240 },
        children: [new TextRun({ text: 'Three brand claims require infrastructure to be true. Without it, they are marketing copy.', font: 'Arial', size: 22, color: IVORY, italics: true })]
      }),

      divider(),

      // THE PROBLEM
      labelPara('THE PROBLEM'),
      claimsTable,
      new Paragraph({ spacing: { before: 160, after: 240 }, children: [bodyRun('Deliver these claims manually and Ruptiv cannot scale, cannot compound, and cannot prove the outcome to a skeptical CFO.')] }),

      divider(),

      // DEPLOYMENT OPTIONS
      labelPara('DEPLOYMENT OPTIONS'),
      optionsTable,

      divider(),

      // DECISION
      labelPara('DECISION'),
      new Paragraph({
        spacing: { before: 0, after: 200 },
        children: [new TextRun({ text: 'Two-tier posture: shared control plane + per-engagement execution tier.', font: 'Arial', size: 22, color: SIGNAL, bold: true })]
      }),
      decisionTable,
      new Paragraph({ spacing: { before: 240, after: 120 }, children: [bodyRun('The Patterns index is the compounding surface. It holds abstract patterns only — no client-identifiable data.')] }),
      new Paragraph({ spacing: { before: 0, after: 120 }, children: [bodyRun('Raw engagement data stays in the client\'s perimeter. Customer GCP is the target. Workstation is acceptable for Phase 1 or air-gapped clients.')] }),

      divider(),

      // DEPLOYMENT FOOTPRINT
      labelPara('DEPLOYMENT FOOTPRINT'),
      new Paragraph({ spacing: { before: 0, after: 80 }, children: [bodyRun('Control Plane — always running:', { bold: true, color: CYAN })] }),
      new Paragraph({ spacing: { before: 0, after: 60 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('AlloyDB Serverless (non-prod) → ~$30-50/month while no active synthesizer jobs')] }),
      new Paragraph({ spacing: { before: 0, after: 60 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('Cloud Run (Synthesizer imprint) → zero when idle')] }),
      new Paragraph({ spacing: { before: 0, after: 60 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('Pub/Sub (pattern event bus) → negligible')] }),
      new Paragraph({ spacing: { before: 0, after: 160 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('Total holding cost: ~$50/month', { bold: true, color: SIGNAL })] }),

      new Paragraph({ spacing: { before: 120, after: 80 }, children: [bodyRun('Per-Engagement Execution — deployed at engagement start:', { bold: true, color: CYAN })] }),
      new Paragraph({ spacing: { before: 0, after: 60 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('Option 1: Customer\'s GCP project — deploy AlloyDB + Cloud Run + Scheduler; client pays the bill')] }),
      new Paragraph({ spacing: { before: 0, after: 60 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('Option 2: MacBook Pro running Postgres + pgvector (Docker) — zero cloud cost; works anywhere')] }),
      new Paragraph({ spacing: { before: 0, after: 160 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('Engagement teardown: fragment store exported to cold archive, workstation wiped')] }),

      new Paragraph({ spacing: { before: 120, after: 80 }, children: [bodyRun('Travel kit (Option 2):', { bold: true, color: CYAN })] }),
      new Paragraph({ spacing: { before: 0, after: 60 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('MacBook Pro M-series, 32GB RAM minimum')] }),
      new Paragraph({ spacing: { before: 0, after: 60 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('Docker: postgres:17-pgvector, cloud-run-emulator, ollama')] }),
      new Paragraph({ spacing: { before: 0, after: 240 }, numbering: { reference: 'bullets', level: 0 }, children: [bodyRun('One-command bootstrap: make engagement-init SLUG=clientname-2026-Q2', { font: 'Courier New' })] }),

      divider(),

      // ARCHITECTURE LAYERS
      labelPara('ARCHITECTURE LAYERS'),
      archTable,

      divider(),

      // DECISION GATE
      labelPara('DECISION GATE'),
      new Paragraph({ spacing: { before: 0, after: 160 }, children: [bodyRun('Two questions at engagement start. No other decisions required.')] }),
      new Paragraph({ spacing: { before: 0, after: 80 }, numbering: { reference: 'numbers', level: 0 }, children: [
        bodyRun('Is the client GCP-capable? ', { bold: true }),
        bodyRun('Yes: deploy into their project.  No: workstation tier.')
      ]}),
      new Paragraph({ spacing: { before: 0, after: 320 }, numbering: { reference: 'numbers', level: 0 }, children: [
        bodyRun('Is the client air-gapped or high-security? ', { bold: true }),
        bodyRun('Yes: workstation only, no control plane sync.  No: sync pattern abstractions to control plane after engagement closes.')
      ]}),

      // Signature line
      new Paragraph({
        spacing: { before: 480, after: 0 },
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: 'Workflows, reinvented.', font: 'Arial', size: 22, color: SIGNAL, italics: true })]
      }),
    ]
  }],
  numbering: {
    config: [
      {
        reference: 'bullets',
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 480, hanging: 240 } }, run: { color: CYAN, font: 'Arial' } }
        }]
      },
      {
        reference: 'numbers',
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 480, hanging: 240 } }, run: { color: CYAN, font: 'Arial', bold: true } }
        }]
      }
    ]
  },
  background: { color: DEEP_INK }
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(__dirname, 'ruptiv-deployment-posture.docx');
  fs.writeFileSync(out, buf);
  console.log('Written:', out);
});
