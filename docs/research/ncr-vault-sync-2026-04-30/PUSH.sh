#!/bin/bash
# NCR vault sync — 2026-04-30
# Run this from your Mac terminal. Requires gh or git SSH auth.
set -e

SYNC_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT=/tmp/ncr-sync-$$

git clone https://github.com/growdirect-llc/ncr.git "$VAULT"

cp "$SYNC_DIR/modules__index.md"       "$VAULT/modules/index.md"
cp "$SYNC_DIR/pitch__index.md"         "$VAULT/pitch/index.md"
cp "$SYNC_DIR/why-canary__index.md"    "$VAULT/why-canary/index.md"
cp "$SYNC_DIR/verticals__gun.md"       "$VAULT/verticals/gun.md"
cp "$SYNC_DIR/verticals__feed-tack.md" "$VAULT/verticals/feed-tack.md"
cp "$SYNC_DIR/verticals__beverage.md"  "$VAULT/verticals/beverage.md"
cp "$SYNC_DIR/verticals__wine-spirits.md" "$VAULT/verticals/wine-spirits.md"

cd "$VAULT"
git add -A
git diff --stat HEAD
git commit -m "ncr: sync from Brain 2026-04-30 — pitch, three-pillar GTM, naming fixes"
git push origin main

rm -rf "$VAULT"
echo "Done — ncr.growdirect.io will update in ~60 seconds."
