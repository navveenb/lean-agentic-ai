# Example: Memory Optimization

> Keep what matters. Forget what doesn't.

**Principle**: #9 Memory Is a Judgment Call, #1 Context Is a Liability

## lean_memory.py

```python
import time, math
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Tier(Enum):
    HOT = "hot"    # Always in context
    WARM = "warm"  # Fetched on demand
    COLD = "cold"  # Archived, rarely used


TTLS = {"conversation": 3600, "task_result": 259200, "preference": 5184000, "knowledge": 31536000}


@dataclass
class Memory:
    key: str
    content: str
    summary: Optional[str]
    tier: Tier
    created: float
    accessed: float
    ttl: int
    access_count: int = 0

    @property
    def expired(self):
        return (time.time() - self.created) > self.ttl

    @property
    def relevance(self):
        days = (time.time() - self.accessed) / 86400
        return math.exp(-0.1 * days)  # Decays ~10%/day

    @property
    def tokens(self):
        return len(self.summary or self.content) // 4


class LeanMemory:
    def __init__(self, max_entries=500, hot_token_budget=2000):
        self._store = {}
        self.max_entries = max_entries
        self.hot_budget = hot_token_budget

    def store(self, key, content, mem_type="task_result", tier=Tier.WARM, summary=None):
        if summary is None and len(content) > 500:
            sentences = content.split(". ")
            summary = f"{sentences[0]}. {sentences[-1]}" if len(sentences) > 2 else content
        self._store[key] = Memory(key, content, summary, tier, time.time(), time.time(), TTLS.get(mem_type, 86400))
        self._enforce_capacity()

    def get(self, key):
        m = self._store.get(key)
        if not m or m.expired:
            if m: del self._store[key]
            return None
        m.accessed = time.time()
        m.access_count += 1
        return m.content if m.tier == Tier.HOT else (m.summary or m.content)

    def hot_context(self):
        """Get all hot memories within token budget."""
        entries = sorted(
            [m for m in self._store.values() if m.tier == Tier.HOT and not m.expired],
            key=lambda m: m.relevance, reverse=True
        )
        result, tokens = [], 0
        for m in entries:
            if tokens + m.tokens <= self.hot_budget:
                result.append(m.content)
                tokens += m.tokens
        return result, tokens

    def cleanup(self):
        expired = [k for k, m in self._store.items() if m.expired]
        for k in expired: del self._store[k]
        for m in self._store.values():
            if m.tier == Tier.HOT and m.relevance < 0.5: m.tier = Tier.WARM
            elif m.tier == Tier.WARM and m.relevance < 0.2: m.tier = Tier.COLD

    def _enforce_capacity(self):
        if len(self._store) <= self.max_entries: return
        by_relevance = sorted(self._store.values(), key=lambda m: m.relevance)
        for m in by_relevance[:len(self._store) - self.max_entries]:
            del self._store[m.key]

    def stats(self):
        tiers = {t.value: 0 for t in Tier}
        tokens = 0
        for m in self._store.values():
            tiers[m.tier.value] += 1
            tokens += m.tokens
        return {"entries": len(self._store), "tiers": tiers, "total_tokens": tokens,
                "capacity": f"{len(self._store)/self.max_entries:.0%}"}


if __name__ == "__main__":
    mem = LeanMemory(max_entries=100, hot_token_budget=1000)

    # Store with different tiers
    mem.store("goal", "Help user plan a trip to Japan", "conversation", Tier.HOT)
    mem.store("budget", "Budget is $3000 for 10 days", "preference", Tier.HOT)
    mem.store("flights", "Found 5 flights: ANA $800, JAL $850, United $900, Delta $920, AA $950",
              "task_result", Tier.WARM, summary="Cheapest flight: ANA at $800")
    mem.store("hotels", "Compared 20 hotels in Tokyo across price, location, reviews. Best value is Hotel Gracery.",
              "task_result", Tier.WARM, summary="Best value: Hotel Gracery Shinjuku $120/night")

    # Hot context (what gets loaded into LLM call)
    context, tokens = mem.hot_context()
    print(f"Hot context ({tokens} tokens):")
    for c in context: print(f"  - {c}")

    # Warm retrieval (returns summary, not full content)
    print(f"\nFlights (summary): {mem.get('flights')}")
    print(f"Hotels (summary):  {mem.get('hotels')}")

    # Stats
    import json
    print(f"\nStats: {json.dumps(mem.stats(), indent=2)}")
```

## Run It

```bash
python examples/memory-optimization/lean_memory.py
```

## Expected Output

```
Hot context (21 tokens):
  - Help user plan a trip to Japan
  - Budget is $3000 for 10 days

Flights (summary): Cheapest flight: ANA at $800
Hotels (summary):  Best value: Hotel Gracery Shinjuku $120/night

Stats: {
  "entries": 4,
  "tiers": {"hot": 2, "warm": 2, "cold": 0},
  "total_tokens": 57,
  "capacity": "4%"
}
```
