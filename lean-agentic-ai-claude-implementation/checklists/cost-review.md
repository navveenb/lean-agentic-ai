# Cost Review Checklist (Run Weekly)

## Step 1: Measure Current Spend
- [ ] Total daily/weekly LLM API spend
- [ ] Breakdown by model tier (small / medium / frontier)
- [ ] Top 5 agents by cost
- [ ] Average cost per user request
- [ ] Average tokens per request (input + output)

## Step 2: Identify Waste

### Model Waste
- [ ] Any agents using frontier models for simple tasks?
- [ ] Have you benchmarked smaller models on your task distribution?
- [ ] What % of calls could be handled by Tier 1?

### Orchestration Waste
- [ ] How many agents in your longest chain?
- [ ] Can any agents be merged?
- [ ] Any agents producing unused outputs?

### Reflection Waste
- [ ] What % of reflection cycles actually change the output?
- [ ] Is reflection conditional or unconditional?

### Context Waste
- [ ] Average context tokens per call?
- [ ] What % of context is relevant to the task?

### Caching Opportunities
- [ ] Current cache hit rate?
- [ ] Estimated cacheable % of requests?
- [ ] Is tool result caching implemented?

## Step 3: Prioritize

Rank optimizations by daily savings. The top 3 are almost always: model routing, caching, and context reduction.

## Step 4: Set Targets
- [ ] Target cost per request: $______
- [ ] Target daily spend: $______
- [ ] Target cache hit rate: ______%
- [ ] Next review date: ______
