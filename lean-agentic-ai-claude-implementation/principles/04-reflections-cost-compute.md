# Principle 4: Reflections Aren't Free — They're Compute

> **Think before you ask an agent to think.**

## When Reflection Is Worth It
Only when the cost of a bad output exceeds the cost of the reflection cycle. Simple formatting? No. Production SQL query? Yes.

## Techniques
1. **Conditional Reflection**: Only reflect when a quality check fails.
2. **Bounded Reflection**: Hard cap at 1-2 cycles. Never unbounded.
3. **External Validation**: Run the code, validate JSON, check math — cheaper than LLM self-critique.
4. **Reflection Sampling**: In batch, reflect on 10% sample, tune prompt for the rest.

## Cost Impact
| Approach | Calls/Day (10K tasks) | Daily Cost |
|----------|----------------------|------------|
| No reflection | 10,000 | $100 |
| Always reflect (2x) | 20,000 | $200 |
| **Conditional (20% trigger)** | **12,000** | **$120** |

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for Purpose-Bound Reasoning.*
