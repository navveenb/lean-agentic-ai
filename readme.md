# Lean Agentic AI  
**Designing Agentic Systems That Minimize Cost, Carbon, and Complexity**

---

Welcome to **Lean Agentic AI** — a growing collection of byte-size learnings to help you design and implement agentic systems that are intelligent, efficient, and architecturally lean.

This series emphasizes:

- 💰 **Cost-efficiency** — through smart architecture and minimal compute  
- 🌱 **Carbon-awareness** — through energy-conscious design and deployment  
- 🧠 **Complexity reduction** — through clear workflows and modular agents  
- ⚖️ **Responsibility** — by embedding autonomy thresholds, ethical tool use, and safeguards in orchestration

📖 For deeper strategies, implementation patterns, and frameworks, refer to the companion book:  
[**Lean Agentic AI: Cost, Carbon, and Control**](https://leanagenticai.com/)

---

## Overview

This repository offers a curated collection of byte-sized insights focused on designing and deploying **lean agentic systems** that minimize cost, carbon, and complexity.

It's designed for AI builders, architects, and decision-makers aiming to optimize the operation of agentic systems—with an emphasis on performance, efficiency, and sustainability.

Topics can be explored in any order—each file is self-contained—or you can follow the thematic sections below.

---

## Guides

| Guide | What It Covers |
|-------|---------------|
| [**HOW-TO-USE.md**](HOW-TO-USE.md) | Installation, setup, running skills, adding your own — start here if you're new to Claude Code |
| [**WALKTHROUGH.md**](WALKTHROUGH.md) | Step-by-step end-to-end run of `/cost-analyzer` against the test codebase — see every piece in action |
| [**CONTRIBUTING.md**](CONTRIBUTING.md) | How to add skills, agents, and commands — templates, scaffolding, PR checklist |

---

## Claude Code Implementation (`.claude/`)

A plug-and-play framework for [Claude Code](https://code.claude.com/) — run built-in skills or add your own.

```bash
# Quick start
claude
/cost-analyzer test-codebase    # Scan for wasteful LLM usage
/bloat-detector                 # Detect 7 types of agentic bloat
/carbon-estimator               # Estimate CO₂ from LLM calls

# Add your own skill
./scripts/scaffold.sh skill prompt-compressor
```

```
.claude/
├── commands/
│   └── cost-analyzer.md              ← /cost-analyzer entry point
├── agents/
│   └── lean-auditor.md               ← Code scanning agent (haiku, read-only)
├── skills/
│   ├── _template/SKILL.md            ← COPY THIS for new skills
│   ├── token-counter/SKILL.md        ← Preloaded: token estimation rules
│   ├── model-recommender/SKILL.md    ← Preloaded: model tier mapping
│   ├── cost-analyzer/SKILL.md        ← Standalone: generates cost report
│   ├── bloat-detector/SKILL.md       ← Standalone: 7-type bloat audit
│   └── carbon-estimator/SKILL.md     ← Standalone: CO₂ estimation
├── rules/lean-principles.md          ← Rules Claude always follows
└── settings.json                     ← Permissions
```

### Test Codebase (try it now)

```
test-codebase/
├── support_bot.py         ← 7 Anthropic SDK calls, all using Opus (deliberately wasteful)
└── content_pipeline.py    ← 4 OpenAI SDK calls, all using GPT-4 (deliberately wasteful)
```

Run `/cost-analyzer test-codebase` to see the full workflow. See [WALKTHROUGH.md](WALKTHROUGH.md) for expected output.

---

## Foundations of Agentic AI

- [What is Agentic AI? From Reactive to Goal-Oriented Systems](foundation-agentic-ai/what-is-agentic-ai.md)  
- [Agent vs. Agentic: Understanding Autonomy, Memory, and Self-Awareness](foundation-agentic-ai/agent-vs-agentic.md)  
- [Why Lean? The Cost, Carbon, and Complexity Lens](foundation-agentic-ai/why-lean-agentic-ai.md)  
- [Anatomy of a Lean Agent: Components, State, Memory, and Tools](foundation-agentic-ai/anatomy-of-a-lean-agent.md)  
- [Common Bloat in Agentic Systems: Tracing Inefficiencies](foundation-agentic-ai/common-bloat-in-agentic-systems.md)  
- [Monolithic AI Calls vs. Modular Agents](foundation-agentic-ai/monolithic-vs-modular-agents.md)  
- [Mental Model: Every Agent Call Costs Money, Energy, and Attention](foundation-agentic-ai/mental-model-agent-call-cost.md)

---

## Design Thinking for Lean Agentic Systems

- [Designing Agent Workflows That Don't Loop Endlessly](lean-agentic-design-thinking/designing-agent-workflows.md)  
- [Aligning Agent Memory Use with Real Needs](lean-agentic-design-thinking/aligning-agent-memory-use.md)  
- [Designing the Right Prompt](lean-agentic-design-thinking/designing-the-right-prompt.md)  
- [Prompt Optimization vs. Agent Optimization](lean-agentic-design-thinking/prompt-vs-agent-optimization.md)  
- [Designing with Data as a First-Class Citizen](lean-agentic-design-thinking/designing-with-data.md)  
- [Designing with Fallback Models (FrugalGPT-style Routing)](lean-agentic-design-thinking/designing-with-fallback-models.md)  
- [Designing with Cost as a First-Class Citizen](lean-agentic-design-thinking/designing-with-cost.md)  
- [Carbon-Aware Decision-Making in Orchestration](lean-agentic-design-thinking/carbon-aware-orchestration.md)  
- [Visualizing Agent Paths: Decision Maps Before Code](lean-agentic-design-thinking/visualizing-agent-paths.md)  
- [Building Upon the Lean Patterns](lean-agentic-design-thinking/building-upon-lean-patterns.md)

---

## The 10 Lean Agentic AI Principles

| # | Principle | Core Idea | Deep Dive |
|---|-----------|-----------|-----------|
| 1 | **Large Context Is a Liability** | More memory ≠ more intelligence | [→](principles/01-context-is-a-liability.md) |
| 2 | **Not Every Prompt Deserves a 70B Response** | Use the smallest brain that gets the job done | [→](principles/02-right-size-your-model.md) |
| 3 | **Agent Orchestration Is Not a Playground** | Every extra agent is a cost, a delay, and an emission | [→](principles/03-orchestration-is-not-a-playground.md) |
| 4 | **Reflections Aren't Free** | Think before you ask an agent to think | [→](principles/04-reflections-cost-compute.md) |
| 5 | **RAG Isn't Always Right** | Retrieve only when it's truly needed | [→](principles/05-rag-isnt-always-right.md) |
| 6 | **Emissions Don't Show Up in Your Logs** | What you don't see, the planet still pays for | [→](principles/06-emissions-are-invisible.md) |
| 7 | **Reuse Is the New Reasoning** | Don't re-run. Re-think. | [→](principles/07-reuse-over-recompute.md) |
| 8 | **More Tools, More Problems** | Every tool adds latency, cost, and risk | [→](principles/08-more-tools-more-problems.md) |
| 9 | **Memory Isn't a Journal** | Storing everything is hoarding, not intelligence | [→](principles/09-memory-is-a-judgment-call.md) |
| 10 | **Governance, Not Just Autonomy** | Left unchecked, autonomy becomes chaos | [→](principles/10-governance-over-autonomy.md) |

---

## Reference Library

| Section | What's Inside |
|---------|--------------|
| [design-patterns/](design-patterns/) | Model routing, cognitive caching, bounded retries, carbon-aware scheduling |
| [checklists/](checklists/) | Pre-deployment, cost review, carbon audit, agent design review |
| [frameworks/](frameworks/) | LangGraph vs CrewAI vs AutoGen vs Semantic Kernel vs Haystack — the lean lens |
| [examples/](examples/) | Working Python: model routing, caching, cost tracking, memory optimization, carbon scheduling |
| [tools/](tools/) | Curated tooling guide for lean agentic development |
| [reports/](reports/) | Token economics analysis, LLM carbon footprint data |

---

## Contributor Framework

| Resource | Purpose |
|----------|---------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Full guide + open skill ideas table |
| [scripts/scaffold.sh](scripts/scaffold.sh) | One-command scaffolding for new skills, agents, commands |
| [.claude/skills/_template/](.claude/skills/_template/SKILL.md) | Skill template — copy this |
| [contrib/agents/TEMPLATE.md](contrib/agents/TEMPLATE.md) | Agent template |
| [contrib/commands/TEMPLATE.md](contrib/commands/TEMPLATE.md) | Command template |

---

## Whitepaper

- [Whitepaper on Green Agentic AI](research/Sustainable%20Agentic%20AI/readme.md)

---

## Learn More

📖 This collection represents just a **small selection of ideas** from the full book:  
**[Lean Agentic AI: Cost, Carbon, and Control](https://leanagenticai.com/)**

Spanning over **350 pages**, the book provides deep, practical insights into the architecture, trade-offs, and future of agentic systems.  
It covers hidden workflow costs, lean design principles, carbon-aware deployment strategies, and evaluations of 12+ leading Agentic AI frameworks — all tailored for builders, architects, and decision-makers aiming to scale agentic AI with clarity, efficiency, and environmental responsibility.

It also introduces new and actionable concepts — including **Purpose-Bound Reasoning**, **Model Minimalism**, **Cost-centric Design**, **Memory Cost Index**, **Elastic Intelligence**, and **Lean Workflow Design** — all focused on making autonomy **efficient, not excessive**.

## License

MIT — Use freely, build responsibly.
