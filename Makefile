# GrowDirect — top-level Makefile.
#
# Repo-wide entry points. Per-project Makefiles still own their domain
# (CanaryGo/Makefile for Go targets, langgraph/Makefile for the LangGraph
# stack). This Makefile holds cross-cutting infrastructure: today, the
# manifest pipeline. Future targets land here when they span multiple
# project trees.

PYTHON      ?= python3
MANIFEST_GEN := services/canary-protocol/manifest/gen
PARSE       := $(MANIFEST_GEN)/parse_manifest.py
RECONCILE   := $(MANIFEST_GEN)/reconcile.py

.PHONY: help manifest manifest-strict manifest-test

help:
	@echo "GrowDirect — top-level targets"
	@echo ""
	@echo "  make manifest         Parse Brain wiki → manifest.yaml, reconcile vs"
	@echo "                        routes-seen.json + openapi.yaml, write drift-report.txt."
	@echo "                        Warn-only by default. (GRO-836 sysadmin module.)"
	@echo ""
	@echo "  make manifest-strict  Same, but exits non-zero on hard-fail validation rules"
	@echo "                        and Phase-1 Gate failure. Phase 4 wires this into CI."
	@echo ""
	@echo "  make manifest-test    Run the pytest suite for parse_manifest + reconcile."
	@echo ""
	@echo "Per-project targets live in:"
	@echo "  CanaryGo/Makefile    (Go: build / test / sqlc-gen / db-reset / dev)"
	@echo "  langgraph/Makefile   (LangGraph: agent + tooling)"

manifest:
	@$(PYTHON) $(PARSE)
	@$(PYTHON) $(RECONCILE)

manifest-strict:
	@$(PYTHON) $(PARSE) --strict
	@$(PYTHON) $(RECONCILE) --strict

manifest-test:
	@cd $(MANIFEST_GEN) && $(PYTHON) -m pytest -q
