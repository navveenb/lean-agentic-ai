# Token Economics of Agentic Systems

## Hidden Cost Multipliers

### 1. System Prompt Repetition
Every agent call re-processes the system prompt. 5 agents = 5× prompt tokens.

| Prompt Size | Single Call | 5-Agent Chain |
|------------|------------|---------------|
| 500 tokens | 500 | 2,500 |
| 2,000 tokens | 2,000 | 10,000 |

### 2. Tool Description Overhead
Each tool schema uses 100-500 tokens. 10 tools = 1,000-5,000 tokens of pure overhead per call.

### 3. Inter-Agent Context Passing
Agent A's full output becomes Agent B's input. Verbose outputs multiply downstream costs.

### 4. Reflection Loops
Each cycle reprocesses entire context + previous output. 2 cycles ≈ 3× token cost.

## Real-World Cost Anatomy (Customer Support Agent)

| Component | Tokens | Cost (Sonnet) |
|-----------|--------|---------------|
| System prompt | 1,500 | $0.0045 |
| Conversation history | 2,000 | $0.0060 |
| Tool descriptions (5) | 1,000 | $0.0030 |
| User query | 200 | $0.0006 |
| RAG results | 3,000 | $0.0090 |
| Response output | 500 | $0.0075 |
| **Total** | **8,200** | **$0.031** |

At 50K queries/day = **$46,500/month**.

### After Lean Optimization
Trim prompt, reduce tools, gate RAG, route 60% to Haiku: **$18,000/month**. That's a **61% reduction** with no quality degradation on most queries.
