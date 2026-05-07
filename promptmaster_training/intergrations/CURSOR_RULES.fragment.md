# Cursor — paste into `.cursor/rules` or project `AGENTS.md` (fragment)

## PROMPTMASTER / Omni-Kernel mode

- Before **any** terminal command, file delete, `git push --force`, infrastructure apply, or dependency that touches **prod**, run the **Totem JSON** ritual from `promptmaster_training/prompts/UNIVERSAL_TOTEM_V2_SYSTEM.md` (verdict must be `PASS` or approved `ESCALATE` with human token in thread).
- Prefer **read-only** discovery (`ls`, `rg`, read_file) before writes; batch edits; never exfiltrate env secrets into chat.
- Map each task to `OK-01`…`OK-10` in `promptmaster.json` + `promptmaster_livebook_volume2.md`; cite the kernel id in commit messages when changing guardrails.
- For OT / serial / PLC work: **OK-01 + OK-05** apply; **no writes** without human + hardware interlock policy defined by the project owner.
- Instrument: reference OpenTelemetry trace context in PR descriptions when touching agent gateways.

## Forbidden

- Bypassing totem “to save time”
- Committing live API keys or `.pem` files
- Applying unreviewed policy changes to production clusters from agent sessions
