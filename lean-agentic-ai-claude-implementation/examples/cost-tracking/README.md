# Example: Cost Tracking

> Track, attribute, and alert on LLM costs per agent, per request, per day.

**Principle**: #10 Governance, #2 Model Selection

## cost_tracker.py

```python
from dataclasses import dataclass, field
from datetime import date
from collections import defaultdict

MODEL_PRICING = {  # per 1M tokens: (input, output)
    "haiku": (0.25, 1.25), "sonnet": (3.00, 15.00), "opus": (15.00, 75.00),
    "gpt-4o-mini": (0.15, 0.60), "gpt-4o": (2.50, 10.00),
}

@dataclass
class CostTracker:
    daily_budget: float = 100.0
    per_request_budget: float = 1.0
    _daily: dict = field(default_factory=lambda: defaultdict(float))
    _by_agent: dict = field(default_factory=lambda: defaultdict(float))
    _by_request: dict = field(default_factory=lambda: defaultdict(float))
    _call_count: int = 0

    def estimate_cost(self, model, input_tokens, output_tokens):
        inp, out = MODEL_PRICING.get(model, (3.0, 15.0))
        return (input_tokens / 1e6) * inp + (output_tokens / 1e6) * out

    def check_budget(self, model, input_tokens, output_tokens, request_id=None):
        """Pre-flight check: will this call exceed budget?"""
        est = self.estimate_cost(model, input_tokens, output_tokens)
        today = date.today().isoformat()
        daily_used = self._daily[today]
        req_used = self._by_request.get(request_id, 0) if request_id else 0
        if request_id and (req_used + est) > self.per_request_budget:
            return {"ok": False, "reason": "request budget exceeded", "est": est}
        if (daily_used + est) > self.daily_budget:
            return {"ok": False, "reason": "daily budget exceeded", "est": est}
        return {"ok": True, "est": est, "daily_remaining": self.daily_budget - daily_used}

    def record(self, agent_name, model, input_tokens, output_tokens, request_id=None):
        """Record a completed LLM call."""
        cost = self.estimate_cost(model, input_tokens, output_tokens)
        today = date.today().isoformat()
        self._daily[today] += cost
        self._by_agent[agent_name] += cost
        if request_id:
            self._by_request[request_id] += cost
        self._call_count += 1
        # Alert at 80%
        if self._daily[today] > self.daily_budget * 0.8:
            print(f"  WARNING: 80% of daily budget used (${self._daily[today]:.2f}/${self.daily_budget})")
        return cost

    def summary(self):
        today = date.today().isoformat()
        return {
            "date": today,
            "total_cost": f"${self._daily[today]:.4f}",
            "calls": self._call_count,
            "by_agent": {k: f"${v:.4f}" for k, v in self._by_agent.items()},
            "budget_used": f"{(self._daily[today]/self.daily_budget)*100:.1f}%",
        }


if __name__ == "__main__":
    tracker = CostTracker(daily_budget=50.0, per_request_budget=0.50)

    # Pre-flight check
    check = tracker.check_budget("sonnet", 2000, 500)
    print(f"Pre-flight: {'OK' if check['ok'] else 'BLOCKED'} (est ${check['est']:.4f})")

    # Record calls
    tracker.record("classifier", "haiku", 500, 50, "req-001")
    tracker.record("summarizer", "sonnet", 3000, 800, "req-001")
    tracker.record("planner", "opus", 5000, 2000, "req-002")

    # Summary
    import json
    print(json.dumps(tracker.summary(), indent=2))
```

## Run It

```bash
python examples/cost-tracking/cost_tracker.py
```

## Expected Output

```
Pre-flight: OK (est $0.0135)
{
  "date": "2026-03-14",
  "total_cost": "$0.2301",
  "calls": 3,
  "by_agent": {
    "classifier": "$0.0002",
    "summarizer": "$0.0210",
    "planner": "$0.2250"
  },
  "budget_used": "0.5%"
}
```
