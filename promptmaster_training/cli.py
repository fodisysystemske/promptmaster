"""CLI entry point for PROMPTMASTER Live Book ingestion checks and totem drills."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from promptmaster_training.totem_engine import (
    RiskTier,
    SourceKind,
    TotemContext,
    TotemVerdict,
    UniversalTotemEngine,
    always_pass_source,
    sha256_digest,
)
from promptmaster_training import __version__


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def cmd_verify(args: argparse.Namespace) -> int:
    root = _repo_root()
    live = root / "promptmaster.json"
    if not live.is_file():
        print("MISSING: promptmaster.json", file=sys.stderr)
        return 2
    text = live.read_text(encoding="utf-8")
    wc = len(text.split())
    est_min = max(15, wc // 200)  # rough: 200 wpm technical read
    print(f"PROMPTMASTER Live Book: {live}")
    print(f"  Words (approx): {wc}")
    print(f"  Suggested human study time: {est_min}+ minutes")
    print(f"  SHA256: {sha256_digest(text)}")
    training = root / "promptmaster_training"
    if training.is_dir():
        py = list(training.rglob("*.py"))
        print(f"  Training modules: {len(py)} Python files under promptmaster_training/")
    return 0


def cmd_totem_demo(args: argparse.Namespace) -> int:
    ctx = TotemContext(
        trace_id="trace-demo",
        span_id="span-1",
        mission_id="mission-demo",
        kernel_id="OK-02",
        risk_tier=RiskTier.T2_MEDIUM,
        intent_text="Read production configmap X in namespace prod",
        tool_name="kubectl_get",
        tool_args_digest=sha256_digest({"ns": "prod", "name": "X"}),
    )
    s1 = always_pass_source("opa", SourceKind.POLICY, "fp:opa:1", 0.96)
    s2 = always_pass_source("live_api", SourceKind.CLOUD_API, "fp:eks:2", 0.95)
    eng = UniversalTotemEngine(confidence_floor=0.94)
    spin = eng.spin(ctx, [s1, s2], human_token_present=False)
    print(spin.verdict.value, spin.aggregate_confidence, spin.reason_codes)
    return 0 if spin.verdict == TotemVerdict.PASS else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="promptmaster", description="PROMPTMASTER 2.0 Live Book CLI")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("verify-livebook", help="Verify livebook presence and print ingest metrics")
    pv.set_defaults(func=cmd_verify)

    pd = sub.add_parser("totem-demo", help="Run a toy totem spin (CI / sanity)")
    pd.set_defaults(func=cmd_totem_demo)

    args = p.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
