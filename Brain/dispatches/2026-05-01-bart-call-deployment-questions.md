---
date: 2026-05-01
type: dispatch
audience: founder
context: bart-call-prep
status: questions-staged
---

# Bart-call deployment questions — RAAS / Counterpoint / RapidPOS

Questions to bring to the next conversation with Bart. These shape the deployment-method architecture for Canary Go (per the agent control plane + historical ingest tickets in [Canary Data Model](https://linear.app/growdirect/project/canary-data-model-84354f7710f6)). Answers determine whether we lean Tier 1 (self-deployed agent), Tier 2 (RapidPOS-published events), or Tier 3 (backup-dump ingest) per merchant.

Internal — do not share. These questions surface positioning and partnership posture; not for a Linear ticket comment.

## 1. Cloud-side infrastructure posture

**Q.** Does RapidPOS operate any cloud middleware that could host a publisher service, or are all your customer installations 100% on-premises Counterpoint with nothing in your control on the cloud side?

**Why it matters.** Determines whether Tier 2 (partner-managed publisher) is viable. If RapidPOS already has a cloud presence per customer (even just for licensing or telemetry), they can host a publisher relatively easily. If they're 100% on-prem, Tier 1 (agent at merchant site) becomes the primary path.

**What we hope to hear.** RapidPOS has *some* cloud middleware — even just per-VAR licensing infrastructure — that we could ride on for event publishing. If not, we plan around Tier 1.

## 2. Customer network posture

**Q.** What's the typical network posture of a RapidPOS customer? Do you grant external API access by default for your installations, or is everything firewalled and accessed only via VPN tunnel?

**Why it matters.** If the Counterpoint API is reachable from outside (with credentials), our cloud-side agent can pull. If it's locked behind a VPN, we either need an agent on-prem (Tier 1) or a tunnel (more work).

**Branch.**
- *External API reachable:* Cloud Run job runs the agent, authenticates over the public internet. Fastest to install.
- *VPN-only:* On-prem Windows-service agent, or Site-to-Site VPN to GCP, or a stargate / tunnel pattern.

## 3. Default data retention on the customer base

**Q.** What's the typical retention shape on your customer base? Do you run any default purge policies as a VAR — "delete records older than N years"? Or do most of your customers just let Counterpoint accumulate forever?

**Why it matters.** Drives backfill sizing. A 10-year-old store with no purge has 10+ years of Documents to ingest — could be tens of millions of transactions. A 25-year-old store could have 100M+. The agent's pagination strategy and the BigQuery storage budget scale accordingly.

**What we hope to hear.** "Most customers never purge — Counterpoint just keeps going." That makes the historical-context-on-day-zero pitch incredibly powerful (we're claiming 10-25 years of context as a Day 0 deliverable).

## 4. Backup format + access

**Q.** What's the standard backup format and cadence at your customer sites? Are SQL Server `.bak` files a normal artifact you can grant us access to, or is that a more unusual ask?

**Why it matters.** Tier 3 (bulk dump ingest) is dramatically faster than Tier 1 (API pagination). For a 10-year-old shop, Tier 1 might take 24-48 hours; Tier 3 might take 2-4 hours. If `.bak` access is a normal customer-grants-on-onboarding artifact, we can promise much faster time-to-context.

## 5. Multi-tenant agent dashboard interest

**Q.** Would RapidPOS want their own view in our agent dashboard for *their* customers — a partner-scoped operational console showing which of their installs are healthy, which are mid-backfill, which are flagging errors?

**Why it matters.** This converts our agent control plane (GRO-729) into a distribution channel for Bart. Multi-tenant dashboard becomes a partner-onboarding incentive: *"sign up to send us your customer data, get an operational console showing all your installs in real time."* Mutual benefit, not extraction.

**What we hope to hear.** Yes, with strong interest. Means RapidPOS has skin in our success — they get visibility, we get reach.

## 6. Counterpoint version + API maturity by customer

**Q.** What versions of Counterpoint are typical across your install base? Are they all on the same major version, or is there a long tail of older deployments?

**Why it matters.** Counterpoint API surface evolves. Older deployments may not have all the endpoints we expect. Our agent might need version-detection logic and graceful degradation for older Counterpoint versions.

## 7. Customer-vs-VAR consent for our access

**Q.** When we onboard a new customer through RapidPOS, who's the consenting party for granting Canary access to the data? Is it the merchant directly? RapidPOS as their VAR? Both?

**Why it matters.** Compliance posture (GDPR / CCPA / contracts) and the operational posture for credentialing the agent. If RapidPOS is the consenting party, our credentials come from them, and we operate under their data processing agreements. If the merchant is the consenting party, we contract directly.

## 8. Pre-existing tooling in the RapidPOS install base

**Q.** Are there any pre-existing tools / agents / sync utilities that already run at your customer sites? Something we could ride on, or that we'd have to interoperate with?

**Why it matters.** Avoid stepping on existing automation, find natural integration points, identify potential conflicts (e.g., another data extractor that's already pulling and would be confused if we joined).

---

## Notes for the call

- These questions land *after* we've established the technical relationship — don't lead with "what's your retention?" Instead, build to it as part of the deployment-architecture conversation.
- Bart is a VAR/distributor first, technical partner second. Frame questions in terms of his customer experience and his economic interest, not our engineering needs.
- The agent dashboard offer (Q5) is the strongest hook — gives him something concrete to point at when justifying the partnership internally.
- If the answers reveal RapidPOS has more cloud infrastructure than expected, we may want to pivot toward Tier 2 (partner publisher) faster than planned.

## Action after the call

Update the [Canary Data Model](https://linear.app/growdirect/project/canary-data-model-84354f7710f6) project with the answers — specifically GRO-727 (adapter contract — sources we're targeting), GRO-728 (Pub/Sub topic — partner credentialing model), and GRO-730 (historical ingest pipeline — sizing assumptions).
