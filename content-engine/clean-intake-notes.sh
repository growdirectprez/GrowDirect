#!/bin/bash
rm -f "Brain/raw/processed/angel/screenshot-2026-04-09-at-9-28-37-am.md"
rm -f "Brain/raw/processed/angel/screenshot-2026-04-08-at-1-53-17-pm.md"
rmdir Brain/raw/processed/angel Brain/raw/processed 2>/dev/null
echo "Deleted intake notes and empty dirs"
rm -- "$0"
