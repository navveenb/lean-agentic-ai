# Designing the Right Prompt  
*Small, Specific, and Scaled with Purpose*

---

### Overview

In agentic systems, prompts are how agents think, talk, and act.

They’re used to invoke models, communicate with tools, pass intent between agents, and guide reasoning.  
But more tokens ≠ better performance.

**Lean Agentic AI** emphasizes designing the **right prompt** — not the longest one.  
Because every extra word adds cost, carbon, and cognitive weight.

---

### Why Prompts Matter in Agentic Systems

| Use Case                     | Prompt Role                                          |
|------------------------------|------------------------------------------------------|
| **Agent reasoning**          | Guides task execution or step-by-step logic          |
| **Tool invocation**          | Structures inputs for APIs or functions              |
| **Model control**            | Sets tone, format, and constraints                   |
| **Delegation between agents**| Communicates goals, constraints, or outcomes         |
| **Reflection and memory**    | Triggers learning or summarization from past runs    |

---

### Prompt Length = Token Cost

Prompts are converted into **tokens**, and most LLM models — including commercial APIs — bill based on the **number of tokens processed**.

That means:

- Longer prompts = more tokens = higher cost  
- More tokens = more compute = higher carbon impact  
- Every unnecessary word adds up at scale

Even small optimizations in prompt design can reduce system-wide energy use and expenses.

---

### Prompting Principles for Lean Systems

1. **Be small but clear**  
   The best prompt gives context in the fewest tokens possible.

2. **Be structured**  
   Use bullets, delimiters, or numbered steps where it improves reliability.

3. **Be scoped**  
   Don’t carry unnecessary history or memory into every prompt.

4. **Design for reuse**  
   Modular prompts can scale across agents, tools, or tasks.

5. **Choose precision over prose**  
   You're writing for a model — not a human reader.

---

### 🛠 Tool-Oriented Prompt: API Summarization Agent

```
You are an API summarization agent.

Goal: Summarize the response from the API in under 60 words.  
Constraints: Highlight only user-facing impacts. Exclude technical jargon.  
Output format: Bullet points.
```

**Why it’s lean:**  
- Clear goal  
- Focused constraint  
- Explicit output format  
- No filler or open-ended instructions

---

### What to Avoid

- Overly verbose instructions  
- Multi-goal prompts in one message  
- Including full memory in every task  
- Repeating system prompts across chained agents

---

### Mental Model

> The right prompt is not about saying more — it’s about saying only what’s needed.  
> In Lean Agentic AI, prompts are efficient, focused, and built to support scalable execution.

---

📖 Learn how prompt strategy intersects with model choice, memory, and orchestration in  
[Lean Agentic AI: Cost, Carbon, and Control](https://leanagenticai.com/)

---
