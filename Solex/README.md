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

## Theme

Plan 4 ships with a branded Tailwind theme approximating Solex Global's look:

| Token | Hex | Use |
|---|---|---|
| `solex-teal`  | `#1F5961` | Primary accents, CTAs, logo |
| `solex-gold`  | `#B79355` | Eyebrows, badges, highlights |
| `solex-leaf`  | `#5E7A5A` | Secondary accents, hover states |
| `solex-clay`  | `#A35E3E` | Alerts, tertiary labels |
| `solex-cream` | `#F7F4EE` | Page background |
| `solex-sand`  | `#E8E0D1` | Subtle section backgrounds, image placeholders |
| `solex-ink`   | `#1C1C1A` | Headings, body text on light |
| `solex-body`  | `#3F3F3B` | Body copy |
| `solex-muted` | `#8A8A84` | Muted metadata |
| `solex-line`  | `#E5E2DC` | Dividers, borders |

Typography: Cormorant Garamond (display) + Inter (body) via Google Fonts.
Tune the palette in `Solex/tailwind.config.js` after seeing real screenshots
against `solexglobal.com`.

## Catalog

- 25 SKUs live in `catalog/products.yaml` across 4 categories (supplements 10,
  devices 5, therapy 5, pet 5).
- Imagery is Pillow-generated placeholder tiles (`solex/static/catalog/images/`).
  Real Solex product photos swap in post-merge.

### Regenerate placeholder tiles

```
docker compose exec web python3 -m solex.cli catalog generate-placeholders
```

### Drop in real imagery

1. Save each photo as JPG or PNG to `Solex/catalog/images/<sku>.<ext>` using
   the lowercased SKU.
2. Update `image_path` in `products.yaml` if the extension changes.
3. Run `docker compose exec web python3 -m solex.cli catalog import` — the
   importer copies updated images from `catalog/images/` to
   `solex/static/catalog/images/`.

See `docs/catalog-curation.md` for the full playbook.
