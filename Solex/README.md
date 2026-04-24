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

## Runbook

### Daily dev

```bash
cd ~/GrowDirect/Solex
./devops/scripts/dev.sh up     # start web + worker + mailhog
./devops/scripts/dev.sh logs   # tail web logs
./devops/scripts/dev.sh shell  # bash in web container
./devops/scripts/dev.sh test   # run pytest in web container
./devops/scripts/dev.sh down   # stop
```

### Reseed catalog

```bash
docker compose exec web python3 -m solex.cli catalog import
```

### Seed admin user (dev only)

```bash
docker compose exec web python3 -m solex.cli admin create-seed-user \
  --email dev@solex.local --password password
```

### Alembic

```bash
docker compose exec web alembic upgrade head
docker compose exec web alembic revision --autogenerate -m "<message>"
```

### Square sandbox test cards

- `cnon:card-nonce-ok` — successful payment
- `cnon:card-nonce-declined` — declined
- See Square docs for CVV/postal-code failure tokens.

### MailHog (dev email inbox)

Web UI: http://localhost:8027

### Webhook tunneling for local dev

Square sandbox webhooks require a public URL. Use Cloudflare Tunnel:

```bash
cloudflared tunnel --url http://localhost:5003
```

Configure the resulting URL + path `/api/webhooks/square` in the Square developer dashboard.

### Running the sandbox-live integration test

Requires `SQUARE_SANDBOX_*` env vars in `.env`:

```bash
docker compose run --rm -e SOLEX_ENV=testing web pytest -m sandbox_live -v
```

If creds are missing, the test is automatically skipped.
