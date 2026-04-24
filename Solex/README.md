# Solex

Canary-observable Square sandbox merchant. See
`../docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md`.

## Dev quickstart

```bash
cp .env.example .env
# fill in Square sandbox credentials
cd devops && docker compose up -d
docker compose exec web python3 -m solex.cli catalog import
open http://localhost:5003
```
