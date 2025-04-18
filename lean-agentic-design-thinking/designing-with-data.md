# Designing with Data as a First-Class Citizen  
*The Right Input Shapes the Right Output*

---

### Overview

In agentic systems, we often obsess over models, memory, and prompts — but overlook the most foundational element: **data**.

**Lean Agentic AI** treats **data as a first-class design decision**, not just a variable passed through.  
Clean, scoped, and meaningful data inputs reduce reasoning complexity, cost, and emissions — while improving output quality.

---

### Why Data Design Matters

| Data Design Element           | Risk if Ignored                                |
|-------------------------------|-------------------------------------------------|
| **Unfiltered inputs**         | Leads to noisy, inconsistent outputs            |
| **Redundant or verbose data** | Increases token count, latency, and model cost  |
| **Poor data structure**       | Confuses tool interfaces and downstream agents  |
| **Unscoped context**          | Makes memory and prompts heavier than needed    |

---

### Lean Data Design Questions

- Is this data necessary for this step or agent?  
- Can it be reduced, compressed, or summarized before use?  
- Can structure (e.g. JSON, tables) improve interpretability?  
- Is the data relevant now — or just carried “in case”?  
- Should the agent retrieve data only when needed (e.g., RAG) instead of receiving it upfront?

---

### Patterns for Data-Aware Design

- **RAG (Retrieval-Augmented Generation)**: Retrieve only what’s needed at inference time  
- **Ingestion Agents**: Preprocess, clean, and format large datasets or documents  
- **Chunking Large Files**: Break into small windows, summarize early  
- **Pre-Filters**: Strip irrelevant sections (e.g., headers, signatures, noise) before agent handoff  
- **Progressive Disclosure**: Pass minimal data first; retrieve more only if needed

---

### Example: Data-Aware Routing

> Instead of passing a full transcript to every summarization agent, a pre-filter removes greetings, filler, and redundant phrases.  
> The result? 30% fewer tokens, same quality summary, lower cost.

---

### Design Tip

Use lightweight preprocessing or retrieval agents to manage **when**, **what**, and **how much** data gets passed into heavier agents.

This keeps downstream systems lean, fast, and focused.

---

### Mental Model

> If you feed an agent everything, it has to process everything.  
> If you feed it only what matters, it can act with speed and clarity.

---

📖 Explore how data scoping, retrieval workflows, and preprocessing agents shape efficiency in  
[Lean Agentic AI: Cost, Carbon, and Control](https://leanagenticai.com/)
