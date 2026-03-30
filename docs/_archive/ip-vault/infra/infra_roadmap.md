---
type: spec
domain: infra
status: active
created: 2026-03-14
updated: 2026-03-19
---
# Canary LP — Infrastructure Roadmap

> Last updated: 2026-03-07

---

## Current State: Local Lab

Everything runs on hardware in Jeffe's office. Two machines on the same wired LAN segment behind a business router, exposed to the internet via Cloudflare Tunnel.

```
Frontier Fiber (47.154.122.225)
  └── DSR-250 Business Router (192.168.10.1)
        ├── .102  Mac Mini M4 16GB — Dev (dev.growdirect.app)
        ├── .117  iMac — QA (qa.growdirect.app — pending tunnel config)
        └── .103  (reserved) Mac Studio — Ollama inference
```

**Monthly cost: ~$0** (hardware owned, Cloudflare free tier, Frontier fiber existing)

---

## Phase 1: Tighten Local Lab (Now)

What we're doing right now. No new hardware, no cloud.

| Task | Status | Linear |
|------|--------|--------|
| Finalize dev → QA deploy pipeline | In progress | — |
| Enable `qa.growdirect.app` tunnel routing | Pending | — |
| Docker disk cleanup (39GB reclaimable) | Pending | — |
| Investigate unhealthy TSP workers + Nginx | Pending | — |
| Nightly PostgreSQL backup to local disk | Pending | — |
| Document network topology | Done | — |
| Document deployment pipeline | Done | — |

---

## Phase 2: Mac Studio + Dedicated Inference (When Needed)

Add a Mac Studio to the wired segment as a dedicated Ollama inference server. Frees the Mac Mini from running both the app stack and the LLM.

| Component | Detail |
|-----------|--------|
| Hardware | Mac Studio M2 Ultra 192GB (~$4,000 one-time) |
| IP | 192.168.10.103 (reserved, DHCP static lease on DSR-250) |
| Service | Ollama running qwen3:14b (or 70B+ with 192GB unified memory) |
| Access | `OWL_URL=http://192.168.10.103:11434` in `.env` |
| Availability | launchd service — auto-restart on crash/reboot |
| Fallback | Flask deterministic mode if Studio unreachable |

**Monthly cost: ~$10** (electricity)
**Amortized: ~$115/mo** over 3 years — cheaper than AWS GPU spot pricing

---

## Phase 3: Lightweight Cloud (When Scale Requires)

Only put in the cloud what NEEDS to be in the cloud. The app stays on local hardware.

### What Goes to AWS

| Service | AWS Component | Why Cloud |
|---------|--------------|-----------|
| **RaaS** (raw data store) | S3 | Merchant data needs redundancy, backup, compliance |
| **Landing page** | CloudFront + S3 | 99.9% uptime, CDN, independent of lab availability |
| **DB backups** | S3 | Off-site backup for disaster recovery |
| **DNS** | Route 53 (or stay on Cloudflare) | Already on Cloudflare — may not need Route 53 |

### What Stays Local

| Service | Machine | Why Local |
|---------|---------|-----------|
| Flask app | Mac Mini → Mac Studio | Cloudflare Tunnel handles access |
| PostgreSQL | Mac Mini | Fine for beta; backup to S3 nightly |
| Valkey | Mac Mini | Ephemeral — rebuilds itself |
| Ollama | Mac Studio | Your model, your hardware, no metered API |

**Monthly cost: ~$20-30** (S3 + CloudFront)

### AWS Issues (Linear)

| Issue | Description | Status |
|-------|------------|--------|
| GRO-150 | Epic: Autonomous Beta Launch | Backlog |
| GRO-151 | AWS Account Setup & IAM | Backlog |
| GRO-152 | Infrastructure-as-Code (Terraform/CDK) | Backlog |
| GRO-153 | Production Docker Image & ECS Pipeline | Backlog |
| GRO-155 | Owl Cloud Deployment (Ollama on EC2) | Backlog |
| GRO-156 | Landing Page (CloudFront + Route 53) | Backlog |
| GRO-158 | Automated Health Check Pipeline | Backlog |
| GRO-161 | Monitoring & Alerting (CloudWatch) | Backlog |
| GRO-163 | System Health Monitor (Ops Dashboard) | Backlog |

**Decision needed:** GRO-155 (Owl GPU on EC2) may not be needed if Mac Studio handles inference locally. Could be repurposed as "Owl failover" — cloud GPU only activates if local inference is down.

---

## Phase 4: Full Cloud Migration (When SLAs Required)

When customer audits require "where is my data?" to say "AWS us-east-1" instead of "a Mac Mini in the founder's office."

| Service | AWS Component | Cost Estimate |
|---------|--------------|---------------|
| Flask | ECS Fargate | ~$30/mo |
| PostgreSQL | RDS (db.t4g.micro) | ~$15/mo |
| Valkey | ElastiCache (t4g.micro) | ~$12/mo |
| Load Balancer | ALB | ~$20/mo |
| DNS + CDN | Route 53 + CloudFront | ~$10/mo |
| Secrets | Secrets Manager | ~$5/mo |
| Monitoring | CloudWatch | ~$5/mo |
| **Subtotal (no GPU)** | | **~$100/mo** |
| Ollama (GPU spot) | EC2 g5.xlarge | +$170/mo |
| Ollama (GPU on-demand) | EC2 g5.xlarge | +$550/mo |

**Critical path:** GRO-151 → GRO-152 → GRO-153 → GRO-155

**When to pull this trigger:**
- Enough merchants that a single Mac can't handle the load
- Customer audit requires AWS-hosted data
- SLA commitment (99.9% uptime) requires redundancy
- Compliance framework (SOC 2, HIPAA) mandates cloud infrastructure

---

## Architecture Decision: Owl Inference

The biggest cost decision in the stack. Three options:

| Option | Where | Cost | Latency | Control |
|--------|-------|------|---------|---------|
| **Mac Studio (local)** | Office, wired LAN | ~$115/mo amortized | <1ms | Full — your model, your hardware |
| **EC2 GPU (cloud)** | AWS g5.xlarge | $170-550/mo | 20-50ms | Full — self-managed Ollama |
| **Managed API** | Bedrock / Anthropic | Pay-per-call | 50-200ms | Limited — vendor dependency |

**Recommendation:** Mac Studio for primary inference, cloud GPU as failover only. Aligns with "local first, cloud behind a gate" principle.

---

## Principle

> "Local first, cloud behind a gate. No unmetered API connections."

The cloud is for redundancy, compliance, and scale — not for running the core product. The app runs on hardware you own, models run on silicon you control, and the cloud catches what falls through.
