# End-to-End Walkthrough: Running the Model Recommender Flow

> This guide walks through the **complete chain**: you type a command → an agent scans your code using the model-recommender skill as background knowledge → a report is generated. Every step explained.

---

## What You're About to Run

```
YOU type: /cost-analyzer test-codebase
    │
    ▼
COMMAND (.claude/commands/cost-analyzer.md)
    │  Model: sonnet (orchestration needs moderate reasoning)
    │  Asks you: "What provider?" → You say: "Mixed"
    │
    ▼
AGENT (.claude/agents/lean-auditor.md)
    │  Model: haiku (scanning is simple — Principle 2)
    │  Tools: Read, Grep, Glob only (Principle 8)
    │  At startup, Claude Code injects FULL content of:
    │    ├── .claude/skills/token-counter/SKILL.md
    │    └── .claude/skills/model-recommender/SKILL.md    ← THIS IS THE KEY
    │
    │  The agent now "knows" the model-recommender rules:
    │    - Classification → Tier 1
    │    - Extraction → Tier 1
    │    - Summarization → Tier 2
    │    - Complex reasoning → Tier 3
    │    - Formatting with no LLM needed → flag it
    │
    │  Agent scans test-codebase/ using Grep:
    │    - Finds 7 calls in support_bot.py (all Opus)
    │    - Finds 4 calls in content_pipeline.py (all GPT-4)
    │    - Classifies each by task type using model-recommender rules
    │    - Estimates tokens using token-counter rules
    │    - Returns structured findings
    │
    ▼
SKILL (.claude/skills/cost-analyzer/SKILL.md)
    │  Invoked by command via Skill tool (not preloaded)
    │  Reads agent findings from context
    │  Generates reports/cost-analysis.md with:
    │    - Per-call analysis
    │    - Cost savings table
    │    - Carbon estimates
    │    - Top 3 quick wins
    │
    ▼
COMMAND presents summary to you
```

---

## Step 0: Setup (one time)

```bash
# Install Claude Code (if not done)
curl -fsSL https://claude.ai/install.sh | bash

# Clone the repo
git clone https://github.com/YOUR-USERNAME/lean-agentic-ai-best-practice.git
cd lean-agentic-ai-best-practice

# Verify the test codebase exists
ls test-codebase/
# Should show: support_bot.py  content_pipeline.py
```

---

## Step 1: Start Claude Code

```bash
claude
```

**What happens behind the scenes:**
1. Claude Code reads `CLAUDE.md` from the project root — this tells Claude about the project structure, the orchestration demo, and the key rules.
2. Claude Code discovers the `.claude/` folder and indexes all commands, agents, and skills.
3. You see a prompt: `>`

**Verify it loaded everything:**
```
> what commands, agents, and skills do you see?
```

Claude should respond with something like:
```
I can see:
- Command: /cost-analyzer — analyzes LLM usage and recommends model right-sizing
- Agent: lean-auditor — scans codebases for LLM API patterns (uses haiku)
- Skills: token-counter, model-recommender (preloaded into agent),
          cost-analyzer, bloat-detector, carbon-estimator (standalone)
```

---

## Step 2: Run the Command

```
> /cost-analyzer test-codebase
```

**What happens:**

### 2a. Command asks you a question

Claude (running the cost-analyzer command on sonnet) asks:
```
What LLM provider are you using?
- OpenAI
- Anthropic
- Google
- Mixed
```

You answer: **Mixed** (because the test codebase uses both Anthropic and OpenAI).

### 2b. Command invokes the lean-auditor agent

Claude uses the Agent tool internally:
```
Agent(
  subagent_type="lean-auditor",
  description="Scan test-codebase for LLM API calls",
  prompt="Scan test-codebase/. Find all LLM API calls...",
  model="haiku"
)
```

**You'll see green-colored output in your terminal** — that's the agent running in its isolated context.

### 2c. Inside the agent: model-recommender in action

The agent was created with these skills preloaded:
```yaml
skills:
  - token-counter
  - model-recommender
```

So when the agent starts, the **entire content** of both SKILL.md files is injected into its context. The agent doesn't call these skills — it already *knows* their content as background knowledge.

The agent then:

1. **Uses Grep** to find LLM API patterns:
   ```
   Grep("client.messages.create", "test-codebase/")
   Grep("client.chat.completions.create", "test-codebase/")
   ```

2. **Uses Read** to examine each file and understand each call.

3. **Applies model-recommender rules** to classify each call:

   | File | Function | Task Type | Current Model | Model-Recommender Says |
   |------|----------|-----------|---------------|----------------------|
   | support_bot.py:22 | classify_spam | Classification | opus | → Tier 1 (Haiku) 🔴 |
   | support_bot.py:37 | extract_contact_info | Extraction | opus | → Tier 1 (Haiku) 🔴 |
   | support_bot.py:52 | analyze_sentiment | Classification | opus | → Tier 1 (Haiku) 🔴 |
   | support_bot.py:67 | route_ticket | Routing | opus | → Tier 1 (Haiku) 🔴 |
   | support_bot.py:81 | summarize_conversation | Summarization | opus | → Tier 2 (Sonnet) ⚠️ |
   | support_bot.py:95 | draft_reply | Drafting | opus | → Tier 2 (Sonnet) ⚠️ |
   | support_bot.py:112 | analyze_escalation | Complex reasoning | opus | → Tier 3 (Opus) ✅ |
   | content_pipeline.py:19 | categorize_article | Classification | gpt-4 | → Tier 1 (GPT-4o-mini) 🔴 |
   | content_pipeline.py:35 | generate_seo_tags | Extraction | gpt-4 | → Tier 1 (GPT-4o-mini) 🔴 |
   | content_pipeline.py:50 | translate_headline | Translation | gpt-4 | → Tier 2 (GPT-4o) ⚠️ |
   | content_pipeline.py:65 | format_article_json | Formatting | gpt-4 | → No LLM needed! 🔴 |

4. **Applies token-counter rules** to estimate cost per call.

5. **Returns findings** to the command.

### 2d. Command invokes the cost-analyzer skill

The command now calls:
```
Skill(skill="cost-analyzer")
```

The cost-analyzer skill reads the agent's findings from context and writes `reports/cost-analysis.md`.

### 2e. Command presents summary

Claude shows you something like:
```
Analysis complete.

Found 11 LLM calls across 2 files:
- 6 significantly over-provisioned (frontier model for Tier 1 tasks)
- 3 moderately over-provisioned (frontier for Tier 2 tasks)
- 1 correctly sized
- 1 shouldn't use an LLM at all

Estimated monthly savings: $X,XXX (XX% reduction)
Full report: reports/cost-analysis.md
```

---

## Step 3: Check the Report

```
> cat reports/cost-analysis.md
```

Or exit Claude Code and read it directly:
```bash
cat reports/cost-analysis.md
```

The report contains per-call analysis, a cost breakdown table, top 3 quick wins, and carbon impact estimates.

---

## What the Model-Recommender Actually Did

Here's the key thing to understand: the `model-recommender` skill is **not a command you run**. It's **background knowledge** that the `lean-auditor` agent carries.

Think of it like this:

| Concept | Human Analogy |
|---------|--------------|
| **Command** (`/cost-analyzer`) | Your boss says "audit this codebase" |
| **Agent** (`lean-auditor`) | The auditor who does the work |
| **Skill** (`model-recommender`) | The auditor's training manual — they studied it before starting, they don't "open" it during work, they just *know* the rules |
| **Skill** (`token-counter`) | Another training manual — cost estimation rules |
| **Skill** (`cost-analyzer`) | A report template — the boss hands it to a report writer after the auditor finishes |

The `model-recommender` rules are what the agent uses to make judgment calls like "classify_spam uses Opus but it's a classification task, so it should be Tier 1."

---

## How to See Each Piece in Action

### See the model-recommender rules:
```bash
cat .claude/skills/model-recommender/SKILL.md
```

### See what the agent is configured to do:
```bash
cat .claude/agents/lean-auditor.md
```
Look at line 8: `skills: - token-counter - model-recommender` — that's where preloading happens.

### See the command orchestration:
```bash
cat .claude/commands/cost-analyzer.md
```
Steps 1-4 show the full flow.

### See the test codebase (what gets scanned):
```bash
cat test-codebase/support_bot.py
cat test-codebase/content_pipeline.py
```
Each function has comments explaining what it does and why it's wasteful.

### See the generated report (after running):
```bash
cat reports/cost-analysis.md
```

---

## Expected Results from the Test Codebase

The test codebase has **11 LLM calls that are deliberately wasteful**. Here's what the model-recommender skill should flag:

### Calls that should be Tier 1 (currently Tier 3)

| Function | Why | Savings/call |
|----------|-----|-------------|
| `classify_spam` | Yes/no classification — simplest possible task | $0.99 |
| `extract_contact_info` | Entity extraction from text | $0.99 |
| `analyze_sentiment` | 3-way classification (positive/negative/neutral) | $0.99 |
| `route_ticket` | Single-choice routing | $0.99 |
| `categorize_article` | Category classification | $0.99 |
| `generate_seo_tags` | Tag extraction | $0.99 |

### Calls that should be Tier 2 (currently Tier 3)

| Function | Why | Savings/call |
|----------|-----|-------------|
| `summarize_conversation` | Single-document summarization | $0.90 |
| `draft_reply` | Template-based email drafting | $0.90 |
| `translate_headline` | Simple translation | $0.90 |

### Calls that are correctly sized

| Function | Why |
|----------|-----|
| `analyze_escalation` | Multi-step reasoning with business context — needs frontier |

### Calls that shouldn't use an LLM at all

| Function | Why |
|----------|-----|
| `format_article_json` | Formatting structured data into JSON — Python's `json.dumps()` does this |

---

## Modify the Test Codebase and Re-Run

Try editing `test-codebase/support_bot.py` — change one of the `model="claude-opus-4-20250514"` calls to `model="claude-haiku-4-5-20241022"` and re-run:

```
> /cost-analyzer test-codebase
```

The report should now show one fewer over-provisioned call.

---

## The Chain Visualized

```
┌──────────────────────────────────────────────────┐
│  YOUR TERMINAL                                    │
│                                                  │
│  > /cost-analyzer test-codebase                  │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │ COMMAND: cost-analyzer.md (sonnet)          │  │
│  │                                            │  │
│  │ "What provider?" → "Mixed"                 │  │
│  │                                            │  │
│  │ Agent(lean-auditor, model=haiku)           │  │
│  │  ┌────────────────────────────────────┐    │  │
│  │  │ AGENT: lean-auditor (haiku, green) │    │  │
│  │  │                                    │    │  │
│  │  │ Preloaded at startup:              │    │  │
│  │  │  ├── token-counter SKILL.md        │    │  │
│  │  │  └── model-recommender SKILL.md    │    │  │
│  │  │                                    │    │  │
│  │  │ Grep → Read → Classify → Return    │    │  │
│  │  └─────────────────┬──────────────────┘    │  │
│  │                    │ findings               │  │
│  │                    ▼                        │  │
│  │ Skill(cost-analyzer)                       │  │
│  │  ┌────────────────────────────────────┐    │  │
│  │  │ SKILL: cost-analyzer               │    │  │
│  │  │ Writes reports/cost-analysis.md    │    │  │
│  │  └────────────────────────────────────┘    │  │
│  │                                            │  │
│  │ "Found 11 calls, 9 over-provisioned..."   │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  >                                               │
└──────────────────────────────────────────────────┘
```

---

## Troubleshooting

**"I don't see /cost-analyzer in autocomplete"**
→ Make sure you're running `claude` from inside the `lean-agentic-ai-best-practice` directory. Claude Code reads `.claude/` from the current working directory.

**"The agent didn't find any LLM calls"**
→ Check that `test-codebase/support_bot.py` and `content_pipeline.py` exist. Run `ls test-codebase/` to verify.

**"No report was generated"**
→ Check that the `reports/` directory exists: `ls reports/`. The skill writes to `reports/cost-analysis.md`.

**"I see errors about permissions"**
→ The `settings.json` pre-allows Read, Grep, Glob, and `Write(reports/*)`. If Claude asks for other permissions, approve them.

**"Green text didn't appear"**
→ Green text = the agent running. If you don't see it, the command might not have invoked the agent. Check if it's asking you a question first.
