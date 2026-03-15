# Principle 2: Not Every Prompt Deserves a 70B Response

> **Use the smallest brain that gets the job done.**

## Model Tiers
- **Tier 1 (Small)**: Classification, extraction, routing, formatting. ~$0.01/call.
- **Tier 2 (Mid)**: Summarization, translation, simple code gen. ~$0.10/call.
- **Tier 3 (Frontier)**: Complex reasoning, novel problems, creative tasks. ~$1.00/call.

## Routing Strategies
1. **Rule-based**: Map task types to tiers explicitly.
2. **Classifier-based**: Tiny model assesses complexity, routes accordingly.
3. **Cascade (FrugalGPT)**: Start small, escalate if confidence is low.

## Cost Impact
| Strategy | Daily Cost (100K calls) |
|----------|------------------------|
| Always Frontier | $1,000 |
| Routed | $175 |
| **Savings** | **$825/day ($300K/year)** |

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for elastic intelligence patterns.*
