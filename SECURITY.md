# Security Policy

## Reporting a Vulnerability

If you believe you have found a security vulnerability in any GrowDirect
repository — Canary, Cove, Angel, the platform itself, or the public
website — please report it privately so we can investigate and remediate
before any details become public.

**Contact:** security@growdirect.io

Please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce (proof-of-concept code or a minimal test case)
- The affected repository, file, route, or endpoint
- Your preferred contact method for follow-up

We will acknowledge receipt within 72 hours, triage within 5 business
days, and keep you informed of remediation progress. Coordinated
disclosure is welcome — we will credit you on resolution unless you
prefer to remain anonymous.

## Scope

In scope:

- Source code in the GrowDirect, Canary, Cove, and Angel repositories
- Running instances at `canary.growdirect.app`, `dev.growdirect.app`,
  `canary.growdirect.io`, and `ownpalosverdes.com`
- The MCP server mesh and memory bus
- Build and deployment infrastructure (Docker, Cloudflare Tunnel, GitHub
  Actions)

Out of scope:

- Denial-of-service (DoS) or volumetric testing
- Social engineering of GrowDirect personnel or partners
- Physical attacks on infrastructure
- Third-party services (Square, Stripe, Cloudflare, GitHub) — report
  those directly to the relevant vendor

## Safe Harbor

Good-faith research consistent with this policy will not result in legal
action from GrowDirect. Do not access, modify, or exfiltrate real
customer data. If you inadvertently access such data, stop testing,
destroy any copies, and notify us immediately.

## Platform Security Posture

GrowDirect products handle sensitive merchant and transaction data. Key
controls:

- Row-level security and tenant isolation at the Postgres level
- Immutable evidence records (hash-chain + Postgres trigger enforcement)
- HMAC signature verification on every inbound webhook
- Session storage in Valkey with short TTLs
- Credentials in environment variables — never in source
- Bitcoin-anchored Merkle trees for downstream audit

For details on the evidence pipeline and detection model, see the
architecture SDDs in each product repo.
