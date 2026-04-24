# Solex Catalog Curation

Dev reference for managing the product catalog in `catalog/products.yaml`
and the static image tiles under `solex/static/catalog/images/`.

---

## Structure

`catalog/products.yaml` is the source of truth for product data during
development. It is loaded into the database via `catalog import` and
into Square via `catalog sync-to-square`.

```
catalog/
  products.yaml        ← source of truth
solex/static/catalog/
  images/              ← one PNG per SKU (generated or real photos)
```

### Product fields

| Field | Required | Notes |
|---|---|---|
| `sku` | yes | Unique. Used as stable identifier in Square sync |
| `slug` | yes | URL-safe. Used in storefront routes |
| `name` | yes | Display name |
| `short_description` | yes | One sentence, shown on product cards |
| `description` | yes | Full copy, shown on product detail page |
| `price_cents` | yes | Integer, USD cents |
| `image_path` | yes | Relative to `catalog/`: `catalog/images/<slug>.png` |
| `category_slug` | yes | Must match a category defined in the same file |
| `active` | yes | `true` / `false` |
| `weight_grams` | yes | Used for shipping rate calculation |
| `starting_inventory` | yes | Seeded into `inventory.on_hand` on first import |

### Categories (current)

| Slug | Name |
|---|---|
| `supplements` | Supplements |
| `devices` | Frequency Devices |
| `therapy` | Light & PEMF Therapy |
| `pet` | Pet |

---

## CLI Commands

### Import catalog into DB

```bash
docker compose -f devops/docker-compose.yml exec web python3 -m solex.cli catalog import
```

- Safe to re-run: existing SKUs are updated, new SKUs are inserted.
- Does NOT touch inventory on re-import (only sets `starting_inventory` on
  first insert).
- If `SOLEX_FLAG_SYNC_CATALOG_TO_SQUARE=true`, also syncs to Square sandbox
  after import.

### Generate placeholder tiles

```bash
docker compose -f devops/docker-compose.yml exec web python3 -m solex.cli catalog generate-placeholders
```

- Reads all SKUs from `catalog/products.yaml`.
- Writes one 600×600 PNG per SKU to `solex/static/catalog/images/<sku-slug>.png`.
- Colors are deterministically hash-derived from the SKU; stable across re-runs.
- Safe to re-run: existing files are overwritten.
- Requires Pillow (in `requirements-dev.txt`).

### Sync to Square

```bash
docker compose -f devops/docker-compose.yml exec web python3 -m solex.cli catalog sync-to-square
```

Requires `SQUARE_SANDBOX_ACCESS_TOKEN`, `SQUARE_SANDBOX_LOCATION_ID` in `.env`.

---

## Adding a Product

1. Add an entry to `catalog/products.yaml` under `products:`.
2. Follow the field schema above. Use a new unique `sku` and `slug`.
3. Run `catalog generate-placeholders` (or drop a real photo at
   `solex/static/catalog/images/<slug>.png`).
4. Run `catalog import` to seed the DB.
5. Run `catalog sync-to-square` if you want the Square sandbox updated too.

---

## Real Photos

When real product images are available, drop them at:

```
solex/static/catalog/images/<slug>.png
```

PNG preferred; JPEG accepted. Target 600×600 or larger square crop. The
`generate-placeholders` command will overwrite any file at the same path, so
run it only when you need to regenerate placeholders (i.e., before real photos
are added, not after).

---

## Image Path Convention

`image_path` in YAML uses the form `catalog/images/<slug>.png`. The catalog
importer copies images from `catalog/` to `solex/static/catalog/`. Storefront
templates reference images via the static URL:

```html
<img src="{{ url_for('static', filename=product.image_path) }}">
```

---

## Current SKU List (25)

| SKU | Category | Price |
|---|---|---|
| AO-YOUTH-30 | supplements | $49.95 |
| AO-YOUTH-90 | supplements | $129.95 |
| AO-MIND-30 | supplements | $54.95 |
| AO-SLEEP-30 | supplements | $44.95 |
| AO-IMMUNE-30 | supplements | $47.95 |
| AO-GUT-30 | supplements | $49.95 |
| AO-ENERGY-30 | supplements | $52.95 |
| AO-JOINT-60 | supplements | $59.95 |
| AO-DETOX-30 | supplements | $46.95 |
| AO-HEART-30 | supplements | $59.95 |
| AO-SCAN-V1 | devices | $1,499.00 |
| AO-SCAN-PRO | devices | $2,499.00 |
| AO-INNER-VOICE | devices | $999.00 |
| AO-SEFI-UNIT | devices | $1,799.00 |
| AO-IMPLANT-STIM | devices | $1,299.00 |
| PEMF-MAT-INF | therapy | $2,599.00 |
| RED-LIGHT-BELT | therapy | $349.00 |
| RED-LIGHT-PANEL-M | therapy | $799.00 |
| PEMF-SPOT-PAD | therapy | $149.00 |
| AO-LIGHT-SPECS | therapy | $249.00 |
| PET-GUT-60 | pet | $34.95 |
| PET-CALM-30 | pet | $29.95 |
| PET-JOINT-60 | pet | $37.95 |
| PET-IMMUNE-30 | pet | $27.95 |
| PET-SCAN-MINI | pet | $899.00 |
