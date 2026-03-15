# Design Pattern: Cognitive Caching

> The fastest LLM call is the one you never make.

**Principle**: #7 Reuse Over Recompute · #6 Emissions

## Cache Layers

```
Request → L1: Exact Match (hash input)
               ↓ miss
          L2: Semantic Cache (embedding similarity)
               ↓ miss
          L3: Tool Result Cache (API response cache)
               ↓ miss
          LLM Inference → store in L1
```

**L1 Exact Match**: Hash the full input. If hash exists, return cached response. Zero ambiguity. 5-15% hit rate.

**L2 Semantic**: Embed the query, find nearest cached query by cosine similarity. Return if above threshold (e.g., 0.95). 15-40% hit rate in Q&A workloads.

**L3 Tool Results**: Cache external API/DB/search results by tool name + parameters. 20-60% hit rate.

## TTL Guidelines

| Content | TTL |
|---------|-----|
| Static knowledge Q&A | 24-72 hours |
| Tool results (weather, prices) | 5-60 minutes |
| Summarization of fixed docs | 7+ days |
| Creative/generative output | Do not cache |
| Classification/routing | 24+ hours |

## Metrics to Track

- Cache hit rate (target: 20-40%)
- Staleness rate (target: < 1%)
- Cost savings: hits × avg_cost_per_call
- Latency improvement: cached ~10ms vs LLM 1-10s

## Working Code

See `examples/caching-strategy/` for a complete Python implementation.
