# Day 11 – Prompt Optimization vs. Agent Optimization  
*Choosing the Right Level to Tune*

---

### Overview

Prompt engineering often gets the spotlight — and for good reason.  
Better prompts can improve accuracy, clarity, and relevance. But prompts alone can’t fix systemic issues in agentic design.

**Lean Agentic AI** draws a clear line:  
**Prompt optimization** improves how a model responds.  
**Agent optimization** improves what the system does, how it behaves, and when it calls a model in the first place.

---

### Prompt Optimization: Task-Level Improvements

Prompt tuning is most useful when:

- A model is misinterpreting intent  
- You need more consistent output formatting  
- The model's logic is almost correct but needs guidance

But it cannot solve:

- Over-delegation between agents  
- Redundant or unnecessary model/tool usage  
- Inefficient memory or retry patterns  
- Costly workflows that run by default

---

### Agent Optimization: System-Level Improvements

Agent optimization answers questions like:

- Does this task require a model at all?  
- Could a rule-based function handle this instead?  
- Is the current agent delegation too deep or unclear?  
- Are we using the smallest effective model for the task?  
- Is memory being retrieved and reused properly?

These choices drive down **cost**, **carbon**, and **complexity**.

---

### When to Optimize What

| Scenario                                | Best Focus Area          |
|-----------------------------------------|---------------------------|
| Model is inconsistent or verbose        | Prompt optimization       |
| Agent calls model too frequently        | Agent optimization        |
| Workflow has unnecessary tool chaining  | Agent optimization        |
| Model fails to follow instructions      | Prompt optimization       |
| Output is fine but system is expensive  | Agent optimization        |

---

### Lean Principle

> Optimize the **system**, not just the sentence.

Begin with agent logic, orchestration, and model selection.  
Then fine-tune the prompt to get clean and efficient outputs — not the other way around.

---

### Mental Model

> The best prompt inside a bloated workflow still wastes money and energy.  
> Agent optimization defines what should happen.  
> Prompt optimization defines how it happens.

---

📖 Explore layered optimization patterns across prompts, agents, and orchestration in  
[Lean Agentic AI: Cost, Carbon, and Control](https://leanagenticai.com/)
