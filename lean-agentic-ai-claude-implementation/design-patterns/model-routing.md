# Design Pattern: Model Routing

> Route each task to the smallest model that handles it.

**Principle**: #2 Right-Size Your Model · #6 Emissions

## Architecture

```
Incoming Task → Router → Tier 1 (Small/Fast, ~$0.01)
                       → Tier 2 (Mid-Range, ~$0.10)
                       → Tier 3 (Frontier, ~$1.00)
```

## Three Strategies

**1. Rule-Based**: Map task types to tiers. Zero overhead, fully predictable. Best for well-defined task distributions.

**2. Classifier-Based**: A tiny model assesses complexity and routes. Handles novel tasks. Small inference cost for the classifier itself.

**3. Cascade (FrugalGPT)**: Start with cheapest model. Escalate if confidence < threshold. Self-optimizing, but worst-case latency is higher.

## When to Use Which

| Scenario | Strategy |
|----------|---------|
| Known task types, stable distribution | Rule-based |
| Mixed/unpredictable tasks | Classifier |
| Cost is #1 priority, latency flexible | Cascade |
| Strict latency SLAs | Rule-based |

## Working Code

See `examples/model-routing/` for a complete Python implementation with all 3 strategies and a savings calculator.
