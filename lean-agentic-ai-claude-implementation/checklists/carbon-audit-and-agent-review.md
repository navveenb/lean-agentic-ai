# Carbon Audit Checklist

## Baseline Your Emissions
```
Daily CO₂ (kg) = Daily LLM Calls × Energy/Call (kWh) × Grid Intensity (gCO₂/kWh) / 1000
```

Energy per call: Small ~0.001 kWh, Medium ~0.005 kWh, Frontier ~0.03 kWh.

- [ ] Daily LLM calls: ______
- [ ] Average model size: ______
- [ ] Deployment region: ______
- [ ] Region carbon intensity: ______ gCO₂/kWh
- [ ] Estimated daily CO₂: ______ kg

## Reduction Levers
- [ ] Deployed in a low-carbon region?
- [ ] Batch workloads time-shifted to green periods?
- [ ] All agents using right-sized models?
- [ ] Cache hit rate reducing total calls?

## Set Targets
- [ ] Current annual CO₂: ______ tonnes
- [ ] Target reduction: ______%
- [ ] Primary lever: ______
- [ ] Carbon estimate in monitoring dashboard?

---

# Agent Design Review Checklist

For each agent in production:

- [ ] Purpose described in one sentence?
- [ ] Does something no other agent does?
- [ ] Removing it would degrade output quality?
- [ ] Model tier: ______ (justified?)
- [ ] Number of tools: ______ (all used?)
- [ ] Total context tokens: ______ (can any be removed?)
- [ ] Memory has TTLs?
- [ ] Max turns: ______ Max cost: $______
- [ ] Failure behavior: retry / fallback / escalate?
- [ ] Output validated before passing downstream?
- [ ] Performance monitored?

**If you can't fill most fields, the agent isn't ready for production.**
