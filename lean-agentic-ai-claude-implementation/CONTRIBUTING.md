# Contributing to Lean Agentic AI Best Practice

> Add your own skills, agents, and commands. Make the framework better.

---

## Quick Start: Add a Skill in 3 Minutes

```bash
# 1. Copy the template
cp -r .claude/skills/_template .claude/skills/your-skill-name

# 2. Edit the SKILL.md
# Open .claude/skills/your-skill-name/SKILL.md and fill in your content

# 3. Test it
claude
# Then type: /your-skill-name (if user-invocable: true)
# Or preload it into an agent by adding it to the agent's skills: list
```

That's it. Claude Code auto-discovers any SKILL.md inside `.claude/skills/*/`.

---

## What Can You Contribute?

| Type | Where It Goes | Template | Difficulty |
|------|--------------|----------|------------|
| **Skill** | `.claude/skills/your-name/SKILL.md` | [Skill Template](.claude/skills/_template/SKILL.md) | Easy |
| **Agent** | `.claude/agents/your-name.md` | [Agent Template](contrib/agents/TEMPLATE.md) | Medium |
| **Command** | `.claude/commands/your-name.md` | [Command Template](contrib/commands/TEMPLATE.md) | Medium |
| **Full Workflow** | Command + Agent + Skill(s) together | See [Cost Analyzer](#built-in-example-cost-analyzer) | Advanced |
| **Principle Deep-Dive** | `principles/` | See existing files | Easy |
| **Design Pattern** | `design-patterns/` | See existing files | Medium |
| **Code Example** | `examples/your-name/` | See existing examples | Medium |

---

## How Each Piece Works

### Skills (`.claude/skills/<name>/SKILL.md`)

Skills are **reusable knowledge**. They come in two flavors:

**User-invocable skills** → Users type `/skill-name` to run them.
```yaml
---
name: my-skill
description: What it does
user-invocable: true        # ← appears in /slash-command menu
---
```

**Agent-preloaded skills** → Background knowledge injected into an agent at startup.
```yaml
---
name: my-background-knowledge
description: Rules for model selection
user-invocable: false       # ← hidden from menu, only for agents
---
```

**Rule of thumb**: If a human would use it directly → `user-invocable: true`. If only an agent needs it → `user-invocable: false`.

### Agents (`.claude/agents/<name>.md`)

Agents are **isolated workers**. They get their own model, tools, and context.

```yaml
---
name: my-agent
tools: Read, Grep            # MINIMUM tools needed
model: haiku                  # SMALLEST model that works
skills:
  - preloaded-skill-1        # Injected at startup
---
```

**When to create an agent vs. just a skill:**
- Need a **different model** than the main session? → Agent
- Need **restricted tools** (e.g., read-only)? → Agent
- Need **isolated context** (don't pollute main session)? → Agent
- Just need to add **knowledge or instructions**? → Skill (no agent needed)

### Commands (`.claude/commands/<name>.md`)

Commands are **entry points** — the `/slash-command` the user types to start a workflow.

```yaml
---
description: Shown in autocomplete
model: sonnet
allowed-tools: Read, Write, Agent, Skill
---
```

**When to create a command:**
- You have a **repeatable workflow** with multiple steps.
- The workflow involves **orchestrating agents and/or skills**.
- You want a **clean entry point** users can discover via `/`.

---

## Contribution Workflow

### Step 1: Pick a Principle

Every contribution should map to at least one of the [10 Lean Agentic AI Principles](principles/). Pick the one your skill/agent/command helps implement.

### Step 2: Copy the Template

```bash
# For a skill:
cp -r .claude/skills/_template .claude/skills/your-skill-name

# For an agent:
cp contrib/agents/TEMPLATE.md .claude/agents/your-agent-name.md

# For a command:
cp contrib/commands/TEMPLATE.md .claude/commands/your-command-name.md
```

### Step 3: Write Your Content

Fill in the template. Follow these rules:

**Naming:**
- Use `kebab-case` for all names: `carbon-estimator`, not `CarbonEstimator`
- Names should be descriptive: `prompt-optimizer` not `po`

**Content quality:**
- Be specific. "Analyze the code" is vague. "Use Grep to find all `model=` parameters in .py files" is specific.
- Include examples of expected input/output.
- State which tools the agent/skill needs and why.

**Lean by default:**
- Skills: Keep under 100 lines. If it's longer, split into multiple skills.
- Agents: Use `haiku` unless you can prove a larger model is needed.
- Commands: Minimize the number of agents invoked. One is ideal, two is acceptable, three needs justification.
- Tools: List only what's needed. Don't add "just in case" tools.

### Step 4: Test Locally

```bash
cd lean-agentic-ai-best-practice
claude

# Test a skill:
/your-skill-name

# Test a command:
/your-command-name

# Verify agent discovery:
> what agents and skills do you see in this project?
```

### Step 5: Submit a PR

```bash
git checkout -b contrib/your-skill-name
git add .claude/skills/your-skill-name/
git commit -m "add skill: your-skill-name (principle #N)"
git push origin contrib/your-skill-name
# Open PR on GitHub
```

**PR checklist:**
- [ ] Maps to at least one of the 10 principles
- [ ] Template fully filled in (no placeholder text left)
- [ ] Tested locally with Claude Code
- [ ] Model choice justified (why this tier?)
- [ ] Tool list is minimal
- [ ] Under 100 lines per SKILL.md

---

## Built-in Example: Cost Analyzer

The repo ships with one complete workflow to use as a reference:

```
.claude/
├── commands/
│   └── cost-analyzer.md            ← /cost-analyzer entry point
├── agents/
│   └── lean-auditor.md             ← Scanning agent (haiku, read-only)
└── skills/
    ├── _template/SKILL.md          ← Copy this for new skills
    ├── token-counter/SKILL.md      ← Preloaded into agent
    ├── model-recommender/SKILL.md  ← Preloaded into agent
    ├── cost-analyzer/SKILL.md      ← Standalone (generates report)
    ├── bloat-detector/SKILL.md     ← Standalone (detects 7 bloat types)
    └── carbon-estimator/SKILL.md   ← Standalone (estimates CO₂)
```

**Flow:**
```
/cost-analyzer
  → asks user for path + provider
  → Agent(lean-auditor) scans code [haiku, read-only]
      ├── uses token-counter knowledge
      └── uses model-recommender knowledge
  → Skill(cost-analyzer) generates report
  → presents summary
```

Study this before building your own. It demonstrates every pattern.

---

## Skill Ideas — Open for Contribution

These don't exist yet. Build one and submit a PR!

| Skill Idea | Principle | Difficulty |
|-----------|-----------|------------|
| `prompt-compressor` — Shorten verbose prompts without losing meaning | #1 Context | Medium |
| `cache-advisor` — Detect cacheable LLM calls in code | #7 Reuse | Medium |
| `agent-consolidator` — Suggest merging redundant agents | #3 Orchestration | Hard |
| `reflection-auditor` — Find unnecessary reflection loops | #4 Reflections | Medium |
| `rag-gate-checker` — Identify queries that don't need retrieval | #5 RAG | Medium |
| `tool-pruner` — Find unused tool definitions in agent configs | #8 Tools | Easy |
| `memory-decay-advisor` — Suggest TTLs for memory entries | #9 Memory | Medium |
| `guardrail-checker` — Verify agents have proper limits set | #10 Governance | Easy |
| `green-region-picker` — Recommend cloud regions by carbon intensity | #6 Emissions | Easy |
| `token-budget-enforcer` — Add token budgets to existing prompts | #1 Context | Medium |

---

## Directory Structure Reference

```
lean-agentic-ai-best-practice/
├── .claude/                          ← CLAUDE CODE READS THIS
│   ├── commands/*.md                 ← /slash-commands (entry points)
│   ├── agents/*.md                   ← Subagents (isolated workers)
│   ├── skills/*/SKILL.md            ← Skills (knowledge + instructions)
│   │   └── _template/SKILL.md       ← COPY THIS for new skills
│   ├── rules/*.md                    ← Rules Claude always follows
│   └── settings.json                 ← Permissions and config
│
├── contrib/                          ← TEMPLATES FOR CONTRIBUTORS
│   ├── skills/                       ← (empty — skills go in .claude/)
│   ├── agents/TEMPLATE.md            ← Agent template
│   └── commands/TEMPLATE.md          ← Command template
│
├── principles/                       ← 10 principle deep-dives
├── foundations/                       ← Core concepts explained
├── design-patterns/                  ← Reusable architecture patterns
├── checklists/                       ← Ready-to-use team checklists
├── frameworks/                       ← Framework comparison
├── examples/                         ← Working Python code examples
├── tools/                            ← Tooling guide
├── reports/                          ← Output directory for analyses
├── scripts/                          ← Utility scripts
│
├── CLAUDE.md                         ← Project memory (read every session)
├── CONTRIBUTING.md                   ← You are here
├── HOW-TO-USE.md                     ← End-to-end setup guide
├── README.md                         ← Project overview
└── LICENSE                           ← MIT
```
