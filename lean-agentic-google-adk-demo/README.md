# Lean Agentic AI — Default vs Lean on Google ADK

A **standalone, runnable** demonstration of the [Lean Agentic AI](https://leanagenticai.com)
discipline using the latest Google Agent Development Kit (**ADK 2.x**, graph-based
Workflow Runtime). Zero credentials needed to try it; runs against live Gemini
when you add a key.

One task — *"Rebalance ESG portfolio for client 84721"* — built twice:

- **DEFAULT**: 5 sequential steps + parse retries, everything on the Pro-tier
  model, full policy + portfolio + client history resent on every call.
- **LEAN**: an ADK `Workflow` **graph** — 2 model calls + 4 pure-code
  `FunctionNode`s, a small model for classification, conditional routing,
  a context-cached policy, and schema-constrained output.

**Real live-Gemini result** (July 2026, client 84721):

| | DEFAULT | LEAN | delta |
|---|---|---|---|
| LLM calls / task | 6 | 2 | -67% |
| Input tokens | 48,427 | 3,725 (90% cached) | -92% |
| Cost / task | $0.171 | $0.0061 | **-96%** |
| SCI / task (gCO₂e) | 3.43 | 0.07 | **-98%** |
| Wall-clock | ~3.8 min | seconds | |
| At 10k tasks/day, per year | $624k · 12.5 tCO₂e | $22k · 0.26 tCO₂e | |

Cost and carbon are always reported as **parallel metrics** — never merged.

## Quick start (zero credentials)

```bash
pip install -r requirements.txt      # just google-adk
python run_comparison.py             # deterministic simulation mode
python run_comparison.py --client 55210   # the NO_ACTION fast-path demo
```

## Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** — installation, live-Gemini
  mode, the three bundled model portfolios, **how to add your own portfolio**,
  reading the output, troubleshooting.
- **[ANALYSIS.md](ANALYSIS.md)** — a plain-language walkthrough of a real
  live run: where the default way wastes money (4 habits), what the lean
  graph does differently (5 moves), with the workflow diagram. **Start here
  if the numbers table is new to you.**

## Yes, it's a real graph

The lean pipeline is an ADK 2.x `Workflow` — nodes and edges, conditional
routing, bounded retries — not a prompt loop:

```
START ─► classify ─► load_portfolio ─► check_caps ─► risk_router ─┬─► NO_ACTION
        (Flash-Lite)    (code)           (code)        (code)     └─► build_prompt ─► synthesizer
                                                                        (code)     (Flash + cached policy)
```

See the `Workflow(edges=[...])` block in [`lean_agent.py`](lean_agent.py) —
the diagram and the code are the same shape. Compliant portfolios take the
`NO_ACTION` branch and the synthesis model never runs at all.

## Project layout

```
portfolios/*.md           Model portfolios (84721 breaches · 91007 fossil-heavy · 55210 compliant)
data/esg_policy.md        ~16K-char ESG policy (the thing worth caching)
meter.py                  Cost / energy / carbon accounting; SCI = (E×I)+M per R
sim_models.py             SimulatedGemini (BaseLlm) + live-mode usage capture
default_agent.py          The wasteful baseline, honestly implemented
lean_agent.py             The lean ADK Workflow — every lever annotated
run_comparison.py         Runs both, prints the table, writes report_<client>.md
```

## Honest caveats

Pricing, energy coefficients, and grid intensities in `meter.py` are
illustrative mid-2026 figures in single editable tables — update before
quoting externally. The energy model uses per-token model-class coefficients
(directionally correct, wide error bars). SCI follows ISO/IEC 21031:
`(E × I) + M per R`, with R = one rebalance task. The default pipeline is
not a strawman — it's what unreviewed first-draft agent code looks like.

---
*Companion code for the talk "Lean Agentic AI on Google Cloud" — Navveen Balani,
Green Software Foundation. Book: [leanagenticai.com](https://leanagenticai.com)*
