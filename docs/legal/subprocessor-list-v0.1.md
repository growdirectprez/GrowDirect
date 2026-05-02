# Canary Protocol Sub-processor List (v0.1)

**Status:** v0.1 working document — incorporated by reference into [DPA Template v0.1](./dpa-template-v0.1.md) §8.
**Owner:** GrowDirect LLC (Canary Protocol)
**Last reviewed:** 2026-05-02
**Source dispatch:** GRO-693
**Notification commitment:** 30 days' prior written notice for any addition or replacement (DPA §8.2)

---

## 0 · Governing thesis

Canary's sub-processor surface is intentionally narrow. The architectural commitments behind that:

1. **No PII transit through general-purpose AI providers in the merchant data path.** LLM/embedding providers (Anthropic, OpenAI, Ollama-as-a-service) are not sub-processors of merchant Personal Data. Where AI is used inside Canary, it runs against synthetic / sandbox / non-PII data or against ephemeral merchant-scoped agents the Merchant explicitly enables. None of those are listed below.
2. **Card data never crosses the Canary boundary.** Payment processors (Stripe, Square, NCR Voyix, etc.) appear here only when they are sub-processors *of Canary's* operating data — not when Canary is consuming their data. The merchant's POS-to-processor flow is **not** a Canary sub-processor relationship.
3. **The evidence-chain anchor providers** (OrdinalsBot, future Lightning provider) handle hashes and payment receipts, not PII. They are listed for transparency but their data scope is non-personal.

---

## 1 · Active sub-processors (Phase 1 — current)

| # | Sub-processor | Role | Data Categories | Region | Status | Sub-processor DPA |
|---|---|---|---|---|---|---|
| 1 | **Google LLC** (Google Cloud Platform) | Compute (Cloud Run), database (Cloud SQL Postgres), storage (Cloud Storage), event streaming (Pub/Sub), secrets (Secret Manager), CI/CD (Cloud Build), container registry (Artifact Registry), logging (Cloud Audit Logs), KMS | All Merchant Data and Personal Data per DPA §3 | `us-central1` (primary) — see [VERIFY] note below | Active | https://cloud.google.com/terms/data-processing-addendum |
| 2 | **Cloudflare, Inc.** | DNS resolution, edge TLS termination for `*.growdirect.io` and `api.canary.growdirect.io`, DDoS mitigation | DNS query metadata, IP addresses, TLS handshake metadata. **No application payload at rest.** | Global anycast | Active | https://www.cloudflare.com/cloudflare-customer-dpa/ |
| 3 | **GrowDirect LLC personnel and contractors** | Internal operations, support, on-call response | All Merchant Data and Personal Data per access-control matrix | United States | Active (intra-entity, listed for transparency) | N/A — bound by employment/contractor confidentiality (DPA §5.2) |

[VERIFY] — Region `us-central1` is inferred from the Artifact Registry path (`us-central1-docker.pkg.dev`) in the GCP foundation runbook. Cloud SQL and Cloud Run regions need to be confirmed in `Brain/wiki/cards/gcp-foundation-runbook.md` before this is published to merchants. If multi-region is enabled, list all enabled regions.

---

## 2 · Planned sub-processors (Phase 1.E and beyond — disclosed for forward transparency)

These providers are not yet receiving production data. They are listed so merchants understand the forward roadmap. They become "active" only after (i) selection, (ii) DPA execution between Canary and the sub-processor, and (iii) 30-day notice to merchants.

| # | Sub-processor | Role | Data Categories | Region | Phase | Sub-processor DPA |
|---|---|---|---|---|---|---|
| 4 | **OrdinalsBot** (or equivalent Bitcoin inscription service) | Bitcoin L2 hash anchoring (evidence-chain rail per DPA §7.3) | Cryptographic hashes only — no Personal Data | Provider-determined | Phase 1.E (planned) | [VERIFY] — DPA URL pending vendor selection |
| 5 | **Lightning Network provider TBD** (e.g., Voltage, LND-as-a-service, self-hosted LND) | Lightning channel management for L402 OTB settlement | Payment-channel metadata (preimages, satoshi amounts, channel state). **No Personal Data.** | Provider-determined | Phase 2+ (planned per GRO-733) | [VERIFY] — vendor not yet selected |
| 6 | **QSA / SOC 2 auditor TBD** | PCI Service Provider attestation; SOC 2 Type II audit | Documentary access during audit periods only. **No production data access.** | United States (likely) | Phase 4 (per GRO-695) | [VERIFY] — vendor not yet selected |

---

## 3 · Excluded — common-but-misconceived sub-processor relationships

This section pre-empts confusion. The following are **not** Canary sub-processors of Merchant Personal Data, despite frequently appearing in similar SaaS DPAs:

| Provider | Why excluded |
|---|---|
| Anthropic, OpenAI, other LLM providers | Canary does not transmit Merchant Personal Data to general-purpose LLM providers in the production merchant data path. AI features that run against merchant data (e.g., the Q&A agent on synthetic / sandbox data, or merchant-explicit agent enablement) are scoped per the order form addendum |
| Square, NCR Voyix, Stripe, other payment processors | When the Merchant uses these for payments, their relationship is **with the Merchant**, not with Canary. Canary receives post-authorization transaction records; we are not in the cardholder-data flow (DPA §7.4) |
| Ollama, Hugging Face, model-hosting services | Embeddings and inference run inside Canary's own compute environment (GCP); model hosts are not external data recipients |
| Slack, Notion, Linear, Obsidian | Internal tooling. Merchant data does not flow into these. They process internal operations data only |

[COUNSEL REVIEW] — Confirm that "internal tooling" exclusion is defensible. Some EU regulators treat ticketing systems (e.g., support tickets that mention a customer name) as creating an indirect processor relationship. If support tickets are likely to contain Merchant PII, Linear/Slack would need to be added.

---

## 4 · Sub-processor change log

| Date | Change | Notice sent to merchants |
|---|---|---|
| 2026-05-02 | Initial list published as v0.1 | N/A — pre-customer |

Future entries will record:
- Date of addition / removal / replacement
- Which sub-processor changed
- Notice sent date and channel
- Effective date of the change (≥ 30 days post-notice)

---

## 5 · How merchants object to a sub-processor

Per DPA §8.3: a Merchant may object to a new sub-processor on reasonable data-protection grounds within 14 days of receiving notice. Send objections to `legal@growdirect.io` with:

- Merchant entity and order-form reference
- Sub-processor objected to
- Specific data-protection grounds (e.g., regulator-issued adequacy concern, documented prior incident, regional adequacy mismatch)

If the parties cannot resolve the objection, the Merchant may terminate the affected portion of the Service with pro-rated refund.

---

## Counsel Review Required (consolidated)

1. **§1 region scope** — confirm GCP region(s) before publication; multi-region must be disclosed
2. **§3 internal tooling exclusion** — Linear/Slack indirect-processor risk if support tickets carry merchant PII
3. **§2 forward disclosure** — confirm forward-listing planned-but-not-active sub-processors is acceptable. Some counsel prefer to list only active providers and notice each addition. The forward-disclosure model is more transparent but creates a longer published list

---

## Change log

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-05-02 | Initial working list — GRO-693 |
