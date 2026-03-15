# Principle 1: Large Context Is Actually a Liability When Left Unmanaged

> **More memory ≠ more intelligence.**

## The Problem
Unmanaged context leads to attention dilution, increased latency, higher cost, and hallucination risk. Every token in your context window should earn its place.

## Practical Techniques
1. **Context Windowing**: Sliding window of recent N turns + compressed summary of earlier context.
2. **Progressive Disclosure**: Load context on demand, not all at once.
3. **Context Budgeting**: Hard token budget per agent call. Exceed → summarize before calling.
4. **Relevance Filtering**: Score retrieved docs for relevance. Drop below-threshold docs.
5. **Tiered Context**: Critical (always), supplementary (if budget allows), archival (on demand).

## The Cost Math
| Scenario | Context Tokens | Cost per Call (frontier) | 1000 Calls/Day |
|----------|---------------|---------------------------|----------------|
| Bloated  | 80,000        | ~$0.80                    | ~$800/day      |
| Lean     | 12,000        | ~$0.12                    | ~$120/day      |

**6.7x cost reduction** from context management alone.

## Anti-Patterns
- "Dump everything in" — passing full databases without summarization
- "Just in case" context — tool descriptions that *might* be relevant
- Ignoring token counts — not tracking context size per call

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for context hydration patterns and memory cost indexing.*
