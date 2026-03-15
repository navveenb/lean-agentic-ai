# Framework Comparison: The Lean Lens

> **No agentic AI framework provides cost controls, carbon tracking, or complexity governance out of the box.** Every lean capability must be built by you or added via third-party tools. This is a gap across the entire ecosystem — not a shortcoming of any single framework.

---

## Summary

| Capability | LangGraph | CrewAI | AutoGen | Semantic Kernel | Haystack | Custom (API) |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| **Model routing** (different model per agent/task) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Cost tracking** (token/dollar per call) | ❌ | ❌ | ❌ | ⚠️ | ❌ | ❌ |
| **Budget enforcement** (hard limits, circuit breakers) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Carbon / energy measurement** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Response caching** | ⚠️ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Orchestration control** | ✅ Graph | ⚠️ Seq/Hier | ⚠️ Chat | ✅ Planner | ✅ Pipeline | ✅ Full |
| **Tool scoping** (per-agent tool restrictions) | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| **Observability** | ⚠️ Paid | ⚠️ Basic | ❌ | ⚠️ OTel | ⚠️ | ❌ |

**Legend**: ✅ Supported · ⚠️ Partial or requires paid add-on · ❌ Not available, must build yourself

---

## Key Takeaways

- **Model routing is universal** — every framework lets you assign different models per agent. But most teams default to one model everywhere and never implement actual routing logic.

- **Cost tracking exists nowhere natively** — LangSmith (paid, $39/seat/mo) estimates cost after the fact for LangGraph. Portkey adds budget caps to CrewAI externally. Semantic Kernel exposes token counts via OpenTelemetry but does no cost calculation. Everything else is DIY.

- **Budget enforcement is entirely DIY** — no framework stops a runaway agent from burning through your API budget. Pre-flight cost checks, per-request limits, and circuit breakers are your responsibility.

- **Carbon and energy tracking is a blind spot** — no framework, no platform, no tool in the agentic AI stack measures emissions natively. External tools like CodeCarbon, Electricity Maps, or WattTime must be integrated manually. This is the biggest gap in the ecosystem.

- **Caching is mostly missing** — Haystack is the only framework with built-in component-level caching. LangGraph Platform (paid cloud, not open-source) has experimental "smart caching." Everyone else needs GPTCache, Redis, or custom code.

- **CrewAI encourages agent proliferation** — the role-based model makes it easy to create many agents where fewer would suffice. Benchmarks show ~56% higher token overhead than LangGraph for equivalent tasks.

---

## This Space Is Evolving

This comparison reflects the state of frameworks as of early 2026. The agentic AI ecosystem is moving fast — frameworks add features quarterly, new entrants emerge, and the gap in cost/carbon tooling is becoming more widely recognized. What's missing today may be built-in tomorrow. Revisit this comparison periodically.

---

📖 *For in-depth framework evaluations including cost benchmarks, architecture trade-offs, and lean scoring across 12+ frameworks, refer to [Lean Agentic AI: Minimizing Cost, Carbon, and Complexity](https://leanagenticai.com/) by Navveen Balani.*
