# Carbon Footprint of LLM Calls

## Energy Per Inference

| Model Class | Energy/Query | CO₂/Query (avg grid) |
|------------|-------------|----------------------|
| Small (1-8B) | ~0.001 kWh | ~0.4g |
| Medium (8-30B) | ~0.005 kWh | ~2g |
| Frontier (70B+) | ~0.03 kWh | ~12g |

## Carbon by Region

| Region | gCO₂/kWh | CO₂ per Frontier Query |
|--------|-----------|----------------------|
| Quebec / Norway | 20-30 | 0.6-1.5g |
| France | 50-80 | 1.5-4g |
| US Average | 350-400 | 10-20g |
| India | 600-750 | 18-37g |

**The gap between cleanest and dirtiest regions is 20-40×.**

## System-Level Example

100K requests/day, 5 calls each, mixed models, US Average:
- Current: ~284 tonnes CO₂/year (~62 cars)
- After routing + caching + green region: ~7.3 tonnes/year (~1.6 cars)
- **Reduction: 97%**

## What You Can Do Today
1. Measure (use the formula above)
2. Route (smaller models for simple tasks)
3. Cache (every cached response = zero carbon)
4. Relocate (green regions for batch workloads)
5. Track (add carbon to your monitoring dashboard)

## Resources
- [Electricity Maps](https://electricitymaps.com/) — Live carbon data
- [Green Software Foundation](https://greensoftware.foundation/) — SCI spec
- [CodeCarbon](https://github.com/mlco2/codecarbon) — Python carbon tracker
