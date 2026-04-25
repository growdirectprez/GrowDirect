---
classification: internal
type: wiki
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source-archive: /Volumes/My Passport/CLIENTS/DELIVERY/ + /Volumes/My Passport/macpro/Users/geoff/Documents/ (sanitized)
provenance: Brain/wiki/founder-context-secure-engagement-archive.md
---

# Video Integration — Solution Pattern

The reusable architectural pattern for integrating a third-party video surveillance system (DVR-based) into a loss-prevention or transaction-analytics platform. The reference implementation uses exacqVision as the surveillance vendor; the pattern itself is independent of the DVR product. Relevant to Canary Module Q (video-into-loss-prevention).

## Intent

Let an analyst, while looking at a transaction-of-interest, click a single icon and watch the video footage from the camera that overlooks the register where that transaction occurred — without leaving the analytics platform.

The integration delivers four outcomes:
1. Cross-reference between transactions and cameras (a register has cameras; a transaction happened on a register; therefore the transaction has cameras).
2. Time-correlated video retrieval (a transaction has a timestamp; the video for that camera at that timestamp is the relevant clip).
3. In-platform video playback (no context switch into a separate DVR client).
4. Bi-modal reference data maintenance (automated feed for scale, manual form for tactical fixes).

## Architecture

The pattern is **distributed by deliberate choice**: video stays at the store DVR. Only the analyst's browser fetches frames over the customer's WAN at the moment of investigation. The analytics platform never holds video.

```
┌──────────────────────────────────────────────────────────────┐
│                    Customer's WAN                             │
│                                                               │
│   ┌──────────────┐                          ┌──────────────┐ │
│   │ Store 1      │                          │ Store 2      │ │
│   │  ┌────────┐  │                          │  ┌────────┐  │ │
│   │  │  DVR   │◄─┼──────┐            ┌──────┼──┤  DVR   │  │ │
│   │  │ camera │  │      │  HTTP(s)   │      │  │ camera │  │ │
│   │  └────────┘  │      │  on demand │      │  └────────┘  │ │
│   └──────────────┘      │            │      └──────────────┘ │
│                         │            │                       │
│                  ┌──────┴────────────┴──────┐                │
│                  │ Analyst's browser        │                │
│                  │  (LP application UI +    │                │
│                  │   embedded video viewer) │                │
│                  └────────────┬─────────────┘                │
│                               │                              │
│                               │ analytics, transactions,     │
│                               │ reference-data lookups       │
│                               │                              │
│                  ┌────────────┴─────────────┐                │
│                  │ LP / Analytics Platform  │                │
│                  │  (hosted; transactions,  │                │
│                  │   alerts, camera ref)    │                │
│                  └──────────────────────────┘                │
└──────────────────────────────────────────────────────────────┘
```

Three networks involved:
- **Store LAN** — DVR is reachable here, cameras are wired to it.
- **Customer WAN** — extends the store LAN to HQ and to the analyst's location. DVRs are reachable from any node on the customer's WAN.
- **Analytics platform tenant** — hosted, reachable from the analyst's browser on the customer WAN.

Two data paths:
- **Transactions and reference data** — analyst browser ↔ analytics platform (HTTPS).
- **Video frames** — analyst browser ↔ DVR (HTTP/HTTPS, direct, no platform proxy).

The **video does not flow through the analytics platform**. This is the central architectural choice. It eliminates platform-side video storage, keeps surveillance retention at the customer's existing infrastructure, and avoids GDPR-class data-residency questions for the platform vendor.

## Components added to the LP platform

Four components must be added to a transaction-analytics platform to support the integration:

1. **Video viewer module** — embedded UI component, launched from the transaction viewer or case-management transaction tab. Uses store + register + transaction-timestamp as its inputs and renders video in an iframe-style player.
2. **Camera reference table** — relational table linking each DVR + camera to a register or set of registers. The connecting tissue between transactions and video.
3. **Reference-data import script** — automated processing of a camera reference file supplied by the customer. Pipe-delimited text, processed on a schedule (manual or automatic upload).
4. **Reference-data maintenance form** — UI screen for manual add/edit/delete of camera reference rows. Used for one-off corrections, new-store cutover, or when the automated feed is unavailable.

## Trigger model

**Pull, not push.** This is the pattern's other central architectural choice.

- The platform does not record clips, alert on motion, or push events to the surveillance system.
- The analyst is the trigger. They identify a transaction-of-interest from analytics, click the camera icon, and the platform pulls the relevant footage.
- Timespan is adjusted by the analyst via a slider above the player.

This pull pattern fits a loss-prevention workflow where the analyst already has signal from the analytics layer (an exception, an alert, a flagged transaction) and wants corroborating video. Pushing every transaction to a video event would 100x the surveillance system's retention burden for negligible analyst benefit.

## Data flow at investigation time

```
1. Analyst opens transaction-of-interest in case management.
2. Click camera icon → viewer overlay opens.
3. Camera dropdown loads from camera-reference-table lookup
   ON (storeNo, posNo) of the transaction.
4. Analyst selects a camera, clicks "Load Camera".
5. Platform constructs DVR URL from reference data:
   - Address (HTTP base URL of the DVR)
   - Camera ID
   - Time = transaction timestamp ± slider window
   - Credentials (Username/Password from reference)
6. Browser opens HTTP(s) connection direct to DVR.
7. Frames stream back, rendered in player.
8. Slider lets analyst adjust playback timespan within the
   archived window.
```

Critical: the DVR URL is constructed client-side, with credentials retrieved from the reference table via the platform's authenticated session. The platform owns reference data including DVR credentials; the browser owns the live network connection to the DVR.

## Camera reference data

The connecting tissue. Stored as a table, sourced from a pipe-delimited file or maintained via the form. The exemplar field set:

| Field | Purpose |
|---|---|
| CameraID | Unique identifier (across all stores and DVRs) |
| StoreNo | Store identifier — the join key to transactions |
| POSNo | Register identifier — the join key to transactions |
| Name | Camera name displayed in the dropdown; should match the DVR's own naming |
| Description | Free-text — what the camera looks at (register, queue, exit) |
| Address | HTTP base URL of the DVR the camera is on |
| CameraStrProperty1 | Name of the DVR (for analyst orientation) |
| Username | DVR access credential (per-camera permission scope) |
| Password | DVR access credential |
| TimeZoneId | Microsoft Time Zone Index for the store |
| ProviderName | DVR vendor identifier (e.g. `ExacqVision`) — selects the player driver |

Three reserved integer slots and three reserved string slots (`CameraIntProperty1-3`, `CameraStrProperty2-3`) provide forward-compatible extension points without schema migration.

**File format:** pipe-delimited text. Customer supplies on a schedule (typically weekly) or on store-cutover events. The import script processes the file and updates the reference table accordingly (insert/update by CameraID).

**Provider abstraction:** `ProviderName` enables multi-vendor support — different DVR vendors require different player drivers. The platform ships drivers per supported vendor; the customer configures `ProviderName` per camera. This is the extension point for adding a second DVR vendor without changing the schema.

## Network and security considerations

The pattern's distributed architecture pushes complexity into the customer's network:

- **Direct browser-to-DVR connectivity is required.** No platform-side proxy. This means the customer's analyst workstations must be on a network segment that can reach all DVRs.
- **Cross-origin resource sharing (CORS)** must be permitted in the customer's browser configuration. The analytics platform is at one origin; each DVR is at another. Without CORS, the browser will not initiate the connection.
- **Per-camera credentials** are sensitive. The reference-data table contains DVR credentials in plaintext at rest by default. Production deployments should encrypt these columns and audit access.
- **HTTPS preferred over HTTP** for DVR connections, especially over the WAN. Many older DVRs support only HTTP — flag this during discovery.
- **Time zone alignment** between DVRs, POS, and the analytics platform is mandatory. A 1-hour drift makes the entire integration silently useless. Use Microsoft Time Zone Index per store, not server-local time.
- **DVR firmware compatibility** with the platform's player driver. Each supported DVR vendor has a tested firmware band; outside it, frames may not render. Document the supported band per `ProviderName`.

## Privacy and retention model

Because video stays at the DVR:
- **The platform vendor never holds video.** This simplifies privacy posture — the platform is not a controller for video data, only a controller for camera-reference metadata.
- **Retention is the customer's responsibility.** Determined by their existing DVR retention policy, not by the platform. If the analyst tries to pull video older than the DVR's retention, the request fails — surface this as a clear error in the player.
- **Audit trail must capture intent.** Every "Load Camera" action should be logged on the platform side: who pulled, which camera, which transaction, when. This is the privacy paper trail.
- **Data subject access requests (DSARs)** for video are the customer's to fulfill. The platform can produce a list of pull events but cannot produce the underlying video.
- **Video is not included in platform backups, replication, or DR.** The pattern is intentionally stateless on video.

## Failure modes

Common failure modes and what they look like in practice:

| Failure | Symptom | Root cause |
|---|---|---|
| Reference file out of date | Cameras missing from dropdown after store cutover | Customer's automated feed broke; manual form is the recovery |
| DVR offline | "Load Camera" hangs or 5xx | Store DVR down or store WAN segment down; platform cannot detect this in advance |
| Time zone drift | Wrong footage plays | Store DVR clock not synced to NTP, or wrong `TimeZoneId` in reference |
| CORS misconfiguration | Black player, console error | Customer's browser policy blocks cross-origin to DVR |
| Credentials rotated on DVR | Player loads then errors | Reference table has stale credentials |
| DVR firmware out of band | No frames render | Firmware older or newer than driver's tested band |

A health-monitoring overlay (a "DVR reachability dashboard") should be considered for any production deployment — it pre-empts most of the above by surfacing DVR availability before the analyst tries.

## Variants and adjustments

**Centralized recording variant.** If the customer's surveillance is recorded centrally (e.g., on a hosted VMS) rather than on per-store DVRs, the pattern flattens to a single DVR-equivalent endpoint. Reference data simplifies (no `Address` per camera). Trade-off: the customer must operate the central VMS at scale.

**Push-event variant.** If the customer wants automated clip-capture on platform-detected events, add a second mode: platform sends an event to a clip-export endpoint at the DVR. Adds significant integration work — a per-vendor export API, retention policy on clips, storage. Recommend keeping pull as the primary pattern and adding push only when analyst workflow demands it.

**Cloud-DVR variant.** If the customer's DVRs are cloud-native (e.g., a cloud video service) the network-direct architecture works without WAN considerations, and CORS becomes the only friction point.

## Application to Canary Module Q

The Canary video module is a pull-based, reference-table-driven integration. Module Q should adopt the pattern's three central choices:

1. **Distributed video retrieval** — frames stream browser-to-source-system, not through Canary.
2. **Pull-based trigger model** — analyst-initiated, not event-driven.
3. **Reference-table connecting tissue** — `(storeNo, posNo) → cameraID + sourceURL + credentials + timezone`.

Open questions specific to Module Q (to be resolved during the engagement):
- Which DVR vendors must be supported at launch — `ProviderName` driver count.
- Whether reference-data feed will be customer-supplied (file) or vendor-managed (one of Canary's onboarding deliverables).
- Per-camera credential storage encryption requirements.
- Audit-trail retention period for "Load Camera" events.
- Whether centralized-VMS variant is required for any target customer (changes architecture).
