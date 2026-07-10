"""meter.py — Cost, energy, and carbon accounting for LLM calls.

Implements the SCI methodology (ISO/IEC 21031): SCI = (E x I) + M per R,
where R (the functional unit) is one rebalance task.

Cost and carbon are tracked as PARALLEL metrics — never collapsed into one number.
All coefficients are configurable in the tables below; defaults are illustrative
mid-2026 figures. Adjust PRICING to current list prices before quoting numbers.
"""

import os
from dataclasses import dataclass, field

# Circuit breaker: hard cap on LLM calls per Meter (i.e., per pipeline run).
# The demo's worst case is 7 (default) / 2 (lean); anything beyond means a
# bug or an unexpected retry storm — stop before it spends more.
MAX_CALLS_PER_RUN = int(os.environ.get("LEAN_DEMO_MAX_CALLS", "10"))

# ── Pricing (USD per 1M tokens) ─────────────────────────────────────────
# cached_in: price applied to tokens served from context cache (~10% of input).
# Keyed by TIER (not model name) — map tiers to concrete models in
# sim_models.LIVE_MODELS, and set these rates to the list price of the
# concrete model your runs actually use.
PRICING = {
    "pro":        {"in": 2.00, "out": 12.00, "cached_in": 0.20},
    "flash":      {"in": 1.50, "out": 9.00,  "cached_in": 0.15},
    "flash-lite": {"in": 0.10, "out": 0.40,  "cached_in": 0.01},
}

# ── Energy model (joules per token, model-class coefficients) ───────────
# Output tokens dominate (autoregressive decode); input is amortized prefill.
ENERGY_J_PER_TOKEN = {
    "pro":        {"in": 0.35, "out": 2.10},
    "flash":      {"in": 0.10, "out": 0.60},
    "flash-lite": {"in": 0.03, "out": 0.16},
}
CACHED_ENERGY_FACTOR = 0.10   # cached prefill skips most recompute

# ── Grid + embodied carbon ──────────────────────────────────────────────
GRID_GCO2_PER_KWH = {
    "us-central1":    404.0,   # illustrative marginal intensity
    "europe-north1":  118.0,   # high-CFE region
}
EMBODIED_GCO2_PER_CALL = 0.012   # M, amortized accelerator lifecycle per call


@dataclass
class Call:
    label: str
    model: str                 # tier key: pro | flash | flash-lite
    tokens_in: int
    tokens_out: int
    tokens_cached: int = 0     # subset of tokens_in served from cache
    actual: str = ""           # concrete model that ran (live mode); display only

    @property
    def fresh_in(self) -> int:
        return max(self.tokens_in - self.tokens_cached, 0)

    def cost_usd(self) -> float:
        p = PRICING[self.model]
        return (self.fresh_in * p["in"]
                + self.tokens_cached * p["cached_in"]
                + self.tokens_out * p["out"]) / 1_000_000

    def energy_wh(self) -> float:
        e = ENERGY_J_PER_TOKEN[self.model]
        joules = (self.fresh_in * e["in"]
                  + self.tokens_cached * e["in"] * CACHED_ENERGY_FACTOR
                  + self.tokens_out * e["out"])
        return joules / 3600.0

    def carbon_g(self, region: str) -> float:
        kwh = self.energy_wh() / 1000.0
        return kwh * GRID_GCO2_PER_KWH[region] + EMBODIED_GCO2_PER_CALL


@dataclass
class Meter:
    name: str
    region: str = "us-central1"
    calls: list = field(default_factory=list)

    def record(self, label, model, tokens_in, tokens_out, tokens_cached=0, actual=""):
        if len(self.calls) >= MAX_CALLS_PER_RUN:
            raise RuntimeError(
                f"Circuit breaker: {self.name} exceeded LEAN_DEMO_MAX_CALLS="
                f"{MAX_CALLS_PER_RUN} LLM calls — aborting to protect quota/cost.")
        self.calls.append(Call(label, model, tokens_in, tokens_out,
                               tokens_cached, actual or model))

    # ── aggregates ──
    def total(self, fn):
        return sum(fn(c) for c in self.calls)

    @property
    def llm_calls(self): return len(self.calls)
    @property
    def tokens_in(self): return self.total(lambda c: c.tokens_in)
    @property
    def tokens_out(self): return self.total(lambda c: c.tokens_out)
    @property
    def tokens_cached(self): return self.total(lambda c: c.tokens_cached)
    @property
    def cost_usd(self): return self.total(lambda c: c.cost_usd())
    @property
    def energy_wh(self): return self.total(lambda c: c.energy_wh())
    @property
    def carbon_g(self): return self.total(lambda c: c.carbon_g(self.region))

    def sci_score(self) -> float:
        """SCI per R, where R = one rebalance task. Units: gCO2e/task."""
        return self.carbon_g

    def breakdown(self) -> str:
        lines = [f"{'call':<22}{'model':<28}{'tier':>11}{'in':>8}{'cached':>8}{'out':>7}{'$':>10}"]
        for c in self.calls:
            lines.append(
                f"{c.label:<22}{c.actual:<28}{c.model:>11}{c.tokens_in:>8}"
                f"{c.tokens_cached:>8}{c.tokens_out:>7}{c.cost_usd():>10.5f}")
        return "\n".join(lines)


def comparison_table(default: Meter, lean: Meter, daily_volume=10_000) -> str:
    def pct(a, b):
        return f"-{(1 - b / a) * 100:.0f}%" if a else "n/a"
    rows = [
        ("LLM calls per task",       default.llm_calls, lean.llm_calls),
        ("Input tokens",             default.tokens_in, lean.tokens_in),
        ("  of which cached",        default.tokens_cached, lean.tokens_cached),
        ("Output tokens",            default.tokens_out, lean.tokens_out),
        ("Cost per task (USD)",      round(default.cost_usd, 5), round(lean.cost_usd, 5)),
        ("Energy per task (Wh)",     round(default.energy_wh, 3), round(lean.energy_wh, 3)),
        ("SCI per task (gCO2e)",     round(default.carbon_g, 4), round(lean.carbon_g, 4)),
    ]
    w = (30, 14, 14, 10)
    out = [f"{'metric':<{w[0]}}{'DEFAULT':>{w[1]}}{'LEAN':>{w[2]}}{'delta':>{w[3]}}",
           "-" * sum(w)]
    for label, d, l in rows:
        delta = pct(float(d), float(l)) if isinstance(d, (int, float)) and float(d) else ""
        out.append(f"{label:<{w[0]}}{d:>{w[1]}}{l:>{w[2]}}{delta:>{w[3]}}")
    # Extrapolation — cost and carbon stay parallel, never merged
    out.append("-" * sum(w))
    out.append(f"At {daily_volume:,} tasks/day:")
    out.append(f"{'  Cost per year (USD)':<{w[0]}}"
               f"{default.cost_usd * daily_volume * 365:>{w[1]},.0f}"
               f"{lean.cost_usd * daily_volume * 365:>{w[2]},.0f}"
               f"{pct(default.cost_usd, lean.cost_usd):>{w[3]}}")
    out.append(f"{'  Carbon per year (kgCO2e)':<{w[0]}}"
               f"{default.carbon_g * daily_volume * 365 / 1000:>{w[1]},.0f}"
               f"{lean.carbon_g * daily_volume * 365 / 1000:>{w[2]},.0f}"
               f"{pct(default.carbon_g, lean.carbon_g):>{w[3]}}")
    return "\n".join(out)
