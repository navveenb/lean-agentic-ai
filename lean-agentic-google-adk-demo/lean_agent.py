"""lean_agent.py — the LEAN pattern, as an ADK 2.x Workflow (the 'after' picture).

Lean levers, on the real ADK graph runtime:
  * Two-stage funnel     — Flash-Lite classifies intent; Pro appears nowhere.
  * Deterministic nodes  — parsing, ESG cap checks, and routing are
                           FunctionNodes: pure code, zero tokens, zero carbon.
  * Scoped context       — synthesis receives a compact findings table.
  * Context caching      — the policy rides in the cache (simulated in sim
                           mode; implicit caching reported by the API in live).
  * Structured output    — output_schema on synthesis; parsing cannot fail.
  * Bounded retries      — RetryConfig(max_attempts=2) on the workflow.
  * Conditional routing  — compliant portfolios take NO_ACTION and never
                           touch the synthesis model at all.

Works identically in simulation mode and live-Gemini mode.
Portfolio parsing is generic: any markdown table with columns
| Ticker | Name | Sector | Weight % | Value USD | ESG Flag | works.
"""

import asyncio
import re
from pathlib import Path

from pydantic import BaseModel
from google.adk import Agent, Workflow, Event
from google.adk.workflow import START, RetryConfig
from google.adk.runners import InMemoryRunner
from google.genai import types

from meter import Meter
from sim_models import model_and_callback, is_live, LIVE_MODELS

DATA = Path(__file__).parent / "data"
POLICY = (DATA / "esg_policy.md").read_text()

SYNTH_INSTRUCTION = ("Given the findings, produce the rebalance plan as JSON "
                     "matching the schema exactly, applying the ESG policy.")


def _try_create_policy_cache():
    """LIVE MODE ONLY: create an explicit Gemini context cache for the policy.

    Returns (cache_name, model_used) or (None, None) on any failure —
    e.g. the '-latest' alias not supporting caching, or the policy being
    under the model's minimum cacheable size. The workflow falls back to
    sending the policy inline, so the demo never breaks.
    """
    try:
        from google import genai
        from google.genai import types as gt
        client = genai.Client()
        model = LIVE_MODELS["flash"]
        cache = client.caches.create(
            model=model,
            config=gt.CreateCachedContentConfig(
                display_name="lean-demo-esg-policy",
                system_instruction=SYNTH_INSTRUCTION,
                contents=[gt.Content(role="user",
                                     parts=[gt.Part(text=POLICY)])],
                ttl="1800s",
            ),
        )
        print(f"   [context cache created: {cache.name} on {model}]")
        return cache.name, model
    except Exception as e:  # caching unsupported for alias, quota, etc.
        print(f"   [explicit cache unavailable ({type(e).__name__}); "
              f"sending policy inline]")
        return None, None

SCOPED_MEMORY = ("Client prefs: ESG lens carbon+governance; moderate risk; "
                 "fossil reduction when practical; quarterly rebalances.")

ROW = re.compile(
    r"\|\s*([A-Z.]+)\s*\|\s*[^|]+\|\s*(\w+)\s*\|\s*([\d.]+)\s*\|\s*[\d,]+\s*\|\s*(\w+)\s*\|")


class Trade(BaseModel):
    ticker: str
    action: str
    from_pct: float | None = None
    to_pct: float | None = None
    watch: str | None = None


class RebalancePlan(BaseModel):
    trades: list[Trade]
    waci_before: float
    waci_after: float
    summary: str
    confidence: float


def parse_holdings(portfolio_text: str) -> list[dict]:
    """Generic table parse: Ticker | Name | Sector | Weight % | Value | Flag."""
    holdings = []
    for line in portfolio_text.splitlines():
        m = ROW.match(line)
        if m and m.group(1) != "Ticker":
            holdings.append({"ticker": m.group(1), "sector": m.group(2),
                             "weight": float(m.group(3)), "flag": m.group(4)})
    return holdings


def score_and_check_caps(holdings: list[dict]) -> dict:
    """ESG cap checks per policy. Deterministic — this NEVER needed an LLM."""
    fossil = [h for h in holdings if h["flag"] == "fossil"]
    governance = [h for h in holdings if h["flag"] == "governance"]
    fossil_wt = sum(h["weight"] for h in fossil)
    sector_wt: dict = {}
    for h in holdings:
        if h["sector"] != "Cash":
            sector_wt[h["sector"]] = sector_wt.get(h["sector"], 0) + h["weight"]
    max_sector, max_wt = max(sector_wt.items(), key=lambda kv: kv[1]) if sector_wt else ("", 0)
    return {
        "fossil_aggregate_pct": fossil_wt,
        "fossil_breach": fossil_wt > 10.0,                       # policy s.2
        "single_fossil_breach": [h["ticker"] for h in fossil if h["weight"] > 4.0],
        "governance_watch": [h["ticker"] for h in governance],   # s.3
        "top_sector": max_sector, "top_sector_pct": max_wt,
        "sector_cap_breach": max_wt > 35.0,                      # s.5
    }


def build_lean_workflow(meter: Meter, portfolio_text: str) -> Workflow:

    # ── FunctionNodes (zero tokens) ─────────────────────────────────────
    def load_portfolio(node_input: str) -> Event:
        return Event(output={"holdings": parse_holdings(portfolio_text),
                             "request": str(node_input)[:200]})

    def check_caps(node_input: dict) -> Event:
        findings = score_and_check_caps(node_input["holdings"])
        return Event(output={**node_input, "findings": findings})

    def risk_router(node_input: dict) -> Event:
        f = node_input["findings"]
        needs_work = (f["fossil_breach"] or f["sector_cap_breach"]
                      or f["single_fossil_breach"])
        return Event(output=node_input, route="REBALANCE" if needs_work else "NO_ACTION")

    def no_action(node_input: dict) -> Event:
        return Event(output="Portfolio within all policy constraints. "
                            "No rebalance required this quarter.")

    def build_prompt(node_input: dict) -> Event:
        f = node_input["findings"]
        compact = (f"Client request: {node_input['request']}\n"
                   f"Memory: {SCOPED_MEMORY}\n"
                   f"Findings: fossil {f['fossil_aggregate_pct']:.1f}% "
                   f"(agg breach={f['fossil_breach']}, single-position "
                   f"breach={f['single_fossil_breach']}); "
                   f"top sector {f['top_sector']} {f['top_sector_pct']:.1f}% "
                   f"(cap breach={f['sector_cap_breach']}); "
                   f"governance watch={f['governance_watch']}.\n"
                   f"Holdings: " +
                   "; ".join(f"{h['ticker']} {h['weight']}% {h['flag']}"
                             for h in node_input["holdings"]))
        return Event(output=compact)

    # ── LLM nodes ───────────────────────────────────────────────────────
    cls_model, cls_cb = model_and_callback(
        "flash-lite", "intent", meter, "1_classify")
    classifier = Agent(
        name="intent_classifier", model=cls_model, after_model_callback=cls_cb,
        timeout=120,
        instruction=f"Classify the rebalance request briefly. Memory: {SCOPED_MEMORY}",
    )

    syn_model, syn_cb = model_and_callback(
        "flash", "synthesis", meter, "2_synthesis",
        cached_chars=len(POLICY))

    # LIVE MODE: try an explicit context cache for the policy. If it works,
    # the policy tokens bill at the cached rate and the API reports them in
    # cached_content_token_count, which the meter picks up automatically.
    gen_config = None
    instruction = f"=== ESG POLICY (cached) ===\n{POLICY}\n{SYNTH_INSTRUCTION}"
    if is_live():
        cache_name, _ = _try_create_policy_cache()
        if cache_name:
            from google.genai import types as gt
            gen_config = gt.GenerateContentConfig(cached_content=cache_name)
            instruction = ""     # policy + instruction now live in the cache

    synthesizer = Agent(
        name="synthesizer", model=syn_model, after_model_callback=syn_cb,
        timeout=180,
        instruction=instruction,
        generate_content_config=gen_config,
        output_schema=RebalancePlan,
    )

    return Workflow(
        name="lean_esg_rebalance",
        retry_config=RetryConfig(max_attempts=2),
        edges=[
            (START, classifier, load_portfolio, check_caps, risk_router),
            (risk_router, {"NO_ACTION": no_action, "REBALANCE": build_prompt}),
            (build_prompt, synthesizer),
        ],
    )


async def run_lean(meter: Meter, portfolio_text: str, request: str) -> str:
    wf = build_lean_workflow(meter, portfolio_text)
    runner = InMemoryRunner(agent=wf, app_name="lean_demo")
    session = await runner.session_service.create_session(
        app_name="lean_demo", user_id="u1")
    msg = types.Content(role="user", parts=[types.Part(text=request)])
    final = ""
    async for ev in runner.run_async(user_id="u1", session_id=session.id, new_message=msg):
        if ev.content and ev.content.parts and ev.content.parts[0].text:
            final = ev.content.parts[0].text
    return final


if __name__ == "__main__":
    portfolio = (Path(__file__).parent / "portfolios" / "84721.md").read_text()
    m = Meter("LEAN")
    asyncio.run(run_lean(m, portfolio, "Rebalance ESG portfolio for client 84721."))
    print(m.breakdown())
    print(f"\nTotal: ${m.cost_usd:.5f} | {m.energy_wh:.3f} Wh | {m.carbon_g:.4f} gCO2e")
