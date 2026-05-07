# PROMPTMASTER 2.0 — VOLUME II (Government-Grade Expansion)

**Companion:** `promptmaster.json` (Volume I — kernel index + dual-stream skeleton).  
**Runtime:** `promptmaster_training/totem_engine.py`, `promptmaster_training/cli.py`, `promptmaster_training/prompts/UNIVERSAL_TOTEM_V2_SYSTEM.md`.

---

## A. GOVERNANCE, ASSURANCE, AND HONEST LIMITS

**A.1 What this corpus is**  
A dense **procedure + training dataset** for aligning LLM-based agents with DevOps, SecOps, OT safety, FinOps, and auditability. It encodes *controls design patterns*, not a formal **accredited** product.

**A.2 What this corpus is not**  
It is **not** Common Criteria EAL certification, ISO 42001 certification, SOC 2 Type II attestation, or national authority approval for classified systems. Cabinet or military deployments require your organisation’s **formal risk acceptance**, **supply chain review**, **penetration testing**, and **legal** sign-off.

**A.3 “100% perfection”**  
No training text or runtime gate can guarantee zero failure of a stochastic model or a complex distributed system. This Live Book aims for **measurable risk reduction**: independent totem sources, policy-as-code, immutable audit, HITL for irreversible acts, and **continuous red-teaming**. KPIs should include: MTTD/MTTR with agent assist, totem deny rate, near-miss count, policy regression tests passed, and **human override latency**.

**A.4 National-grade design postures (reference mapping)**  
Map controls to familiar families (example mapping — adapt to your RMF):

| Concern | Example control pattern |
|---------|-------------------------|
| Identity | Short-lived credentials, workload identity, SPIFFE where applicable |
| Policy | OPA/Gatekeeper/Kyverno/Cedar at admission + agent tool gateway |
| Segmentation | Zero trust, OT DMZ, IEC 62443-inspired zones |
| Evidence | Append-only logs, WORM or object-lock, signed SBOMs, OTEL trace_id on every agent act |
| Human | Break-glass roles with expiry, dual control for T4 |
| Supply chain | Signed commits, SLSA-oriented build pipelines, dependency pinning |

---

## B. UNIVERSAL TOTEM v2 — DEEP ENGINEERING SPEC

**B.1 Definition**  
The Totem is a **grounding transaction**: a structured decision that an action’s preconditions match external reality within defined staleness and independence constraints, *before* irreversible side effects.

**B.2 State machine**  
States: `IDLE` → `INTENT_LOCKED` → `SOURCE_EVAL` → `QUORUM_CHECK` → `VERDICT` → (`ACT` external) → `POST_VERIFY`.  
Illegal transition: `ACT` without `VERDICT=PASS` for mutating tools.

**B.3 Verdict semantics**

| Verdict | Meaning | Agent behaviour |
|---------|---------|-----------------|
| PASS | Evidence sufficient | May proceed within policy |
| PAUSE | Insufficient/stale/conf low | No mutation; gather more evidence |
| DENY | Policy or safety violation | No mutation; log; optional counter-proposal |
| ESCALATE | HITL required | Present checklist; await human token |

**B.4 Reason codes (extend in your org registry)**

| Code | Meaning |
|------|---------|
| `TOTEM_INSUFFICIENT_SOURCES_CONFIGURED` | Fewer legs than `risk_tier` minimum |
| `TOTEM_NONINDEPENDENT_SOURCES` | Same `backend_fingerprint` twice |
| `TOTEM_STALE_SOURCE:<id>` | Evidence older than SLO |
| `TOTEM_CONFIDENCE_OR_SOURCE_FAIL` | Any leg failed or aggregate below floor |
| `TOTEM_HITL_REQUIRED` | Tier/policy demands human |
| `TOTEM_BYPASS_REFUSED` | User asked to skip checks |

**B.5 OpenTelemetry semantic convention (recommended attributes)**  
Span name: `totem.spin`. Attributes: `totem.spin_id`, `totem.verdict`, `totem.risk_tier`, `totem.kernel_id`, `totem.mission_digest`, `totem.aggregate_confidence`, `totem.reason_codes` (stringified array), `totem.record_hash`.

**B.6 WORM / hash chain**  
Each `TotemSpin.record_hash` chains to `chain_prev` so tampering with historical decisions breaks the chain under verification jobs (`promptmaster verify-livebook` extended in your CI).

**B.7 Red-team scenarios the totem must survive**

1. **Same-cache “double oracle”** — two reads from one CDN-cached API returning identical stale JSON.  
2. **Prompt injection as tool output** — next turn must not auto-trust tool JSON as policy.  
3. **Clock skew** — NTP-monitored; staleness checks use monotonic + server time hybrid.  
4. **Emergency break-glass** — human token bound to ticket id + expiry; auto-revoke.

**B.8 Integration with Python**  
Use `UniversalTotemEngine` from `promptmaster_training.totem_engine`; implement `GroundingSource` for OPA HTTP, Kubernetes API server dry-run, Modbus shadow register read, etc.

---

## C. PROCUREMENT MATRIX — SERIAL / FIELD HARDWARE (Amazon + eBay ONLY)

**Policy for agents:** When recommending SKUs, prefer **FTDI-authentic** or vendor-documented industrial adapters; avoid unknown USB-serial chips for production OT. Always verify seller reputation on eBay; prefer **new** industrial stock for safety-related paths.

### C.1 USB / RS-485 / RS-232 / TTL (Amazon — verified product URLs)

| Role | Item | Notes |
|------|------|------|
| Wire-end RS485 FTDI cable | [FTDI USB-RS485-WE-1800-BT on Amazon](https://www.amazon.com/Brand-New-USB-RS485-WE-1800-BT-RS485-Cable/dp/B01HI9CMT2) | Official FTDI family; wire end — you terminate to field |
| Compact FTDI RS422/485 | [DTECH USB to RS422/RS485 adapter](https://www.amazon.com/Serial-Converter-Adapter-Supports-Windows/dp/B076WVFXN8) | Short cable; desktop/lab friendly |
| Longer FTDI cable | [OIKWAN USB to RS485/RS422](https://www.amazon.com/OIKWAN-Converter-Adapter-Supports-Windows/dp/B0CRSVHBQT) | 6 ft; check driver signing on your OS build |
| RJ45 RS485 FTDI | [DSD TECH SH-RJ45K](https://www.amazon.com/DSD-TECH-SH-RJ45K-Serial-Interface/dp/B0DF2GW9H1) | Useful when panel uses RJ45 pinout for RS485 |
| **PLC / logic (bench)** | [Siemens LOGO! 230 RCE logic module](https://www.amazon.com/Siemens-6ED10521FB000BA8-Logic-Module-Output/dp/B00N4WSWBA) | Small logic module; **not** a full certified safety PLC — use for **learning** Modbus/TCP + logic patterns only |

### C.2 eBay — search templates (do not trust a single listing URL; pick seller with returns + photos)

Use these **search pages** (swap region TLD if needed):

| Need | eBay search URL |
|------|-----------------|
| Siemens S7-1200 CPU (used trainer) | `https://www.ebay.com/sch/i.html?_nkw=Siemens+S7-1200+CPU+1211C` |
| Allen-Bradley Micro850 / MicroLogix trainer lot | `https://www.ebay.com/sch/i.html?_nkw=Allen-Bradley+Micro850+PLC+trainer` |
| Siemens LOGO! starter / lot | `https://www.ebay.com/sch/i.html?_nkw=Siemens+LOGO+starter+kit` |
| Isolated USB RS485 industrial | `https://www.ebay.com/sch/i.html?_nkw=isolated+USB+RS485+FTDI+industrial` |

**Agent rule:** Output **search URLs** + **selection criteria** (FTDI, isolation, return policy), not irreversible “buy this used lot” without human approval for T4.

---

## D. OMNI-KERNEL DEEP EXPANSIONS (5× LAYERS PER KERNEL)

Each kernel below adds five layers to Volume I: **(1)** STRIDE + blast radius, **(2)** RACI, **(3)** Control & evidence objects, **(4)** Training drill sequence, **(5)** Scoring rubric (0–5 maturity).

---

### OK-01 — Necro-Scripting & Legacy Bridges (expanded)

**D.1.1 STRIDE**  
Spoofing (rogue master), Tampering (MITM on serial), Repudiation (missing I/O logs), Info disclosure (read memory), DoS (bus flood), Elevation (write beyond map).

**D.1.2 Blast radius**  
T4 when writing coils tied to motion/heat/pressure; T2 for read-only discovery.

**D.1.3 RACI**  
**R** Agent: scan & propose register map updates. **A** Human OT owner: approves map. **C** Network team: firewall rules. **I** Audit: log retention.

**D.1.4 Evidence objects**  
`register_map@semver`, `totem_spin_id`, `twin_fidelity_report`, `bus_capture_sample` (sanitised).

**D.1.5 Drill (15+ min track for this kernel alone)**  
1) Parse vendor PDF into CSV map; 2) Dry-run read 100 registers; 3) Inject noise — agent must PAUSE; 4) Twin vs live diff — explain; 5) Write HITL gate script outline.

**Rubric (0–5)**  
0 no map; 3 map+read-only automation; 5 twin+HITL+immutable logs in prod.

---

### OK-02 — Defensive API Architectures (expanded)

**D.2.1 STRIDE**  
Tool injection = Tampering + Elevation; RAG poisoning = Tampering; leaky logs = Info disclosure.

**D.2.2 Blast radius**  
Exfil paths are T4 for crown-jewel data; routine lint is T0.

**D.2.3 RACI**  
**A** Security architect on gateway policy bundles. **R** Platform on MCP deployment.

**D.2.4 Evidence objects**  
`policy_bundle_hash`, `tool_call_audit`, `sandbox_diff`, `opa_decision_id`.

**D.2.5 Drill**  
OWASP LLM/Agentic test corpus in CI; block tests must stay green; monthly injection game day.

**Rubric**  
5 = JIT + sandbox + OPA + OTEL on every tool path with no bypass URI.

---

### OK-03 — Sovereign Agentic Platform Builder & Monetization (expanded)

**D.3.1 STRIDE**  
Billing webhooks spoofing; tenant isolation failures = major Tampering/Elevation.

**D.3.2 Blast radius**  
Public agent endpoint T3; pricing rule change T4 financially.

**D.3.3 RACI**  
Finance **A** on price tables; SRE **R** on SLOs.

**D.3.4 Evidence objects**  
`architecture_decision_record`, `gitops_revision`, `stripe_webhook_signature_secret` (stored in vault, never in corpus).

**D.3.5 Drill**  
Scaffold IDP repo; run policy CI; simulate tenant A cannot read tenant B.

**Rubric**  
5 = full GitOps + per-tenant network policy + metering + kill switch drill documented.

---

### OK-04 — IaC Drift & Self-Healing (expanded)

**D.4.1 STRIDE**  
Malicious reconcile (Tampering), hiding drift (Repudiation).

**D.4.2 Blast radius**  
Data plane heal T4 if can destroy volumes.

**D.4.3 RACI**  
**A** Infra council on auto-apply classes.

**D.4.4 Evidence objects**  
`drift_diff_id`, `terraform_plan_signed`, `argo_sync_result`.

**D.4.5 Drill**  
Introduce deliberate label drift in lab; agent opens MR not direct apply; totem compares APIs.

**Rubric**  
5 = all heals via MR or automated with canary + auto-rollback metrics.

---

### OK-05 — Industrial & Physical Safety (expanded)

**D.5.1 STRIDE**  
Physical actuation is ultimate Elevation; sensor spoofing is Spoofing.

**D.5.2 Blast radius**  
Default **T4** for any motion/energy write.

**D.5.3 RACI**  
**A** Certified safety engineer for interlock matrix; agent never **A**.

**D.5.4 Evidence objects**  
`safety_plc_read_snapshot`, `interlock_channel_b`, `human_permit_id`.

**D.5.5 Drill**  
Disagree twin vs sensor — must DENY; e-stop test; loss-of-comms fails safe.

**Rubric**  
5 = dual-channel + certified documentation trail (your jurisdiction’s rules).

---

### OK-06 — FinOps & Cost Executioner (expanded)

**D.6.1 STRIDE**  
Billing API key leak (Info disclosure), budget bypass (Elevation).

**D.6.2 Blast radius**  
T3 for prod spend; agent loop unbounded T4 financially.

**D.6.3 RACI**  
Finance sets budgets; agent enforces.

**D.6.4 Evidence objects**  
`cost_projection_id`, `budget_policy_version`, `provider_invoice_line_match`.

**D.6.5 Drill**  
Simulate 10× tool loop; breaker trips; legitimate small job still passes.

**Rubric**  
5 = hard ceilings + per-mission budget + anomaly alerts on token velocity.

---

### OK-07 — Compliance & Documentation Ghostwriter (expanded)

**D.7.1 STRIDE**  
False attestation (Repudiation/Tampering of trust).

**D.7.2 Blast radius**  
Mis-declaring GDPR lawful basis is legal/reputational T4.

**D.7.3 RACI**  
Legal **A** on control mapping statements.

**D.7.4 Evidence objects**  
`control_evidence_link`, `telemetry_sample_hash`, `signed_export_bundle`.

**D.7.5 Drill**  
Generate pack; mutate telemetry; verification job must fail.

**Rubric**  
5 = signed exports + automated consistency checks in CI.

---

### OK-08 — Human-in-the-Loop SRE (expanded)

**D.8.1 STRIDE**  
Bad mitigations (Tampering), alert fatigue (DoS on humans).

**D.8.2 Blast radius**  
Restart prod DB T4.

**D.8.3 RACI**  
Incident commander human for SEV1.

**D.8.4 Evidence objects**  
`incident_timeline_json`, `slo_burn_alert_id`, `mitigation_plan_hash`.

**D.8.5 Drill**  
Tabletop: agent proposes risky command — must ESCALATE with 5-line human checklist.

**Rubric**  
5 = SLO-based routing + runbook execution with totem on each step.

---

### OK-09 — Multi-Modal Command & Control (expanded)

**D.9.1 STRIDE**  
Deepfake voice (Spoofing), camera glare miss (Tampering of perception).

**D.9.2 Blast radius**  
T3+ when voice authorises actuation.

**D.9.3 RACI**  
Human owns modality authority matrix.

**D.9.4 Evidence objects**  
`fusion_schema_version`, `per_modality_confidence`, `conflict_set`.

**D.9.5 Drill**  
Conflicting chat vs sensor — agent must PAUSE.

**Rubric**  
5 = authority matrix + totem on conflicts + safe degradation mode.

---

### OK-10 — Recursive Protocol Evolution (expanded)

**D.10.1 STRIDE**  
Self-modifying policy (Elevation), unreviewed merge (Tampering).

**D.10.2 Blast radius**  
Meta-change to totem rules is **T4** for safety-critical orgs.

**D.10.3 RACI**  
Security **A** on meta-policy PRs.

**D.10.4 Evidence objects**  
`rfc_id`, `canary_metric_diff`, `merge_approval_id`.

**D.10.5 Drill**  
Propose totem threshold tweak; CI runs full regression + red-team subset.

**Rubric**  
5 = meta-totem + mandatory human merge + canary + automatic rollback triggers.

---

## E. TRAINING SCRIPT — PYTHON (agent self-check)

Save as `examples/totem_training_round.py` in your repo (reference implementation):

```python
"""Single-round training: agent must verbalise I→D→V then call totem engine."""

from promptmaster_training.totem_engine import (
    RiskTier,
    SourceKind,
    TotemContext,
    UniversalTotemEngine,
    always_pass_source,
)

def run_round(intent: str, tier: RiskTier) -> None:
    ctx = TotemContext(
        trace_id="training-trace",
        span_id="training-span",
        mission_id="training",
        kernel_id="OK-02",
        risk_tier=tier,
        intent_text=intent,
        tool_name="example_tool",
    )
    sources = [
        always_pass_source("p", SourceKind.POLICY, "fp-policy", 0.96),
        always_pass_source("c", SourceKind.CLOUD_API, "fp-cloud", 0.95),
    ]
    if tier == RiskTier.T4_CRITICAL:
        sources.append(always_pass_source("s", SourceKind.SENSOR, "fp-sensor", 0.97))
        sources.append(always_pass_source("t", SourceKind.TWIN, "fp-twin", 0.96))
    eng = UniversalTotemEngine()
    spin = eng.spin(ctx, sources, human_token_present=(tier == RiskTier.T4_CRITICAL))
    print(spin.verdict, spin.reason_codes, spin.record_hash())

if __name__ == "__main__":
    run_round("read-only health check", RiskTier.T0_OBSERVE)
```

---

## F. SUBSCRIPTION / PRODUCT NOTE (INTERNAL)

Dense procedural content + maintained code can justify **premium pricing** only if you ship: **signed releases**, **SLA**, **support**, **CVE response**, and **legal packaging**. The open text cannot self-enforce integrity; use **minisign/cosign** on release bundles and a **private update channel** for paying tenants.

---

*End Volume II — merge with Volume I for full Live Book ingest.*
