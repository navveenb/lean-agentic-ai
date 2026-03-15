# Lean Agentic AI Reference implementation

**A plug-and-play framework for building lean agentic AI systems that minimize cost, carbon, and complexity.**

> _"Every design decision has a price — in dollars, in emissions, and in complexity. Lean agentic AI is the discipline of paying only what the outcome is worth."_ — Inspired by [Lean Agentic AI](https://leanagenticai.com/) by Navveen Balani

---

## What Is This?

A **framework + reference repo** for [Claude Code](https://code.claude.com/) that ships with working skills, agents, and commands — and lets anyone add their own.

**Use it as-is** to audit your agentic systems for waste. **Extend it** by dropping in new skills that implement the 10 lean principles. **Learn from it** by reading the deep-dives, patterns, and examples.

## Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR-USERNAME/lean-agentic-ai.git
cd lean-agentic-ai-claude-implementation

# 2. Start Claude Code
claude

# 3. Run a built-in skill
/cost-analyzer           # Scan a codebase for wasteful LLM usage
/bloat-detector          # Detect the 7 types of agentic bloat
/carbon-estimator        # Estimate CO₂ from your LLM calls

# 4. Add your own skill
./scripts/scaffold.sh skill prompt-compressor
# Edit .claude/skills/prompt-compressor/SKILL.md
# Test: claude → /prompt-compressor
```

> **Requires**: Claude Code installed + Claude Pro or Max or API key. See [HOW-TO-USE.md](HOW-TO-USE.md) for full setup.

---

## Guides

| Guide | What It Covers |
|-------|---------------|
| [**HOW-TO-USE.md**](HOW-TO-USE.md) | Installation, setup, running skills, adding your own — start here if you're new |
| [**WALKTHROUGH.md**](WALKTHROUGH.md) | Step-by-step end-to-end run of `/cost-analyzer` against the included test codebase — see every piece in action |
| [**CONTRIBUTING.md**](CONTRIBUTING.md) | How to add skills, agents, and commands — templates, scaffolding, PR checklist |

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

## What's Inside

### 🔌 Plug-and-Play Claude Code Config (`.claude/`)

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

### 🧪 Test Codebase (try it now)

```
test-codebase/
├── support_bot.py         ← 7 Anthropic SDK calls, all using Opus (deliberately wasteful)
└── content_pipeline.py    ← 4 OpenAI SDK calls, all using GPT-4 (deliberately wasteful)
```

Run `/cost-analyzer test-codebase` to see the full workflow in action. See [WALKTHROUGH.md](WALKTHROUGH.md) for what to expect.

### 📚 Reference Library

| Section | What's Inside |
|---------|--------------|
| [principles/](principles/) | Deep dives into all 10 principles with cost math and anti-patterns |
| [foundations/](foundations/) | Core concepts: what agentic AI is, why lean matters, bloat audit |
| [design-patterns/](design-patterns/) | Model routing, cognitive caching, bounded retries, carbon scheduling |
| [checklists/](checklists/) | Pre-deployment, cost review, carbon audit, agent design review |
| [frameworks/](frameworks/) | LangGraph vs CrewAI vs AutoGen vs Semantic Kernel vs Haystack |
| [examples/](examples/) | Working Python: routing, caching, cost tracking, memory, carbon |
| [tools/](tools/) | Curated tooling guide for lean agentic development |
| [reports/](reports/) | Token economics analysis, LLM carbon footprint data |

### 🤝 Contributor Framework

| Resource | Purpose |
|----------|---------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Full guide + skill ideas table |
| [scripts/scaffold.sh](scripts/scaffold.sh) | One-command scaffolding |
| [.claude/skills/_template/](.claude/skills/_template/SKILL.md) | Skill template |
| [contrib/agents/TEMPLATE.md](contrib/agents/TEMPLATE.md) | Agent template |
| [contrib/commands/TEMPLATE.md](contrib/commands/TEMPLATE.md) | Command template |

---

## How the Cost Analyzer Workflow Works

```
/cost-analyzer
  │
  ├─ Step 1: Asks user for path + provider
  │
  ├─ Step 2: Agent(lean-auditor) scans code
  │   ├── Model: haiku (cheap — Principle 2)
  │   ├── Tools: Read, Grep, Glob only (Principle 8)
  │   ├── Preloaded: token-counter skill
  │   └── Preloaded: model-recommender skill
  │
  ├─ Step 3: Skill(cost-analyzer) generates report
  │   └── Writes to reports/cost-analysis.md
  │
  └─ Step 4: Presents summary to user
```

> **See it in action**: [WALKTHROUGH.md](WALKTHROUGH.md) has the full end-to-end run with expected output for every step.

---

## Add Your Own Skill

```bash
# Scaffold
./scripts/scaffold.sh skill prompt-compressor

# Edit
# Open .claude/skills/prompt-compressor/SKILL.md

# Test
claude
/prompt-compressor

# Submit
git checkout -b contrib/prompt-compressor
git add .claude/skills/prompt-compressor/
git commit -m "add skill: prompt-compressor (principle #1)"
git push && # open PR
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide and open skill ideas.

---

## Learn More

📖 **Book**: [Lean Agentic AI: Minimizing Cost, Carbon, and Complexity](https://leanagenticai.com/) by Navveen Balani
🔗 **Author's Repo**: [navveenb/lean-agentic-ai](https://github.com/navveenb/lean-agentic-ai)
📝 **Medium**: [Rethinking Agentic AI: Why Lean Is the New Smart](https://navveenbalani.medium.com/rethinking-agentic-ai-why-lean-is-the-new-smart-030319860304)
🎙️ **Podcast**: [Agentic AI: The Future of Intelligent Systems](https://podcasts.apple.com/us/podcast/agentic-ai-the-future-of-intelligent-systems/id1789969824)
📋 **Inspiration**: [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)

## License

MIT — Use freely, build responsibly.
