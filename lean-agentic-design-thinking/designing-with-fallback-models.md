# Designing with Fallback Models (FrugalGPT-Style Routing)  
*Smaller Models First, Bigger Models Only If Needed*

---

### Overview

Not every task needs the biggest or most capable model.  
In many cases, smaller models can produce equally good results at a fraction of the cost, latency, and carbon impact.

**Lean Agentic AI** promotes **fallback-based routing**, inspired by ideas like FrugalGPT — starting with the least expensive model and escalating only if necessary.

This approach ensures systems are **efficient by default**, not excessive by design.

---

### The Case for Fallback-Based Routing

| Strategy                   | Benefit                                                 |
|----------------------------|----------------------------------------------------------|
| **Start small**            | Reduces average token and compute cost                   |
| **Escalate only when needed** | Keeps latency low and emissions down                 |
| **Use model confidence**   | Enables objective switching between models               |
| **Route by task type**     | Matches model size to complexity                         |

---

### Model Tiering by Capability

Group models and tools based on complexity and cost, and escalate only when required.

| Tier     | Type of Model/Logic                   | Example Use Cases                 | Examples                           |
|----------|----------------------------------------|-----------------------------------|------------------------------------|
| **Tier 1** | Rules, regex, deterministic functions | Pattern matching, lookups         | Regex filters, routing rules       |
| **Tier 2** | Small models                          | Classification, summarization     | Claude Haiku, LLaMA 7B, Gemini Nano|
| **Tier 3** | Medium models                         | Multi-step reasoning              | GPT-3.5, Mistral 7B with CoT       |
| **Tier 4** | Large-scale models                    | Complex generation, fallback only | GPT-4, Claude Opus                 |

Use these tiers to build escalation paths that reduce unnecessary compute while maintaining reliability.

---

### Common Fallback Patterns

- **Confidence-based escalation**  
  If small model response is low-confidence or unclear → try larger model

- **Task-based routing**  
  Use small models for simple classification, larger ones for summarization or reasoning

- **Rule-model hybrid**  
  Try rules or retrieval first. If unresolved, escalate to a model

- **Dynamic routing agents**  
  Orchestrators that choose models based on token budget, latency, or quality metrics

---

### Example Routing Strategy

```python
if rules.solve(input):
    return result
elif small_model.confidence > 0.85:
    return small_model.output
else:
    return large_model.output
```

This structure can reduce overall LLM calls by 50% or more in production systems.

---

### Don’t Just Fall Back — Fall Forward

Fallbacks are not about limiting intelligence.  
They’re about **prioritizing precision and efficiency**, escalating only when necessary.

---

### Mental Model

> Always ask:  
> Can this task be handled by a lighter model before I reach for the heaviest one?

Design systems that think twice before scaling up.

---

📖 Explore fallback architectures, model routing agents, and FrugalGPT design patterns in  
[Lean Agentic AI: Cost, Carbon, and Control](https://leanagenticai.com/)
