import { useState } from "react";

const LAYERS = [
  {
    id: "parcel",
    name: "PARCEL",
    label: "Foundation",
    color: "#000",
    bg: "#f7f7f7",
    records: "~180,000",
    sources: ["LA County Assessor", "Cove Bridge"],
    fields: ["APN", "Address", "Lot Size", "Year Built", "SqFt", "Zoning", "Owner", "Assessed Value", "School District"],
    status: "free",
    desc: "Every parcel in the South Bay. The spine everything else attaches to. Downloaded from LA County Open Data, enriched with Cove community links."
  },
  {
    id: "transactions",
    name: "TRANSACTIONS",
    label: "What Happened",
    color: "#000",
    bg: "#fff",
    records: "~50,000+",
    sources: ["CRMLS RESO API", "County Recorder", "ATTOM"],
    fields: ["MLS#", "List Price", "Close Price", "DOM", "Status", "List Agent", "Buyer Agent", "Close Date", "Price/SqFt"],
    status: "crmls-access",
    desc: "Every listing event — active, pending, closed, expired. CRMLS is the primary source. County recorder adds grant deeds. ATTOM fills historical gaps."
  },
  {
    id: "agents",
    name: "AGENTS",
    label: "Who's Active",
    color: "#333",
    bg: "#f7f7f7",
    records: "~8,000+",
    sources: ["CRMLS Member", "CA DRE File"],
    fields: ["MLS ID", "DRE#", "Name", "Office", "Brokerage", "Transaction Count", "Volume", "Market Share"],
    status: "free",
    desc: "Every agent who's touched a deal. DRE file is free (daily download). CRMLS Member resource adds MLS ID and office. Derived metrics show market share."
  },
  {
    id: "valuations",
    name: "VALUATIONS",
    label: "What It's Worth",
    color: "#333",
    bg: "#fff",
    records: "~180,000",
    sources: ["ATTOM AVM", "County Assessor", "CRMLS Comps"],
    fields: ["AVM Estimate", "Assessed Value", "Comp Sale Prices", "Price/SqFt", "Equity Estimate"],
    status: "paid-api",
    desc: "Automated valuations for every parcel. County assessed value is free but lags market. ATTOM AVM is the real-time estimate. CRMLS comps validate."
  },
  {
    id: "schools",
    name: "SCHOOLS",
    label: "Decision Driver",
    color: "#666",
    bg: "#f7f7f7",
    records: "~60 schools",
    sources: ["GreatSchools API", "PVPUSD/MBUSD/TUSD", "Angelique"],
    fields: ["Rating", "Test Scores", "Feeder Pattern", "Enrollment", "Boundary", "Parent Experience"],
    status: "free",
    desc: "The #1 factor for relocating families. GreatSchools API is free. Angelique's personal experience annotations are the unique layer no one else has."
  },
  {
    id: "signals",
    name: "SIGNALS",
    label: "Predictive Intel",
    color: "#666",
    bg: "#fff",
    records: "Continuous",
    sources: ["CRMLS", "ATTOM", "LADBS Permits", "SmartZip", "GA4"],
    fields: ["Likely to Sell Score", "Permit Activity", "Ownership Duration", "Price Reductions", "DOM Thresholds", "Web Behavior"],
    status: "mixed",
    desc: "The lead engine. Combines transaction signals (price cuts, expired listings) with predictive scores and behavioral data from OwnPalosVerdes.com."
  }
];

const SEO_TARGETS = [
  { keyword: "best schools Palos Verdes", vol: 720, diff: 45, auth: 92, cat: "school", status: "published" },
  { keyword: "corporate relocation South Bay LA", vol: 320, diff: 32, auth: 78, cat: "relocation", status: "published" },
  { keyword: "PVPHS vs PVHS", vol: 260, diff: 18, auth: 95, cat: "school", status: "drafted" },
  { keyword: "Palos Verdes vs Manhattan Beach families", vol: 210, diff: 28, auth: 85, cat: "relocation", status: "published" },
  { keyword: "moving to Palos Verdes with kids", vol: 170, diff: 22, auth: 88, cat: "relocation", status: "planned" },
  { keyword: "Lunada Bay homes for sale", vol: 150, diff: 55, auth: 90, cat: "neighborhood", status: "published" },
  { keyword: "PVE elementary school rankings", vol: 140, diff: 20, auth: 95, cat: "school", status: "drafted" },
  { keyword: "RPV real estate agent", vol: 130, diff: 60, auth: 70, cat: "neighborhood", status: "planned" },
  { keyword: "is Rancho Palos Verdes safe families", vol: 110, diff: 15, auth: 85, cat: "relocation", status: "planned" },
  { keyword: "Lunada Bay neighborhood review", vol: 90, diff: 12, auth: 95, cat: "neighborhood", status: "drafted" },
  { keyword: "Portuguese Bend horse property", vol: 60, diff: 8, auth: 65, cat: "neighborhood", status: "planned" },
  { keyword: "Hollywood Riviera Torrance guide", vol: 80, diff: 14, auth: 55, cat: "neighborhood", status: "planned" },
];

const PIPELINE_STAGES = [
  { stage: "Mine", icon: "⛏", desc: "CRMLS transactions → power zones, price bands, agent market share", color: "#000" },
  { stage: "Map", icon: "🗺", desc: "Cross-reference authority with SEO keywords + search volume", color: "#222" },
  { stage: "Write", icon: "✍", desc: "Content briefs → blog posts, guides, market reports in Angelique's voice", color: "#444" },
  { stage: "Rank", icon: "📈", desc: "Schema markup, E-E-A-T signals, internal linking, distribution", color: "#666" },
  { stage: "Convert", icon: "🎯", desc: "Google → OwnPalosVerdes → retarget → lead capture → client", color: "#888" },
];

const STATUS_COLORS = { free: "#2d8a5e", "crmls-access": "#b8860b", "paid-api": "#dc2626", mixed: "#7c3aed" };
const STATUS_LABELS = { free: "Free / Available Now", "crmls-access": "Requires CRMLS Access", "paid-api": "Paid API", mixed: "Mixed Sources" };
const CAT_COLORS = { school: "#2563eb", relocation: "#7c3aed", neighborhood: "#2d8a5e" };
const STAT_COLORS = { published: "#2d8a5e", drafted: "#b8860b", planned: "#999" };

export default function AngelDataPipeline() {
  const [activeLayer, setActiveLayer] = useState(null);
  const [view, setView] = useState("layers");

  return (
    <div style={{ fontFamily: "'DM Sans', system-ui, sans-serif", background: "#fff", minHeight: "100vh", color: "#1a1a1a" }}>
      {/* Header */}
      <div style={{ background: "#000", color: "#fff", padding: "2.5rem 2rem 2rem" }}>
        <div style={{ maxWidth: 960, margin: "0 auto" }}>
          <div style={{ fontSize: "0.6rem", letterSpacing: "0.2em", textTransform: "uppercase", color: "#999", marginBottom: "0.75rem" }}>
            Angel · GrowDirect Platform
          </div>
          <h1 style={{ fontFamily: "Georgia, serif", fontSize: "2rem", fontWeight: 400, marginBottom: "0.5rem" }}>
            South Bay Proprietary Dataset
          </h1>
          <p style={{ color: "#999", fontSize: "0.88rem", maxWidth: 600, lineHeight: 1.7 }}>
            180,000 parcels. Every transaction. Every agent. Every school. Mined for SEO authority and real-world marketing intelligence.
          </p>
        </div>
      </div>

      {/* Nav */}
      <div style={{ borderBottom: "1px solid #e0e0e0", background: "#f7f7f7" }}>
        <div style={{ maxWidth: 960, margin: "0 auto", display: "flex", gap: "1.5rem", padding: "0 2rem" }}>
          {[["layers", "Data Layers"], ["pipeline", "Mine → Convert Pipeline"], ["seo", "SEO Target Map"]].map(([key, label]) => (
            <button key={key} onClick={() => setView(key)}
              style={{
                padding: "0.75rem 0", background: "none", border: "none", cursor: "pointer",
                fontSize: "0.78rem", letterSpacing: "0.08em", textTransform: "uppercase", fontWeight: 600,
                color: view === key ? "#000" : "#999",
                borderBottom: view === key ? "2px solid #000" : "2px solid transparent",
              }}>
              {label}
            </button>
          ))}
        </div>
      </div>

      <div style={{ maxWidth: 960, margin: "0 auto", padding: "2rem" }}>

        {/* DATA LAYERS VIEW */}
        {view === "layers" && (
          <div>
            <div style={{ fontSize: "0.65rem", letterSpacing: "0.15em", textTransform: "uppercase", color: "#999", marginBottom: "0.5rem" }}>
              8 Data Layers · APN-Keyed
            </div>
            <h2 style={{ fontFamily: "Georgia, serif", fontSize: "1.4rem", fontWeight: 400, marginBottom: "1.5rem" }}>
              The intelligence stack no one else has assembled
            </h2>

            <div style={{ display: "flex", flexDirection: "column", gap: "2px", background: "#e0e0e0" }}>
              {LAYERS.map((layer) => (
                <div key={layer.id}
                  onClick={() => setActiveLayer(activeLayer === layer.id ? null : layer.id)}
                  style={{ background: layer.bg, padding: "1.25rem 1.5rem", cursor: "pointer", transition: "all 0.2s" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                      <div style={{
                        width: 6, height: 36, background: layer.color, borderRadius: 1
                      }} />
                      <div>
                        <div style={{ fontSize: "0.6rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "#999", marginBottom: "0.15rem" }}>
                          {layer.label}
                        </div>
                        <div style={{ fontFamily: "Georgia, serif", fontSize: "1.1rem", color: "#000" }}>
                          {layer.name}
                        </div>
                      </div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                      <span style={{ fontSize: "0.78rem", color: "#666" }}>{layer.records} records</span>
                      <span style={{
                        fontSize: "0.6rem", letterSpacing: "0.06em", textTransform: "uppercase", fontWeight: 600,
                        padding: "3px 8px", background: STATUS_COLORS[layer.status] + "18", color: STATUS_COLORS[layer.status],
                      }}>
                        {STATUS_LABELS[layer.status]}
                      </span>
                      <span style={{ color: "#999", fontSize: "0.9rem" }}>{activeLayer === layer.id ? "−" : "+"}</span>
                    </div>
                  </div>

                  {activeLayer === layer.id && (
                    <div style={{ marginTop: "1rem", paddingLeft: "1.5rem", borderLeft: "2px solid #e0e0e0", marginLeft: "3px" }}>
                      <p style={{ fontSize: "0.85rem", color: "#666", lineHeight: 1.7, marginBottom: "0.75rem" }}>{layer.desc}</p>
                      <div style={{ display: "flex", gap: "2rem", marginBottom: "0.75rem" }}>
                        <div>
                          <div style={{ fontSize: "0.58rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "#999", marginBottom: "0.25rem" }}>Sources</div>
                          <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                            {layer.sources.map(s => (
                              <span key={s} style={{ fontSize: "0.72rem", padding: "2px 8px", background: "#f2f2f2", color: "#333" }}>{s}</span>
                            ))}
                          </div>
                        </div>
                        <div>
                          <div style={{ fontSize: "0.58rem", letterSpacing: "0.1em", textTransform: "uppercase", color: "#999", marginBottom: "0.25rem" }}>Key Fields</div>
                          <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                            {layer.fields.map(f => (
                              <span key={f} style={{ fontSize: "0.72rem", padding: "2px 8px", background: "#000", color: "#fff" }}>{f}</span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* PIPELINE VIEW */}
        {view === "pipeline" && (
          <div>
            <div style={{ fontSize: "0.65rem", letterSpacing: "0.15em", textTransform: "uppercase", color: "#999", marginBottom: "0.5rem" }}>
              5 Stages
            </div>
            <h2 style={{ fontFamily: "Georgia, serif", fontSize: "1.4rem", fontWeight: 400, marginBottom: "1.5rem" }}>
              Transaction Data becomes Content Authority becomes Clients
            </h2>

            <div style={{ display: "flex", gap: "2px", background: "#e0e0e0", marginBottom: "2rem" }}>
              {PIPELINE_STAGES.map((s, i) => (
                <div key={s.stage} style={{
                  flex: 1, background: s.color, padding: "1.5rem 1rem", color: "#fff", position: "relative",
                  textAlign: "center"
                }}>
                  <div style={{ fontSize: "1.5rem", marginBottom: "0.5rem" }}>{s.icon}</div>
                  <div style={{ fontSize: "0.6rem", letterSpacing: "0.12em", textTransform: "uppercase", marginBottom: "0.25rem", color: "rgba(255,255,255,0.6)" }}>
                    Stage {i + 1}
                  </div>
                  <div style={{ fontFamily: "Georgia, serif", fontSize: "1rem", marginBottom: "0.5rem" }}>{s.stage}</div>
                  <div style={{ fontSize: "0.72rem", color: "rgba(255,255,255,0.7)", lineHeight: 1.5 }}>{s.desc}</div>
                  {i < PIPELINE_STAGES.length - 1 && (
                    <div style={{ position: "absolute", right: -8, top: "50%", transform: "translateY(-50%)", color: "#e0e0e0", fontSize: "1.2rem", zIndex: 2 }}>
                      {"\u2192"}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Example Flow */}
            <div style={{ background: "#f7f7f7", padding: "1.5rem", marginBottom: "1.5rem" }}>
              <div style={{ fontSize: "0.6rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "#999", marginBottom: "0.5rem" }}>
                Example: Lunada Bay Content Pipeline
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                {[
                  ["Mine", "CRMLS query: 12 closed deals in Lunada Bay (90274), $38M total volume, avg DOM 28 days, 8 listing-side + 4 buy-side"],
                  ["Map", "Target keyword: \"Lunada Bay homes for sale\" (150/mo, difficulty 55) — authority score 90 (12 deals = top agent in zone)"],
                  ["Write", "Content brief: \"The Insider's Guide to Lunada Bay\" — 1,200 words, leads with \"I've helped 12 families find their home here\""],
                  ["Rank", "Published to OwnPalosVerdes.com/lunada-bay with RealEstateAgent schema, FAQ schema, internal links to school guide"],
                  ["Convert", "Mom in Austin reads guide at 11pm → retargeted on Instagram → downloads relocation guide → email sequence → Angelique calls"],
                ].map(([stage, detail]) => (
                  <div key={stage} style={{ display: "flex", gap: "1rem", alignItems: "flex-start" }}>
                    <span style={{
                      fontSize: "0.6rem", letterSpacing: "0.08em", textTransform: "uppercase", fontWeight: 600,
                      padding: "3px 8px", background: "#000", color: "#fff", minWidth: 55, textAlign: "center"
                    }}>{stage}</span>
                    <span style={{ fontSize: "0.82rem", color: "#333", lineHeight: 1.6 }}>{detail}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Real-World Marketing Tie-ins */}
            <h3 style={{ fontFamily: "Georgia, serif", fontSize: "1.15rem", fontWeight: 400, marginBottom: "1rem" }}>Real-World Marketing Powered by Data</h3>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "2px", background: "#e0e0e0" }}>
              {[
                { channel: "Farming Mailers", desc: "Quarterly postcards to power zones with her actual stats: \"12 homes sold in your neighborhood, avg 28 DOM\"", data: "Neighborhood stats table" },
                { channel: "Open Houses", desc: "Hold opens in neighborhoods with highest deal count — \"I sold three homes on this street\" is the ultimate credibility", data: "Listings table filtered by zone" },
                { channel: "Sphere Nurture", desc: "Annual equity updates to past clients: \"You bought at $1.8M in 2020 — current AVM is $2.3M\"", data: "Owners + Valuations tables" },
                { channel: "Listing Pitches", desc: "\"My Private Exclusive listings close 3.1% higher and sell 12 days faster than direct-to-MLS\" — backed by her actual data", data: "Listings table: PE vs MLS" },
              ].map(item => (
                <div key={item.channel} style={{ background: "#fff", padding: "1.25rem" }}>
                  <div style={{ fontFamily: "Georgia, serif", fontSize: "0.95rem", marginBottom: "0.35rem" }}>{item.channel}</div>
                  <p style={{ fontSize: "0.82rem", color: "#666", lineHeight: 1.6, marginBottom: "0.5rem" }}>{item.desc}</p>
                  <span style={{ fontSize: "0.65rem", padding: "2px 6px", background: "#f2f2f2", color: "#666" }}>
                    Data: {item.data}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* SEO TARGETS VIEW */}
        {view === "seo" && (
          <div>
            <div style={{ fontSize: "0.65rem", letterSpacing: "0.15em", textTransform: "uppercase", color: "#999", marginBottom: "0.5rem" }}>
              {SEO_TARGETS.length} Keywords Mapped
            </div>
            <h2 style={{ fontFamily: "Georgia, serif", fontSize: "1.4rem", fontWeight: 400, marginBottom: "0.5rem" }}>
              SEO targets ranked by transaction authority
            </h2>
            <p style={{ fontSize: "0.85rem", color: "#666", lineHeight: 1.7, marginBottom: "1.5rem" }}>
              Every keyword is scored against her actual sales data. Higher authority = she has real deals backing her expertise. That's what Google's E-E-A-T rewards.
            </p>

            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.82rem" }}>
              <thead>
                <tr style={{ background: "#000", color: "#fff" }}>
                  <th style={{ padding: "0.6rem 0.75rem", textAlign: "left", fontWeight: 500, fontSize: "0.7rem", letterSpacing: "0.05em", textTransform: "uppercase" }}>Keyword</th>
                  <th style={{ padding: "0.6rem 0.75rem", textAlign: "center", fontWeight: 500, fontSize: "0.7rem", letterSpacing: "0.05em", textTransform: "uppercase" }}>Vol/mo</th>
                  <th style={{ padding: "0.6rem 0.75rem", textAlign: "center", fontWeight: 500, fontSize: "0.7rem", letterSpacing: "0.05em", textTransform: "uppercase" }}>Difficulty</th>
                  <th style={{ padding: "0.6rem 0.75rem", textAlign: "center", fontWeight: 500, fontSize: "0.7rem", letterSpacing: "0.05em", textTransform: "uppercase" }}>Authority</th>
                  <th style={{ padding: "0.6rem 0.75rem", textAlign: "center", fontWeight: 500, fontSize: "0.7rem", letterSpacing: "0.05em", textTransform: "uppercase" }}>Priority</th>
                  <th style={{ padding: "0.6rem 0.75rem", textAlign: "center", fontWeight: 500, fontSize: "0.7rem", letterSpacing: "0.05em", textTransform: "uppercase" }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {SEO_TARGETS
                  .sort((a, b) => {
                    const scoreA = (a.auth * 0.3) + (a.vol / 10 * 0.25) + ((100 - a.diff) * 0.25) + (a.vol / 10 * 0.2);
                    const scoreB = (b.auth * 0.3) + (b.vol / 10 * 0.25) + ((100 - b.diff) * 0.25) + (b.vol / 10 * 0.2);
                    return scoreB - scoreA;
                  })
                  .map((t, i) => {
                    const priority = ((t.auth * 0.3) + (t.vol / 10 * 0.25) + ((100 - t.diff) * 0.25) + (t.vol / 10 * 0.2)).toFixed(0);
                    return (
                      <tr key={t.keyword} style={{ background: i % 2 === 0 ? "#fff" : "#f7f7f7" }}>
                        <td style={{ padding: "0.6rem 0.75rem", borderBottom: "1px solid #f2f2f2" }}>
                          <span style={{ color: "#1a1a1a" }}>{t.keyword}</span>
                          <span style={{
                            marginLeft: "0.5rem", fontSize: "0.6rem", padding: "1px 5px",
                            background: CAT_COLORS[t.cat] + "15", color: CAT_COLORS[t.cat],
                            textTransform: "uppercase", letterSpacing: "0.05em", fontWeight: 600
                          }}>{t.cat}</span>
                        </td>
                        <td style={{ padding: "0.6rem 0.75rem", textAlign: "center", borderBottom: "1px solid #f2f2f2", color: "#666" }}>{t.vol}</td>
                        <td style={{ padding: "0.6rem 0.75rem", textAlign: "center", borderBottom: "1px solid #f2f2f2" }}>
                          <div style={{
                            display: "inline-block", width: 50, height: 6, background: "#f2f2f2", borderRadius: 3, overflow: "hidden"
                          }}>
                            <div style={{ width: `${t.diff}%`, height: "100%", background: t.diff > 50 ? "#dc2626" : t.diff > 30 ? "#b8860b" : "#2d8a5e" }} />
                          </div>
                          <span style={{ fontSize: "0.72rem", color: "#666", marginLeft: "0.35rem" }}>{t.diff}</span>
                        </td>
                        <td style={{ padding: "0.6rem 0.75rem", textAlign: "center", borderBottom: "1px solid #f2f2f2" }}>
                          <div style={{
                            display: "inline-block", width: 50, height: 6, background: "#f2f2f2", borderRadius: 3, overflow: "hidden"
                          }}>
                            <div style={{ width: `${t.auth}%`, height: "100%", background: "#000" }} />
                          </div>
                          <span style={{ fontSize: "0.72rem", color: "#1a1a1a", fontWeight: 600, marginLeft: "0.35rem" }}>{t.auth}</span>
                        </td>
                        <td style={{
                          padding: "0.6rem 0.75rem", textAlign: "center", borderBottom: "1px solid #f2f2f2",
                          fontFamily: "Georgia, serif", fontSize: "1rem", fontWeight: 400, color: "#000"
                        }}>{priority}</td>
                        <td style={{ padding: "0.6rem 0.75rem", textAlign: "center", borderBottom: "1px solid #f2f2f2" }}>
                          <span style={{
                            fontSize: "0.6rem", letterSpacing: "0.06em", textTransform: "uppercase", fontWeight: 600,
                            padding: "3px 8px", color: STAT_COLORS[t.status],
                            background: STAT_COLORS[t.status] + "15"
                          }}>{t.status}</span>
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>

            <div style={{ marginTop: "1.5rem", padding: "1.25rem", background: "#f7f7f7", borderLeft: "3px solid #000" }}>
              <div style={{ fontSize: "0.6rem", letterSpacing: "0.12em", textTransform: "uppercase", color: "#999", marginBottom: "0.35rem" }}>
                How Authority Score Works
              </div>
              <p style={{ fontSize: "0.85rem", color: "#333", lineHeight: 1.7 }}>
                Authority is calculated from Angelique's actual CRMLS transaction history in the geographic zone each keyword targets.
                12 closed deals in Lunada Bay = authority score of 90+. 2 deals in Hollywood Riviera = 55.
                This drives content prioritization: write first where she has the most proof points, then expand into growth zones.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{ textAlign: "center", padding: "2rem", fontSize: "0.7rem", color: "#999", borderTop: "1px solid #f2f2f2" }}>
        Angel · GrowDirect Platform · South Bay Proprietary Dataset Architecture
      </div>
    </div>
  );
}
