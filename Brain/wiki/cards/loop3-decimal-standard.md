---
title: Decimal Standard for Canary Go — shopspring/decimal canonical adoption + retrofit roadmap
type: standard
status: active
date: 2026-05-03
linear: GRO-762
parent: GRO-739
authority: OQ Resolution Pack §A.1 OQ-2.3 (founder-approved 2026-05-03)
last-compiled: 2026-05-03
needs-review: 2026-08-03
---

# Decimal Standard for Canary Go

## Decision

**Canonical type:** [`github.com/shopspring/decimal`](https://github.com/shopspring/decimal) v1.4.0+, exposed as `internal/db/types.Decimal` (direct type alias).

**Authority:** OQ Resolution Pack §A.1 OQ-2.3, founder-approved 2026-05-03 per dispatch [GRO-762](https://linear.app/growdirect/issue/GRO-762).

**Phase B.4 deliverable (this card lands with):**
- `go.mod` adds `github.com/shopspring/decimal v1.4.0`
- `internal/db/types/decimal.go` declares the canonical alias + helper constructors

## Why shopspring/decimal

Loop 2 left every module hand-rolling its own decimal handling. The catalog of pain:

| Module | Current pattern | Problem |
|---|---|---|
| `internal/chirp/rules/cash_variance.go` | `numericStringToCents(*string) int64` | int64 truncation; no precision >2dp |
| `internal/chirp/rules/voids.go` | same | same |
| `internal/adapters/square/parser.go` | `centsToDecimalString(int64) string` | round-trips through string for every tender amount |
| `internal/adapters/counterpoint/parser.go` | `decimalString(float64) string` (`'f', 4`) | float64 cannot represent 0.10 exactly |
| `internal/db/types/q.go` | `LossAmountEstimated *string` (NUMERIC column → string in code) | `// using string for Loop 2` annotated TODO |
| `internal/db/types/q.go` | `SignalStrength *string` (NUMERIC column → string in code) | `// using string for Loop 2` |
| `internal/db/types/ledger.go` | `QuantityDelta string` | `// using string for Loop 2` |
| `internal/owl/...` | string-based Subtotal/RefundsTotal/DiscountsTotal aggregation | string → float64 via strconv at every aggregation |
| `internal/pricing/...` | `decimal.Decimal` would replace string-based tier / promo math | already aware; Loop 2 deferred |

Each module's choice was reasonable in isolation. Across the codebase it's an explosion of boundary-conversion code that:

1. **Loses precision** — float64 can't represent USD cleanly; int64-cents-as-string assumes 2dp universally (FX, weight × price for produce, percent fields all break)
2. **Makes arithmetic awkward** — every Add becomes a parse + convert + add + format
3. **Silently rounds** at boundaries (the most dangerous failure mode for accounting code)

`shopspring/decimal` is the answer the Go ecosystem has converged on for financial math:

- **Arbitrary precision** via internal `*big.Int` representation
- **Deterministic rounding modes** (RoundUp, RoundDown, RoundHalfEven, RoundHalfUp, RoundCash)
- **Native `database/sql` Scanner / Valuer** — pgx scan/value just works against `numeric(14,4)` columns
- **Native `json.Marshaler` / `json.Unmarshaler`** — wire format is the natural string ("12.34")
- **Battle-tested** — 4.6k stars, used by Stripe, Shopify, Square's own Go consumers, every fintech Go project the founder can name
- **Pure Go** — no cgo, no system deps, no surprises on cross-compile

## Canonical alias surface

```go
// internal/db/types/decimal.go
type Decimal = decimal.Decimal  // alias, not wrapper
```

Helper constructors (re-exports so non-substrate packages don't have to import `shopspring/decimal` directly):

- `types.NewDecimal(value int64, exp int32)` — value × 10^(-exp)
- `types.NewDecimalFromString(s string)` — at system boundaries
- `types.NewDecimalFromFloat(f float64)` — only when source is genuinely float (Counterpoint wire)
- `types.NewDecimalFromInt(i int64)` — lossless
- `types.ZeroDecimal` — pre-allocated zero

Full upstream API available via the alias: `.Add`, `.Sub`, `.Mul`, `.Div`, `.Cmp`, `.Round(places int32)`, `.RoundCash(interval int8)`, `.IsZero()`, `.IsNegative()`, etc.

## Retrofit roadmap (Loop 3 Wave 2 + later waves)

Phase B.4 (Wave 1) does **not** retrofit any module — it lands the substrate only. Loop 3 Wave 2 retrofits in dependency order; later waves ship the long tail.

### Wave 2 priority targets (the boundary code that costs the most to leave broken)

| # | Target | Current | Target end-state | Wave |
|---|---|---|---|---|
| 1 | `internal/adapters/square/parser.go::centsToDecimalString` | int64 cents → string with manual digit math | `types.NewDecimal(cents, 2).String()` (and store the Decimal upstream so the string conversion is at the wire-out boundary only) | Wave 2 |
| 2 | `internal/adapters/counterpoint/parser.go::decimalString` | `strconv.FormatFloat(v, 'f', 4, 64)` | `types.NewDecimalFromFloat(v).StringFixed(4)` | Wave 2 |
| 3 | `internal/chirp/rules/cash_variance.go::numericStringToCents` | manual string parse to int64 | `types.NewDecimalFromString(*e.Variance)` + `.IsNegative()` / `.Abs()` for compare | Wave 2 |
| 4 | `internal/chirp/rules/voids.go::numericStringToCents` | same | same | Wave 2 |
| 5 | `internal/db/types/q.go` Detection.SignalStrength + Case.LossAmount* | `*string` for NUMERIC columns | `*Decimal` (pgx scan/value handles the rest) | Wave 2 |
| 6 | `internal/db/types/ledger.go` LedgerStockMovement.QuantityDelta | `string` | `Decimal` | Wave 2 |
| 7 | `internal/owl/metrics/*` aggregation | string → float64 at every aggregate | `Decimal.Add()` / `.Cmp()` end-to-end | Wave 3 |
| 8 | `internal/pricing/...` | string-based tier math | `Decimal` end-to-end (priority — pricing is the rail that drives everything else) | Wave 2 |

### Migration patterns

**Pattern 1 — boundary parse (POS adapter wire → canonical):**

```go
// before
canonical.Subtotal = centsToDecimalString(money.Amount)

// after
canonical.Subtotal = types.NewDecimal(money.Amount, 2)
```

The `Subtotal` field type changes from `string` → `Decimal`. pgx scan/value handles the `numeric(14,4)` round-trip natively. JSON marshaling round-trips via the upstream library's MarshalJSON (string format on the wire).

**Pattern 2 — comparison rule (chirp evaluator):**

```go
// before
cents, err := numericStringToCents(*e.Variance)
abs := cents
if cents < 0 { abs = -cents }
if abs >= p.ThresholdCents { ... }

// after
variance, err := types.NewDecimalFromString(*e.Variance)
threshold := types.NewDecimal(int64(p.ThresholdCents), 2)
if variance.Abs().Cmp(threshold) >= 0 { ... }
```

Note: `ThresholdCents` int64 in the rule_definition.parameters block stays — it's the wire format from the merchant config UI; the comparison side-converts.

**Pattern 3 — aggregation:**

```go
// before
var voidedCents int64
for _, li := range items {
    cents, _ := numericStringToCents(li.LineTotal)
    if cents < 0 { cents = -cents }
    voidedCents += cents
}

// after
total := types.ZeroDecimal
for _, li := range items {
    amount, _ := types.NewDecimalFromString(li.LineTotal)
    total = total.Add(amount.Abs())
}
```

### Acceptance criteria per Wave 2 retrofit

Each module's retrofit closes when:

1. The module has no remaining `*string` fields backed by `numeric(N,M)` columns
2. All boundary conversions go through `types.NewDecimalFrom*` constructors
3. All arithmetic uses `Decimal.Add`/`Sub`/`Mul`/`Div`/`Cmp` — no `strconv.ParseFloat`, no manual digit math
4. Existing unit + integration tests pass without modification (the type change is internal — JSON round-trips and DB round-trips behave identically)
5. The `// using string for Loop 2` and `// decimal.Decimal dep needed` TODO comments are removed

## What this standard does NOT mandate

- **Money type wrapper:** keep `Decimal` flat; no `Money struct { Amount Decimal; Currency string }` ceremony. Currency travels alongside as a separate string field on the parent struct, same as today.
- **Database column type changes:** the schema's `numeric(14,4)` columns stay as-is. Decimal scan/value handles the round-trip.
- **Wire-format changes:** JSON wire format remains string ("12.34"), matching today's behavior. Public API unchanged.
- **Currency-specific rounding:** module-specific (e.g., cash drawers use `RoundCash`, percent calculations use `Round(4)`, display formatting uses `StringFixed(2)`). Each module picks per its semantics.

## Cross-references

- [`docs/superpowers/plans/2026-05-03-oq-resolution-pack.md`](../../../docs/superpowers/plans/2026-05-03-oq-resolution-pack.md) — §A.1 OQ-2.3 founder approval
- [`Brain/wiki/cards/loop2-build-report.md`](loop2-build-report.md) — top-10 finding #9 (decimal scatter)
- [`docs/sdds/go-handoff/canonical-data-model.md`](../../../docs/sdds/go-handoff/canonical-data-model.md) — `numeric(14,4)` is the schema's universal monetary precision
- Memory `feedback_flag_dependency_changes` — drove the explicit founder-approval gate on this dependency add
- Memory `feedback_no_hand_rolling_outside_core_ip` — drove the choice to adopt the proven library rather than continue scattered string/int64 hand-roll
