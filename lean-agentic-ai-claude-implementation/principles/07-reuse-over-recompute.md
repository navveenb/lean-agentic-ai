# Principle 7: Reuse Is the New Reasoning

> **Don't re-run. Re-think.**

## Caching Strategies
1. **Exact-Match**: Hash input, return cached response. Best for classification, extraction.
2. **Semantic Cache**: Embedding similarity match. Best for Q&A, summarization.
3. **Tool Result Cache**: Cache API/DB/search results. 20-60% hit rate.
4. **Intermediate Result Cache**: Cache pipeline stage outputs.
5. **Prompt Prefix Cache**: Use provider's prompt caching features.

## Impact (30% cache hit rate)
| Metric | Without | With Caching |
|--------|---------|-------------|
| LLM Calls/day | 100K | 70K |
| Monthly Savings | — | **$4,500** |

Cache infrastructure costs 1-5% of savings.

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for cognitive caching architectures.*
