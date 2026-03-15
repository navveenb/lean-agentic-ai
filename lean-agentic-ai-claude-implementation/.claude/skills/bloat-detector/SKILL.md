---
name: bloat-detector
description: Detect the 7 types of agentic bloat in a codebase or system design
user-invocable: true
argument-hint: [file-or-directory-path]
allowed-tools: Read, Grep, Glob, Write
model: sonnet
---

# Bloat Detector

Scan a codebase or system description for the 7 types of agentic bloat and produce a scored audit.

## Lean Principle

- [x] #1 Context is a liability
- [x] #2 Right-size your model
- [x] #3 Orchestration is not a playground
- [x] #4 Reflections cost compute
- [x] #5 RAG isn't always right
- [x] #7 Reuse over recompute
- [x] #8 More tools, more problems

## Instructions

### Step 1: Scan for each bloat type

Use Grep and Read to look for evidence of these 7 bloat patterns:

**1. Model Bloat** — Look for hardcoded frontier model names (`gpt-4`, `claude-opus`, `gemini-ultra`) used for simple tasks (classification, extraction, formatting).

**2. Orchestration Bloat** — Count distinct agent definitions, multi-agent chains, sequential agent invocations. Flag if more than 3 agents are chained sequentially.

**3. Reflection Bloat** — Look for self-critique patterns: "review your output", "improve your answer", retry loops, `while` loops around LLM calls without exit conditions.

**4. Context Bloat** — Look for large system prompts (>2000 chars), full document injection, unbounded conversation history loading, many tool descriptions.

**5. Tool Bloat** — Count tool/function definitions per agent. Flag agents with more than 5 tools.

**6. Memory Bloat** — Look for unbounded storage: missing TTLs, "store everything", no cleanup/expiry logic, full transcript storage.

**7. Retrieval Bloat** — Look for RAG pipelines that run on every query without gating: always-on vector search, no relevance thresholds, no caching of retrieval results.

### Step 2: Score each category

Score each bloat type 0-3:
- 0 = No evidence of bloat
- 1 = Minor (some instances, manageable)
- 2 = Moderate (multiple instances, should optimize)
- 3 = Severe (systemic, causing significant waste)

### Step 3: Write report

Write a report to `reports/bloat-audit.md` with:
- Score per category (0-3)
- Total score out of 21
- Specific file:line references for each finding
- Severity rating: 0-5 Lean, 6-12 Moderate bloat, 13-21 Severe bloat
- Top 3 recommended fixes

## Output

Report saved to `reports/bloat-audit.md`

## Example

Input: A project with 5 chained agents all using GPT-4, no caching, 10 tools per agent.
Output:
```
Model Bloat: 3/3 — All 5 agents use frontier model for mixed tasks
Orchestration Bloat: 2/3 — 5 agents chained, 2 could be merged
Tool Bloat: 3/3 — 10 tools per agent, most unused
Total: 15/21 — SEVERE bloat. Start with model routing and tool pruning.
```
