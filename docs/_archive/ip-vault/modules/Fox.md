---
type: module
domain: fox
status: active
created: 2026-03-19
updated: 2026-03-19
---
# The Fox — Case Management

> "Catch them. Track them. Build the case. Close the loop."

---

## Overview

The Fox is Canary's case management module — the place where alerts become investigations, investigations become evidence, and evidence becomes action. When Canary chirps, Owl flags, or Goose detects a crypto anomaly, Fox auto-creates a case file and starts building the record.

Right now, small retailers catch a thief and... nothing. They ban the person, maybe call the cops, and hope it doesn't happen again. There's no system of record, no pattern tracking, no way to know if the same person hit three of your franchise locations last month.

Fox fixes that. Every incident gets a case. Every case gets a timeline, evidence locker, loss calculation, and action queue. Over time, Fox builds a rap sheet for every bad actor — employees, customers, vendors — and surfaces patterns that no single-store owner would ever see on their own.

---

## Core Features

### Subject Profiles
- Auto-populated from Canary/Owl data: name, employee ID, transaction history, alert history
- Photo attachment capability (from CCTV stills or uploaded images)
- Contact details, social profiles, and known associates (for organized retail crime tracking)
- Cross-location linking: same subject flagged at multiple franchise locations gets a unified profile

### Incident Detail
- What was stolen/frauded: item, quantity, SKU, serial number, dollar amount
- When: timestamp, shift, day of week pattern
- Where: location, register, camera zone
- How: method (refund abuse, void manipulation, sweethearting, inventory ghost, crypto wash)
- Evidence: receipt data, transaction logs, alert metadata — auto-attached from Canary

### Loss Calculator
- Auto-calculates total loss per case: retail price + cost of goods + shrinkage impact + recovery costs
- Aggregates across cases for total exposure per subject, per location, per time period
- Tags severity: Minor (under $100), Significant ($100-$1,000), Critical ($1,000+), Organized (multi-location/multi-subject)

### Evidence Locker
- Encrypted file storage for photos, video clips, receipts, voice notes, written statements
- Chain of custody tracking: who uploaded, when, who accessed
- Admin-only visibility — RBAC-locked so only authorized roles can view sensitive evidence
- Exportable evidence package for law enforcement or legal proceedings

### Action Queue
- Configurable action templates per case type:
  - Report to law enforcement (with pre-formatted incident report)
  - Issue trespass notice / ban from store
  - Terminate employee (with HR documentation trail)
  - Blacklist from merchant network (shared across franchise locations)
  - Escalate to corporate LP team
  - File insurance claim
  - Refer to legal counsel
- Status tracking: Open, Under Investigation, Action Taken, Closed, Referred

### Timeline & Rap Sheet
- Chronological record of every interaction with a subject across all locations
- Every refund, every void, every alert, every return — builds a complete behavioral history
- Pattern visualization: frequency charts, escalation trends, time-of-day heatmaps
- Recidivism tracking: "This subject has been flagged 4 times in 60 days across 3 locations"

### AI Threat Scoring
- Owl-powered threat level (1-10) based on behavioral patterns, frequency, and financial impact
- Score of 7+ auto-escalates for manager review
- Score of 9+ auto-generates law enforcement referral package
- Predictive: "Based on pattern, subject likely to strike Location #4 within 2 weeks"

---

## Why It Wins

- **Closes the loop** — alerts without case management are just noise. Fox turns detection into action
- **Franchise power** — corporate sees all cases across all locations. Pattern emerges that no single store would see
- **Legal readiness** — proper evidence chain and documentation makes prosecution viable for cases that used to be write-offs
- **Network effect** — shared blacklists and subject profiles across the merchant network make every store safer
- **Retention driver** — once a merchant has case history in Fox, switching costs are high. It's the stickiest module in the stack

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Flask Blueprint, integrated with Canary's existing auth/RBAC |
| Database | PostgreSQL — cases, subjects, evidence metadata, action logs |
| File Storage | Encrypted blob storage for evidence files (S3-compatible, with at-rest encryption) |
| Search | Full-text search across cases, subjects, and evidence notes |
| Export | PDF case reports, CSV bulk export, JSON API for enterprise integrations |
| Auth | Role-gated: Viewer sees case status, Analyst sees details, Manager resolves, Admin manages evidence |

---

## Roadmap

| Phase | Timeline | Deliverables |
|---|---|---|
| **Alpha** | Q2 2026 | Basic case CRUD. Auto-create from Canary alerts. Subject profiles. Loss calculator |
| **Beta** | Q3 2026 | Evidence locker (encrypted). Action queue. PDF export for law enforcement |
| **v1.0** | Q4 2026 | Owl threat scoring integration. Cross-location subject linking. Franchise dashboard |
| **v1.5** | Q1 2027 | Network-wide blacklists. Predictive recidivism. API for enterprise LP systems |

---

## RBAC Permissions

| Capability | Viewer | Analyst | Manager | Admin |
|---|---|---|---|---|
| View case list | Yes | Yes | Yes | Yes |
| View case details | — | Yes | Yes | Yes |
| Create cases manually | — | Yes | Yes | Yes |
| Resolve / close cases | — | — | Yes | Yes |
| Access evidence locker | — | — | Yes | Yes |
| Manage subjects | — | — | Yes | Yes |
| Export case reports | — | Yes | Yes | Yes |
| Delete cases | — | — | — | Yes |
| Configure action templates | — | — | — | Yes |

---

## Integration Points

| Module | How Fox Connects |
|---|---|
| **Canary** | Auto-creates case when alert severity hits threshold. Links transaction data as evidence |
| **Owl** | Receives threat scores per subject. Gets pattern analysis for case enrichment |
| **Goose** | Crypto fraud cases auto-created when Goose detects wash trading or suspicious Lightning activity |

---

*Module Owner: Eva (PM) + Jeremy (Developer Quant)*
*Version: 1.0*
*Date: February 15, 2026*
*Source: Jeffe/Grok strategy session*
