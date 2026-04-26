#!/usr/bin/env bash
# Dev helper. Runs from Solex/ root after cd.
set -euo pipefail

# `dirname $0` is devops/scripts/. Go up TWO levels to Solex/.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOLEX_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$SOLEX_ROOT"

COMPOSE="docker compose -f devops/docker-compose.yml"

build_assets() {
  # Gitignored build artifacts that the container's volume mount shadows —
  # must be populated on host before the stack starts.
  if [ ! -d node_modules ]; then
    echo "==> npm install (first run)"
    npm install --silent
  fi
  if [ ! -f solex/static/css/output.css ] || [ tailwind.config.js -nt solex/static/css/output.css ]; then
    echo "==> Building Tailwind CSS"
    npx tailwindcss -i ./solex/static/css/input.css -o ./solex/static/css/output.css --minify
  fi
  if [ ! -f solex/static/js/vendor/alpine.min.js ]; then
    echo "==> Copying Alpine to static/js/vendor/"
    mkdir -p solex/static/js/vendor
    cp node_modules/alpinejs/dist/cdn.min.js solex/static/js/vendor/alpine.min.js
  fi
}

case "${1:-up}" in
  up)
    build_assets
    $COMPOSE up -d
    ;;
  down)
    $COMPOSE down
    ;;
  rebuild)
    build_assets
    $COMPOSE build
    ;;
  logs)
    $COMPOSE logs -f "${2:-web}"
    ;;
  shell)
    $COMPOSE exec web bash
    ;;
  test)
    $COMPOSE exec web pytest "${@:2}"
    ;;
  assets)
    build_assets
    ;;
  *)
    echo "usage: dev.sh up|down|rebuild|logs [svc]|shell|test|assets"
    exit 1
    ;;
esac
