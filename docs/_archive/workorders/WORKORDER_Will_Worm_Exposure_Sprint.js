const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, LevelFormat, ExternalHyperlink
} = require("docx");

// ─── Shared Styles ───
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };
const headerShading = { fill: "1A1A2E", type: ShadingType.CLEAR };
const headerRun = (text) => new TextRun({ text, bold: true, color: "FFFFFF", font: "Arial", size: 20 });
const bodyRun = (text, opts = {}) => new TextRun({ text, font: "Arial", size: 20, ...opts });
const boldRun = (text, opts = {}) => new TextRun({ text, font: "Arial", size: 20, bold: true, ...opts });

// Content width for US Letter with 1" margins = 9360 DXA
const CONTENT_WIDTH = 9360;

// ─── Helper: simple 2-col table ───
function twoColTable(rows, col1Width = 2800, col2Width = 6560) {
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [col1Width, col2Width],
    rows: rows.map(([label, value], i) =>
      new TableRow({
        children: [
          new TableCell({
            borders,
            width: { size: col1Width, type: WidthType.DXA },
            margins: cellMargins,
            shading: i === 0 ? headerShading : { fill: "F5F5F5", type: ShadingType.CLEAR },
            children: [new Paragraph({ children: [i === 0 ? headerRun(label) : boldRun(label)] })]
          }),
          new TableCell({
            borders,
            width: { size: col2Width, type: WidthType.DXA },
            margins: cellMargins,
            shading: i === 0 ? headerShading : undefined,
            children: [new Paragraph({ children: [i === 0 ? headerRun(value) : bodyRun(value)] })]
          }),
        ],
      })
    ),
  });
}

// ─── Helper: multi-col table ───
function multiColTable(headers, rows, colWidths) {
  const headerRow = new TableRow({
    children: headers.map((h, i) =>
      new TableCell({
        borders,
        width: { size: colWidths[i], type: WidthType.DXA },
        margins: cellMargins,
        shading: headerShading,
        children: [new Paragraph({ children: [headerRun(h)] })]
      })
    ),
  });
  const dataRows = rows.map((row) =>
    new TableRow({
      children: row.map((cell, i) =>
        new TableCell({
          borders,
          width: { size: colWidths[i], type: WidthType.DXA },
          margins: cellMargins,
          children: [new Paragraph({ children: [bodyRun(cell)] })]
        })
      ),
    })
  );
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, ...dataRows],
  });
}

// ─── Helper: spacer ───
const spacer = (pts = 120) => new Paragraph({ spacing: { after: pts }, children: [] });

// ─── Helper: bullet config ───
const numbering = {
  config: [
    {
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "\u2022",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    },
    {
      reference: "numbers",
      levels: [{
        level: 0, format: LevelFormat.DECIMAL, text: "%1.",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    },
    {
      reference: "actions",
      levels: [{
        level: 0, format: LevelFormat.DECIMAL, text: "%1.",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    },
  ],
};

// ─── Bullet helper ───
const bullet = (text, ref = "bullets") =>
  new Paragraph({
    numbering: { reference: ref, level: 0 },
    spacing: { after: 60 },
    children: [bodyRun(text)]
  });

const actionItem = (text) =>
  new Paragraph({
    numbering: { reference: "actions", level: 0 },
    spacing: { after: 80 },
    children: [bodyRun(text)]
  });

// ─── BUILD DOCUMENT ───
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1A1A2E" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2E4057" },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 }
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "3D5A80" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
      },
    ]
  },
  numbering,
  sections: [
    // ─── PAGE 1: COVER / METADATA ───
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "F59E0B", space: 1 } },
            children: [
              boldRun("GrowDirect Inc.", { color: "1A1A2E", size: 18 }),
              bodyRun("  |  WORK ORDER  |  CONFIDENTIAL", { color: "888888", size: 16 }),
            ]
          })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            border: { top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC", space: 1 } },
            children: [
              bodyRun("Page ", { size: 16, color: "888888" }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "888888", font: "Arial" }),
            ]
          })]
        })
      },
      children: [
        spacer(600),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 80 },
          children: [new TextRun({ text: "WORK ORDER", font: "Arial", size: 44, bold: true, color: "1A1A2E" })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          children: [new TextRun({ text: "Exposure Sprint: Will + WORM", font: "Arial", size: 32, color: "F59E0B" })]
        }),
        spacer(200),
        twoColTable([
          ["Field", "Value"],
          ["Work Order ID", "WO-2026-0316-EXPOSURE"],
          ["Date Issued", "March 16, 2026"],
          ["Issued By", "ALX (Chief of Staff)"],
          ["Primary Owners", "Will (Lead Gen) + WORM (Local SEO)"],
          ["Supporting", "Art (Design), Jess (Investor Docs), Eva (Marketplace)"],
          ["Sprint", "6.5 \u2192 7 Bridge"],
          ["Priority", "HIGH \u2014 First-mover window open"],
          ["Deadline", "Phase 1: March 23 | Phase 2: April 5 | Phase 3: Ongoing"],
          ["Classification", "CONFIDENTIAL \u2014 INTERNAL USE ONLY"],
        ]),
        spacer(300),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("This work order assigns Will and WORM a coordinated exposure sprint based on competitive intelligence gathered from the Square Community forums, industry conference calendars, and competitive landscape analysis. The gap is confirmed: no loss prevention app exists on the Square Marketplace. The demand is loud and unserved. This is Canary\u2019s lane.")]
        }),
      ],
    },

    // ─── PAGE 2: INTELLIGENCE BRIEF ───
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: [
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("1. Intelligence Brief")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1.1 Square Community Forum Findings")] }),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("ALX conducted a systematic search of community.squareup.com on March 16, 2026. The following threads represent confirmed, unserved merchant demand that maps directly to Canary\u2019s Chirp detection engine.")]
        }),

        multiColTable(
          ["Thread Topic", "Merchant Pain", "Canary Mapping"],
          [
            ["$0 transaction opens cash drawer", "Anyone can open drawer with fake $0 sale \u2014 theft vector", "Chirp C-004: After-hours / anomalous transaction detection"],
            ["Cash refund not in drawer report", "Refunds vanish from cash drawer reconciliation", "Chirp C-001: Rapid refund correlation"],
            ["No inventory shrinkage report", "Merchants mark items as theft but can\u2019t pull reports", "Fox case management + analytics dashboard"],
            ["95% chargeback loss rate", "Banks side with customers; merchants have no proof", "TSP receipt verification + .jeffe proof chain"],
            ["Cancelled cash sales invisible", "No way to find voided cash transactions", "Chirp C-002: Excessive void/refund rate detection"],
            ["Fraud alert on refund fees", "Square charges processing fees even on fraudulent refunds", "Alert engine + refund pattern flagging"],
          ],
          [2600, 3200, 3560]
        ),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1.2 Key Forum Thread URLs")] }),
        new Paragraph({ spacing: { after: 60 }, children: [bodyRun("Will and WORM should mine these threads for language, pain points, and content hooks:")] }),
        bullet("Cash drawer $0 exploit: community.squareup.com/t5/Square-Staff-and-Payroll/.../idi-p/755923"),
        bullet("Inventory shrinkage report gap: community.squareup.com/t5/Square-for-Retail/.../td-p/329513"),
        bullet("Cash refund tracking failure: community.squareup.com/t5/Archived-Discussions/.../td-p/45529"),
        bullet("Chargeback protection: community.squareup.com/t5/Payments-Troubleshooting/.../td-p/676000"),
        bullet("Cancelled cash sales: community.squareup.com/t5/Hardware-Setup-Troubleshooting/.../m-p/735799"),
        bullet("Fraud alert + refund fees: community.squareup.com/t5/Square-for-Retail/.../m-p/666651"),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1.3 Competitive Landscape")] }),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("Retail shrink hit $112.1B in 2025. The LP software market is dominated by enterprise players. No one is serving SMB Square merchants.")]
        }),
        multiColTable(
          ["Competitor", "Focus", "Price Range", "Gap vs. Canary"],
          [
            ["Spot AI", "Video + POS integration", "$300\u2013$1,500/mo", "Camera-first, no transaction intelligence"],
            ["Appriss Retail", "ORC + predictive analytics", "Enterprise only", "100+ location minimum"],
            ["RetailNext", "IoT sensors + foot traffic", "Enterprise only", "Hardware-heavy, no POS-native detection"],
            ["POS Nation", "Basic inventory tracking", "$149+/mo", "No AI, no pattern detection, not Square-native"],
            ["Square (native)", "Activity logs only", "Free (manual)", "Zero alerting, zero automation, zero LP tools"],
          ],
          [1800, 2200, 1800, 3560]
        ),
        new Paragraph({
          spacing: { before: 120, after: 120 },
          children: [
            boldRun("Bottom line: "),
            bodyRun("Canary has zero direct competitors in the \u201CAI loss prevention for Square SMB merchants\u201D category. Square Marketplace expanded to ~1,000 partner integrations in February 2026 and not one is a loss prevention app."),
          ]
        }),
      ],
    },

    // ─── PAGE 3: CONFERENCES & EVENTS ───
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: [
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("2. Conferences, Events & Gatherings")] }),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("The following events represent exposure opportunities for GrowDirect / Canary LP. Sorted by date. ALX recommends attending RILA and NRF PROTECT as intelligence-gathering missions (not exhibiting yet) and the Small Business Expos for direct merchant contact.")]
        }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.1 Loss Prevention / Asset Protection (Core Industry)")] }),
        multiColTable(
          ["Event", "Date", "Location", "Why It Matters"],
          [
            ["RILA Retail Asset Protection Conference", "April 19\u201322, 2026", "Phoenix, AZ", "1,000+ LP leaders. See who\u2019s exhibiting. Validate positioning. 84% are buyers."],
            ["NRF PROTECT 2026", "June 8\u201310, 2026", "Grapevine, TX (Gaylord Texan)", "Largest LP event in N. America. 200+ solution providers. Expo sells out yearly."],
          ],
          [2200, 1800, 2200, 3160]
        ),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.2 Retail Tech / SMB (Merchant Contact)")] }),
        multiColTable(
          ["Event", "Date", "Location", "Why It Matters"],
          [
            ["Small Business Expo \u2014 Multiple Cities", "Ongoing 2026 (Boston: May 27)", "US major metros", "America\u2019s largest B2B event for SMB owners. Direct merchant conversations."],
            ["CommerceNext Growth Show", "June 24\u201326, 2026", "New York, NY", "Ecommerce + retail decision-makers. Good for partnership intros."],
            ["ShopTalk Fall", "Sept 29 \u2013 Oct 1, 2026", "Nashville, TN", "Senior retail decision-makers. Strategic visibility."],
            ["NRF Retail\u2019s Big Show Europe", "Sept 15\u201317, 2026", "Paris, France", "Omnichannel commerce. International expansion signal."],
          ],
          [2200, 1800, 2000, 3360]
        ),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.3 Square-Specific")] }),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("Square runs webinars and community events through community.squareup.com/Events. Recent: \u201CAI for small business: 5 game-changing uses in 2026.\u201D Square does not currently host a large annual seller conference, but their community events page is where partnership announcements and seller webinars surface. WORM should monitor this weekly.")]
        }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.4 Recommended Conference Actions")] }),
        multiColTable(
          ["Event", "Action", "Owner", "Budget Est."],
          [
            ["RILA (April)", "Attend. Recon only. Map exhibitor landscape. Collect business cards.", "Jeffe + Will", "$1,500\u2013$2,500 (pass + travel)"],
            ["NRF PROTECT (June)", "Attend. Walk the expo floor. Identify integration partners.", "Jeffe + Will", "$2,000\u2013$3,000 (pass + travel)"],
            ["Small Business Expo (ongoing)", "Attend nearest city. Test merchant pitch in person.", "Will", "$0\u2013$500 (free expo pass + travel)"],
            ["Square Community Events", "Monitor weekly. Engage in relevant threads.", "WORM", "$0"],
          ],
          [2200, 3000, 1800, 2360]
        ),
      ],
    },

    // ─── PAGE 4: COMMUNITY FORUM STRATEGY ───
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: [
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("3. GrowDirect Community Forum \u2014 Build vs. Buy")] }),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("Jeffe asked whether GrowDirect should generate its own user forum. Short answer: yes, but staged. Here\u2019s the breakdown.")]
        }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.1 Why a Forum Matters")] }),
        bullet("Merchants discussing loss prevention in a GrowDirect-owned space = organic SEO + community lock-in"),
        bullet("Forum threads rank in Google. Every \u201Chow to detect employee theft with Square\u201D post is a Canary lead"),
        bullet("Community = moat. Merchants helping merchants builds trust that advertising cannot buy"),
        bullet("User-generated content feeds Will\u2019s lead gen and WORM\u2019s SEO simultaneously"),
        bullet("Square Community proves the demand exists but Square isn\u2019t solving it \u2014 we own the conversation"),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.2 Platform Options")] }),
        multiColTable(
          ["Platform", "Type", "Cost", "Pros", "Cons"],
          [
            ["Discourse", "Self-hosted (open source)", "$50\u201380/mo hosting", "Full control, SEO-optimized, infinite customization, no per-user fees", "Requires server management, setup time"],
            ["Circle", "SaaS", "$89\u2013$299/mo", "Clean UX, courses/events built in, fast launch", "Per-user pricing scales up, less SEO control"],
            ["Mighty Networks", "SaaS", "$41\u2013$360/mo", "Community + courses + events, mobile app", "Less technical audience fit, branded as \u201Ccreator\u201D platform"],
            ["Bettermode", "SaaS", "$399+/mo", "Deep customization, SSO, API access", "Expensive for early stage, complex setup"],
            ["WordPress + BuddyBoss", "Self-hosted", "$50\u201380/mo hosting + $228/yr plugin", "Familiar stack, total control, one-time plugin cost", "Plugin maintenance, slower than purpose-built"],
          ],
          [1600, 1200, 1600, 2400, 2560]
        ),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.3 ALX Recommendation: Staged Rollout")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Phase 1: Guerrilla (Now \u2013 April)")] }),
        bullet("Don\u2019t build a forum yet. Engage on Square Community directly."),
        bullet("WORM creates a GrowDirect account on community.squareup.com and starts answering LP-related threads with helpful advice (not sales pitches)"),
        bullet("Will monitors threads weekly, extracts pain-point language for content calendar"),
        bullet("Build credibility before building infrastructure"),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Phase 2: Content Hub (April \u2013 May)")] }),
        bullet("Launch a blog / knowledge base on growdirect.io with the content calendar from Section 4"),
        bullet("Every article targets a keyword from the Square Community threads"),
        bullet("Include a \u201CJoin the conversation\u201D CTA pointing to a simple email list or waitlist"),
        bullet("WORM handles SEO. Will handles copy. Art handles design."),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Phase 3: Community Forum (Post-Marketplace Approval)")] }),
        bullet("Once Canary is on the Square Marketplace, launch a self-hosted Discourse forum at community.growdirect.io"),
        bullet("Discourse recommended: open source, SEO-native, no per-user fees, full control"),
        bullet("Seed it with the top 20 FAQ threads from the Square Community (rewritten, not copied)"),
        bullet("Invite early Canary users to join. Offer \u201CFounder Member\u201D status to first 100 merchants"),
        bullet("Estimated cost: $50\u201380/mo (DigitalOcean or similar) + WORM\u2019s time for setup and moderation"),
        spacer(),

        new Paragraph({
          spacing: { after: 120 },
          children: [
            boldRun("Why Discourse over Circle: "),
            bodyRun("Discourse threads are individual pages that Google indexes natively. Circle content is walled. For a company selling to merchants who are already searching Google for LP help, Discourse\u2019s SEO advantage is the deciding factor. At $50\u201380/mo vs. $299/mo for Circle at scale, the economics also favor Discourse."),
          ]
        }),
      ],
    },

    // ─── PAGE 5: CONTENT CALENDAR ───
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: [
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("4. Content Calendar \u2014 12-Week Sprint")] }),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("Each piece maps to a Square Community pain point, a Chirp rule, and a target keyword. Will writes. WORM optimizes for SEO. Art provides visual assets.")]
        }),

        multiColTable(
          ["Week", "Content Piece", "Target Keyword", "Chirp / Feature Map", "Forum Source"],
          [
            ["1 (Mar 17)", "5 Signs Your Employees Are Stealing From Your Cash Drawer", "employee theft POS detection", "C-004 + Cash drawer anomaly", "$0 transaction thread"],
            ["2 (Mar 24)", "Why Square\u2019s Activity Log Isn\u2019t Enough to Catch Refund Fraud", "Square refund fraud detection", "C-001 Rapid Refund", "Cash refund report thread"],
            ["3 (Mar 31)", "The Small Retailer\u2019s Guide to Loss Prevention (No Cameras Required)", "loss prevention small business", "Full Chirp engine overview", "Inventory shrinkage thread"],
            ["4 (Apr 7)", "How to Track Inventory Shrinkage When Square Won\u2019t", "Square inventory shrinkage report", "Fox case + analytics", "No shrinkage report thread"],
            ["5 (Apr 14)", "Why You\u2019re Losing 95% of Your Chargebacks (And What to Do)", "Square chargeback protection", "TSP receipt verification", "Chargeback thread"],
            ["6 (Apr 21)", "After-Hours Transactions: The Red Flag You\u2019re Ignoring", "POS after hours transaction alert", "C-004 timestamp check", "Cash drawer exploit thread"],
            ["7 (Apr 28)", "What $112B in Retail Shrink Means for Your Shop", "retail shrink 2025 small business", "Industry context piece", "NRF data"],
            ["8 (May 5)", "The AI Loss Prevention Stack: What Enterprise Has That You Don\u2019t (Yet)", "AI loss prevention software SMB", "Canary positioning", "Spot AI / Appriss comparison"],
            ["9 (May 12)", "Refund Rate Red Flags: When 5% Becomes a Pattern", "excessive refund rate employee", "C-002 window aggregation", "Refund tracking threads"],
            ["10 (May 19)", "Your Receipt Is Your Proof: Why Transaction Verification Matters", ".jeffe + TSP intro", "TSP + .jeffe namespace", "Chargeback + proof threads"],
            ["11 (May 26)", "How to Prepare for a Loss Prevention Audit (Even If You\u2019re Tiny)", "loss prevention audit small business", "Fox case export + analytics", "General LP awareness"],
            ["12 (Jun 2)", "The Square Marketplace Gap Nobody Is Filling", "Square Marketplace loss prevention app", "Canary marketplace positioning", "All threads + competitive data"],
          ],
          [1000, 2200, 2000, 2000, 2160]
        ),
      ],
    },

    // ─── PAGE 6: PRIORITY DELIVERABLES ───
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: [
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("5. Priority Deliverables \u2014 Three Outputs, No Excuses")] }),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("Before the content calendar starts, before the forum engagement begins, three concrete deliverables must ship. These are the foundation everything else builds on. Nothing goes out the door without these.")]
        }),

        // ─── DELIVERABLE 1: ONE-PAGER ───
        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("5.1 Deliverable 1: The Canary One-Pager")] }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            boldRun("Owner: "),
            bodyRun("Will (write) + Art (design)"),
          ]
        }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            boldRun("Deadline: "),
            bodyRun("March 21, 2026 (Friday)"),
          ]
        }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            boldRun("Format: "),
            bodyRun("Single-page PDF, print-ready, both digital and physical distribution"),
          ]
        }),
        spacer(60),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("Will\u2019s B-072 messaging framework is 400 lines of internal strategy. Nobody outside GrowDirect can use it. This deliverable distills it into something you can hand to a merchant at a Small Business Expo, paste into a Square Community reply, attach to a cold email, or leave on a counter at RILA.")]
        }),
        new Paragraph({ spacing: { after: 60 }, children: [boldRun("Required Sections (in this order):")] }),
        actionItem("THE PAIN: \u201CYou\u2019re losing money and you can\u2019t see where.\u201D Two sentences max. Use the exact language merchants use on Square Community forums (\u201Ccash drawer discrepancy,\u201D \u201Cno way to track theft,\u201D \u201CI\u2019m constantly astounded by Square\u2019s limitations\u201D)."),
        actionItem("THE FIX: \u201CCanary watches your Square transactions and alerts you when something doesn\u2019t add up.\u201D Three bullet points: refund pattern detection, after-hours transaction alerts, employee risk scoring. No jargon. No \u201CAI-powered.\u201D Just what it does."),
        actionItem("THE PROOF: \u201CWorks with Square. No cameras. No hardware. $29/month.\u201D Show a single screenshot of the Chirp alert dashboard from the sandbox (the Suspicious Steve rapid refund scenario). One image, real data, instant credibility."),
        actionItem("THE CTA: \u201CSee it live\u201D \u2192 URL to sandbox demo. \u201CJoin the waitlist\u201D \u2192 email signup. Both options, no dead ends."),
        spacer(),
        new Paragraph({
          spacing: { after: 120 },
          children: [
            boldRun("Why this matters: "),
            bodyRun("Every conference, every forum reply, every email, every investor conversation needs a leave-behind. Right now GrowDirect has none. This is the single most important marketing asset the company doesn\u2019t have."),
          ]
        }),

        // ─── DELIVERABLE 2: LANDING PAGE ───
        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("5.2 Deliverable 2: Live Landing Page on growdirect.io")] }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            boldRun("Owner: "),
            bodyRun("WORM (build + deploy) + Art (design) + Will (copy)"),
          ]
        }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            boldRun("Deadline: "),
            bodyRun("March 28, 2026 (one week after one-pager)"),
          ]
        }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            boldRun("Format: "),
            bodyRun("Single responsive landing page at growdirect.io, mobile-first"),
          ]
        }),
        spacer(60),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("growdirect.io is stale. WORM\u2019s own HANDOFF says so. Before any content calendar matters, before any SEO strategy kicks in, the front door needs to work. Every forum reply, every conference card, every email needs somewhere to send people. Right now there\u2019s nowhere to go.")]
        }),
        new Paragraph({ spacing: { after: 60 }, children: [boldRun("Required Sections (top to bottom):")] }),
        actionItem("HERO: Headline from Will\u2019s one-pager pain statement + subheadline describing the fix. One CTA button: \u201CJoin the Waitlist.\u201D"),
        actionItem("THREE BENEFIT BLOCKS: (1) Detects refund fraud patterns your activity log can\u2019t catch. (2) Alerts you to after-hours and anomalous transactions in real time. (3) Scores employee risk so you know where to look. Each block gets an icon and two sentences. No more."),
        actionItem("SOCIAL PROOF SECTION: Pull 3\u20134 anonymized merchant quotes directly from Square Community forum threads. Real pain, real language. Attribute as \u201CSquare merchant, community forum.\u201D"),
        actionItem("HOW IT WORKS: Three-step visual. (1) Connect your Square account. (2) Canary analyzes your transactions. (3) Get alerts when something\u2019s off. Include a screenshot from the sandbox dashboard."),
        actionItem("WAITLIST FORM: Email capture. Simple. \u201CBe first to know when Canary launches on the Square Marketplace.\u201D"),
        actionItem("FOOTER: GrowDirect Inc. branding. Links to future blog (placeholder OK). No dead links."),
        spacer(),
        new Paragraph({
          spacing: { after: 120 },
          children: [
            boldRun("Blocker: "),
            bodyRun("B-038 \u2014 Jeffe needs to pick the primary domain from the 7 on Cloudflare. WORM cannot deploy until this decision drops. If growdirect.io is the choice, WORM can start building now on that assumption and redirect later if needed. ALX recommends: build on growdirect.io, redirect canaryapp.io or whatever Jeffe picks later."),
          ]
        }),

        // ─── DELIVERABLE 3: EXPLAINER VIDEO ───
        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("5.3 Deliverable 3: Two-Minute Explainer Video")] }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            boldRun("Owner: "),
            bodyRun("Will (script) + WORM (screen capture) + Art (edit + polish)"),
          ]
        }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            boldRun("Deadline: "),
            bodyRun("April 5, 2026 (before RILA conference April 19)"),
          ]
        }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            boldRun("Format: "),
            bodyRun("2-minute MP4, 1080p, voiceover + screen recording of live sandbox demo"),
          ]
        }),
        spacer(60),
        new Paragraph({
          spacing: { after: 120 },
          children: [bodyRun("The sandbox demo is real and complete. The app has 5 working pages, pre-seeded alert data from a realistic \u201CSaturday at Torrance Farmers Market\u201D scenario, a working Owl AI chat, Fox investigation cases, and a full operations console. This is not a prototype \u2014 it\u2019s a functioning product that needs a human voice explaining what it does. A working demo with voiceover is worth more than any amount of blog content at this stage.")]
        }),
        new Paragraph({ spacing: { after: 60 }, children: [boldRun("Script Structure (Will writes, 120 seconds max):")] }),
        actionItem("0\u201315s \u2014 THE HOOK: \u201CYou\u2019re losing money from your Square register and you can\u2019t see where. Canary can.\u201D Show the login page, then the dashboard with alerts."),
        actionItem("15\u201340s \u2014 THE PAIN: Quick montage of Square Community forum posts (anonymized screenshots). \u201CThousands of Square merchants are asking for help with employee theft, refund fraud, and cash drawer security. Square\u2019s answer? Check your activity log.\u201D"),
        actionItem("40\u201375s \u2014 THE PRODUCT: Walk through the Chirp alert tab showing the Suspicious Steve scenario. Click into an alert. Show the severity, the rule, the employee, the source transaction. Click into Owl and ask \u201CShow me Steve\u2019s refunds this week.\u201D Show the response."),
        actionItem("75\u201395s \u2014 THE DASHBOARD: Show the health score, risk employees, risk locations. \u201CCanary scores your employees and locations by risk level so you know exactly where to look.\u201D"),
        actionItem("95\u2013115s \u2014 THE CLOSE: \u201CNo cameras. No hardware. Connects to Square in one click. $29 a month.\u201D Show the settings page with the Square integration connected."),
        actionItem("115\u2013120s \u2014 THE CTA: \u201CJoin the waitlist at growdirect.io.\u201D Fade to logo."),
        spacer(),
        new Paragraph({
          spacing: { after: 120 },
          children: [
            boldRun("Production notes: "),
            bodyRun("WORM captures the screen recording from the live sandbox (/oauth/sandbox entry, navigate through all tabs). Art edits, adds transitions, lower thirds, and the GrowDirect brand kit (dark #0d1117, Bitcoin amber #f59e0b, Inter + Space Grotesk). Voiceover can be Jeffe or a professional VO \u2014 Jeffe\u2019s call. The video embeds on the landing page hero section and gets uploaded to YouTube for SEO."),
          ]
        }),

        // ─── DELIVERY TIMELINE ───
        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("5.4 Delivery Timeline")] }),
        multiColTable(
          ["Deliverable", "Owner", "Draft Due", "Final Due", "Dependency"],
          [
            ["Canary One-Pager (PDF)", "Will + Art", "Mar 19", "Mar 21", "Sandbox screenshot from Jeremy"],
            ["Landing Page (growdirect.io)", "WORM + Art + Will", "Mar 25", "Mar 28", "One-pager copy + B-038 domain decision"],
            ["Explainer Video (2 min)", "Will + WORM + Art", "Mar 30 (script)", "Apr 5", "Landing page live + sandbox screen capture"],
          ],
          [2000, 1600, 1200, 1200, 3360]
        ),
        spacer(),
        new Paragraph({
          spacing: { after: 120 },
          children: [
            boldRun("The stack: "),
            bodyRun("One-pager feeds the landing page copy. Landing page hosts the video. Video drives the waitlist. Waitlist proves demand for the Marketplace submission. Everything chains. Nothing ships in isolation."),
          ]
        }),
      ],
    },

    // ─── PAGE 7: ASSIGNMENTS ───
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: [
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("6. Agent Assignments")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("6.1 Will \u2014 Lead Generation")] }),
        new Paragraph({
          spacing: { after: 120 },
          children: [
            boldRun("Status Check: "),
            bodyRun("Will\u2019s last output was March 1 (B-072 Lead Gen Messaging). HANDOFF assigned him to update lead gen with RaaS framing and share B-072 with Jess, Worm, and Art. That was March 2. It\u2019s March 16. No evidence of handoff. Will needs to catch up and pivot to this exposure sprint."),
          ]
        }),

        new Paragraph({ spacing: { after: 60 }, children: [boldRun("Immediate Actions (by March 23):")] }),
        actionItem("Read all 6 forum threads listed in Section 1.2. Extract merchant language, pain descriptors, and feature requests."),
        actionItem("Write Week 1 and Week 2 content pieces from the calendar (Section 4)."),
        actionItem("Share B-072 Lead Gen deliverable with Jess, WORM, and Art (overdue from March 2)."),
        actionItem("Register for the nearest Small Business Expo and propose attendance to Jeffe."),
        spacer(),

        new Paragraph({ spacing: { after: 60 }, children: [boldRun("Ongoing (weekly):")] }),
        bullet("Produce one content piece per week per the calendar"),
        bullet("Monitor Square Community forums for new LP-related threads (minimum 1x/week scan)"),
        bullet("Coordinate with WORM on keyword targeting before writing each piece"),
        bullet("Feed anonymized merchant quotes to Art for visual content"),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("6.2 WORM \u2014 Local SEO & Digital Presence")] }),
        new Paragraph({
          spacing: { after: 120 },
          children: [
            boldRun("Status Check: "),
            bodyRun("WORM\u2019s last handoff was March 2: hold DNS config until Jeremy confirms propagation, update growdirect.io stale content, monitor CRM inbox weekly. B-038 (7 domains on Cloudflare) is still waiting on Jeffe to select a primary domain. growdirect.io content is stale. WORM needs a kick."),
          ]
        }),

        new Paragraph({ spacing: { after: 60 }, children: [boldRun("Immediate Actions (by March 23):")] }),
        actionItem("Create a GrowDirect account on community.squareup.com. Begin engaging helpfully in LP-related threads (no sales pitches)."),
        actionItem("Audit growdirect.io for stale content. Propose update plan to ALX."),
        actionItem("Set up Google Business Profile for GrowDirect if not already done."),
        actionItem("Build keyword target list from the 12-week content calendar. Prioritize by search volume."),
        spacer(),

        new Paragraph({ spacing: { after: 60 }, children: [boldRun("Ongoing (weekly):")] }),
        bullet("SEO-optimize each content piece before publication"),
        bullet("Monitor Square Community events page (community.squareup.com/Events) for new webinars or partnership announcements"),
        bullet("Track keyword rankings for all 12 target terms"),
        bullet("Monitor CRM inbox (existing directive \u2014 confirm cadence with ALX)"),
        bullet("Prepare Discourse forum deployment plan for Phase 3 (post-Marketplace approval)"),
        spacer(),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("6.3 Supporting Agents")] }),
        multiColTable(
          ["Agent", "Role in This Sprint", "Deliverables"],
          [
            ["Art", "Visual assets for content pieces + landing page design", "Hero images, infographics, brand-consistent blog templates"],
            ["Jess", "Investor narrative alignment \u2014 ensure exposure content matches fundraising story", "Review Will\u2019s content for message consistency with investor materials"],
            ["Eva", "Square Marketplace E2 certification \u2014 the ultimate exposure play", "Keep R-002 on critical path. Target submission by April."],
            ["Jeremy", "Technical validation of Chirp rule descriptions in content", "Review each content piece for technical accuracy before publication"],
          ],
          [1200, 4000, 4160]
        ),
      ],
    },

    // ─── PAGE 8: SUCCESS METRICS & SIGN-OFF ───
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: [
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("7. Success Metrics")] }),
        multiColTable(
          ["Metric", "Target", "Measured By", "Timeframe"],
          [
            ["Canary One-Pager shipped", "Final PDF, print-ready", "Will + Art", "March 21"],
            ["Landing page live", "growdirect.io updated, waitlist form active", "WORM + Art", "March 28"],
            ["Explainer video published", "2-min MP4 on landing page + YouTube", "Will + WORM + Art", "April 5"],
            ["Content pieces published", "12 (one/week)", "Will + ALX", "12 weeks"],
            ["Square Community engagements", "2+ helpful replies/week", "WORM", "Ongoing"],
            ["Keyword rankings (top 20)", "6 of 12 target keywords", "WORM", "By Week 8"],
            ["Email list / waitlist signups", "100 merchants", "Will + WORM", "By Week 12"],
            ["Conference attendance", "RILA + 1 Small Business Expo minimum", "Will + Jeffe", "By June"],
            ["Square Marketplace E2 submission", "Submitted", "Eva + Syd", "By April"],
            ["Discourse forum live", "Deployed at community.growdirect.io", "WORM + Jeremy", "Post-Marketplace approval"],
          ],
          [2800, 2200, 1800, 2560]
        ),
        spacer(300),

        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("8. Blockers & Dependencies")] }),
        multiColTable(
          ["Blocker", "Impact", "Owner", "Resolution Path"],
          [
            ["B-038: Primary domain not selected", "WORM can\u2019t configure DNS or launch content hub", "Jeffe", "Pick primary domain from the 7 on Cloudflare. This week."],
            ["growdirect.io stale content", "Any traffic driven by content calendar lands on a stale site", "WORM", "Audit + update plan by March 23."],
            ["B-072 handoffs not completed", "Will\u2019s lead gen work is siloed, not shared with Jess/Art/WORM", "Will", "Share B-072 deliverable this week."],
            ["R-002: E2 Marketplace cert", "Can\u2019t list on Square Marketplace without certification", "Eva + Syd", "Keep on critical path. Target April submission."],
            ["Sandbox screenshot for one-pager", "One-pager needs a real Chirp alert screenshot", "Jeremy", "Export 1080p screenshot of alert dashboard with Suspicious Steve data by March 19."],
            ["Square Solutions Partner waitlist", "First-mover as only LP specialist in directory", "Jeffe", "Submit GrowDirect info at squareup.com/us/en/partnerships/solutions-partner-program this week."],
          ],
          [2800, 2400, 1200, 2960]
        ),
        spacer(300),

        new Paragraph({
          border: { top: { style: BorderStyle.SINGLE, size: 6, color: "F59E0B", space: 8 } },
          spacing: { before: 200, after: 200 },
          children: [
            boldRun("SIGN-OFF: ", { size: 24, color: "1A1A2E" }),
            bodyRun("This work order is effective immediately. Will and WORM: read this document, confirm receipt with ALX, and begin Phase 1 actions by March 23, 2026. ALX will track progress against the content calendar weekly.", { size: 22 }),
          ]
        }),
        spacer(200),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            bodyRun("Issued by: ", { color: "888888" }),
            boldRun("ALX \u2014 Chief of Staff, GrowDirect Inc."),
          ]
        }),
        new Paragraph({
          spacing: { after: 60 },
          children: [
            bodyRun("Date: ", { color: "888888" }),
            boldRun("March 16, 2026"),
          ]
        }),
        new Paragraph({
          children: [
            bodyRun("Classification: ", { color: "888888" }),
            boldRun("CONFIDENTIAL \u2014 INTERNAL USE ONLY", { color: "CC0000" }),
          ]
        }),
      ],
    },
  ],
});

// ─── GENERATE ───
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("/sessions/peaceful-keen-maxwell/mnt/GrowDirect/WORKORDER_Will_Worm_Exposure_Sprint.docx", buffer);
  console.log("Work order generated successfully.");
});
