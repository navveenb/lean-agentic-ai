---
name: token-counter
description: Estimate token usage for LLM API calls found in code
user-invocable: false
---

# Token Counter Skill

When you find an LLM API call in code, estimate its token usage using these rules:

## Estimation Rules

### Input Tokens
- **System prompt**: Look for system message content. Estimate 1 token per 4 characters.
- **User message**: Look for user/human message content. If it includes variable interpolation, estimate based on typical content size.
- **Few-shot examples**: Count examples in the messages array. Each example ≈ 200-500 tokens.
- **Tool descriptions**: Count tool/function definitions. Each tool ≈ 100-500 tokens.

### Output Tokens
- **max_tokens parameter**: If set, use that as the upper bound.
- **If not set**: Estimate by task type:
  - Classification/routing: ~10-50 tokens
  - Extraction: ~50-200 tokens
  - Summarization: ~100-500 tokens
  - Code generation: ~200-2000 tokens
  - Creative writing: ~500-4000 tokens

## Cost Rates (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| Haiku / GPT-4o-mini | $0.25 | $1.25 |
| Sonnet / GPT-4o | $3.00 | $15.00 |
| Opus / GPT-4 / o1 | $15.00 | $75.00 |

## Per Call Output

- Estimated input tokens: ____
- Estimated output tokens: ____
- Current model cost per call: $____
- Right-sized model cost per call: $____
