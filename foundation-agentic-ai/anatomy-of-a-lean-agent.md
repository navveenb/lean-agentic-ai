# Anatomy of a Lean Agent  
*Components, State, Memory, Models, and Tools*

---

### Overview

A Lean Agent is not just a wrapper around a model or a task executor.  
It’s a **focused, efficient, and responsible unit** designed with clear intent, minimal memory, purposeful tool access, and environmental awareness.

Understanding the anatomy of a Lean Agent is key to avoiding waste and complexity.

---

### Core Components of a Lean Agent

| Component     | Purpose in the Agent's Design                                        |
|---------------|----------------------------------------------------------------------|
| **Goal**       | The specific outcome the agent is meant to achieve                  |
| **State**      | Temporary context used during a task or within a session            |
| **Memory**     | Information remembered across runs (when and why it matters)        |
| **Models & Tools** | APIs, language models, search utilities, or other agents it can invoke |
| **Reasoning**  | Logic to decide next steps based on input and current state         |
| **Boundaries** | When to stop, escalate, or defer — based on purpose and constraints |
| **Impact**     | Awareness of the cost and carbon impact of decisions                |

A Lean Agent should know its limits — and act with precision and awareness.

---

### Example

> **Goal**: Summarize today’s AI policy news  
> **State**: Topic = “AI Regulation”; Date = “Today”  
> **Memory**: Last 3 days of summaries  
> **Models & Tools**: Lightweight web search, low-emission summarization model  
> **Reasoning**: Skip if no new policy updates  
> **Boundary**: Do not summarize repetitive or low-impact headlines  
> **Impact**: Prefer efficient models; log skipped steps to avoid unnecessary compute

---

### Lean vs. Bloated Agents

| Aspect         | Lean Agent                                | Bloated Agent                              |
|----------------|--------------------------------------------|---------------------------------------------|
| **Scope**      | One clear responsibility                   | Broad or overlapping tasks                  |
| **Memory Use** | Stores only what’s needed and reused       | Retains unnecessary or unused data          |
| **Models & Tools** | Used sparingly with clear justification | Invoked frequently, often without checks    |
| **Behavior**   | Predictable with fallback logic            | Open-ended or difficult to trace            |
| **Impact**     | Cost and carbon aware                      | Ignores efficiency and environmental load   |

---

### Design Tip

Before you build an agent, ask:

- What is its specific outcome?
- What does it **really** need to remember?
- What **models and tools** can it access — and what’s their cost or carbon impact?
- How does it know when to stop, defer, or escalate?

This kind of intentional design keeps agents lean, transparent, and aligned with responsible compute practices.

---

### Mental Model

> A Lean Agent is like a thoughtful specialist:  
> Focused on its mission, aware of its tools, and accountable for its footprint.

---

📖 Dive deeper into reusable patterns, model selection trade-offs, and agent boundary design in  
[Lean Agentic AI: Cost, Carbon, and Control](https://leanagenticai.com/)
