---
name: model-recommender
description: Recommend the right model tier for each LLM task type
user-invocable: false
---

# Model Recommender Skill

## Task-to-Tier Mapping

### Tier 1: Small / Fast (Haiku, GPT-4o-mini, Gemini Flash)
- Classification (spam/not-spam, category assignment)
- Entity extraction (names, dates, emails)
- Sentiment analysis
- Routing decisions
- Simple formatting (JSON restructuring, template filling)
- Yes/no judgments, slot filling

### Tier 2: Mid-Range (Sonnet, GPT-4o, Gemini Pro)
- Summarization (single document)
- Translation
- Simple code generation (known patterns)
- Structured data extraction from complex documents
- Q&A with provided context
- Email/message drafting

### Tier 3: Frontier (Opus, GPT-4/o1, Gemini Ultra)
- Complex multi-step reasoning
- Novel problem solving
- Nuanced creative writing
- Multi-document synthesis
- Architectural planning
- Novel/complex code generation

## Decision Rules

1. When in doubt, start small — default to Tier 1.
2. Classification is ALWAYS Tier 1.
3. Extraction is almost always Tier 1.
4. Summarization is Tier 2 (unless multi-document → Tier 3).
5. Code generation: boilerplate = Tier 1, standard = Tier 2, novel = Tier 3.
6. If a task could be done with regex/rules → no LLM at all.

## Red Flags
- Frontier model for classification → should be Tier 1
- Frontier model for formatting/extraction → should be Tier 1
- Frontier model for simple summarization → should be Tier 2
- Any LLM call for a deterministic task → should be code, not LLM
