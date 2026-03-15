# Principle 6: Emissions Don't Show Up in Your Logs

> **What you don't see, the planet still pays for.**

## Energy Per Inference
| Model Size | Energy/Query | CO₂/Query (avg grid) |
|-----------|-------------|----------------------|
| Small (1-8B) | ~0.001 kWh | ~0.4g |
| Medium (8-30B) | ~0.005 kWh | ~2g |
| Large (70B+) | ~0.01-0.05 kWh | ~5-20g |

## Techniques
1. **Green Region Deployment**: Hydro/wind regions reduce carbon 50-80%.
2. **Time-Shifting**: Schedule batch workloads during low-carbon grid periods.
3. **Model Right-Sizing**: Smaller models use 10-50x less energy.
4. **Carbon Budgeting**: Set per-workflow carbon limits.
5. **Carbon Dashboards**: Track estimated emissions.

## Scale Example
100K requests/day × 5 calls × frontier model = ~365 tonnes CO₂/year (~80 cars).

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for Green Software Foundation integration.*
