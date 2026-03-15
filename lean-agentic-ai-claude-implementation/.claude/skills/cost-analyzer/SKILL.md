---
name: cost-analyzer
description: Generate a lean cost analysis report with model right-sizing recommendations and savings estimates
allowed-tools: Read, Write
---

# Cost Analyzer Report Skill

Generate a cost analysis report from scan results in context. Write to `reports/cost-analysis.md`.

## Report Structure

```markdown
# Lean Cost Analysis Report
> Principle 2: "Not every prompt deserves a 70B response"

## Summary
- Total LLM calls found: [count]
- Calls using frontier models: [count]
- Calls that could be downgraded: [count]
- Estimated current monthly cost: $[amount] (at [N] calls/day)
- Estimated optimized monthly cost: $[amount]
- Monthly savings: $[amount] ([X]% reduction)

## Findings by File
[Per-call analysis with file:line, model, task type, recommendation, status emoji]

## Cost Breakdown Table
[Task type | Count | Current tier | Recommended tier | Monthly savings]

## Top 3 Quick Wins
[Highest impact changes]

## Carbon Impact
[Current vs optimized CO₂ estimates]

## Next Steps
[Actionable checklist]
```

## Rules
- Write to `reports/cost-analysis.md`
- Use concrete numbers
- Assume 10,000 calls/day if volume not specified
- Use 0.005 kWh per medium call, 0.03 kWh per frontier call for carbon
- Be honest — if frontier IS needed, say so
