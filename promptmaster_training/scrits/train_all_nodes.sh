#!/usr/bin/env bash
# PROMPTMASTER — sequential training ingest for CI or human rehearsal.
# Requires: python3, optional `wc`, repo root as cwd or first arg.

set -euo pipefail
ROOT="${1:-.}"
cd "$ROOT"

echo "=== PROMPTMASTER Live Book ingest ==="
python3 -m promptmaster_training.cli verify-livebook || python3 -c "from pathlib import Path; import hashlib; p=Path('promptmaster.json'); print('words', len(p.read_text().split())); print('sha256', hashlib.sha256(p.read_bytes()).hexdigest())"
python3 -m promptmaster_training.cli totem-demo

for f in \
  promptmaster.json \
  promptmaster_livebook_volume2.md \
  promptmaster_training/prompts/UNIVERSAL_TOTEM_V2_SYSTEM.md \
  promptmaster_training/integrations/CURSOR_RULES.fragment.md \
  promptmaster_training/integrations/CLAUDE_PROJECT.md \
  promptmaster_training/integrations/GENERIC_LLM_BOOTSTRAP.md
do
  if [[ -f "$f" ]]; then
    echo "[OK] $f ($(wc -w < "$f" 2>/dev/null || echo 0) words)"
  else
    echo "[MISSING] $f" >&2
    exit 2
  fi
done

echo "=== Kernel order drill (echo checklist) ==="
for k in OK-01 OK-02 OK-03 OK-04 OK-05 OK-06 OK-07 OK-08 OK-09 OK-10; do
  echo "  - $k: Interrogate → Decompose → Validate (Totem) → Act → Log outcome"
done

echo "=== Done. Minimum agent read budget: 15 minutes at 200 wpm technical ==="
