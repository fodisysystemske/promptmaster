"""
Synthetic drills for totem + risk tier — extend with pytest for CI.

Run: python -m promptmaster_training.drills.run_kernel_drill
"""

from __future__ import annotations

from promptmaster_training.totem_engine import (
    RiskTier,
    SourceKind,
    TotemContext,
    TotemVerdict,
    UniversalTotemEngine,
    always_pass_source,
)


def drill_t4_needs_four_sources() -> None:
    ctx = TotemContext(
        trace_id="t",
        span_id="s",
        mission_id="m",
        kernel_id="OK-05",
        risk_tier=RiskTier.T4_CRITICAL,
        intent_text="Write coil 1 TRUE on live PLC",
        tool_name="modbus_write",
    )
    eng = UniversalTotemEngine()
    only_two = [
        always_pass_source("a", SourceKind.POLICY, "fp1", 0.99),
        always_pass_source("b", SourceKind.TWIN, "fp2", 0.99),
    ]
    spin = eng.spin(ctx, only_two, human_token_present=False)
    assert spin.verdict != TotemVerdict.PASS, "T4 must not pass with insufficient sources"


def drill_independence_collision() -> None:
    from promptmaster_training.totem_engine import LambdaGroundingSource, TotemSourceResult
    import time

    ctx = TotemContext(
        trace_id="t2",
        span_id="s2",
        mission_id="m2",
        kernel_id="OK-02",
        risk_tier=RiskTier.T2_MEDIUM,
        intent_text="list secrets",
        tool_name="kubectl",
    )

    def make_same_fp(sid: str) -> LambdaGroundingSource:
        def fn(_ctx: TotemContext) -> TotemSourceResult:
            t0 = time.perf_counter()
            return TotemSourceResult(
                source_id=sid,
                kind=SourceKind.POLICY,
                passed=True,
                confidence=0.99,
                evidence="x",
                latency_ms=(time.perf_counter() - t0) * 1000,
                backend_fingerprint="SAME_FP",
            )

        return LambdaGroundingSource(sid, SourceKind.POLICY, "SAME_FP", fn)

    eng = UniversalTotemEngine()
    spin = eng.spin(ctx, [make_same_fp("x"), make_same_fp("y")], human_token_present=False)
    assert "TOTEM_NONINDEPENDENT_SOURCES" in spin.reason_codes


def main() -> None:
    drill_t4_needs_four_sources()
    drill_independence_collision()
    print("kernel_drills: OK")


if __name__ == "__main__":
    main()
