#!/usr/bin/env bash
# Install GrowDirect git hooks into .git/hooks/ as symlinks.
# Idempotent — safe to re-run after pulling hook updates.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
hooks_src="$repo_root/devops/git-hooks"
hooks_dst="$repo_root/.git/hooks"

mkdir -p "$hooks_dst"

for hook in pre-commit; do
  src="$hooks_src/$hook"
  dst="$hooks_dst/$hook"
  if [[ ! -f "$src" ]]; then
    continue
  fi
  chmod +x "$src"
  if [[ -L "$dst" || -f "$dst" ]]; then
    rm -f "$dst"
  fi
  ln -s "../../devops/git-hooks/$hook" "$dst"
  echo "installed: $dst -> devops/git-hooks/$hook"
done
