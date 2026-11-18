#!/bin/bash
# Headless entry point for Blue Hammer. Starts the orchestrator, which picks
# the next stage, delegates to specialists, and commits only if the quality
# gate passes. Never force-push. Never read .env or Keychain secrets.
set -euo pipefail
cd "$(dirname "$0")/.."
exec claude -p --agent bh-orchestrator --permission-mode bypassPermissions \
  "Run the Blue Hammer orchestrator (bh-orchestrator). Read .claude/agents/HARD-RULES.md, AUDIT-2026-11-18.md, AGENT-LOG.md and docs/brand.md. Pick the next stage, break it into tasks, delegate to the specialist subagents (bh-designer, bh-seo-content, bh-images, bh-qa), run the quality gate, and only then commit and push to main (fast-forward only). Do not ask the owner questions you can answer yourself. Log the run in AGENT-LOG.md and list Needs Rodrigo items. Do not force-push, hard-reset, wipe, or read .env or Keychain secrets."
