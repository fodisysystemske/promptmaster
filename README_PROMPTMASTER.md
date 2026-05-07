# PROMPTMASTER 2.0 — Live Book (installable package)

## Install (local / PyPI path)

```bash
pip install -e .
promptmaster verify-livebook
promptmaster totem-demo
```

## Contents

| Path | Purpose |
|------|---------|
| `PROMPTMASTER_KDP_MANUSCRIPT.md` | **Human-first trade book** (regenerate via `python scripts/build_kdp_manuscript.py`) — Amazon KDP / print; includes dual-stream chapters, Mermaid per kernel, prompts, one-page summary, 20 references |
| `BUILD_KDP_PDF.md` | How to produce **PDF** with Pandoc or Word |
| `promptmaster.json` | Dual-stream Omni-Kernel Live Book (Markdown inside `.json` for single-file ingest) |
| `promptmaster_livebook_volume2.md` | Government-grade expansion: deep totem, 5× kernel depth, hardware matrix |
| `promptmaster_training/totem_engine.py` | Production-style totem quorum engine |
| `promptmaster_training/prompts/` | System prompts for Claude / generic hosts |
| `promptmaster_training/integrations/` | Cursor rules fragment, Claude project text |

## Assurance

This distribution implements **engineering controls** and **training material**. It is **not** a certified product under Common Criteria, ISO 42001 certification, or national accreditation schemes. Deployments for cabinet-level or critical national infrastructure require your organisation’s formal risk acceptance, legal review, and country-specific controls.

## Licence

Replace with your licence before publishing to PyPI.
