#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-up}" in
  up)    docker compose -f devops/docker-compose.yml up -d ;;
  down)  docker compose -f devops/docker-compose.yml down ;;
  logs)  docker compose -f devops/docker-compose.yml logs -f "${2:-web}" ;;
  shell) docker compose -f devops/docker-compose.yml exec web bash ;;
  test)  docker compose -f devops/docker-compose.yml exec web pytest "${@:2}" ;;
  *) echo "usage: dev.sh up|down|logs [svc]|shell|test" && exit 1 ;;
esac
