# Common Bloat in Agentic Systems

7 categories. Score each 0-3. Use the `/bloat-detector` skill to audit automatically.

## The Seven Sources

| # | Bloat Type | What It Looks Like | Fix |
|---|-----------|-------------------|-----|
| 1 | **Model** | GPT-4/Opus for classification tasks | Model routing (Principle 2) |
| 2 | **Orchestration** | 5-agent chain where 1 agent would work | Agent consolidation (Principle 3) |
| 3 | **Reflection** | 2-3 reflection cycles on every call, even simple tasks | Conditional reflection (Principle 4) |
| 4 | **Context** | 50K+ tokens stuffed into every call | Context budgeting (Principle 1) |
| 5 | **Tool** | 10-15 tools per agent, most unused | Task-scoped toolkits (Principle 8) |
| 6 | **Memory** | Full transcripts stored forever, no TTLs | Summarize + expire (Principle 9) |
| 7 | **Retrieval** | RAG on every query, even when model knows the answer | Retrieval gating (Principle 5) |

## Scoring

- **0-5**: Lean and efficient.
- **6-12**: Moderate bloat. Targeted optimizations recommended.
- **13-21**: Severe waste. Prioritize the highest-scoring categories.
