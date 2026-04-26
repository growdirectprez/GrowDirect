# Solex photo inbox

Drop product photos here named `<lowercase-sku>.<ext>` (jpg/png/webp).

The 25 SKUs live in `catalog/products.yaml`. Match the filename to the SKU.

## Apply photos

```bash
cd ~/GrowDirect/Solex

# Copy from inbox into the catalog imagery directory (overwrites placeholder PNGs)
cp catalog/inbox/*.{jpg,png,webp} catalog/images/ 2>/dev/null

# If the extension differs from the .png placeholder, fix the image_path in products.yaml
# (only needed for non-png replacements):
for f in catalog/inbox/*.jpg; do
  [ -e "$f" ] || continue
  sku=$(basename "$f" .jpg)
  sed -i '' "s|catalog/images/${sku}.png|catalog/images/${sku}.jpg|g" catalog/products.yaml
done

# Reimport to copy into solex/static/catalog/images/
docker compose -f devops/docker-compose.yml exec web python3 -m solex.cli catalog import

# Hard-refresh the browser to bypass image cache (Cmd-Shift-R)
```

## SKUs

```
AO-CLEANSE        AO-COLLAGEN       AO-DETOX-30       AO-ELEMENTAL
AO-ENERGY-30      AO-FOCUS-30       AO-GUT-30         AO-HEART-30
AO-IMMUNE-30      AO-IMPLANT-STIM   AO-INFINITY-MAT   AO-INNER-VOICE
AO-JOINT-60       AO-LIGHT-SPECS    AO-MIND-30        AO-SCAN-V1
AO-SCAN-PRO       AO-SEFI-UNIT      AO-SLEEP-30       AO-YOUTH-30
AO-YOUTH-90       PEMF-SPOT-PAD     PET-CALM-30       PET-GUT-60
PET-IMMUNE-30     PET-JOINT-60      PET-SCAN-MINI     RED-LIGHT-BELT
RED-LIGHT-PANEL-M
```

## Files here are gitignored

Only this README is committed.
