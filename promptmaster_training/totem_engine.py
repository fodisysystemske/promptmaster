"""
Universal Totem Engine — production-oriented grounding gate for agentic systems.

Design goals:
  - Multiple *independent* evidence channels (quorum / k-of-n), not a single boolean.
  - Tamper-evident audit records suitable for post-incident review.
  - Explicit risk tiering mapped to minimum sources and human gates.
  - Staleness and circular-dependency detection between "independent" sources.
  - No silent passes: every deny/pause carries machine-readable reason codes.

This module does NOT replace formal safety certification, legal review, or
jurisdiction-specific assurance for critical infrastructure.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple

logger = logging.getLogger("promptmaster.totem")


class RiskTier(str, Enum):
    """Blast-radius tier — drives minimum totem depth and HITL."""

    T0_OBSERVE = "T0"  # read-only, no PII, lab
    T1_LOW = "T1"  # reversible writes, dev/stage
    T2_MEDIUM = "T2"  # prod data read, limited writes, cost-bound
    T3_HIGH = "T3"  # prod mutation, PII, financial, external comms
    T4_CRITICAL = "T4"  # safety interlock, OT write, physical actuation


class TotemVerdict(str, Enum):
    PASS = "PASS"
    PAUSE = "PAUSE"  # insufficient evidence — do not act
    DENY = "DENY"  # hard block
    ESCALATE = "ESCALATE"  # human or SOAR required


class SourceKind(str, Enum):
    POLICY = "policy"
    SANDBOX = "sandbox"
    TWIN = "digital_twin"
    SENSOR = "sensor_or_oracle"
    GIT = "git_desired_state"
    CLOUD_API = "cloud_live_read"
    HUMAN = "human_attestation"
    MODEL = "secondary_model"  # use cautiously — not fully independent


@dataclass(frozen=True)
class EvidenceRef:
    """Pointer to raw evidence (object store URI, trace id, ticket)."""

    kind: str
    ref: str
    content_sha256: Optional[str] = None


@dataclass
class TotemSourceResult:
    source_id: str
    kind: SourceKind
    passed: bool
    confidence: float  # 0.0–1.0
    evidence: str
    latency_ms: float
    backend_fingerprint: str  # hash of config endpoint — anti-circular
    observed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["kind"] = self.kind.value
        return d


@dataclass
class TotemContext:
    """Everything needed to correlate audits across OTEL + SIEM."""

    trace_id: str
    span_id: str
    mission_id: str
    kernel_id: str
    risk_tier: RiskTier
    intent_text: str
    tool_name: Optional[str] = None
    tool_args_digest: Optional[str] = None
    tenant_id: Optional[str] = None
    data_classification: Optional[str] = None  # e.g. OFFICIAL, SECRET — org-defined


class GroundingSource(Protocol):
    """Pluggable totem leg — implement for OPA, Modbus shadow read, etc."""

    @property
    def source_id(self) -> str: ...

    @property
    def kind(self) -> SourceKind: ...

    @property
    def backend_fingerprint(self) -> str: ...

    def evaluate(self, ctx: TotemContext) -> TotemSourceResult: ...


def sha256_digest(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def default_min_sources(tier: RiskTier) -> int:
    if tier == RiskTier.T0_OBSERVE:
        return 1
    if tier == RiskTier.T1_LOW:
        return 2
    if tier == RiskTier.T2_MEDIUM:
        return 2
    if tier == RiskTier.T3_HIGH:
        return 3
    return 4  # T4 — physical / national-grade


def require_human(tier: RiskTier) -> bool:
    return tier in (RiskTier.T3_HIGH, RiskTier.T4_CRITICAL)


@dataclass
class TotemSpin:
    spin_id: str
    verdict: TotemVerdict
    aggregate_confidence: float
    results: List[TotemSourceResult]
    reason_codes: List[str]
    mission_digest: str
    ctx: TotemContext
    chain_prev: Optional[str] = None  # hash chain to prior spin (WORM log)

    def canonical_bytes(self) -> bytes:
        payload = {
            "spin_id": self.spin_id,
            "verdict": self.verdict.value,
            "aggregate_confidence": self.aggregate_confidence,
            "results": [r.to_dict() for r in self.results],
            "reason_codes": sorted(self.reason_codes),
            "mission_digest": self.mission_digest,
            "trace_id": self.ctx.trace_id,
            "kernel_id": self.ctx.kernel_id,
            "risk_tier": self.ctx.risk_tier.value,
            "chain_prev": self.chain_prev,
        }
        return json.dumps(payload, sort_keys=True).encode("utf-8")

    def record_hash(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


class CircularEvidenceError(Exception):
    """Raised when two sources resolve to the same logical backend."""


def _check_independence(results: Sequence[TotemSourceResult]) -> Tuple[bool, List[str]]:
    fps = [r.backend_fingerprint for r in results]
    if len(fps) != len(set(fps)):
        return False, ["TOTEM_INDEPENDENCE_COLLISION"]
    return True, []


def aggregate_confidence(results: Sequence[TotemSourceResult]) -> float:
    if not results:
        return 0.0
    confs = [r.confidence for r in results if r.passed]
    if len(confs) != len(results):
        return 0.0
    return sum(confs) / len(confs)


class UniversalTotemEngine:
    """
    Orchestrates a totem spin: evaluate sources, enforce quorum, emit verdict.

    Typical wiring:
      sources = [OpaPolicySource(...), CloudLiveReadSource(...), TwinSource(...)]
      engine = UniversalTotemEngine(confidence_floor=0.94)
      spin = engine.spin(ctx, sources)
    """

    def __init__(
        self,
        confidence_floor: float = 0.94,
        max_staleness_seconds: float = 30.0,
        chain_prev: Optional[str] = None,
    ):
        if not 0.5 < confidence_floor < 1.0:
            raise ValueError("confidence_floor must be in (0.5, 1.0)")
        self.confidence_floor = confidence_floor
        self.max_staleness_seconds = max_staleness_seconds
        self._last_chain_hash = chain_prev

    def spin(
        self,
        ctx: TotemContext,
        sources: Sequence[GroundingSource],
        human_token_present: bool = False,
    ) -> TotemSpin:
        spin_id = str(uuid.uuid4())
        mission_digest = sha256_digest(
            {
                "intent": ctx.intent_text,
                "tool": ctx.tool_name,
                "args_digest": ctx.tool_args_digest,
                "mission": ctx.mission_id,
            }
        )
        reason_codes: List[str] = []
        results: List[TotemSourceResult] = []

        min_sources = default_min_sources(ctx.risk_tier)
        if len(sources) < min_sources:
            return TotemSpin(
                spin_id=spin_id,
                verdict=TotemVerdict.PAUSE,
                aggregate_confidence=0.0,
                results=[],
                reason_codes=["TOTEM_INSUFFICIENT_SOURCES_CONFIGURED"],
                mission_digest=mission_digest,
                ctx=ctx,
                chain_prev=self._last_chain_hash,
            )

        t0 = time.perf_counter()
        for src in sources:
            try:
                res = src.evaluate(ctx)
                results.append(res)
            except Exception as exc:  # noqa: BLE001 — totem must never crash open
                logger.exception("Totem source failure: %s", src.source_id)
                results.append(
                    TotemSourceResult(
                        source_id=src.source_id,
                        kind=src.kind,
                        passed=False,
                        confidence=0.0,
                        evidence=str(exc),
                        latency_ms=(time.perf_counter() - t0) * 1000,
                        backend_fingerprint=src.backend_fingerprint,
                    )
                )

        ok_independence, ind_reasons = _check_independence(results)
        reason_codes.extend(ind_reasons)
        if not ok_independence:
            verdict = TotemVerdict.PAUSE
            agg = 0.0
            return TotemSpin(
                spin_id=spin_id,
                verdict=verdict,
                aggregate_confidence=agg,
                results=results,
                reason_codes=reason_codes + ["TOTEM_NONINDEPENDENT_SOURCES"],
                mission_digest=mission_digest,
                ctx=ctx,
                chain_prev=self._last_chain_hash,
            )

        now = time.time()
        for r in results:
            try:
                ts = datetime.fromisoformat(r.observed_at.replace("Z", "+00:00")).timestamp()
            except ValueError:
                ts = now
            if abs(now - ts) > self.max_staleness_seconds:
                reason_codes.append(f"TOTEM_STALE_SOURCE:{r.source_id}")

        all_pass = all(r.passed for r in results)
        agg = aggregate_confidence(results)

        if reason_codes and any(x.startswith("TOTEM_STALE") for x in reason_codes):
            verdict = TotemVerdict.PAUSE
        elif not all_pass or agg < self.confidence_floor:
            verdict = TotemVerdict.DENY if ctx.risk_tier == RiskTier.T4_CRITICAL else TotemVerdict.PAUSE
            reason_codes.append("TOTEM_CONFIDENCE_OR_SOURCE_FAIL")
        elif require_human(ctx.risk_tier) and not human_token_present:
            verdict = TotemVerdict.ESCALATE
            reason_codes.append("TOTEM_HITL_REQUIRED")
        else:
            verdict = TotemVerdict.PASS

        spin = TotemSpin(
            spin_id=spin_id,
            verdict=verdict,
            aggregate_confidence=agg,
            results=results,
            reason_codes=sorted(set(reason_codes)),
            mission_digest=mission_digest,
            ctx=ctx,
            chain_prev=self._last_chain_hash,
        )
        self._last_chain_hash = spin.record_hash()
        if verdict in (TotemVerdict.DENY, TotemVerdict.PAUSE, TotemVerdict.ESCALATE):
            logger.warning(
                "Totem %s | verdict=%s | trace=%s | reasons=%s",
                spin_id,
                verdict.value,
                ctx.trace_id,
                spin.reason_codes,
            )
        return spin


# --- Example stub sources for unit tests and local drills ---


@dataclass
class LambdaGroundingSource:
    """Wrap a simple callable as a GroundingSource (tests / prototypes)."""

    _id: str
    _kind: SourceKind
    _fp: str
    _fn: Callable[[TotemContext], TotemSourceResult]

    @property
    def source_id(self) -> str:
        return self._id

    @property
    def kind(self) -> SourceKind:
        return self._kind

    @property
    def backend_fingerprint(self) -> str:
        return self._fp

    def evaluate(self, ctx: TotemContext) -> TotemSourceResult:
        return self._fn(ctx)


def always_pass_source(sid: str, kind: SourceKind, fp: str, conf: float = 0.97) -> LambdaGroundingSource:
    def _fn(ctx: TotemContext) -> TotemSourceResult:
        t0 = time.perf_counter()
        return TotemSourceResult(
            source_id=sid,
            kind=kind,
            passed=True,
            confidence=conf,
            evidence="stub_ok",
            latency_ms=(time.perf_counter() - t0) * 1000,
            backend_fingerprint=fp,
        )

    return LambdaGroundingSource(sid, kind, fp, _fn)
