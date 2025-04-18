# Day 4 – Anatomy of a Lean Agent  
*Components, State, Memory, Tools*

---

### Overview

A lean agent is more than just a wrapper around a language model.  
It’s a thoughtfully designed unit that knows its purpose, manages its resources, and fits cleanly into a larger workflow.

Let’s break down what makes up a **Lean Agent**.

---

### Core Components

| Component     | Role in a Lean Agent                                         |
|---------------|---------------------------------------------------------------|
| **Goal**       | The specific objective the agent is responsible for          |
| **State**      | Context or temporary data held during execution              |
| **Memory**     | Information remembered across runs (short or long-term)      |
| **Tools**      | APIs, databases, models, or other agents it can invoke       |
| **Reasoning Logic** | How it decides what to do next based on inputs and state |

---

### Example

> Goal: Summarize the latest AI news  
> State: Topic = “Generative AI”; Date = “Today”  
> Memory: Last 3 days’ headlines  
> Tool: Web search, summarization model  
> Reasoning: If no major update, skip summary for today

---

### Lean vs. Bloated Agents

| Aspect       | Lean Agent                          | Bloated Agent                          |
|--------------|--------------------------------------|-----------------------------------------|
| Scope        | Single, well-defined task            | Broad or unclear responsibilities       |
| Memory Use   | Stores only what’s necessary         | Retains everything “just in case”       |
| Tool Calls   | Purposeful and minimal               | Frequent, redundant, or exploratory     |
| Decision Flow| Clear logic, few paths               | Complex, nested, or unclear flow        |

---

### Design Tip

Before building any agent, define these clearly:

- What outcome should it achieve?
- What inputs and memory are truly needed?
- What tool access is essential?
- How should it behave when uncertain?

This clarity avoids complexity and waste.

---

### Mental Model

> A Lean Agent is like a well-trained specialist — focused, prepared, and efficient.

---

📖 Explore deeper agent structures and real-world design patterns in  
[Lean Agentic AI: Cost, Carbon, and Control](https://leanagenticai.com/)
