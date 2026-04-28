---
title: Canary — Commercial Context & Go Build Direction
tags: [canary, rapidpos, strategy, go, var-channel]
last-compiled: 2026-04-28
classification: internal
needs-review: 2026-05-12
---

# Canary — Commercial Context & Go Build Direction

## What This Article Is

This captures the strategic context behind the Go pivot and the VAR distribution model — the why behind decisions that show up as constraints in the SDDs. Read this before working on any Canary-facing build task.

## The Commercial Opportunity

Canary's primary commercial path is NCR Counterpoint VARs. The immediate engagement is with the Rapid POS VAR channel: established Counterpoint resellers who have long-term relationships with SMB specialty retailers (garden centers, gun stores, feed-tack, beverage, wine). These VARs own the merchant relationship; Canary provides the product layer they deliver.

The channel model is: VAR brings merchant trust and domain expertise, Canary brings detection/case management/analytics. No cold-start acquisition problem. The merchant already trusts their VAR.

## The Go Stack Decision

The production build is Go. This is non-negotiable and was driven by the commercial partner's engineering orientation — not by technical preference. The Python prototype (GRO-617) proved the model; it is reference only. All new development is Go: `pgx` + `sqlc` + `Chi` + `go-redis` + `pgvector-go`.

Never suggest extending or deploying the Python prototype for production RapidPOS use cases.

## ARTS-Native Data Contract

Canary's canonical retail data model is built against the ARTS POSLOG standard. NCR Counterpoint is the reference implementation — full inventory, receiving, purchase orders, paycode structures, EJ spine, multi-store transfers. Square is a lightweight subset: its entire data surface maps cleanly into the ARTS model Canary already handles natively.

This means: build to the full ARTS surface area, and Square compatibility comes for free. Any future POS connector that speaks ARTS or a subset of it connects as an adapter projection. The reverse — building Square-first and trying to extend to enterprise retail — requires rearchitecting the data model entirely.

GRO-626 (ARTS POSLOG alignment) was the foundation work for this. The Go build starts with that alignment as a given.

## Agent-Driven, Minimal HIL

The defining design constraint: Canary must run with near-zero human-in-the-loop intervention. This is not a product feature — it is an operational necessity for the target customer.

SMB retailers (1–31 locations) cannot afford dedicated loss prevention staff. The platform is the LP department. Agents handle detection, evidence packaging, case initiation, and compliance tracking. Human review is an escalation path for ambiguous or legally sensitive decisions — not the default operating mode.

Every design decision should be evaluated against this constraint: does this require a human to operate it routinely? If yes, rework it.

## Stakeholders (as of 2026-04-28)

- **Jeff Roberts** — senior engineering / capital. Go-biased. The strategic backer behind the build direction.
- **Matt Becks** — ex-Starbucks. Works for Jeff Roberts. Intermediary.
- **Tim Mooney** — ex-colleague of founder. Connector. Tim@Monach.com.
- **Bart (RapidPOS VAR owner)** — 20+ years as a Counterpoint VAR. Knows his stack is aging (2012 SQL Server, on-premise). Needs a modern product underneath his existing merchant relationships. Distribution asset, not technical buyer.

## What Exists Today

- Python prototype: Square Marketplace-certified, Chirp + Fox live, near-beta. Reference only going forward.
- Go build specifications: `docs/sdds/go-handoff/` — 17 SDDs, language-agnostic, production-ready.
- NCR vault: `ncr.growdirect.io` — external-facing product site for VAR co-sell conversations.
- Memory bus: 448 embeddings indexed as of 2026-04-28.

## What the Go Build Is Not

- Not a port of the Python prototype — it is a clean build from design documents
- Not Square-first — Square is a supported connector, Counterpoint is primary
- Not a pivot away from the product vision — the detection model, evidence chain, and case management core are unchanged
