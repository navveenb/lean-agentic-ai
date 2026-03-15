# Principle 3: Agent Orchestration Is Not a Playground

> **Every extra agent is a cost, a delay, and an emission.**

## The Agent Justification Test
Every agent must pass 3 gates:
1. Is this task distinct enough to require a separate context?
2. Does this agent need different tools, model, or permissions?
3. Does removing this agent measurably degrade output quality?

If any answer is no, don't create the agent.

## Lean Orchestration Patterns
- Single agent with multi-step prompting (instead of 4 separate agents)
- Parallel where possible, sequential where necessary
- Early termination — short-circuit when task is already complete
- Periodic agent consolidation audits

## Cost Multipliers
| Topology | Agents | Cost Multiplier |
|----------|--------|-----------------|
| Single agent | 1 | 1x |
| Sequential chain (3) | 3 | 3x |
| Sequential chain (5) | 5 | 5x+ |

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for orchestration topology evaluation.*
