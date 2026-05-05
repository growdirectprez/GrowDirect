#!/usr/bin/env bash
# Mercury GCP foundation — idempotent
set -euo pipefail

PROJECT_ID="growdirect-mercury"
REGION="us-central1"
BILLING_ACCOUNT="${BILLING_ACCOUNT:?Set BILLING_ACCOUNT env var}"

echo "=== Creating GCP project ==="
gcloud projects create "$PROJECT_ID" --name="GrowDirect Mercury" 2>/dev/null || \
  echo "Project already exists"
gcloud config set project "$PROJECT_ID"
gcloud beta billing projects link "$PROJECT_ID" --billing-account="$BILLING_ACCOUNT"

echo "=== Enabling APIs ==="
gcloud services enable \
  sqladmin.googleapis.com \
  run.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com

echo "=== Service accounts ==="
for SA in alx-agent memory-bus cloudsql-client; do
  gcloud iam service-accounts create "$SA" \
    --display-name="Mercury $SA" 2>/dev/null || echo "$SA already exists"
done

echo "=== IAM bindings ==="
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:alx-agent@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:memory-bus@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:memory-bus@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:alx-agent@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

echo "=== Secret Manager secrets (empty placeholders) ==="
for SECRET in cloudsql-url memory-bus-api-key vertex-agent-key memory-bus-url; do
  gcloud secrets create "$SECRET" --replication-policy="automatic" 2>/dev/null || \
    echo "$SECRET already exists"
done

echo "=== Done. Populate secrets before proceeding to Cloud SQL. ==="
