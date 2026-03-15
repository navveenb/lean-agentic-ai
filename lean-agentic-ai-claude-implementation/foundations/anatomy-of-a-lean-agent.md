# Anatomy of a Lean Agent

Every agent has 6 components. Each is a source of potential waste.

## Components and Where Waste Hides

**1. Prompt** — Overly verbose instructions, unnecessary few-shot examples, redundant formatting rules.
*Lean*: Audit prompts. Remove every sentence that doesn't measurably improve output.

**2. Model** — Frontier model for tasks a small model handles fine.
*Lean*: Benchmark smaller models. Use routing (Principle 2).

**3. Tools** — 15 tools exposed when only 3 are used. Each tool description consumes context tokens.
*Lean*: Scope tools per task (Principle 8).

**4. Memory** — Full transcripts stored forever, loaded into every call.
*Lean*: Summarize, set TTLs, tier by relevance (Principle 9).

**5. State** — Full intermediate results carried between steps.
*Lean*: Pass minimal state. Compress between steps.

**6. Guardrails** — Absence of limits is itself a source of waste.
*Lean*: Cost caps, turn limits, circuit breakers (Principle 10).

## The Formula

```
Lean Agent = Minimum Viable Prompt
           + Right-Sized Model
           + Scoped Tools (only what's needed)
           + Tiered Memory (summarized, time-bounded)
           + Minimal State (compressed between steps)
           + Hard Guardrails (cost, turns, time)
```
