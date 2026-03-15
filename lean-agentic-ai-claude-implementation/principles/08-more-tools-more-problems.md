# Principle 8: More Tools, More Problems

> **Every tool adds latency, cost, and risk. Use wisely.**

## The Tool Tax
| Tools Available | Extra Context Tokens | Selection Accuracy |
|----------------|---------------------|-------------------|
| 2-3 | ~500 | 95%+ |
| 5-7 | ~1,500 | 85-90% |
| 10-15 | ~3,000-5,000 | 70-80% |

## Techniques
1. **Task-Scoped Toolkits**: Only include tools the agent needs for its specific task.
2. **Tool Gating**: Include expensive tools only when pre-check confirms need.
3. **Tool Consolidation**: Overlapping tools → pick one.
4. **Dynamic Tool Lists**: Build per-task, not load-all.
5. **Tool Call Budgets**: Max calls per task.

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for tool optimization patterns.*
