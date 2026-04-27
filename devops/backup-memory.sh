#!/bin/bash
# GrowDirect Memory Bus — Backup Script
# Run manually or via cron. Creates timestamped pg_dump in devops/backups/.
# Usage: ./devops/backup-memory.sh
# Cron (daily at 2am): 0 2 * * * /Users/gclyle/GrowDirect/devops/backup-memory.sh

set -e

DOCKER=/usr/local/bin/docker
BACKUP_DIR="$(dirname "$0")/backups"
STAMP=$(date +%Y%m%d_%H%M%S)
DUMP_FILE="gd_memory_${STAMP}.dump"
KEEP_DAYS=14  # retain 2 weeks of backups

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting memory bus backup..."

# Verify postgres is up
if ! $DOCKER exec growdirect_postgres pg_isready -U growdirect -q 2>/dev/null; then
  echo "[ERROR] growdirect_postgres is not ready. Aborting."
  exit 1
fi

# Dump inside container, copy out
$DOCKER exec growdirect_postgres pg_dump \
  -U growdirect growdirect_memory \
  -Fc -f "/tmp/${DUMP_FILE}"

$DOCKER cp "growdirect_postgres:/tmp/${DUMP_FILE}" "${BACKUP_DIR}/${DUMP_FILE}"

SIZE=$(du -sh "${BACKUP_DIR}/${DUMP_FILE}" | cut -f1)
echo "[$(date)] Backup complete: ${BACKUP_DIR}/${DUMP_FILE} (${SIZE})"

# Row count sanity check
ROWS=$($DOCKER exec growdirect_postgres psql -U growdirect -d growdirect_memory \
  -t -A -c "SELECT COUNT(*) FROM alx_memories;")
SEEDS=$($DOCKER exec growdirect_postgres psql -U growdirect -d growdirect_memory \
  -t -A -c "SELECT COUNT(*) FROM seed_embeddings;")
echo "[$(date)] DB state: alx_memories=${ROWS}  seed_embeddings=${SEEDS}"

# Prune old backups
find "$BACKUP_DIR" -name "gd_memory_*.dump" -mtime +${KEEP_DAYS} -delete
echo "[$(date)] Pruned backups older than ${KEEP_DAYS} days."

echo "[$(date)] Done."
