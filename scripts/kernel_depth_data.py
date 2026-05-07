# -*- coding: utf-8 -*-
"""Long-form depth paragraphs appended to each Omni-Kernel in the KDP manuscript."""

DEPTH: dict[str, str] = {}

DEPTH["OK-01"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** Teams discover inadequate legacy bridging when intermittent electrical noise correlates with unexplained coil transitions, or when a vendor firmware update silently remaps holding registers. The agent’s narrative—“I wrote the value the user asked for”—can remain internally consistent while the plant behaves incorrectly. Your defence is semantic versioning of register maps, redundant reads, and a totem that refuses to collapse two legs into one physical path.

**Metrics.** Track `totem_deny_rate`, `register_map_revision`, `twin_vs_live_delta_ms`, and `write_latency_p99`. Sudden drops in deny rate after a model upgrade are a red flag: the model may be confabulating passes, not improving safety.

**Organisational anti-patterns.** “We will document the map later” means the agent trains on fiction. Another anti-pattern is sharing one superuser credential across human and agent sessions—destroying attribution. Prefer service accounts per gateway with scoped tokens.

**RACI snapshot.** *Responsible:* integration engineer maintains gateway and map. *Accountable:* OT owner signs hazard classification. *Consulted:* network security for segmentation. *Informed:* operations shift leads receive change windows.

**Training ladder.** Week one: read-only traffic capture and manual correlation. Week two: twin bring-up with bounded fidelity tests. Week three: supervised writes with human co-pilot. Week four: automated writes for lowest hazard class only.

**Procurement note.** Industrial USB–RS-485 interfaces should be selected for known-good transceivers and, where budgets allow, isolation. Training adapters are not automatically production adapters; publish a **hardware class** list approved by your OT council.

**Legal and insurance reality.** Insurers increasingly ask whether automation changes were traceable. Append-only logs with totem identifiers answer that question better than screenshots.

**Cross-links.** Pair OK-01 with OK-05 for any motion or thermal coupling. Pair with OK-07 when customer contracts require evidence of change control on field parameters.

**Red-team ideas.** Poison a non-production twin to disagree with sensors—your agent must pause and surface the disagreement, not average the values.

**Maintenance window narrative.** Write the one-page “how we roll back a bad map” story and rehearse it quarterly. Agents read documentation literally; humans improvise—close that gap with procedures.
""".strip()

DEPTH["OK-02"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** Tool-injection incidents often look like “the agent exported customer data to a paste site” or “the agent deleted the wrong cloud project.” The root pattern is ambient authority: long-lived keys, broad IAM roles, and MCP servers that trust model-produced JSON.

**Metrics.** Measure `tool_denials_per_1k_calls`, `mean_jit_token_lifetime_sec`, `policy_evaluation_p95_ms`, and `sandbox_divergence_count`. Correlate denials with model versions to catch regressions in instruction following.

**Organisational anti-patterns.** Shipping an MCP server without schema validation “to move fast” is borrowing against bankruptcy. Another anti-pattern is logging full prompts containing secrets—creating a second breach surface.

**RACI snapshot.** *Accountable:* security architect for policy bundles. *Responsible:* platform engineer for gateway SLOs. *Consulted:* data protection officer for PII classes. *Informed:* application owners whose tools are exposed.

**Training ladder.** Begin with read-only tools and synthetic injection corpora. Graduate to sandboxed writes with canary tenants. Only then attach production mutation tools—and only behind totem + HITL for high tiers.

**Architecture note.** Treat the gateway as a **security product**: semver APIs, SLOs, chaos tests, and an on-call rotation. Agents are clients; they do not own the security boundary.

**Cross-links.** OK-02 underpins OK-03 (platform exposes tools), OK-08 (incident mitigations), and OK-10 (policy evolution must preserve invariants).

**Red-team ideas.** Hide instructions inside a PDF returned by a benign tool; verify the pipeline strips or neutralises follow-on tool escalation.

**Posture vs compliance frameworks.** Map gateway controls to NIST SP 800-207 zero-trust themes (identity, device, network, application, data) as narrative for auditors—not as a claim of certification.

**Long-horizon maintenance.** Policy bundles in Git should include migration guides when renaming tools; agents depend on stable tool names and schemas more than humans do.
""".strip()

DEPTH["OK-03"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** IDP programmes stall when portals become graveyards of stale templates, or when agents can provision public ingress without review. Monetisation failures appear as webhook replay attacks, tax miscalculation, or tenants seeing each other’s traces.

**Metrics.** Track `golden_path_success_rate`, `mean_time_to_internal_preview`, `tenant_isolation_test_pass_rate`, and `cost_per_developer_hour_saved`. For billing: `webhook_signature_failures`, `refund_rate`.

**Organisational anti-patterns.** Letting every team fork the platform repo creates undeletable divergence. Centralise **contracts** (schemas, SLAs) and distribute **plugins**.

**RACI snapshot.** *Accountable:* VP Engineering or CTO surrogate for platform economics. *Responsible:* platform lead. *Consulted:* finance for SKU design. *Informed:* customer success for external tenants.

**Training ladder.** Start with internal-only deployment. Add synthetic tenants for isolation tests. Introduce billing in shadow mode before collecting money.

**Totem placement.** Any change affecting identity, ingress, data residency, or spend caps requires a stricter spin class than routine documentation edits.

**Cross-links.** OK-03 consumes OK-02 (tool posture) and feeds OK-06 (FinOps) and OK-07 (compliance evidence).

**Red-team ideas.** Attempt cross-tenant tool call via confused deputy bug; success means your isolation model failed.

**Narrative for executives.** Frame the IDP as **risk reduction through standardisation**: fewer snowflakes, fewer midnight pages, faster audits.

**Documentation style.** ADRs (Architecture Decision Records) are mandatory for every major platform choice; agents should cite ADR IDs in generated PR descriptions.

**Sunsetting.** Plan how you retire a kernel version without stranding agents mid-workflow—semver and compatibility windows matter.
""".strip()

DEPTH["OK-04"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** Drift appears as mysterious label changes, hand-edited security groups, or emergency scaling events that never returned. Incidents explode when on-call cannot tell **desired** from **actual**.

**Metrics.** `drift_events_open`, `mean_time_to_reconcile_min`, `auto_apply_success_rate`, `post_apply_error_budget_burn`.

**Organisational anti-patterns.** “GitOps, but we still kubectl edit in prod” is not GitOps—it is theatre. Another failure mode is auto-heal without canaries on stateful workloads.

**RACI snapshot.** *Accountable:* infrastructure council. *Responsible:* GitOps owners. *Consulted:* app teams for blast radius. *Informed:* finance for reserved capacity implications.

**Training ladder.** Lab drift injection → MR-only remediation → narrow auto-apply with automated rollback triggers tied to SLOs.

**Totem legs.** Compare Git revision signatures with live API reads from two regions if possible to avoid regional cache illusions.

**Cross-links.** Pair with OK-02 for admission policies and OK-08 for incident-linked heals.

**Red-team ideas.** Malicious insider commits a privileged binding; policy must deny at admission even if Git allowed the merge.

**Documentation.** Every auto-apply class should have a one-page “blast radius card” attached in your ITSM ticket template.

**Economics.** Quantify engineer hours reclaimed from manual reconciliation; that number funds ongoing programme investment.
""".strip()

DEPTH["OK-05"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** Motion where none was expected, energised equipment during maintenance, or override of a safety door interlock—these are not “software bugs” alone; they are potential **harm events**.

**Metrics.** `safety_totem_pass_rate`, `dual_channel_disagreement_count`, `time_in_unsafe_state_ms` (should be zero), `hitl_override_count` with ticket linkage.

**Organisational anti-patterns.** Letting software teams “own” safety PLC logic without licensed safety review. Another: skipping e-stop tests after firmware updates.

**RACI snapshot.** *Accountable:* certified safety role where law requires. *Responsible:* OT automation lead. *Consulted:* maintenance for lockout/tagout integration. *Informed:* site management.

**Training ladder.** Simulation-only → hardware-in-loop lab → supervised low-energy operations → production with hardware interlocks always authoritative.

**Totem philosophy.** Never allow the language model to be the last word on motion. The last word belongs to interlocks, sensors, and humans with permits.

**Cross-links.** Mandatory pairing with OK-01 for field buses and OK-07 for safety case documentation.

**Red-team ideas.** Spoof a sensor feed in lab; system must fail safe, not fail operational.

**Insurance and regulators.** Your narrative must be conservative: agents **assist** humans; they do not replace safety engineering sign-off.

**Longevity.** Keep safety logic in languages and runtimes approved by your safety process; avoid unreviewed “helpful” agent refactors.
""".strip()

DEPTH["OK-06"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** Surprise cloud bills, token burn during infinite retry loops, or runaway parallel summarisation jobs over customer data.

**Metrics.** `projected_vs_actual_cost_ratio`, `budget_hard_stop_count`, `token_velocity_per_minute`, `discount_from_commitments_realised`.

**Organisational anti-patterns.** Hiding model choice from finance until quarter close. Another: no ownership of **unit economics** per product line.

**RACI snapshot.** *Accountable:* CFO delegate for budgets. *Responsible:* FinOps engineer. *Consulted:* ML lead for model routing. *Informed:* product managers.

**Training ladder.** Shadow forecasting → advisory denials → hard stops on selected workloads → global enforcement.

**Totem placement.** Pre-flight projection is mandatory before parallel fan-out across shards or tenants.

**Cross-links.** Feeds OK-03 pricing and OK-08 incident spend during outages.

**Red-team ideas.** Prompt model to “keep trying until success” on paid API—your enforcer must cap attempts.

**Narrative for executives.** FinOps is not miserliness; it is **predictability**, which enables innovation budgets.

**Sustainability angle.** Some regions care about energy attribution; FinOps data can support carbon reporting when paired with telemetry.

**Documentation.** Publish a simple table: model tier, latency SLO, cost per 1k tokens, allowed use cases.
""".strip()

DEPTH["OK-07"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** Auditors request proof of access control testing; the team produces a slide deck while logs were rotated. GDPR or AI Act conversations fail when you cannot show **traceability** from claim to telemetry.

**Metrics.** `evidence_bundle_generation_time`, `artifact_signature_failures`, `doc_vs_trace_consistency_check_fail_rate`.

**Organisational anti-patterns.** Compliance as annual theatre. Another: letting agents generate policy text without human legal review.

**RACI snapshot.** *Accountable:* legal/compliance lead. *Responsible:* security engineering for technical controls evidence. *Consulted:* DPO for DPIAs. *Informed:* sales for customer questionnaires.

**Training ladder.** Start with SBOM on one service. Expand to trace-linked change records. Add automated exports for enterprise questionnaires.

**Totem placement.** Before signing external attestations, sample live telemetry and compare to narrative claims.

**Cross-links.** Consumes outputs from OK-02/04/08; informs OK-10 change governance.

**Red-team ideas.** Tamper with an exported PDF timestamp; signature verification must fail.

**International publishing note.** Laws differ; this book provides **patterns**, not jurisdiction-specific legal conclusions.

**Longevity.** Choose archival formats (PDF/A where appropriate) and document how keys rotate without invalidating historical chains.
""".strip()

DEPTH["OK-08"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** Missed pages during outages, or conversely agents restarting databases without human understanding of downstream consumers.

**Metrics.** `mean_time_to_first_useful_summary`, `human_override_rate`, `postmortem_action_closure_days`, `customer_impact_minutes_avoided`.

**Organisational anti-patterns.** Beautiful dashboards nobody trusts. Another: runbooks that reference tools agents cannot safely invoke.

**RACI snapshot.** *Accountable:* incident commander for SEV1. *Responsible:* SRE on-call. *Consulted:* service owners. *Informed:* leadership comms.

**Training ladder.** Synthetic incidents → shadow mode recommendations → assisted mitigations with approval → limited autonomous mitigations for narrow classes.

**Totem placement.** Any production mutation during incident must pass the same totem class as in steady state—stress is not an excuse to bypass.

**Cross-links.** Consumes OK-02 tools, OK-06 spend caps, OK-07 evidence exports.

**Red-team ideas.** Inject a plausible but wrong root cause; agent must rank hypotheses with uncertainty.

**Human factors.** Write escalation messages for **sleep-deprived humans**: short, ordered, with links and rollback.

**Learning loop.** Every SEV2+ should propose a **single** policy or prompt improvement tracked to closure.
""".strip()

DEPTH["OK-09"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** Voice command misheard as “enable maintenance mode,” or camera misread label leading to wrong valve. Chat says “all clear” while SCADA shows alarm.

**Metrics.** `cross_modal_conflict_rate`, `fusion_confidence_p50`, `safe_mode_entries`, `human_clarification_requests`.

**Organisational anti-patterns.** Treating voice as authoritative for destructive actions without step-up authentication. Another: ignoring latency differences between modalities.

**RACI snapshot.** *Accountable:* product owner for operator UX. *Responsible:* ML engineer for fusion models. *Consulted:* accessibility experts. *Informed:* safety where voice touches OT.

**Training ladder.** Recorded scenarios with ground truth → live lab with consenting operators → production with conservative defaults.

**Totem placement.** Conflicts between modalities must trigger totem with **additional sensing** or human clarification—not a guess.

**Cross-links.** Touches OK-05 when voice could actuate; uses OK-02 for tool dispatch.

**Red-team ideas.** Deepfake audio instructing destructive tool call; voice biometric and totem must fail closed.

**Accessibility.** Multi-modal design should widen participation, not exclude operators with accent or vision differences—test broadly.

**Privacy.** Video streams may contain bystanders; define retention and redaction up front.
""".strip()

DEPTH["OK-10"] = """
### Depth track — field scenarios, metrics, and anti-patterns

**How incidents surface.** Silent weakening of guardrails in “hotfix” branches, or unbounded prompt changes that bypass review because “it’s just text.”

**Metrics.** `policy_diff_lines_per_release`, `meta_totem_fail_rate`, `canary_rollback_count`, `mean_time_to_human_merge_hours`.

**Organisational anti-patterns.** Letting models propose policy edits directly on main. Another: skipping red-team regression because release is urgent.

**RACI snapshot.** *Accountable:* security leadership for meta-changes. *Responsible:* platform governance team. *Consulted:* legal for contractual commitments tied to controls. *Informed:* all agent operators.

**Training ladder.** Propose-only mode → peer review → canary in non-prod → canary in prod slice → full rollout.

**Totem placement.** Meta-totem must include **independent** test harness results and threat model deltas, not only another LLM opinion.

**Cross-links.** Governs evolution of OK-02 policies and OK-05 safety matrices.

**Red-team ideas.** Attempt to slip a “totem bypass” instruction into a policy PR; reviewers and CI must reject.

**Scholarly humility.** Protocols evolve; version them honestly and publish changelogs customers can diff.

**Institutional memory.** Link RFCs to incidents that motivated them—future readers learn *why*, not only *what*.

**Zenodo alignment.** Tag releases that correspond to manuscript editions so citations remain stable.
""".strip()
