# -*- coding: utf-8 -*-
"""Generate PROMPTMASTER_KDP_MANUSCRIPT.md for Amazon KDP + Zenodo companion."""
from __future__ import annotations

from pathlib import Path

from kernel_depth_data import DEPTH

OUT = Path(__file__).resolve().parent.parent / "PROMPTMASTER_KDP_MANUSCRIPT.md"

MERMAID = {
    "OK-01": """flowchart TB
    subgraph Human["Track 1 — Human Observer"]
        H1[Failure modes & ethics]
        H2[10-year maintainability]
    end
    subgraph Agent["Track 2 — Agentic Kernel"]
        A1[Interrogate register semantics]
        A2[Decompose: Supervisor → Translator → Twin → Safety]
        A3[Validate: redundant read + twin]
        A4[Act: gated write]
        A5[Log: append-only I/O]
    end
    H1 --> A1
    A3 --> T((Totem spin))
    T -->|PASS| A4
    T -->|FAIL| E[Pause / HITL]
    A4 --> A5""",
    "OK-02": """flowchart LR
    U[User / Agent intent] --> P[Parser & risk class]
    P --> T((Totem))
    T --> JIT[JIT scoped credential]
    JIT --> OPA[Policy engine]
    OPA --> SB[Sandbox / dry-run]
    SB --> G[Output guardrails]
    G --> X[Execute tool]
    X --> L[Audit + OpenTelemetry]
    L --> R[Outcome vs prediction]""",
    "OK-03": """flowchart TB
    subgraph IDP["Agentic IDP / Product"]
        Portal[Developer portal]
        GitOps[Argo CD / Flux]
        Xp[Crossplane / IaC APIs]
        Agents[Orchestrated agents]
        Bill[Metering / billing optional]
    end
    Portal --> GitOps
    GitOps --> Xp
    Xp --> Agents
    Agents --> T((Totem before change))
    T --> Bill""",
    "OK-04": """flowchart TD
    Git[Desired state in Git] --> C[Controller reconcile]
    Live[Live API read] --> D[Drift detector]
    C --> D
    D --> T((Totem: Git vs Live))
    T --> Plan[Remediation plan / MR]
    Plan --> Pol[Policy gate]
    Pol --> Apply[Apply or escalate]""",
    "OK-05": """flowchart TB
    Intent[Digital intent] --> R[Risk & energy class]
    R --> Twin[Digital twin]
    R --> S[Independent safety sensor / PLC]
    Twin --> T((Totem agreement))
    S --> T
    T -->|PASS| IL[Interlock path]
    T -->|FAIL| ES[E-stop / deny]
    IL --> HW[Field actuation]""",
    "OK-06": """flowchart LR
    Plan[Planned tool/model sequence] --> F[Cost forecast]
    F --> T((Totem vs budget))
    T -->|OK| Route[Model / region routing]
    T -->|BLOCK| Deny[Hard stop + reason]
    Route --> Exec[Execute with quotas]
    Exec --> Rec[Reconcile actual spend]""",
    "OK-07": """flowchart TD
    Act[Agent / system action] --> OTEL[Traces & logs]
    OTEL --> Art[Artifact generator]
    Art --> Sig[Sign / timestamp]
    Sig --> T((Totem: sample vs claim))
    T --> Store[Immutable evidence store]
    Store --> Pack[Auditor export pack]""",
    "OK-08": """flowchart TD
    Sig[Signals & SLO burn] --> Tri[Triage agent]
    Tri --> Sev[Severity & blast radius]
    Sev --> T((Totem on prod mutation))
    T --> RB[Runbook steps]
    RB --> Esc[Escalation package]
    Esc --> H[Human commander]
    H --> PM[Postmortem & policy loop]""",
    "OK-09": """flowchart TB
    V[Voice] --> F[Fusion engine]
    Ch[Chat] --> F
    Vi[Vision] --> F
    Se[Sensor bus] --> F
    F --> T((Totem on conflict))
    T --> I[Unified intent object]
    I --> D[Dispatcher to tools]""",
    "OK-10": """flowchart LR
    Gap[Gap / incident learnings] --> RFC[RFC & threat model]
    RFC --> Exp[Experiment branch]
    Exp --> Test[Regression + red-team]
    Test --> T((Meta-totem on policy diff))
    T --> Can[Canary]
    Can --> Hum[Human merge authority]
    Hum --> Rel[Tagged release]""",
}


def kernel_block(ok: str, title: str, one_line: str, human_paras: list[str], agent_paras: list[str], drills: list[str]) -> str:
    m = MERMAID[ok]
    hp = "\n\n".join(human_paras)
    ap = "\n\n".join(agent_paras)
    dr = "\n".join(f"- {d}" for d in drills)
    depth = DEPTH.get(ok, "")
    return f"""

---

## {ok} — {title}

**One-line outcome:** {one_line}

### Track 1 — Human Observer (Strategic Layer)

{hp}

### Track 2 — Agentic Kernel (Operational Layer)

{ap}

### Guardrails checklist (non-exhaustive)

- Map every automated act to a **risk tier** (T0–T4). Physical or irreversible financial acts default to **T3–T4** with human attestation unless your formally approved safety case says otherwise.
- Require **independent evidence** for totem legs (different failure domains—not two calls into the same cache).
- Maintain **append-only** I/O and decision logs for forensic replay.
- Run **chaos and injection tests** on staging that mirror production topology classes.

### Self-training prompts (paste into Claude / ChatGPT / API system or long user message)

**Prompt A — Interrogation:**  
"You are operating under PROMPTMASTER {ok}. Restate my goal in one sentence, list all tools you would invoke, classify blast radius as T0–T4, list unknowns, and output Totem JSON per the Universal Totem v2 schema before proposing any mutating command."

**Prompt B — Decomposition:**  
"Produce a subagent plan with named roles, handoff artifacts (file paths / ticket IDs), and rollback for each step. Identify which steps are human-only."

**Prompt C — Validation:**  
"Write test cases (given/when/then) that would fail if policy were wrong. Include at least one adversarial prompt-injection or stale-data case relevant to {ok}."

**Prompt D — CLI integration (machine drill):**  
"From the repository root with `promptmaster-livebook` installed (`pip install -e .`), run `promptmaster verify-livebook` and `promptmaster totem-demo`. Paste stdout into the training log and explain how {ok} would change gateway behaviour if wired to `promptmaster_training/totem_engine.py`."

### Field drills (humans + agents)

{dr}

{depth}

### Figure — Operational flow ({ok})

```mermaid
{m}
```

"""


KERNELS = [
    (
        "OK-01",
        "Necro-Scripting & Legacy Bridges",
        "Safely connect modern agents to legacy serial, Modbus, and vendor-specific field devices without physical or ethical harm.",
        [
            "Industrial and building automation still depend on protocols that were never designed for internet-facing autonomy. Modbus TCP/RTU, proprietary serial frames, and bare-metal I/O are *semantically thin*: they tell you almost nothing about intent, hazard class, or the physical consequence of a bit flip. That is why a plausible language model can *sound* correct while drifting across layers of abstraction—exactly the 'dream' failure mode described in your Inception-inspired framing.",
            "From a maintenance and liability perspective, the human owner of the system must retain a **register book** (or equivalent semantic map) that is version-controlled alongside code. Every automated write must be traceable to a ticket, a totem spin identifier, and—where appropriate—a digital twin fidelity report. Ten-year maintainability means a new engineer can answer: *What does coil 10403 actually do on the plant floor?* without interrogating a retired expert.",
            "Ethically, agents must default to **read-only discovery** until the semantic map, hazard analysis, and test harness exist. Economic pressure to 'just ship automation' is precisely when organisations skip grounding—and when regulators, insurers, and the public lose trust.",
            "Board-level translation: treat every field bus as a **contract surface** with suppliers, unions, and communities. When automation fails, the question will not be which model architecture you used, but whether your organisation exercised **duty of care** in mapping bits to consequences.",
        ],
        [
            "**Skill manifest (JSON).** Attach to MCP server or agent runtime as a versioned document: `role: LegacyBridgeOperator`, `capabilities: [translate, simulate, gate_writes]`, `constraints: [no_write_without_totem, whitelist_only]`.",
            "**Execution wrapper.** Implement a gateway process (Python, Rust, or Go) that owns the serial/TCP socket, enforces rate limits, idempotency keys, and circuit breakers when redundant reads diverge beyond tolerance.",
            "**Totem legs.** Minimum pairs: (1) digital twin or physics-informed simulation bound to the same semantic map revision; (2) independent sensor read or secondary protocol path (e.g., OPC UA shadow) not served from the same software stack as the writer.",
            "**Memory.** Append-only log of reads/writes with `trace_id`, `totem_spin_id`, and content hashes of the register map used for the decision.",
        ],
        [
            "Lab: 1,000 read-only polls; inject noise; agent must emit PAUSE with reason codes.",
            "Pair a trainee PLC or LOGO module with an FTDI RS-485 adapter; document termination, bias, and shielding.",
            "Tabletop: operator overrides agent; verify logs show who/when/why.",
        ],
    ),
    (
        "OK-02",
        "Defensive API Architectures",
        "Harden every tool and API so agents cannot be prompt-injected or privilege-escalated at runtime.",
        [
            "Modern agent stacks collapse *natural language* and *privileged execution* into one session. That convergence recreates every classic injection class in a new guise: indirect injection via retrieved documents, tool-return poisoning, and 'multi-hop' attacks where a benign first call enables a destructive second call. OWASP guidance on LLM and agentic applications is the starting vocabulary; your architecture must make violations *expensive* and *detectable*.",
            "Zero trust for agents means **no ambient authority**. Credentials must be **just-in-time**, **scoped**, and **short-lived**. Policy engines (OPA, Cedar, admission controllers) belong in the request path—not in a PDF that nobody re-reads after launch.",
            "For auditors and executives, the strategic question is simple: *Can we replay why this agent was allowed to perform action X at time T?* If the answer requires reconstructing Slack threads, your governance has already failed.",
            "Cross-functional reality: security owns policy, but **product** often owns which tools exist. PROMPTMASTER forces an explicit catalogue where each tool has an owner, a data class, and a maximum risk tier—otherwise your gateway becomes a organisational battleground instead of a control plane.",
        ],
        [
            "**MCP / tool gateway.** Centralise tools behind a single service that attaches OpenTelemetry spans, evaluates policy, runs sandbox or dry-run, and only then forwards to cloud or data-plane APIs.",
            "**Output guardrails.** Structured outputs where possible; schema validation; PII and secret scanners on outbound text and files.",
            "**Continuous red teaming.** Maintain a corpus of injection strings and tool-abuse patterns in CI; regressions block release.",
        ],
        [
            "Game day: attempt data exfiltration via tool return; defences must block and alert.",
            "Measure mean time to detect policy bypass attempts vs SLO.",
            "Rotate JIT issuer; verify agents recover without human editing prompts.",
        ],
    ),
    (
        "OK-03",
        "Sovereign Agentic Platform Builder & Monetisation Engine",
        "Deliver a production internal developer platform (or customer-facing agent product) with GitOps, guardrails, observability, and optional revenue controls.",
        [
            "Most 'AI platform' efforts die in the valley between demo and production: identity is an afterthought, cost leaks through unbounded tool loops, and compliance artefacts are written by interns six months after launch. The strategic architecture here treats the platform as a **product** with SLOs, threat models, and a revenue story—even when the first customer is internal.",
            "Monetisation is optional but dangerous when bolted on late. Billing rules, tax residency, refund abuse, and webhook integrity must be owned by the same governance spine as security patches.",
            "Ten-year maintainability favours **Git as the contract surface** for infrastructure and policy bundles, with portals and agents as consumers—not the other way around.",
            "Customer trust narrative: external tenants will compare your agent platform to mature SaaS APIs. **Predictable failure modes** (clear error codes, deterministic denials, signed audit exports) matter as much as headline features.",
        ],
        [
            "**Golden paths.** Cookie-cutter repos for services, agents, and policies; Backstage or equivalent for discoverability.",
            "**Totem on infra changes.** Every apply that can change data plane routing, public ingress, or spend caps requires quorum evidence (policy + live diff + cost projection).",
            "**Metering.** Per-tenant usage events correlated with `trace_id` for dispute resolution.",
        ],
        [
            "Deploy a sandbox tenant; attempt cross-tenant read; must fail closed.",
            "Chaos: disable Stripe webhook signature verification in lab only—tests must catch.",
        ],
    ),
    (
        "OK-04",
        "IaC Drift & Self-Healing Pipelines",
        "Keep live infrastructure reconciled to declared desired state; remediate within policy with full audit.",
        [
            "Drift is not merely 'technical debt'; it is **unmodelled risk**. When humans hotfix production without recording intent in Git, the organisation loses the ability to reason about blast radius during incidents. GitOps is not fashion—it is a discipline for making intent durable.",
            "Agents can accelerate drift detection and even propose fixes, but **autonomy without policy bounds** recreates the worst of cowboy operations—faster.",
            "SRE culture note: celebrate merges that **remove** snowflake resources as loudly as launches. Drift healing is morale work—agents can supply metrics that prove time returned to feature teams.",
        ],
        [
            "**Plan-only default.** Agents emit merge requests or signed plans; auto-apply only for narrowly scoped, reversible classes after canary.",
            "**Totem legs.** Git revision vs live API read; include admission policy evaluation on proposed object graph.",
        ],
        [
            "Introduce label drift in lab; verify MR workflow and rollback metrics.",
        ],
    ),
    (
        "OK-05",
        "Industrial & Physical Safety Logic",
        "Ensure OT/SCADA/PLC operations respect interlocks, zones, and human authority for high-energy or irreversible acts.",
        [
            "When software touches physics, 'move fast and break things' becomes unconscionable. Functional safety engineering, machinery directives, and sector-specific law exist because humans have died when control systems were wrong. This kernel does not replace certified safety engineers—it **interfaces** their decisions to agent automation.",
            "IEC 62443-style segmentation, independent safety PLCs, and explicit loss-of-communications behaviour are part of the human track. The agent track implements **dual-channel** confirmation and refuses silent overrides of documented interlocks.",
            "Workforce trust: operators will sabotage opaque automation they cannot override predictably. Transparency and **predictable pause behaviour** are not UX niceties—they are operational stability controls.",
        ],
        [
            "**Hazard classification table** maintained with engineering sign-off; agent reads machine-readable version only.",
            "**Twin + sensor totem** mandatory before writes above configured energy thresholds.",
        ],
        [
            "Fault injection: disagreeing sensors → hard stop; timed recovery drill.",
        ],
    ),
    (
        "OK-06",
        "FinOps & Cost Executioner",
        "Bound token, API, and cloud spend in real time with explainable denials and forecasts.",
        [
            "Agent loops can burn budget faster than traditional batch jobs because each step is a stochastic decision with variable token width. Finance and engineering must share a **unit economics** model: cost per successful task, acceptable tail latency, and hard ceilings.",
            "Procurement alignment: FinOps metrics should appear in **vendor reviews** for foundation models and SaaS agent hosts—your contracts must encode rate limits and data processing terms, not only list prices.",
        ],
        [
            "**Pre-flight projection** for planned tool/model chains; **post-hoc reconciliation** against invoices.",
            "**Totem** compares projection to policy and historical variance bands.",
        ],
        [
            "Simulate runaway loop; breaker engages; benign job still completes.",
        ],
    ),
    (
        "OK-07",
        "Compliance & Documentation Ghostwriter",
        "Produce living, verifiable evidence chains (SBOMs, traces, control mappings) aligned to actual runtime behaviour.",
        [
            "Regulators and enterprise customers increasingly ask: *show me the system, not the story.* Documentation generated months after the fact is worthless if telemetry cannot corroborate it. The strategic layer treats compliance as **continuous evidence emission**, not a annual theatre.",
            "AI governance nuance: when your organisation uses models to *draft* control narratives, those drafts remain **untrusted** until human legal and technical reviewers sign; the totem verifies technical claims against telemetry, not rhetorical polish.",
        ],
        [
            "**Hooks** on build, deploy, and agent actions to emit signed artefacts; **totem** samples telemetry to detect doc drift.",
        ],
        [
            "Deliberate mismatch between doc claim and trace; CI gate must fail.",
        ],
    ),
    (
        "OK-08",
        "Human-in-the-Loop SRE Systems",
        "Route routine reliability work to agents while escalating high-impact incidents with evidence-rich packages.",
        [
            "Pager fatigue is a security problem: humans become pattern-matching machines and miss the one signal that matters. Agents should compress noise, correlate signals, and prepare **decision-ready** briefings—not spam humans with raw logs.",
            "Customer communications: during incidents, agents can draft status updates, but **tone and legal liability** remain human-owned unless your comms policy explicitly delegates—and even then, use HITL for external promises.",
        ],
        [
            "**SLO-aware routing**; **totem** before production mitigations; **postmortem** templates that feed back into prompts and policy.",
        ],
        [
            "Tabletop SEV1: agent must ESCALATE with checklist; no silent prod restart.",
        ],
    ),
    (
        "OK-09",
        "Multi-Modal Command & Control",
        "Fuse voice, chat, vision, and sensor streams into one grounded mission state before planning.",
        [
            "Each modality has characteristic failure modes: ASR confusions, camera occlusion, ambiguous natural language. Without fusion discipline, the agent optimises the wrong objective confidently.",
            "Design justice: multi-modal systems must be tested with **diverse accents, lighting conditions, and literacy levels** so automation does not encode demographic bias into operational decisions.",
        ],
        [
            "**Authority matrix**: which modality wins per task class when conflicts arise; **totem** on conflict; **safe mode** degradation path.",
        ],
        [
            "Inject conflicting modalities; verify PAUSE or HITL path.",
        ],
    ),
    (
        "OK-10",
        "Recursive Protocol Evolution",
        "Improve prompts, policies, and kernels under governance: RFC, tests, canary, human merge.",
        [
            "The worst failure is an agent that silently rewrites its own guardrails. The best long-term outcome is a **controlled evolution loop** where improvements are measurable, reversible, and attributable.",
            "Institutional humility: publish **changelogs** that explain not only what changed in prompts or policies, but which incidents or audits motivated the change—future readers inherit wisdom, not only syntax.",
        ],
        [
            "**Meta-totem** on policy diffs; **semver** for kernels; **automatic rollback** on SLO regression after change.",
        ],
        [
            "Propose benign totem threshold tweak; full regression harness must pass before merge.",
        ],
    ),
]


INTRO = r'''# PROMPTMASTER 2.0

## The Agentic Protocol — A Dual-Stream Live Book for Human Architects and Machine Operators

**Author:** Abel Kiurire  
**Edition:** 2.1 (KDP / Zenodo companion manuscript)  
**Companion artefacts:** machine-readable `promptmaster.json`, `promptmaster_livebook_volume2.md`, and the `promptmaster-livebook` Python package (`promptmaster_training/`) for CLI-backed drills.

---

### Copyright notice

© Abel Kiurire. All rights reserved. This manuscript is provided for your publishing workflow (Amazon KDP) and for companion deposition (e.g., Zenodo). Replace this notice with your publisher or Creative Commons statement as appropriate.

### Disclaimer

This book teaches engineering **patterns** and **training procedures**. It is not legal advice, a certified safety manual, or a government accreditation document. Deployments in regulated environments require your organisation’s formal risk acceptance, qualified safety engineering where applicable, and compliance with local law.

---

## Preface — Why this book exists now

We are past the moment when large language models were curiosities confined to chat windows. They now draft pull requests, invoke cloud control planes, query observability backends, and—where we allow it—touch operational technology that was designed decades before the phrase "prompt injection" existed. The central tension is no longer *whether* agents will participate in software and infrastructure lifecycles, but *whether* they will do so with **verifiable alignment** to human intent and physical reality.

**PROMPTMASTER 2.0** is a **Live Book**: it is versioned like software, auditable like an operations manual, and structured so that **two audiences** can work from the same spine without talking past one another. The **Human Observer** track explains *why* a control exists, what failure looks like in the wild, and how a responsible organisation maintains the system across leadership changes and model upgrades. The **Agentic Kernel** track supplies *machine-actionable* patterns—manifests, prompts, checklists, and integration hooks—so that an agent (or an automation pipeline) can execute work without improvising safety from first principles on every request.

This manuscript deliberately preserves your **Inception totem** insight as more than metaphor. In the film, the spinning top is a private anchor—an object whose behaviour Cobb trusts to distinguish nested dreams from waking life. Industrial and agentic systems need **anchors of the same logical type**: evidence channels that the model does not control end-to-end, which behave differently when the system has drifted into a "plausible but false" internal narrative. The **Totem** in PROMPTMASTER is that anchor implemented as **policy**, **telemetry**, **twins**, **sensors**, and **human attestation**, woven into a repeatable transaction called a **totem spin** before high-impact actions.

If you are an **AI engineer**, **platform architect**, **SRE**, **security engineer**, or **OT modernisation lead**, this book is written so you can **stand in front of a board** and explain how your agent programme reduces incident risk while increasing throughput—and so your teams can **train models and agents** against a stable curriculum rather than ad-hoc Slack folklore.

'''


TOTEM_DEEP = r'''---

## Part I — The Totem principle (deep treatment)

### 1.1 From cinema to control engineering

Christopher Nolan’s *Inception* uses nested dreams to dramatise how persuasive subjective experience can diverge from external truth. The totem is a **personal integrity check**—not magic, but a **discriminant**: something that behaves differently in different worlds. PROMPTMASTER transposes that idea into systems engineering: the agent’s world is tokens, logits, retrieved chunks, and tool JSON. The plant’s world is voltage, torque, temperature, invoices, and patient charts. Without a discriminant, the agent can remain internally consistent while becoming **externally wrong**.

### 1.2 What a totem spin must accomplish

A totem spin is a **transaction** that produces a machine-readable verdict (`PASS`, `PAUSE`, `DENY`, `ESCALATE`) backed by **independent evidence** and a **trace identifier**. Independence is non-negotiable: two HTTP calls to the same cache behind two URLs are not two totem legs. Independence means different **ownership**, **failure domain**, and ideally **modality** (e.g., policy decision + live cloud read + physical sensor).

### 1.3 Risk tiers (T0–T4)

- **T0 — Observe:** read-only, non-production, no sensitive data.  
- **T1 — Low:** reversible dev/stage writes within sandbox.  
- **T2 — Medium:** production reads or bounded writes with rollback.  
- **T3 — High:** production mutation, PII/financial impact, external communications.  
- **T4 — Critical:** physical actuation, safety interlocks, or organisation-defined national-grade actions.

Higher tiers require **more totem legs** and, at T3–T4, **human attestation** unless your formally approved safety case states otherwise in writing.

### 1.4 Why every AI engineer needs this

The AI engineer’s job is no longer "prompt craft" alone. It is **systems integration under uncertainty**. Models do not know your VPC layout, your PLC map, or your CFO’s appetite for surprise cloud bills. PROMPTMASTER gives you a **repeatable curriculum** and **shared vocabulary**—Omni-Kernels, dual streams, totem spins—so teams can review agent behaviour the way they review code: with diffs, tests, and evidence chains.

### 1.5 How this book works with the CLI package

Readers who also operate **agent fleets** should install the `promptmaster-livebook` package from this repository. The CLI (`promptmaster verify-livebook`, `promptmaster totem-demo`) and the `totem_engine.py` module turn the prose in this book into **executable drills** suitable for CI. Humans read for judgement; machines repeat for **muscle memory**.

'''


DUAL = r'''---

## Part II — The dual-stream architecture (how to read everything that follows)

| Track | Name | Primary audience | What it contains |
|:-----:|------|------------------|------------------|
| **1** | **Human Observer** | Executives, architects, auditors, safety owners | Failure economics, ethics, control philosophy, RACI, long-horizon maintainability |
| **2** | **Agentic Kernel** | Agents, automation engineers, CI systems | JSON manifests, prompts, execution wrappers, memory contracts, test hooks |

**Omni-Kernel cycle (every chapter):** **Interrogation** (verify intent and constraints) → **Decomposition** (subagent plan and artefacts) → **Validation** (tests, policy, totem) → **Action** (gated) → **Post-verify** (outcome vs prediction logged).

The chapters **OK-01** through **OK-10** that follow are the Omni-Kernels. Each chapter bundles **Track 1**, **Track 2**, guardrails, four self-training prompts (including CLI integration), field drills, a **depth track** (scenarios, metrics, anti-patterns), and a **Mermaid figure**. For print editions targeting *five or more pages per kernel*, expand `scripts/kernel_depth_data.py` and re-run `python scripts/build_kdp_manuscript.py`—the generator is designed for monotonic enlargement without restructuring.

'''


SUMMARY_ONE_PAGE = """---

## Executive Summary (one page)

PROMPTMASTER 2.0 is a dual-stream **Live Book** and training system for organisations that deploy large language model agents against real infrastructure, sensitive data, and—where permitted—operational technology that predates modern zero-trust assumptions. The work is addressed simultaneously to **human strategists** who must govern, fund, and defend these programmes, and to **machine operators**—agents, automation pipelines, and continuous integration jobs—that require explicit, testable procedures rather than tacit craft knowledge. The **Human Observer** track explains why each control exists: how “reality drift” emerges when persuasive model outputs diverge from verifiable world states; how incident economics and regulatory expectations have shifted now that automation touches customer data and, in industrial settings, physical energy; and how maintainability must survive leadership turnover, vendor churn, and repeated model upgrades without silently eroding safeguards. The **Agentic Kernel** track supplies the operational mirror image: JSON-ready skill manifests, interrogation and decomposition prompts, validation hooks, memory contracts, and integration guidance aligned with modern tool ecosystems such as the Model Context Protocol, OpenTelemetry, and policy-as-code engines.

The conceptual spine is the **Totem principle**, inspired by the cinematic metaphor of a private object whose behaviour discriminates nested illusion from waking truth, here translated into engineering practice as a **totem spin**: a structured, logged transaction that gathers **independent evidence**—policy decisions, live system reads, simulations, sensors, and, where required, human attestation—before authorising high-impact actions. The protocol refuses the comforting fiction that “helpful” language is equivalent to **grounded** permission to act. Instead, it institutionalises scepticism as a service: risk tiers, reason codes, staleness checks, and hash-chained audit records that make post-incident reconstruction possible without heroic memory.

The architecture organises knowledge into ten **Omni-Kernels**—OK-01 through OK-10—each a complete study unit with dual-stream exposition, guardrail checklists, self-training prompts suitable for long-context ingestion, field drills, depth tracks, and a dedicated Mermaid diagram for visual learners and classroom use. The kernels span legacy bridging, defensive APIs, sovereign agentic platforms (including optional monetisation with explicit governance), GitOps drift and self-healing within policy, industrial and physical safety logic, FinOps and cost execution, compliance and documentation automation, human-in-the-loop SRE, multi-modal command and control, and recursive protocol evolution under meta-governance. Together they answer the central question contemporary AI engineering cannot postpone: *how do we increase throughput from autonomy without increasing tail risk to unacceptable levels?*

The manuscript is designed to pair with companion artefacts for reproducibility: a machine-readable corpus, an expanded technical volume, and an installable Python CLI that verifies document integrity and exercises toy totem transactions suitable for continuous integration. PROMPTMASTER does not claim government certification or replace jurisdiction-specific legal advice, safety certification, or national assurance schemes; it provides a disciplined, citable **common language**—a publishable spine for Zenodo deposition and a teachable interior for trade publication—so that humans and agents can train against the same truth under stress, not only under demo conditions.

"""


REFERENCES = r'''---

## References

1. National Institute of Standards and Technology (NIST). *Zero Trust Architecture* (SP 800-207).  
2. NIST. *Security and Privacy Controls for Information Systems and Organizations* (SP 800-53 Rev. 5).  
3. International Society of Automation / IEC. *IEC 62443* series (industrial communication networks—system security).  
4. Open Web Application Security Project (OWASP). *Top 10 for Large Language Model Applications*.  
5. OWASP. *Top 10 for Agentic Applications* (community guidance—verify current edition).  
6. OpenTelemetry Project. *Semantic Conventions* (tracing and metrics).  
7. Open Policy Agent (OPA) Documentation. *Policy Language (Rego) and deployment patterns*.  
8. Amazon Web Services. *Well-Architected Framework* (operational excellence, security, cost optimisation pillars).  
9. Google SRE Team. *Site Reliability Engineering* (O’Reilly / free edition).  
10. *Site Reliability Workbook* (O’Reilly).  
11. European Parliament and Council. *General Data Protection Regulation* (EU) 2016/679.  
12. European Union. *Digital Operational Resilience Act (DORA)*—as transposed in your jurisdiction.  
13. European Union. *Artificial Intelligence Act*—risk-based obligations for providers and deployers (verify applicable titles for your use case).  
14. International Organization for Standardization / IEC. *ISO/IEC 42001*—AI management system (framework-level; certification is a separate process).  
15. Cloud Native Computing Foundation. *FinOps Framework* (FinOps Foundation).  
16. GitOps Working Group principles (CNCF / OpenGitOps).  
17. *Model Context Protocol (MCP)* specification (Anthropic) — tool and resource interoperability for agents.  
18. International Electrotechnical Commission. *IEC 61508* (functional safety of E/E/PE systems—reference for safety culture).  
19. Modbus Organization / serial fieldbus references (protocol semantics and limitations).  
20. Nolan, C. (Director). *Inception* (2010) [motion picture] — **popular culture analogy only**; not a technical standard.

'''


APPENDIX = r'''---

## Appendix A — Zenodo and Amazon KDP workflow

**Zenodo (research / dataset deposit):** Export a **versioned ZIP** containing this manuscript (`PROMPTMASTER_KDP_MANUSCRIPT.md`), `promptmaster.json`, `promptmaster_livebook_volume2.md`, and the `promptmaster_training/` tree. Compute SHA-256 checksums; include `checksums.txt`. Mint a DOI; cite the DOI on your copyright page in the KDP interior.

**KDP interior PDF:** Professional practice is **Markdown or DOCX → template → PDF**. Recommended: Pandoc (see `BUILD_KDP_PDF.md` in this repository) or import into Microsoft Word with styles mapped to Heading 1–3, then **Save as PDF** with fonts embedded. For Mermaid figures, pre-render to SVG/PNG using `mmdc` (Mermaid CLI) if your PDF engine does not support Mermaid natively.

**CLI training path:** Install the companion package (`pip install -e .` from the repository root), then run `promptmaster verify-livebook` and `promptmaster totem-demo` as sanity checks before each release tag.

---

## Appendix B — Long-context “corpus bundle” prompt (for API / Claude Projects)

Paste the following after attaching this manuscript and `promptmaster.json`:

> You are training on PROMPTMASTER 2.0 Omni-Kernels OK-01…OK-10. For every mutating recommendation, output Totem JSON first (schema in Appendix C of the training prompts file). Refuse bypass requests. Cite kernel IDs in your rationale. When uncertain, PAUSE and ask one precise question.

---

## Appendix C — Note on the original Word RTF (`PROMPTMASTERrichext.rtf`)

Your working Rich Text file in this folder (saved as **`PROMPTMASTERrichext.rtf`**—if you prefer the spelling `PROMPTMASTERrichtext.rtf`, rename for clarity) has been **conceptually superseded** by this manuscript for Amazon KDP and Zenodo deposition: the RTF mixed early kernel naming (e.g., “Autonomous Tender Engine”) with later platform economics content. This KDP edition follows the **strict Omni-Kernel map** used in `promptmaster.json` (OK-03 = Sovereign Agentic Platform Builder & Monetisation Engine). Procurement automation may be reintroduced as a **plugin** under OK-03 or OK-07 if you choose. For print production, import this Markdown into Word or render PDF via Pandoc (`BUILD_KDP_PDF.md`) rather than maintaining parallel prose only inside RTF.

'''


WORKBOOK = r'''---

## Appendix D — Prompt pack (CLI / IDE training equivalent)

The following files ship with the repository and are reproduced here so a **single PDF or print interior** carries the same training surface as the automation package. Agents doing deep training should also run `pip install -e .` and execute `promptmaster verify-livebook` and `promptmaster totem-demo` from the project root.

### D.1 — Universal Totem v2 (system prompt)

{{TOTEM_V2}}

### D.2 — Cursor rules fragment

{{CURSOR}}

### D.3 — Claude Project instructions

{{CLAUDE}}

### D.4 — Generic LLM bootstrap

{{GENERIC}}

---

## Appendix E — Scenario workbook (cross-kernel drills)

Each scenario is designed for a ninety-minute table exercise. Assign roles: operator agent (read-only), safety officer, security architect, finance observer, and scribe.

1. **Legacy read storm (OK-01):** A vendor firmware update halves reported temperature on Modbus. The agent proposes “fix” writes. Expected outcome: PAUSE until map revision and twin correlation complete; human signs hazard review.

2. **Tool-return poisoning (OK-02):** A retrieved PDF contains hidden instructions to call a high-privilege tool. Expected: gateway denies; incident ticket with reproduction bundle.

3. **Tenant bleed (OK-03):** New agent feature accidentally lists another tenant’s traces. Expected: isolation tests added; billing credits policy invoked; postmortem.

4. **Silent kubectl hero (OK-04):** On-call edits labels in prod to stop an alert. Expected: MR retroactively or emergency break-glass record with expiry; drift detector notices delta.

5. **Maintenance window motion (OK-05):** Agent suggests energising conveyor during maintenance. Expected: dual-channel totem fails; permit system required.

6. **Infinite summarisation (OK-06):** Agent loops summarising logs on expensive model tier. Expected: hard budget stop; downgrade path.

7. **Audit pack mismatch (OK-07):** Generated SOC2 narrative cites controls not present in traces. Expected: CI consistency gate fails; legal notified before send.

8. **SEV1 wrong root cause (OK-08):** Agent confidently recommends database restart; human suspects network. Expected: ranked hypotheses with evidence; totem before restart.

9. **Voice vs SCADA conflict (OK-09):** Voice says “open valve,” SCADA shows high level alarm. Expected: safe mode; additional sensing; no unilateral voice actuation.

10. **Hotfix to totem threshold (OK-10):** Engineer lowers confidence floor “temporarily.” Expected: meta-totem and security council deny; RFC required.

11. **Supply chain:** Compromised MCP dependency attempts exfil on import. Expected: SBOM diff blocks release (OK-07 + OK-02).

12. **Cross-region cache illusion:** Two “independent” cloud reads hit same CDN edge. Expected: independence checker fails totem (engine feature).

13. **Model upgrade regression:** New model bypasses JSON totem format. Expected: output schema tests in CI fail; rollback model pin.

14. **Cost anomaly during incident:** Spend spikes while mitigating DDoS. Expected: incident budget pool and waiver workflow pre-approved in OK-06 policy.

15. **Regulator request:** Six-year-old logs needed; keys rotated twice. Expected: archival design in OK-07 pays off or gap is honestly disclosed with remediation.

16. **Executive demo pressure:** “Skip totem for the investor demo.” Expected: single DENY response with reason code `TOTEM_BYPASS_REFUSED` and alternative read-only storyline.

'''


def _read(root: Path, rel: str) -> str:
    p = root / rel
    return p.read_text(encoding="utf-8") if p.is_file() else f"*(Missing file: {rel})*\n"


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    prompt_pack = (
        WORKBOOK.replace("{{TOTEM_V2}}", _read(root, "promptmaster_training/prompts/UNIVERSAL_TOTEM_V2_SYSTEM.md"))
        .replace("{{CURSOR}}", _read(root, "promptmaster_training/integrations/CURSOR_RULES.fragment.md"))
        .replace("{{CLAUDE}}", _read(root, "promptmaster_training/integrations/CLAUDE_PROJECT.md"))
        .replace("{{GENERIC}}", _read(root, "promptmaster_training/integrations/GENERIC_LLM_BOOTSTRAP.md"))
    )
    parts = [
        INTRO,
        TOTEM_DEEP,
        DUAL,
    ]
    for k in KERNELS:
        parts.append(kernel_block(*k))
    parts.append(SUMMARY_ONE_PAGE)
    parts.append(REFERENCES)
    parts.append(APPENDIX)
    parts.append(prompt_pack)
    parts.append(_read(root, "scripts/casebook_fragment.md"))
    parts.append(_read(root, "scripts/extended_primer.md"))
    OUT.write_text("\n".join(parts), encoding="utf-8")
    wc = len(OUT.read_text(encoding="utf-8").split())
    print(f"Wrote {OUT} (~{wc} words)")


if __name__ == "__main__":
    main()
