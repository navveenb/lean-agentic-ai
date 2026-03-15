# Principle 10: Agentic Systems Need Governance, Not Just Autonomy

> **Left unchecked, autonomy becomes chaos.**

## Hard Limits Every Agent Needs
| Limit | Example |
|-------|---------|
| Max turns per task | 10 |
| Max tokens per call | 4,096 output |
| Max tool calls per task | 5 |
| Max cost per request | $0.50 |
| Max runtime | 60 seconds |

## Governance Stack
1. **Access**: Tool permissions, data access controls
2. **Resource**: Token limits, turn caps, tool budgets
3. **Behavioral**: Output validation, content filtering
4. **Operational**: Monitoring, alerting, circuit breakers
5. **Business**: Cost budgets, SLAs, compliance

## Techniques
- Circuit breakers on consecutive failures
- Human-in-the-loop escalation for high-stakes decisions
- Audit logging (every decision, tool call, cost)
- Periodic agent topology review

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for comprehensive governance frameworks.*
