---
name: carbon-estimator
description: Estimate the carbon footprint of an agentic AI system based on its LLM usage
user-invocable: true
allowed-tools: Read, Write
model: haiku
---

# Carbon Estimator

Estimate the CO₂ emissions of an agentic system based on model usage, call volume, and deployment region.

## Lean Principle

- [x] #6 Emissions don't show up in your logs

## Instructions

### Step 1: Gather inputs

From the user or from context, determine:
- **Daily LLM call volume** (or estimate from code scan)
- **Model distribution** (% small, % medium, % frontier)
- **Deployment region** (or assume US Average if unknown)

### Step 2: Calculate energy

Use these energy-per-call estimates:

| Model Size | Energy per Call (kWh) |
|-----------|----------------------|
| Small (Haiku, GPT-4o-mini, Flash) | 0.001 |
| Medium (Sonnet, GPT-4o, Pro) | 0.005 |
| Frontier (Opus, GPT-4, o1, Ultra) | 0.03 |

```
Total daily energy (kWh) =
  (small_calls × 0.001) + (medium_calls × 0.005) + (frontier_calls × 0.03)
```

### Step 3: Calculate carbon

Use these regional carbon intensities (gCO₂/kWh):

| Region | gCO₂/kWh |
|--------|-----------|
| Quebec / Norway / Iceland | 25 |
| France / Sweden | 70 |
| US West (Oregon) | 100 |
| Netherlands / UK | 200 |
| US Average | 380 |
| Germany | 350 |
| India | 700 |
| Poland / Coal regions | 800 |

```
Daily CO₂ (grams) = Total daily energy × Regional carbon intensity
Annual CO₂ (kg) = Daily CO₂ × 365 / 1000
```

### Step 4: Calculate optimized scenario

Assume lean optimizations:
- Model routing: shift 60% of frontier calls to medium, 30% of medium calls to small
- Caching: 30% cache hit rate (reduces total calls by 30%)
- Green region: use the cleanest available region (25 gCO₂/kWh)

Recalculate with these optimizations applied.

### Step 5: Write report

Write to `reports/carbon-estimate.md` with:
- Current estimated annual CO₂ (kg)
- Optimized estimated annual CO₂ (kg)
- Reduction percentage
- Human-relatable equivalents:
  - Cars driven for a year (÷ 4,600 kg)
  - Flights (÷ 255 kg per domestic flight)
  - Phone charges (÷ 0.008 kg per charge)
- Top recommendation

## Example

Input: 50,000 calls/day, 70% medium, 30% frontier, deployed in US Average.

Output:
```
Current: 50K calls/day → 212.5 kWh/day → 80.75 kg CO₂/day → 29,474 kg/year
Equivalent: ~6.4 cars driven for a year

Optimized: 35K calls/day (caching) → 28 kWh/day (routing) → 0.7 kg CO₂/day (green region) → 256 kg/year
Equivalent: ~1 domestic flight

Reduction: 99.1%
Top recommendation: Move batch workloads to Quebec (25 gCO₂/kWh)
```
