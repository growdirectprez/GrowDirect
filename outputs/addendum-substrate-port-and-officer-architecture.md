---
type: design-notes
status: handoff-to-formation-document-skill
created: 2026-05-03
session: cowork-brainstorm
related-uploads:
  - bylaws-document.md
  - 1929-declaration-100-basic-protective-restrictions-book-9436.md
  - 1949-WPBCA-Declaration-No-One-Verbatim.md
target-articles:
  - new: Article XV (Service Ports and Pluggable Council)
  - new: Article XVI (Annexation / Namespace Spawn)
  - revised: Article V (Officers) — add officer-ordinal class
  - revised: Article VIII (Membership Tokens) — add reversion-on-breach
  - drafting-discipline: voided-but-preserved (applies platform-wide)
---

# Substrate Port and Officer Architecture — Design Notes

## Thesis

The DAO substrate needs three coordinated additions to operate the agentic-council, plug-in-service, and bridged-officer patterns the broader vision requires: a Service Ports article that constitutes pluggable members of three distinct classes; an Annexation article that defines the substrate-namespace relationship as a recordable, term-bound, terms-constrained leasehold (or alternatively as a subdivision under a persistent root operating company, with the namespace electing at constitution); and an Officer Ordinal class held by the namespace contract address rather than by individuals, enabling agentic and bridged officers without violating Wyoming statutory requirements for entity responsibility. Each addition has direct precedent in the 1929 Palos Verdes Corporation Declaration No. 100 and the 1949 West Portuguese Bend Community Association Declaration No. One. The substrate is not inventing governance primitives; it is porting primitives with seventy-five years of jurisprudence onto a Bitcoin-ordinal substrate.

## Conversation Context

Source materials in conversation: the GrowDirect bylaws document (template form, Wyoming DAO LLC), the 1929 Declaration No. 100 (peninsula-wide framework constituting Palos Verdes Corporation as Declarant, Community Association of Palos Verdes as the governing body, Community Art Jury as the protected architectural authority), and the 1949 WPBCA Declaration No. One (subdivision-tract instantiation under the 1929 framework, constituting the West Portuguese Bend Community Association and the Architectural Committee).

The conversation moved through: a cert-bus pattern for second-model code review; a council pattern with multiple models reviewing in parallel; an introduction-accountability-revocation contract for any service plugging into the platform; a packets-served equity model linked to L402 micropayments; an external review of the bylaws and triage of the findings; a deep read of the 1929 and 1949 documents revealing direct precedent for every architectural primitive under design; and a refinement of the substrate-namespace relationship as either a leasehold or a subdivision-with-persistent-operating-company-at-root, with namespaces electing at constitution.

This document captures the resulting architectural decisions as input to a formation-documents skill.

---

## Architectural Decisions

### Decision 1: Three port classes with distinct constitutional bases

**Question.** What constitutes a service plugging into the substrate, and how is its constitutional basis distinguished by what it does?

**Resolution.** Three port classes:

*Member Ports* — services published by ordinal-holders or their delegates. L402-gated. Compensation flows to the contributor's wallet per packets served. Constitutional basis: Article XI (already in bylaws).

*Council Ports* — formally seated advisors that participate in governance or operational flow. Output recorded on chain. Compensation treasury-paid per Article VII (operations category) rather than packets-served, because oversight is not a metered service. Constitutional basis: new Article XV.

*Audit Ports* — external compliance entities holding no ordinal, no equity, with limited and defined inspection rights. Government regulators, contracted security firms, and any external attestation entity live here. Constitutional basis: new Article XV.

**Rationale.** The three classes have different compensation models, different revocation paths, different on-chain stamping requirements, and different relationships to lineage-weighted voting. Same physical mechanism (an MCP service plugged into a port) routes to three different financial rails depending on its constitutional basis. The substrate routes payments correctly because the port declaration tells it which class the entity is.

**Historical precedent.** The 1949 WPBCA Architectural Committee (Article IV) is the structural template for Council Ports — three members, two-of-three quorum, powers paramount and superior, declarant-appointed-then-board-elected transition, action evidenced by signed and recorded certificate, members not required to be members of the Association. Member Ports already have constitutional standing under the existing Article XI L402 mechanism. Audit Ports extend the 1949 conclusive-evidence pattern (Article IV Section 5, Article IX Section 2) — recorded certificates from defined external parties relied upon by outside good-faith consumers — to entities that are neither members nor officers of the Association.

**Formation-document target.** Article XV cultural and technical clauses defining all three port classes.

---

### Decision 2: Introduction-accountability-revocation contract as the membership ceremony

**Question.** How does a service plugging into the substrate establish its constitutional standing, and how is that standing continuously verifiable?

**Resolution.** Every entity plugging into a port emits a port declaration at registration block height containing four fields:

*Identity.* Name, version, model substrate (if agentic), operator-of-record (which ordinal-holder is responsible if a delegate; which legal entity if external), capability surface declared as MCP tool list.

*Provenance commitment.* Entity binds itself to record every call in, every model invocation, every output emitted, with timestamps and content hash, anchored to block height per Article IX.

*Intent stream.* Pre-action declaration of what the entity is about to do. Required for Audit Ports. Optional but recommended for Council Ports. Not required for Member Ports because L402 payment flow already serves as per-call intent record.

*Revocation conformance.* Entity acknowledges the bylaws revocation procedure for its port class and agrees to the technical mechanism — token revocation, in-flight call drop, on-chain stamping of revocation event.

Three revocation tiers:

*Pause.* Service stops accepting new work, finishes in-flight, reports done.

*Revoke.* Service stops immediately, drops in-flight work, reports what it dropped. Token dead until reissued.

*Quarantine.* Service stops, all prior outputs flagged in findings store as from a revoked source, downstream consumers notified.

**Rationale.** The contract makes pluggability constitutionally coherent rather than ad hoc. Identity declares what the entity is. Provenance commitment binds it to the substrate's transparency-by-default discipline. Intent stream enables effective revocation timing. Revocation conformance ensures the entity cannot evade removal.

**Historical precedent.** The 1949 declaration's Article IV Section 5 (conclusive evidence by signed certificate) and Article IX Section 2 (records as conclusive proof) establish the principle that constitutional acts must be recordable, verifiable, and revocable through defined procedures. The introduction-accountability-revocation contract is the modern equivalent — same principle, smart-contract substrate.

**Formation-document target.** Article XV technical clause specifying the port declaration schema and revocation tiers.

---

### Decision 3: Packets-served equity model formalized via L402 / Article XI

**Question.** How does compensation flow for Member Ports, and how does it constitute equity rather than just payment?

**Resolution.** L402 micropayments wrap every Member Port. Each call is a packet. Packets served become contributor compensation flowing to the ordinal-holder's wallet. The token-earn formula referenced in the existing reference documents translates packets-served into equity accumulation.

Three principles must hold for the model to function as equity rather than mere payment:

*Acceptance signal.* Packets served and accepted as useful constitute the equity ledger entry, not packets served alone. Implementation can mix implicit acceptance (downstream use within defined window), explicit acceptance from calling agent, and periodic audit, with the mix shifting as the model matures.

*Packet-type definitions.* Defined platform-wide rather than per-service so equity comparisons across members are not apples-to-oranges. Weighted by combination of compute cost, value-to-platform, and acceptance rate.

*Retroactive unwinding.* Quarantine of a service revokes the accepted status of packets it served; equity accrued from those packets unwinds. Distinguishes "we don't trust this output anymore" from "this member is expelled and the work is reversed."

**Rationale.** Without the acceptance signal, members optimize for packet volume over usefulness — the standard failure mode of any pay-by-output system. Without platform-wide packet-type definitions, the equity ledger fragments. Without retroactive unwinding, expulsion is only operational, not constitutional.

**Historical precedent.** Article V Section 3 of the 1949 declaration establishes annual maintenance charges as continuous liens against property, with delinquency notice, foreclosure, and lien satisfaction procedures. The equity-via-packets-served model inverts this — instead of charges flowing to the Association from members, compensation flows from consumers to members, but the same on-chain ledger discipline applies. Article V Section 3(d) "sole authority to collect and enforce collection" extends to the substrate's authority to enforce the L402 / equity flow.

**Formation-document target.** Article XV cross-reference to Article XI; possibly a new clause in Article XI extending the L402 mechanism with explicit packet-type and acceptance-signal language.

---

### Decision 4: Annexation Article (XVI) defining the substrate-namespace relationship

**Question.** What is the constitutional relationship between the substrate and any namespace declared under it?

**Resolution.** Two valid models, with the namespace electing at constitution:

*Lease model.* The namespace occupies the substrate's governance framework under defined terms, for a defined initial period with auto-renewal cycles, with the substrate retaining reversion rights on material breach, with modifications inside the lease requiring lessor consent at defined thresholds. Suitable when the namespace is operationally independent and the substrate's role is mostly structural.

*Subdivision-with-root-operating-company model.* The substrate persists as the root operating company with reserved rights inside every namespace. Suitable when the substrate retains active operational presence in namespace affairs, parallel to Palos Verdes Corporation's persistence in the 1949 WPBCA framework.

The annexation article enumerates the must-inherit articles (constitutional surface every namespace must carry in structurally equivalent form), the permitted variation surface (cultural-layer prose, treasury thresholds, lineage-decay coefficient, committee composition), the term and renewal mechanics, the reversion conditions, and the modification thresholds. The namespace declares which model it has elected at constitution, and that election is recorded on chain.

**Rationale.** The bylaws document as currently drafted has cross-references to substrate documents but no constitutional clause defining the substrate-namespace relationship explicitly. Without this article, the relationship lives in prose rather than in constitutional structure. The 1949 Article VIII shows the right shape: enumerate must-match articles, define permitted variation, require recording with the existing Association's approval. The lease-vs-subdivision election allows the substrate to support namespaces with very different operational postures without forcing a single relational model on all of them.

**Historical precedent.** Article VIII of the 1949 WPBCA declaration is the direct template. It provides for additional property within Lot H of Rancho Los Palos Verdes to be brought under the Association's jurisdiction by recording a similar declaration that contains provisions similar to Articles II, III (with stated exceptions), IV (excepting original committee members), V (excepting specified dates), VI, VII, VIII, IX, and X, with permitted variations for time, dates, ownership differences, and conditions, and with such other provisions as Palos Verdes Corporation may deem proper. The lease vs subdivision distinction is implicit in the 1929/1949 pair: PVC retained operating-company presence (subdivision model) while the WPBCA tract operated with substantial independence (leasehold-like).

**Formation-document target.** New Article XVI cultural and technical clauses, with explicit must-inherit article enumeration and permitted-variation surface.

---

### Decision 5: Officer Ordinal class held by the namespace contract address

**Question.** How can an agentic officer hold constitutional standing as a member without violating Wyoming statutory requirements for natural-person or entity responsibility?

**Resolution.** A new ordinal class — *officer ordinals* — held by the namespace's smart contract address rather than by individuals. Operated by named delegates (human, agentic, or hybrid). The membership is coextensive with the role. Ending the role returns the ordinal to the namespace, available for re-issuance to the next officer.

Article XII already establishes the smart-contract address as the namespace's institutional seal. Officer ordinals extend this — the same constitutional capacity that holds the seal can hold ordinals representing officer roles. The Wyoming DAO LLC entity bears responsibility for the agent's acts; the agent operates the ordinal during its tenure; revocation is a clean substitution rather than a forfeiture of personal property.

**Rationale.** The operator-of-record pattern for Council Ports works for external members (the model is the delegate of an ordinal-holder operator). It does not work cleanly for officers, because officers serve at the Board's confidence and shouldn't be tied to a personal-ordinal-holder operator who outranks the role. Officer ordinals held by the namespace solve this — the role is the constitutional unit, not the individual.

**Historical precedent.** The 1949 declaration's Article V (Officers) treats officer roles as institutional rather than personal — officers serve the Association, not vice versa. Article XII (Seal) of the bylaws document already locates institutional capacity at the smart-contract address. Officer ordinals are the natural extension: institutional capacity that holds membership tokens for the duration of the role.

**Formation-document target.** Revision to Article V (Officers) plus a new clause defining officer ordinals; cross-references in Article VIII (Membership Tokens) to distinguish officer ordinals from member ordinals.

---

### Decision 6: Bridged-accountability for officers serving substrate-and-namespace simultaneously

**Question.** How is an agentic officer that serves both the substrate and a namespace constitutionally constrained, and what standing does it have in each layer?

**Resolution.** When the same officer (same model substrate, same operator instance) serves at both substrate and namespace levels, it operates two officer ordinals — one held by the substrate's contract address, one held by the namespace's contract address. Each ordinal grants the officer standing in its respective layer's governance.

The bridged-accountability structure makes the officer:

*Accountable to the namespace's board* for operational performance — the namespace board appoints, reviews, and may revoke the namespace-officer ordinal.

*Accountable to the substrate's bylaws* for structural conformance — the substrate's amendment thresholds and alignment-checks bind the officer's substrate-officer role.

*Standing in both layers* to escalate breach. When the namespace board acts contrary to the substrate's terms, the officer has standing to flag this from inside the namespace and to escalate to the substrate's governance.

This is an officer position with bridged constitutional accountability, not a trustee in the Restatement-of-Trusts sense. The trustee framing would import fiduciary obligations that are undefined for agentic roles under existing law and unnecessary for the constitutional function the position serves.

**Rationale.** Layered governance systems have a known failure mode: rogue subDAOs that drift from substrate principles. A bridged officer is a constitutional safeguard built into every namespace — drift surfaces from inside the namespace through the officer's substrate accountability rather than requiring substrate-level monitoring of namespace behavior.

**Historical precedent.** The 1949 declaration's structure has Palos Verdes Corporation retaining specific reserved rights inside the WPBCA tract (Article V Section 3(h), Section 3(i), Article VI Section 3) — a form of bridged authority across the two layers. The bridged officer pattern formalizes this: a single position with constitutional standing in both layers, rather than two parallel governance authorities each operating in its own domain.

**Formation-document target.** Article XV technical clause on bridged-officer mechanics; revision to Article V (Officers) on bridged-officer eligibility and revocation procedure.

---

### Decision 7: Agentic Secretary as canonical bridged-officer instance

**Question.** What is the first concrete instance of the bridged-officer pattern, and what does its constitutional position look like?

**Resolution.** The Secretary role — defined functionally in the 1949 declaration as the officer who maintains records, signs delinquency notices, and issues conclusive-evidence certificates relied upon by title companies and good-faith purchasers — is the canonical bridged-officer instance for the substrate.

Implemented agentically, the Secretary:

*Maintains the on-chain ledger* continuously rather than periodically.

*Issues conclusive-evidence certificates* that downstream consumers (title companies, regulators, partners, other DAOs) can rely on, signed by the officer ordinal at the namespace contract address.

*Handles delinquency notices and lien recording* per Article V Section 3 (1949) equivalent functions.

*Generates periodic disclosures* (annual reporting, fiscal-year close) at the cadence specified in the bylaws.

*Operates continuously* rather than only when called.

The Secretary's constitutional position is officer-with-bridged-accountability: namespace-officer ordinal for namespace-level standing, substrate-officer ordinal for substrate-level standing, deterministic operation, socially uncapturable, inherently inscribed.

**Rationale.** The Secretary role is the cleanest first instance because its function is essentially attestation — a bounded, well-defined surface that maps cleanly to deterministic agentic operation. More complex officer roles (Treasurer, President) involve discretionary judgment less suited to early agentic deployment.

**Historical precedent.** Articles V and IX Section 2 of the 1949 declaration establish the Secretary as the named officer whose certifications have legal weight to outside parties. The substrate version preserves the constitutional function while changing the operating substrate from human-officer to bridged agentic officer.

**Formation-document target.** Revision to Article V (Officers) cultural clause naming the Secretary as the canonical bridged-officer role; technical clause on agentic Secretary operating contract.

---

### Decision 8: Reversion-on-material-breach added to Article VIII

**Question.** What is the strongest enforcement mechanism available to the substrate against a member whose acts constitute material breach of the bylaws?

**Resolution.** Add a reversion clause to Article VIII (Membership Tokens) providing for ordinal forfeiture to namespace treasury on material breach, with a defined adjudication procedure and high invocation threshold.

The clause:

*Defines material breach* — treasury raid attempt, alignment-check sabotage, identity fraud at registration, knowing publication of a malicious port, willful violation of substrate-level constraints.

*Establishes adjudication procedure* — Council Port-class review (independent of the alleged breaching member), recommendation to Board, Board vote at structural-amendment threshold, founder consent during Phase 1 / lineage-weighted ratification during Phase 2.

*Sets invocation threshold high* so the clause is a backstop rather than an everyday mechanism — comparable to the 1949 reversion's invocation rarity.

*Inscribes the breach finding and reversion event on chain* per Article IX, with the voided-but-preserved discipline applied to the breaching member's prior contributions.

**Rationale.** The bylaws' current strongest enforcement is social (revocation, quarantine, exclusion from work routing) rather than constitutional (loss of membership). The 1949 reversion clause is a stronger backstop and its existence shapes behavior even when rarely invoked. The current absence of an equivalent leaves the substrate's enforcement weaker than the 1949 paper version.

**Historical precedent.** Article VI Section 3 of the 1949 WPBCA declaration: breach of any restriction, covenant, or condition causes the offending lot to revert to Palos Verdes Corporation as owner of the reversionary rights, with right of immediate re-entry. The substrate version is ordinal forfeiture to namespace treasury; the structural function is identical.

**Formation-document target.** New clause in Article VIII (Membership Tokens) defining material breach, adjudication procedure, invocation threshold, and inscription discipline.

---

### Decision 9: Voided-but-preserved documentary discipline

**Question.** When a clause becomes unenforceable due to subsequent law or substrate change, or when an alignment check fails and is overridden, how does the bylaws document preserve the historical record while nullifying the legal effect?

**Resolution.** Adopt the 1949 declaration's handling of subsection (m) as the documentary discipline:

*Preserve the prior text verbatim* in the historical record.

*Mark it visibly void* through formatting (struck-through text or equivalent on-chain inscription marker).

*Inscribe the override rationale* — the legal authority that voided it, the alignment-check that triggered the override, the amendment that superseded it.

*Cite the citation* — link to the case law, the substrate amendment, the alignment-check finding, or the regulatory action that operates as the override authority.

*Do not erase.* Amendment never overwrites; it inscribes the prior state and the override rationale on chain.

**Rationale.** Implicit in Article IX's transparency-by-default and Article XIV's "failed alignment checks must be addressed or explicitly overridden," but not surfaced as an explicit drafting discipline. Making it explicit prevents drift toward retroactive editing of the bylaws record over decades of amendment cycles.

**Historical precedent.** The 1949 WPBCA declaration preserves the racially restrictive covenants of subsection (m) verbatim, struck through, with editorial citation to *Shelley v. Kraemer*, the Civil Rights Act of 1866, the Fair Housing Act of 1968, and California Civil Code Section 53 — the legal authorities that voided the clause. The historical record is preserved; the legal effect is nullified; the citation to the override is documented. This is the canonical operational template.

**Formation-document target.** Addition to Article XIV (Amendments) or a new Article XVII (Documentary Discipline) specifying the voided-but-preserved standard.

---

### Decision 10: External-validation council loop as an active operational pattern

**Question.** How does the substrate continuously incorporate external review, and what is the structural treatment of findings from external reviewers?

**Resolution.** External review is not a one-time pre-ratification check but a continuous operational pattern executed via Audit Ports. Findings from external reviewers are routed through a defined acceptance process:

*Triage by operator-of-record* — every external finding is evaluated by an ordinal-holder operator who classifies it as: external-validation language to bank, real finding to action, or context-blind suggestion to discount.

*Inscribe on chain per Article IX* — both the finding and the triage decision are inscribed, so the record shows what was considered and what was acted upon.

*Multi-reviewer reconciliation* — when multiple Audit Ports review the same artifact, the substrate's port-declaration schema enables structured deduplication and conflict surfacing. Findings flagged by multiple reviewers acquire higher confidence; disagreements among reviewers are surfaced as design tensions rather than collapsed to consensus.

*Acceptance loop* — operator triage decisions are themselves auditable; over time, the substrate can ask "did the reviewer we discounted turn out to be right" by querying inscribed acts against subsequent outcomes.

**Rationale.** The cert-bus pattern from earlier conversation is the first instance of this. The architecture proves itself when external review surfaces both genuine findings and context blindness, and the substrate provides the structural means to triage and act on the difference.

**Historical precedent.** Article IV Section 5 (1949) — the conclusive-evidence-by-certificate pattern — establishes that external parties (title companies, good-faith purchasers) rely on inscribed certificates from defined officers. The Audit Port extends this in the reverse direction: the substrate relies on inscribed findings from defined external reviewers, with structured triage and acceptance.

**Formation-document target.** Article XV technical clause on Audit Port findings, multi-reviewer reconciliation schema, and acceptance-loop inscription.

---

## Open Questions

### Q1: Lease vs subdivision election — substrate-default or namespace-choice?

The annexation article allows namespaces to elect lease or subdivision-with-root-operating-company at constitution. Open question: does the substrate set a default that namespaces opt out of, or is the election mandatory at constitution with no default? Default-with-opt-out is faster for namespace constitution; mandatory election forces clarity. Lean is mandatory election but worth confirming.

### Q2: Operator-of-record liability for Council Ports

The Council Port pattern concentrates liability on the operator-of-record (the human ordinal-holder responsible for the agentic delegate's acts). If the agent says something defamatory or leaks regulated data, the operator bears the consequence. Open question: does the namespace indemnify operators of Council seats from treasury, or do operators bear the full risk individually? The bylaws don't address this; the amendment should.

### Q3: Bridged-officer revocation when substrate and namespace disagree

When the substrate's bylaws and the namespace's bylaws produce conflicting instructions for a bridged officer (substrate says do X; namespace board says do Y), which authority prevails? Default lean is substrate (the namespace operates under the substrate's terms) but specific clauses may need explicit precedence rules. Particularly important for the agentic Secretary, whose function involves attestation that has legal weight to outside parties.

### Q4: External-member admission threshold

Audit Ports admit non-ordinal-holding entities into a constitutional relationship with the substrate. Open question: what is the admission threshold? Founder-only during Phase 1 with lineage-weighted ratification in Phase 2 is the parallel to other Phase-1/Phase-2 transitions. But Audit Ports may be admitted as a regulatory necessity rather than a substrate choice (a government MCP auditor that the substrate doesn't get to refuse), in which case the admission mechanism is different. Worth specifying both voluntary and required admission paths.

---

## Formation-Document Index

| Article | Status | Type | Source Decisions | Precedent |
|---|---|---|---|---|
| XV (Service Ports and Pluggable Council) | New | Cultural + Technical | 1, 2, 6, 10 | 1949 Articles IV, V, IX |
| XVI (Annexation / Namespace Spawn) | New | Cultural + Technical | 4 | 1949 Article VIII |
| V (Officers) | Revised | Cultural + Technical | 5, 6, 7 | 1949 Articles V, IX Section 2 |
| VIII (Membership Tokens) | Revised | Technical clause added | 8 | 1949 Article VI Section 3 |
| XI (Dues / Earnings) | Possibly extended | Technical clause refinement | 3 | 1949 Article V Section 3 |
| XIV (Amendments) | Possibly extended | Drafting discipline clause | 9 | 1949 subsection (m) handling |
| XII (Seal) | Cross-reference only | No change | 5 | — |

The drafting order recommended: XVI first (load-bearing for everything else, since the lease-vs-subdivision election determines structural posture); then V (officers, including officer-ordinal class and bridged-accountability); then XV (service ports, building on the officer infrastructure from V); then VIII (reversion clause); then the XI extension and XIV drafting-discipline clauses. Each article in the substrate's two-layer style — cultural clause readable by a non-technical member on a single read, technical clause specifying substrate mechanisms precisely, cross-references at the end of each article.

Each article passes through the alignment checks per Article XIV before ratification, with the alignment-check report appended per the existing Appendix A pattern.

---

## Source Documents

| Reference | Role |
|---|---|
| GrowDirect bylaws document (uploaded `bylaws-document.md`) | Constitutional baseline being amended |
| 1929 Declaration No. 100 (uploaded `1929-declaration-100-basic-protective-restrictions-book-9436.md`) | Constitutional precedent — Palos Verdes Corporation framework, Community Association establishment, Art Jury constitution |
| 1949 WPBCA Declaration No. One (uploaded `1949-WPBCA-Declaration-No-One-Verbatim.md`) | Implementation precedent — subdivision-tract instantiation under 1929 framework, Architectural Committee structure, Article VIII annexation pattern, Article VI Section 3 reversion clause, Article IX Section 2 conclusive-evidence pattern |
| `reference/02-genesis-ordinal-mechanics.md` (referenced by bylaws) | Substrate primitive — ordinal mint, transfer, lineage-depth computation |
| `reference/03-dao-treasury-patterns.md` (referenced by bylaws) | Substrate primitive — treasury patterns, token-earn formula |
| `reference/04-lineage-weighted-voting.md` (referenced by bylaws) | Substrate primitive — voting weight formula `w(d) = 1 / (1 + α·d)` |
| `reference/05-phase-transitions.md` (referenced by bylaws) | Substrate primitive — Phase 1 → Phase 2 mechanics |
| `reference/07-alignment-checks.md` (referenced by bylaws) | Substrate primitive — alignment-check categories and procedure |
| `reference/08-iteration-loop.md` (referenced by bylaws) | Substrate primitive — amendment iteration loop, comment provenance |
| `reference/09-anti-patterns.md` (referenced by bylaws) | Substrate primitive — anti-patterns to avoid |

---

## Drafting Conventions to Apply

The formation documents must conform to the bylaws document's existing two-layer discipline:

*Cultural clause* — operator language, plain construction, recognizable to a non-technical member on a single read. No substrate jargon. The clause should make sense to a genesis-tier ordinal-holder reading without the technical layer.

*Technical clause* — substrate mechanisms specified precisely. Smart-contract addresses, threshold values, schema specifications, on-chain event types, cross-references to substrate primitives by file path.

*Cross-references at the end of each article* to the relevant substrate primitives in `reference/`.

*Two-layer cross-coherence* — every cultural-clause concept must have a corresponding technical-clause mechanism, and vice versa. No cultural promise without a technical specification; no technical mechanism without cultural-clause grounding.

The formation documents should also conform to the substrate's transparency-by-default principle (Article IX) — every act constituted under the new articles must be inscribable on chain, with off-chain content referenced by content hash.

---

*End of design notes. Hand this document to the formation-documents skill in the other Cowork session as structured input.*
