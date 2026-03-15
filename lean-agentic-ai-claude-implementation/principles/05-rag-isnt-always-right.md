# Principle 5: RAG Isn't Always Right

> **Retrieve only when it's truly needed.**

## When RAG Makes Sense
- Task requires recent, specific, or proprietary information
- Factual accuracy is critical (legal, medical, financial)
- Knowledge base changes frequently

## When RAG Is Wasteful
- Model already knows the answer
- Retrieved docs don't improve quality
- Query is creative/reasoning-heavy — retrieval adds noise
- Same docs retrieved repeatedly (use caching)

## Techniques
1. **Retrieval Gating**: Lightweight check before retrieval — does this need external knowledge?
2. **Retrieval Caching**: Cache similar query results.
3. **Quality-Scored Retrieval**: Only inject above-threshold docs.
4. **Hybrid**: Let agent decide mid-task if it needs retrieval.

## Unnecessary RAG Cost
At 50K queries/day: **$1,500–$3,500/month** in pure waste from always-on RAG.

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for adaptive RAG architectures.*
