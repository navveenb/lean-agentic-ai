# Example: Cognitive Caching

> The fastest LLM call is the one you never make.

**Principle**: #7 Reuse Over Recompute

## cognitive_cache.py

```python
import hashlib, time, json
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class CacheEntry:
    value: str
    created_at: float
    ttl: int
    hits: int = 0

    @property
    def expired(self):
        return (time.time() - self.created_at) > self.ttl


class CognitiveCache:
    """Multi-layer cache: exact-match + tool results."""

    def __init__(self):
        self._exact = {}     # hash -> CacheEntry
        self._tools = {}     # tool:hash -> CacheEntry
        self.hits = 0
        self.misses = 0
        self._cost_saved = 0.0

    def _hash(self, *parts):
        return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:16]

    # --- Layer 1: Exact Match ---

    def get(self, prompt, context="", avg_cost=0.05):
        key = self._hash(prompt, context)
        entry = self._exact.get(key)
        if entry and not entry.expired:
            entry.hits += 1
            self.hits += 1
            self._cost_saved += avg_cost
            return entry.value
        if entry and entry.expired:
            del self._exact[key]
        self.misses += 1
        return None

    def store(self, prompt, context, response, ttl=3600):
        key = self._hash(prompt, context)
        self._exact[key] = CacheEntry(response, time.time(), ttl)

    # --- Layer 2: Tool Results ---

    def get_tool(self, tool_name, params):
        key = f"{tool_name}:{self._hash(json.dumps(params, sort_keys=True))}"
        entry = self._tools.get(key)
        if entry and not entry.expired:
            entry.hits += 1
            return entry.value
        return None

    def store_tool(self, tool_name, params, result, ttl=300):
        key = f"{tool_name}:{self._hash(json.dumps(params, sort_keys=True))}"
        self._tools[key] = CacheEntry(result, time.time(), ttl)

    # --- Stats ---

    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def stats(self):
        return {
            "exact_entries": len(self._exact),
            "tool_entries": len(self._tools),
            "hits": self.hits, "misses": self.misses,
            "hit_rate": f"{self.hit_rate:.0%}",
            "cost_saved": f"${self._cost_saved:.2f}",
        }


if __name__ == "__main__":
    cache = CognitiveCache()

    queries = [
        ("What is the return policy?", "ecommerce"),
        ("What is the return policy?", "ecommerce"),  # HIT
        ("How do I track my order?", "ecommerce"),
        ("What is the return policy?", "ecommerce"),  # HIT
        ("How do I track my order?", "ecommerce"),     # HIT
    ]

    for prompt, ctx in queries:
        cached = cache.get(prompt, ctx, avg_cost=0.05)
        if cached:
            print(f"  CACHE HIT:  {prompt}")
        else:
            cache.store(prompt, ctx, f"Answer to: {prompt}")
            print(f"  LLM CALL:   {prompt}")

    # Tool caching
    cache.store_tool("weather_api", {"city": "Mumbai"}, '{"temp": 32}', ttl=600)
    result = cache.get_tool("weather_api", {"city": "Mumbai"})
    print(f"\n  Tool cache: {result}")
    print(f"\n  Stats: {json.dumps(cache.stats(), indent=2)}")
```

## Run It

```bash
python examples/caching-strategy/cognitive_cache.py
```

## Expected Output

```
  LLM CALL:   What is the return policy?
  CACHE HIT:  What is the return policy?
  LLM CALL:   How do I track my order?
  CACHE HIT:  What is the return policy?
  CACHE HIT:  How do I track my order?

  Tool cache: {"temp": 32}

  Stats: {
    "exact_entries": 2, "tool_entries": 1,
    "hits": 3, "misses": 2,
    "hit_rate": "60%", "cost_saved": "$0.15"
  }
```
