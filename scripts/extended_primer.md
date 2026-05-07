---

## Appendix G — Glossary, interview questions, and examiner rubric

### G.1 — Glossary (selected)

- **Omni-Kernel:** A complete study unit combining human strategy and agentic procedure for one domain of risk (OK-01…OK-10).
- **Totem spin:** A logged transaction collecting independent evidence before high-impact action.
- **Reality drift:** Plausible internal model behaviour diverging from verifiable external state.
- **GitOps:** Declarative desired state in Git continuously reconciled to live systems.
- **HITL:** Human-in-the-loop attestation for decisions machines must not own alone.
- **MCP:** Model Context Protocol—standardised tool/resource attachment for agents.

### G.2 — Interview questions for principal AI engineers

1. How do you prove two totem legs are independent in your topology?  
2. What is your default verdict when evidence is stale—pass or pause—and why?  
3. Show a redacted totem log for a production mutation and narrate the rollback story.  
4. How does your organisation prevent “prompt hotfixes” from bypassing CI?  
5. Where does FinOps enforcement live: gateway, scheduler, or both?

### G.3 — Rubric for certifying “agent-ready” teams (0–4 maturity)

| Criterion | 0 | 2 | 4 |
|-----------|---|---|---|
| Totem coverage | Ad hoc | Major tools gated | All mutating paths |
| Policy | Manual review only | Git-versioned bundles | Automated diff + meta-totem |
| Evidence | Screenshots | Centralised logs | Signed bundles + trace linkage |
| Drills | None | Annual | Quarterly + post-incident |

### G.4 — Long primer — why dual-stream documentation wins

Single-audience documentation forces an impossible choice: either you write for executives in abstract nouns, leaving engineers without executable detail, or you write low-level runbooks that leaders cannot govern. Dual-stream documentation **threads one spine** with two voices. The Human Observer sections answer procurement, ethics, insurance, and ten-year maintainability questions that appear in board reviews. The Agentic Kernel sections answer the questions automation asks: what JSON manifest applies, which prompt precedes a tool call, what memory keys to write, and which CI job proves regression. When controversy arises, both audiences can cite the **same chapter and version hash**, reducing organisational schizophrenia.

### G.5 — International publishing checklist (KDP)

- Assign ISBN if required in your territory; link edition to Zenodo DOI.  
- Register copyright as applicable.  
- Choose trim size and re-flow Mermaid figures to images for print clarity.  
- Proofread with a human editor; models draft, humans certify.  
- Add “About the author” and “Acknowledgements” pages in Word after Markdown import.

### G.6 — Suggested course outline (12 weeks)

Weeks 1–2: Totem + OK-02. Weeks 3–4: OK-01 + OK-05 lab safety. Weeks 5–6: OK-04 + OK-08. Weeks 7–8: OK-03 + OK-06. Weeks 9–10: OK-07 + evidence automation. Week 11: OK-09. Week 12: OK-10 meta-governance and capstone tabletop covering all kernels.
