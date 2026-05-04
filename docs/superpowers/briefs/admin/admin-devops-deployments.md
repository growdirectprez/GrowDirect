---
screen: /admin/devops/deployments
title: Deployment Log
role: ADM
wave: Cross
origin: FD
cp_equivalent: "None"
---

# Deployment Log

**URL:** `/admin/devops/deployments`  
**Primary role:** ADM  
**Entry points:** Admin nav → DevOps → Deployments; Health dashboard → "what changed recently?"

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Deployments", environment selector (prod/staging) | Defaults to prod |
| Filter bar | Date range, service/module, deployer, status (success/failed/rollback) | Combinable |
| Main content | Deployment log table | Newest first |
| Detail panel | Opens on row click — commit info, changed services, health delta | Side panel |

## Key Elements

### Deployment Table
Columns: Timestamp, Version (semver tag), Environment (prod/staging), Services Deployed (badge list), Deployed By (actor), Duration (seconds), Status (Success / Failed / Rolled Back), Health Delta (health status before vs after — green = no regression, yellow = degraded post-deploy, red = deploy triggered an incident).

The Health Delta column is the critical signal: it answers "did this deployment cause a problem?" at a glance without requiring a separate health check.

**Empty state:** "No deployments in the selected date range."

### Detail Panel
Opens on row click. Contains: Full commit SHA + link to git tag, Changeset description (from deployment metadata), Specific services and modules changed (e.g., "Q-module v2.3.1 → v2.3.2"), Rollback button (if status = Success, rollback available for 24h), Pre/post health snapshot comparison.

### Rollback Action
Available for 24h after a successful deployment. Triggers an automated rollback to the prior version. Requires confirmation modal with specific confirmation text ("ROLLBACK PRODUCTION"). Rollback is itself logged as a deployment entry.

## Interaction Flows

1. **Diagnose post-deployment degradation:** Health dashboard shows Q-module degraded → ADM checks deployment log → sees Q-module deployed 20 minutes ago → opens detail panel → Health Delta shows green→yellow transition → initiates rollback
2. **Audit who deployed a change:** ADM investigating a rule behavior change → checks deployment log for the date range → finds relevant deployment → sees "Deployed By: github-actions[bot]" + commit SHA → follows to git history
3. **Verify staging before promoting:** ADM selects staging environment → reviews recent staging deployments → confirms test pass → proceeds with production deployment manually

## UX Callout

Canary runs on GCP with CI/CD pipelines. The deployment log is the bridge between code changes and operational reality. When something breaks in production, the first question is always "what changed?" — this screen answers that in seconds without requiring Kubernetes CLI access. The Health Delta column specifically closes the loop between deployment events and their observable impact, which is otherwise invisible unless you know to cross-reference the health dashboard manually.

## Navigation Exits

- `/admin/devops/health` — confirm current service health
- `/admin/devops/infra` — infrastructure view for resource-level context

## Open Questions

None.
