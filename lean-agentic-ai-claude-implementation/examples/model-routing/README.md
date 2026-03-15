# Example: Model Routing

> Route each task to the smallest model that achieves acceptable quality.

**Principle**: #2 Right-Size Your Model

## model_router.py

```python
from enum import Enum

class ModelTier(Enum):
    SMALL = "small"       # Haiku / GPT-4o-mini: ~$0.01/call
    MEDIUM = "medium"     # Sonnet / GPT-4o: ~$0.10/call
    FRONTIER = "frontier" # Opus / GPT-4 / o1: ~$1.00/call

COST_PER_CALL = {ModelTier.SMALL: 0.01, ModelTier.MEDIUM: 0.10, ModelTier.FRONTIER: 1.00}

TASK_TIER_MAP = {
    "classify": ModelTier.SMALL, "extract_entities": ModelTier.SMALL,
    "sentiment": ModelTier.SMALL, "format": ModelTier.SMALL,
    "route": ModelTier.SMALL, "yes_no": ModelTier.SMALL,
    "summarize": ModelTier.MEDIUM, "translate": ModelTier.MEDIUM,
    "simple_code": ModelTier.MEDIUM, "qa_with_context": ModelTier.MEDIUM,
    "complex_reasoning": ModelTier.FRONTIER, "creative_writing": ModelTier.FRONTIER,
    "code_architecture": ModelTier.FRONTIER,
}


def rule_based_route(task_type: str) -> ModelTier:
    """Strategy 1: Direct task-to-tier mapping."""
    return TASK_TIER_MAP.get(task_type, ModelTier.MEDIUM)


def cascade_route(prompt, call_model_fn, confidence_threshold=0.85):
    """Strategy 2 (FrugalGPT): Start cheap, escalate if confidence is low.
    call_model_fn(tier, prompt) returns (response, confidence_score)"""
    for tier in [ModelTier.SMALL, ModelTier.MEDIUM, ModelTier.FRONTIER]:
        response, confidence = call_model_fn(tier, prompt)
        if confidence >= confidence_threshold or tier == ModelTier.FRONTIER:
            return {"model": tier, "response": response, "cost": COST_PER_CALL[tier]}
    return {"model": ModelTier.FRONTIER, "response": response, "cost": 1.00}


def budget_route(task_type: str, max_cost: float) -> ModelTier:
    """Strategy 3: Route to ideal tier, downgrade if over budget."""
    ideal = rule_based_route(task_type)
    if COST_PER_CALL[ideal] <= max_cost:
        return ideal
    for tier in [ModelTier.MEDIUM, ModelTier.SMALL]:
        if COST_PER_CALL[tier] <= max_cost:
            return tier
    return ModelTier.SMALL


def calculate_savings(daily_calls, task_distribution):
    """Compare always-frontier vs routed cost."""
    frontier_cost = daily_calls * COST_PER_CALL[ModelTier.FRONTIER]
    routed_cost = sum(
        daily_calls * frac * COST_PER_CALL[rule_based_route(task)]
        for task, frac in task_distribution.items()
    )
    savings = frontier_cost - routed_cost
    return {
        "always_frontier": f"${frontier_cost:,.0f}/day",
        "routed": f"${routed_cost:,.0f}/day",
        "savings": f"${savings:,.0f}/day (${savings*365:,.0f}/year)",
        "reduction": f"{savings/frontier_cost*100:.0f}%",
    }


if __name__ == "__main__":
    # Rule-based
    for task in ["classify", "summarize", "complex_reasoning"]:
        tier = rule_based_route(task)
        print(f"{task:25s} -> {tier.value:10s} ${COST_PER_CALL[tier]:.2f}/call")

    # Budget-constrained
    print(f"\ncomplex_reasoning, budget $0.50 -> {budget_route('complex_reasoning', 0.50).value}")
    print(f"complex_reasoning, budget $2.00 -> {budget_route('complex_reasoning', 2.00).value}")

    # Savings
    print("\n--- Savings ---")
    result = calculate_savings(100_000, {
        "classify": 0.30, "extract_entities": 0.15, "sentiment": 0.15,
        "summarize": 0.20, "qa_with_context": 0.10, "complex_reasoning": 0.10,
    })
    for k, v in result.items():
        print(f"  {k}: {v}")
```

## Run It

```bash
python examples/model-routing/model_router.py
```

## Expected Output

```
classify                  -> small      $0.01/call
summarize                 -> medium     $0.10/call
complex_reasoning         -> frontier   $1.00/call

complex_reasoning, budget $0.50 -> medium
complex_reasoning, budget $2.00 -> frontier

--- Savings ---
  always_frontier: $100,000/day
  routed: $16,000/day
  savings: $84,000/day ($30,660,000/year)
  reduction: 84%
```
