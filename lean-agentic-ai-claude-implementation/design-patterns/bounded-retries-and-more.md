# Design Patterns: Bounded Retries, Context Hydration, Intentional Forgetting, Carbon-Aware Scheduling

**Bounded Retries**: Max 2-3 tool retries, 5-15 agent turns, $0.25-2.00 per request. Always have fallback paths.

**Context Hydration**: Start minimal, add context only when agent determines it needs more. Reduces avg context 40-70%.

**Intentional Forgetting**: TTL-based expiry, relevance decay, summarize-then-discard, deduplication, capacity limits.

**Carbon-Aware Scheduling**: Use Electricity Maps/WattTime APIs. Batch workloads → run when grid is greenest. Green regions (Quebec, Norway) reduce carbon 90%+.
