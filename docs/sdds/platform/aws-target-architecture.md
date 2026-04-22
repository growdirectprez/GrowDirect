# Shared Infrastructure — AWS Target Architecture

> **Status:** Production-grade ops contract (target state — not yet deployed)
> **Type:** Platform Service
> **Namespace:** platform
> **Last updated:** 2026-04-13
> **Dev stack:** See [[docs/sdds/platform/shared-infrastructure|Shared Infrastructure]]
> **Author role:** [[Canary/docs/profiles/ops/DevOps|DevOps]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

**Wiki:** [[Brain/wiki/growdirect-workflow|GrowDirect Workflow]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Related:** [[docs/sdds/platform/shared-infrastructure|Shared Infrastructure]] · [[docs/sdds/platform/memory-bus|Memory Bus]]
> **Deployment status:** Planning. No AWS resources provisioned yet.

---

## Purpose

This document defines the production AWS topology that replaces the Docker Compose dev stack. Every Docker service maps to a managed AWS equivalent. The goal is zero self-managed stateful infrastructure — AWS handles backups, patching, failover, and encryption. App containers run on ECS Fargate.

---

## Service Mapping — Docker to AWS

| Dev (Docker Compose) | Production (AWS) | Key Differences |
|---------------------|-----------------|----------------|
| `growdirect_postgres` (pgvector/pgvector:pg17) | **RDS PostgreSQL 17** with pgvector extension | Managed backups, Multi-AZ, storage encryption, IAM auth option |
| `growdirect_valkey` (valkey/valkey:8-alpine) | **ElastiCache for Redis** (Valkey-compatible) | Multi-AZ, automatic failover, encryption at rest + in transit, IAM auth |
| `growdirect_ollama` (ollama/ollama) | **ECS Fargate task** (GPU) or **SageMaker endpoint** | GPU instance for inference. Alternative: move to API-based embedding provider (OpenAI, Cohere) to eliminate GPU management. |
| `growdirect_pgadmin` | **Not deployed.** Use AWS RDS Query Editor or bastion host with pgAdmin. | pgAdmin is dev-only. |
| `growdirect_memory_bus` | **ECS Fargate task** | Same container image, different config injection. |
| `canary_flask` / `cove_flask` | **ECS Fargate tasks** behind **ALB** | Auto-scaling, health check routing, TLS termination at ALB. |
| Canary TSP consumers (sub1-sub4) | **ECS Fargate tasks** (no ALB, long-running) | Stream consumers, no inbound traffic. Scale independently. |
| Docker `growdirect` network | **VPC with private subnets** | Security groups replace Docker network isolation. |

---

## Target Architecture

```
                         ┌──────────────┐
                         │  CloudFront  │
                         │   (CDN/TLS)  │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │     ALB      │
                         │  (HTTPS:443) │
                         └──┬───────┬───┘
                            │       │
                   ┌────────▼──┐ ┌──▼────────┐
                   │  Canary   │ │   Cove    │
                   │  ECS Task │ │  ECS Task │
                   │ (Fargate) │ │ (Fargate) │
                   └────┬──┬───┘ └──┬──┬─────┘
                        │  │        │  │
        ┌───────────────┘  │        │  └───────────────┐
        │                  │        │                  │
   ┌────▼─────┐     ┌─────▼────────▼─────┐     ┌─────▼──────┐
   │ RDS      │     │    ElastiCache     │     │  Secrets   │
   │ Postgres │     │   (Valkey/Redis)   │     │  Manager   │
   │ Multi-AZ │     │     Multi-AZ       │     │            │
   └──────────┘     └────────────────────┘     └────────────┘
        │
   ┌────▼──────┐     ┌──────────────┐
   │  Memory   │     │   Ollama /   │
   │  Bus ECS  │     │  SageMaker   │
   │  (Fargate)│     │ (embeddings) │
   └───────────┘     └──────────────┘
```

All resources in a single VPC. App tasks in private subnets. RDS and ElastiCache in isolated subnets (no public IP). ALB in public subnets.

---

## Dependencies

| AWS Service | Purpose | Required Config |
|-------------|---------|----------------|
| VPC + private subnets | Network isolation | At least 2 AZs for Multi-AZ |
| ALB | HTTPS termination, request routing | ACM certificate for `*.growdirect.app` |
| ECS Fargate | Container runtime | Task definitions per app |
| RDS PostgreSQL 17 | Database (replaces Docker PostgreSQL) | `db.t3.medium` minimum, pgvector extension |
| ElastiCache Redis 7 | Sessions + cache (replaces Docker Valkey) | `cache.t3.micro` minimum, encryption enabled |
| Secrets Manager | Credential storage | One secret per service (DB password, API keys, etc.) |
| ECR | Container image registry | One repo per app image |
| CloudWatch | Logging + monitoring | Log groups per ECS task |
| S3 | Database backups, document storage | Versioning enabled, lifecycle rules |
| ACM | TLS certificates | Auto-renewing wildcard cert |

---

## Data Flow & PII Map (Production)

Same data flows as dev stack, but with encryption at every layer:

| Layer | Dev State | Production Target |
|-------|-----------|------------------|
| Data at rest (PostgreSQL) | Unencrypted Docker volume | RDS storage encryption (AES-256, AWS-managed key) |
| Data at rest (Valkey) | Unencrypted Docker volume | ElastiCache encryption at rest (AES-256) |
| Data in transit (app to DB) | Plaintext TCP | `sslmode=require` on all PostgreSQL connections |
| Data in transit (app to cache) | Plaintext TCP | ElastiCache in-transit encryption (TLS) |
| Data in transit (client to app) | HTTP (dev) / HTTPS via mkcert (Canary) | ALB TLS termination with ACM certificate |
| Secrets | Hardcoded in compose / `.env` files | AWS Secrets Manager, injected via ECS task definition `secrets` block |
| Backup | None | RDS automated backups (7-day retention), WAL archiving to S3 |

### PII Encryption Requirements (Production)

| Data Category | Current State | Required State | Implementation |
|--------------|--------------|---------------|----------------|
| Member emails, phones, names | Plaintext in PostgreSQL | Field-level AES-256-GCM | Extend Canary `crypto.py` pattern to Cove models |
| OAuth tokens (Canary) | AES-256-GCM encrypted | No change needed | Already implemented — reference implementation for other fields |
| Ballot content | Plaintext, RLS-gated | RLS + field-level encryption | Encrypt ballot `vote` column; decrypt only in election result tallying |
| Session tokens | Plaintext in Valkey | Encrypted in transit (TLS) | ElastiCache in-transit encryption handles this |
| Lead contact info (Angel) | Plaintext in PostgreSQL | Field-level AES-256-GCM | Encrypt `email`, `phone`, `name` fields on lead model |
| Database credentials | In compose files and .env | Secrets Manager | `boto3` retrieval at app startup, or ECS `secrets` injection |

---

## Operations

### RDS PostgreSQL

| Setting | Value | Rationale |
|---------|-------|-----------|
| Instance class | `db.t3.medium` (start) | 2 vCPU, 4 GB RAM. Scale based on connection count and query load. |
| Storage | 100 GB gp3, encrypted | AES-256 with AWS-managed key |
| Multi-AZ | Yes | Automatic failover for HA |
| Backup retention | 7 days | Point-in-time recovery within 7-day window |
| Maintenance window | Sun 04:00-05:00 UTC | Off-peak for US Pacific users |
| Parameter group | Custom: `pgvector`, `pgcrypto`, `uuid-ossp` preloaded | Match dev extensions |
| Connection limit | 100 (default) | Monitor via CloudWatch `DatabaseConnections` metric |
| SSL enforcement | `rds.force_ssl = 1` | Reject unencrypted connections |

**Database separation:** Same as dev — one RDS instance, multiple databases (`canary`, `cove`, `growdirect_memory`). Each app gets its own IAM-authenticated database user or Secrets Manager credential.

### ElastiCache (Redis/Valkey)

| Setting | Value | Rationale |
|---------|-------|-----------|
| Node type | `cache.t3.micro` (start) | Scale based on session count and stream throughput |
| Engine | Redis 7.x (Valkey-compatible) | ElastiCache does not yet offer native Valkey |
| Multi-AZ | Yes | Automatic failover |
| Encryption at rest | Yes (AWS-managed key) | Protect session data |
| Encryption in transit | Yes (TLS) | All connections encrypted |
| AUTH | Yes (token in Secrets Manager) | Per-cluster auth token |
| Maxmemory policy | `allkeys-lru` | Graceful eviction under memory pressure |
| Backup | Daily snapshot, 7-day retention | Session data is ephemeral but streams need recovery |

**App isolation:** Same logical database model (DB 0 = Canary, DB 1 = Cove, DB 4 = TSP streams). Consider ElastiCache ACL for per-app access control.

### ECS Fargate Task Definitions

| Task | CPU | Memory | Min/Max Instances | Health Check |
|------|-----|--------|-------------------|-------------|
| Canary Flask | 512 | 1024 MB | 1/4 | ALB target group `/health` |
| Cove Flask | 512 | 1024 MB | 1/4 | ALB target group `/health` |
| Canary TSP sub1-sub4 | 256 each | 512 MB each | 1/1 (per consumer) | ECS container health check |
| Memory Bus | 256 | 512 MB | 1/2 | Container health check on `:8003/health` |
| Angel Agent | 256 | 512 MB | 1/2 | Container health check on `:8004/health` |

### Secrets Management

| Secret | Consumers | Rotation |
|--------|-----------|----------|
| `growdirect/rds/master` | RDS admin operations only | 90 days (automatic) |
| `growdirect/rds/canary` | Canary Flask, TSP consumers | 90 days |
| `growdirect/rds/cove` | Cove Flask, Angel Agent | 90 days |
| `growdirect/rds/memory` | Memory Bus | 90 days |
| `growdirect/elasticache/auth` | All app tasks | 90 days |
| `canary/square/oauth` | Canary Flask | Manual (Square-controlled) |
| `canary/flask/secret-key` | Canary Flask | On rotation schedule |
| `cove/flask/secret-key` | Cove Flask | On rotation schedule |
| `angel/anthropic-api-key` | Angel Agent | Manual |
| `memory-bus/mcp-api-key` | Memory Bus | 90 days |

### Monitoring & Alerting

| Metric | Source | Alert Threshold | Action |
|--------|--------|----------------|--------|
| RDS CPU utilization | CloudWatch | > 80% for 5 min | Scale up instance class |
| RDS free storage | CloudWatch | < 10 GB | Increase storage |
| RDS connections | CloudWatch | > 80 | Check for connection leaks, add PgBouncer |
| ElastiCache memory | CloudWatch | > 80% | Scale node type or review eviction |
| ECS task health | ALB target group | Unhealthy > 2 min | ECS replaces task automatically |
| ECS CPU/Memory | CloudWatch | > 80% sustained | Auto-scale task count |
| 5xx error rate | ALB | > 1% of requests | Page on-call |
| Application logs | CloudWatch Logs | Error patterns | CloudWatch Alarms |

### CI/CD Pipeline

```
git push → GitHub Actions →
  1. Run tests (pytest against canary_test/cove_test)
  2. Build Docker images
  3. Push to ECR
  4. Update ECS task definitions
  5. ECS rolling deployment (blue/green)
  6. Health check passes → traffic shifts
  7. Rollback on health check failure
```

**Database migrations:** Run as a one-shot ECS task before deploying new app version. Alembic `upgrade head` in a Fargate task with the same network config as the app.

---

## Deployment

### Infrastructure as Code

Terraform (preferred) or AWS CDK for all resources. No manual console provisioning.

Key modules:
- `vpc` — VPC, subnets, security groups, NAT gateway
- `rds` — PostgreSQL instance, parameter group, subnet group
- `elasticache` — Redis cluster, subnet group
- `ecs` — Cluster, task definitions, services, auto-scaling
- `alb` — Load balancer, target groups, listener rules
- `secrets` — Secrets Manager secrets
- `ecr` — Image repositories
- `monitoring` — CloudWatch dashboards, alarms, SNS topics

### Security Groups

| Resource | Inbound | Outbound |
|----------|---------|----------|
| ALB | 443 from `0.0.0.0/0` | App SG on 5000 |
| App tasks (Canary, Cove) | 5000 from ALB SG | RDS SG on 5432, ElastiCache SG on 6379, Ollama SG on 11434 |
| RDS | 5432 from App SG, Memory Bus SG | None (managed by AWS) |
| ElastiCache | 6379 from App SG | None (managed by AWS) |
| Memory Bus | 8003 from App SG | RDS SG on 5432, Ollama SG on 11434 |

### Cost Estimate (Starting)

| Service | Config | Monthly Estimate |
|---------|--------|-----------------|
| RDS `db.t3.medium` Multi-AZ | 100 GB gp3 | ~$140 |
| ElastiCache `cache.t3.micro` Multi-AZ | Default | ~$25 |
| ECS Fargate (6 tasks avg) | 512-256 CPU, 512-1024 MB | ~$80 |
| ALB | 1 LB, moderate traffic | ~$25 |
| Secrets Manager | 10 secrets | ~$5 |
| CloudWatch | Logs + metrics | ~$20 |
| NAT Gateway | 1 AZ | ~$35 |
| **Total** | | **~$330/mo** |

---

## Code Review Findings (Production-Specific)

These findings are specific to the AWS deployment target. Dev-stack findings are in [[docs/sdds/platform/shared-infrastructure|Shared Infrastructure]].

### P0 — Blocks Production

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P0-AWS-1 | **No IaC exists.** Zero Terraform/CDK modules. All AWS resources must be provisioned from scratch. | Write Terraform modules for VPC, RDS, ElastiCache, ECS, ALB, Secrets Manager before any deployment. |
| P0-AWS-2 | **No CI/CD pipeline.** No GitHub Actions workflow for building images, pushing to ECR, or deploying to ECS. | Build GitHub Actions workflow: test, build, push ECR, deploy ECS. Gate on test pass. |
| P0-AWS-3 | **Ollama GPU hosting undefined.** No decision on self-hosted GPU (expensive) vs. API provider (OpenAI/Cohere embedding endpoint). | Decide: SageMaker endpoint with GPU for self-hosted, or switch to API-based embedding (cheaper, simpler, higher availability). Document in ADR. |

### P1 — Before GA

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P1-AWS-1 | **No WAF rules.** ALB has no Web Application Firewall. Exposed to common web attacks. | Enable AWS WAF with managed rule sets (SQL injection, XSS, rate limiting). |
| P1-AWS-2 | **No DDoS protection.** Standard AWS Shield only (automatic). No advanced protection configured. | Evaluate AWS Shield Advanced based on risk profile. CloudFront provides basic DDoS mitigation. |
| P1-AWS-3 | **No log retention policy.** CloudWatch Logs default to never expire. Costs grow unbounded. | Set log group retention: 30 days for app logs, 90 days for access logs, 7 days for debug logs. |

---

## Production Readiness Checklist

- [ ] Terraform modules written and reviewed for all AWS resources
- [ ] VPC with private subnets in 2+ AZs
- [ ] RDS PostgreSQL provisioned with storage encryption and Multi-AZ
- [ ] ElastiCache provisioned with encryption at rest + in transit
- [ ] All secrets migrated to Secrets Manager
- [ ] ECS task definitions created with Secrets Manager references
- [ ] ALB configured with ACM certificate and health checks
- [ ] CI/CD pipeline deploying to ECS on merge to main
- [ ] Database migrations run as pre-deploy ECS task
- [ ] CloudWatch dashboards for RDS, ElastiCache, ECS, ALB
- [ ] CloudWatch alarms for critical metrics (5xx rate, CPU, storage)
- [ ] WAF rules enabled on ALB
- [ ] Per-app database users (no shared superuser)
- [ ] Ollama replacement strategy decided and implemented
- [ ] Load testing completed under expected production traffic
- [ ] Disaster recovery procedure documented and tested
- [ ] GDPR/CCPA data deletion procedure documented
