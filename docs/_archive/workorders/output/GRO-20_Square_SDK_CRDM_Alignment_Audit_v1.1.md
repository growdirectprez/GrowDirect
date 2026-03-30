---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-20 — Square SDK → CRDM Alignment Audit v1.1

**Issue:** GRO-20 (B-036)
**Prepared By:** ALX (Chief of Staff)
**Original Date:** March 2, 2026
**Refresh Date:** March 4, 2026
**Classification:** Internal — Technical Audit
**Gate:** Gates Tom's DDL work on GRO-18. Tom validates, Jeremy implements.
**SDK Version:** v44.0.1.20260122 (Fern-generated, Pydantic models)
**API Target:** Square API 2025-10-16 (latest stable)

---

## v1.1 Refresh Summary

This refresh incorporates three changes since v1.0:

1. **GRO-19 Decision (2026-03-04):** Accept and preserve full payload in all cases. No scrub logic. No field filtering. Grab everything Square exposes.
2. **SDK Version Confirmed:** v44.0.1.20260122 — well past the 2025-05-21 threshold for Timecard endpoints. No migration needed.
3. **Labor Webhook Correction:** The v1.0 audit incorrectly stated Labor API has no webhooks. As of API version 2025-05-21, Labor supports `labor.timecard.created`, `labor.timecard.updated`, and `labor.timecard.deleted`. This materially changes GRO-27 scope.

---

## Changes from v1.0

### GRO-19 Impact — Full Payload Preservation

The following v1.0 gates and caveats are **removed**:

| v1.0 Item | v1.0 Status | v1.1 Status |
|-----------|-------------|-------------|
| `card_last4` retention | ⚠️ Legal gate — pending Syd ruling, default STRIP | ✅ **KEEP** — full payload directive |
| `scrub_version` column | ✅ New (per GRO-19 memo) | ❌ **REMOVED** — no scrub logic, no version tracking needed |
| `payload` storage | "JSONB storage after scrub" | ✅ **Raw storage as-is** — confirmed in `webhooks_tsp.py` line 151 |
| Customer `email`, `phone` | "PII — retention per GRO-19" | ✅ **KEEP** — full payload directive |

**Code confirmation:** `webhooks_tsp.py` stores `raw_bytes.decode("utf-8", errors="replace")` with zero field filtering. The pipeline already implements the GRO-19 directive correctly.

### Payment Object — Fields Missing from v1.0 Audit

The v1.0 audit mapped 16 columns. The actual Square Payment object (SDK v44) exposes significantly more. Fields NOT captured in v1.0:

| Field | Type | Loss Prevention Value | Action |
|-------|------|----------------------|--------|
| `risk_evaluation` | RiskEvaluation | **HIGH** — Square's own fraud risk scoring (created_at + risk_level: PENDING/NORMAL/MODERATE/HIGH) | Add to CRDM — direct Chirp input |
| `device_details` | DeviceDetails | **HIGH** — device_id + device_installation_id for device-level anomaly detection | Already mapped via `device_id`, but `device_installation_id` is new |
| `application_details` | ApplicationDetails | **MEDIUM** — which Square product (POS, Invoices, Virtual Terminal, etc.) processed payment | Add to CRDM — channel attribution |
| `wallet_details` | WalletDetails | **MEDIUM** — Cash App payment details | Store in raw payload, extract when Cash App volume justifies |
| `buy_now_pay_later_details` | BuyNowPayLaterDetails | **LOW** — BNPL provider details | Store in raw payload |
| `bank_account_details` | BankAccountDetails | **LOW** — ACH/bank payment details | Store in raw payload |
| `cash_details` | CashPaymentDetails | **MEDIUM** — buyer_supplied_money + change_back_money for cash transaction auditing | Add to CRDM — cash drawer reconciliation |
| `external_details` | ExternalPaymentDetails | **LOW** — payments processed outside Square | Store in raw payload |
| `terminal_checkout_id` | string | **MEDIUM** — links payment to Terminal device checkout session | Store for device-session correlation |
| `buyer_email_address` | string | **MEDIUM** — buyer contact info at payment level | Already in Customer; redundant but preserved |
| `billing_address` | Address | **LOW** — card billing address | Store in raw payload |
| `shipping_address` | Address | **LOW** — shipping address if provided | Store in raw payload |
| `statement_description_identifier` | string | **LOW** — card statement text | Store in raw payload |
| `receipt_url` | string | **LOW** — Square-generated receipt URL | Store in raw payload |
| `approved_money` | Money | **MEDIUM** — may differ from amount_money if reauthorized | Add to CRDM — detects auth/capture discrepancies |
| `processing_fee` | ProcessingFee[] | **MEDIUM** — fee breakdown per payment | Useful for merchant reporting |
| `refunded_total_money` | Money | **MEDIUM** — running refund total | Already derivable from refunds table but useful as cross-check |
| `delay_duration` | string | **LOW** — auto-complete delay | Store in raw payload |

**Recommendation:** The raw payload already captures all of these (confirmed via `webhooks_tsp.py`). The CRDM should add explicit columns for `risk_evaluation`, `application_details.square_product`, `cash_details`, and `approved_money` — these have direct Chirp rule value. Everything else lives in the raw JSONB payload and can be extracted on demand.

### Webhook Coverage Matrix — CORRECTED

| CRDM Data Source | Webhook Available? | Event Types | Polling Fallback Needed? |
|------------------|--------------------|-------------|--------------------------|
| Transactions (Payments) | ✅ Yes | `payment.created`, `payment.updated` | No |
| Orders | ✅ Yes | `order.created`, `order.updated` | No |
| Refunds | ✅ Yes | `refund.created`, `refund.updated` | No |
| Customers | ✅ Yes | `customer.created`, `customer.updated` | No |
| Catalog/Products | ✅ Yes | `catalog.version.updated` | No |
| Inventory | ✅ Yes | `inventory.count.updated` | No |
| Disputes | ✅ Yes | `dispute.created`, `dispute.state.updated` | No |
| **Labor (Timecards)** | **✅ Yes (CORRECTED)** | `labor.timecard.created`, `labor.timecard.updated`, `labor.timecard.deleted` | **No — webhooks available since API 2025-05-21** |
| **Cash Drawers** | ❌ No | None | **YES — polling required** |
| **Locations** | ❌ No | None | Low-frequency poll OK |
| Gift Card Activities | ⚠️ Verify | `gift_card.activity.created` (unconfirmed) | May need polling |

**v1.0 → v1.1 change:** Labor now has webhook support. GRO-27 scope changes from "build polling adapters for Labor + Cash Drawers" to "subscribe to Labor timecard webhooks + build polling adapter for Cash Drawers only."

### Catalog API — `include_related_objects` Parameter

The Catalog API supports an `include_related_objects` boolean parameter on `RetrieveCatalogObject` and `BatchRetrieveCatalogObjects`. When `true`, the response includes one level of linked objects (e.g., item → variations → modifier lists → taxes). This should be enabled for all catalog sync operations to ensure we capture the full catalog graph.

**Action:** Verify our catalog polling/webhook handler uses `include_related_objects=true` when hydrating catalog objects.

---

## Revised Gap Summary

| Gap | Severity | v1.0 Status | v1.1 Status |
|-----|----------|-------------|-------------|
| `transaction_type` derivation | HIGH | Open | **Open** — state machine still needed |
| `card.last_4` retention | MEDIUM | Gated on GRO-19 | **Closed** — keep everything |
| No Labor webhooks | MEDIUM | Open (GRO-27) | **Closed** — webhooks exist since 2025-05-21 |
| No Cash Drawer webhooks | MEDIUM | Open (GRO-27) | **Open** — still poll-only |
| COGS not in Catalog API | LOW | Open | **Open** — manual entry, post-MVP |
| Merchandise hierarchy | LOW | Open | **Open** — Tom's GSLM pattern, post-MVP |
| `is_voided` derivation | LOW | Open | **Open** — session-window heuristic |
| Shift → Timecard rename | INFO | Open | **Closed** — SDK v44 uses Timecard natively |
| Gift card webhook availability | INFO | Open | **Open** — verify |
| **NEW: risk_evaluation not in CRDM** | **HIGH** | n/a | **Open** — Square fraud scoring available, not captured |
| **NEW: application_details not in CRDM** | **MEDIUM** | n/a | **Open** — channel attribution not captured |
| **NEW: cash_details not in CRDM** | **MEDIUM** | n/a | **Open** — cash transaction audit fields not captured |
| **NEW: catalog include_related_objects** | **MEDIUM** | n/a | **Open** — verify we request full object graph |

---

## Revised Action Items

1. **Jeremy:** Subscribe to `labor.timecard.created/updated/deleted` webhooks in webhook handler. Remove Labor from GRO-27 polling scope. GRO-27 becomes Cash Drawer polling only.
2. **Tom:** Add CRDM columns for `risk_evaluation` (risk_level + created_at), `application_details.square_product`, `cash_details` (buyer_supplied_money + change_back_money), `approved_money`. These have direct Chirp rule value.
3. **Jeremy:** Verify catalog sync uses `include_related_objects=true`. If not, add it.
4. **Jeremy:** Verify all webhook subscriptions include the full event type list from the corrected matrix above.
5. **Jim:** Integration test plan should validate that raw payloads contain all expected nested objects (risk_evaluation, device_details, application_details, etc.). Use SchemaFingerprint infrastructure (models exist, TODO for implementation).
6. **GRO-27 scope reduction:** Remove Labor polling, keep Cash Drawer polling only.

---

## Pipeline Confirmation

Verified in codebase (2026-03-04):

| Component | Status | File |
|-----------|--------|------|
| Raw payload storage (no scrub) | ✅ Confirmed | `webhooks_tsp.py:151` — `raw_bytes.decode()` |
| HMAC validation | ✅ Confirmed | `webhooks_tsp.py:90-105` |
| SHA-256 hash before JSON parse | ✅ Confirmed | `webhooks_tsp.py:109` |
| Idempotency (dedup cache + DB unique) | ✅ Confirmed | `webhooks_tsp.py:129-137` + `ingestion.py:26` |
| Schema drift detection models | ✅ Models exist | `webhooks.py:79-182` — `SchemaFingerprint`, `SchemaDriftAlert` |
| Schema drift detection logic | ⚠️ TODO | `webhooks.py:84` — "TODO(jeremy): Implement fingerprinting" |
| Ingestion log | ✅ Confirmed | `ingestion.py:12-95` — full audit trail |
| Dead letter queue | ✅ Confirmed | `ingestion.py:152-222` — retry infrastructure |
| SDK version | ✅ v44.0.1.20260122 | `square_capability_explorer.py:18` |

---

*ALX | GRO-20 v1.1 | March 4, 2026*
