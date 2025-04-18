# Day 5 – Common Bloat in Agentic Systems  
*Identifying Inefficiencies Before They Scale*

---

### Overview

As agentic systems grow in capability, they often accumulate unintended inefficiencies — consuming more compute, memory, and model capacity than needed.

**Bloat** is what happens when agents do more than necessary, remember more than they should, or call models and tools without clear purpose.

In Lean Agentic AI, detecting and eliminating bloat early is key to building cost-effective, carbon-aware, and manageable systems.

---

### Signs of Bloat in Agentic Systems

| Pattern                         | What to Watch For                                                  |
|----------------------------------|--------------------------------------------------------------------|
| **Over-delegation**              | Agents calling other agents for simple or redundant tasks         |
| **Over-memory**                  | Storing all context, even when it’s never used                    |
| **Over-calling**                 | Using large models or tools multiple times without optimization   |
| **Looping Workflows**            | Agents triggering each other in cycles, especially without limits |
| **Tool or Model Overreach**      | Invoking tools/models when lightweight alternatives would suffice |
| **No Exit Strategy**             | Lack of boundaries or conditions to end reasoning or retries      |

---

### Example of Hidden Bloat

> A research agent tries to “think deeply” by calling a large LLM 3 times  
> Then it delegates summarization to another agent  
> That agent pulls in multiple tools — including search and a separate model — to perform the task

Result: One query spawns 7+ model calls, multiple tool invocations, and memory writes — many of which could be skipped.

---

### What Causes Bloat?

- Lack of scoped agent responsibilities  
- No carbon- or cost-awareness in orchestration logic  
- Assumption that more context = better results  
- Using general-purpose tools when task-specific ones are more efficient  
- Designing without guardrails or fallback logic

---

### Mental Model

> Every unnecessary agent call, memory write, or model run adds to the system’s invisible cost — in money, carbon, and complexity.

---

### How to Avoid It

- Design agents with single-responsibility principles  
- Introduce cost/carbon-aware decision checkpoints  
- Set boundaries on model and tool usage  
- Use lightweight tools for lightweight tasks  
- Regularly audit agent behavior using logs or traces

---

📖 Learn more about agent orchestration strategies and efficiency scoring in  
[Lean Agentic AI: Cost, Carbon, and Control](https://leanagenticai.com/)
