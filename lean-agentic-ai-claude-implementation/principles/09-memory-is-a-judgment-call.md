# Principle 9: Memory Isn't a Journal — It's a Judgment Call

> **Storing everything is hoarding, not intelligence.**

## Memory Tiers
- **Hot** (in-context): Current task state, always loaded. Small.
- **Warm** (retrievable): Recent interactions, fetched on demand. Indexed.
- **Cold** (archival): Historical patterns. Compressed, rarely accessed.
- **Discarded**: Redundant, stale, low-value. Gone. That's okay.

## Techniques
1. **TTLs**: Conversation = session, task results = 1-7 days, preferences = 30-90 days.
2. **Summarize-then-Discard**: 10-word summary of 500-word conversation. 2% storage.
3. **Relevance Decay**: Exponential decay on unused memories.
4. **Capacity Limits**: Hard cap, evict lowest-relevance on exceed.
5. **Memory Cost Index**: `(storage + retrieval + context cost) / likelihood of future use`.

📖 *See [Lean Agentic AI](https://leanagenticai.com/) for intentional forgetting strategies.*
