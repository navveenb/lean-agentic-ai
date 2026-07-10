"""default_agent.py — the DEFAULT pattern (the 'before' picture).

Every anti-pattern from the talk, implemented honestly:
  * Every step goes to the largest model tier.
  * Full context injected on every call: entire ESG policy + entire portfolio
    + fabricated 3-session history. Nothing is scoped, nothing is cached.
  * Five sequential LLM steps even though three are deterministic table work.
  * Free-form synthesis output -> JSON parse attempt -> full-context retries
    (capped at 2 so live mode can't loop forever).

Works identically in simulation mode and live-Gemini mode.
"""

import asyncio
import json
import re
from pathlib import Path

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

from meter import Meter
from sim_models import model_and_callback

DATA = Path(__file__).parent / "data"
POLICY = (DATA / "esg_policy.md").read_text()

HISTORY = ("[Session 2026-03-15] Discussed quarterly rebalance, client asked about "
           "fossil exposure. " * 40 +
           "[Session 2026-01-10] Reviewed annual performance, benchmark tracking. " * 40 +
           "[Session 2025-11-02] Onboarding conversation, risk questionnaire. " * 40)


def _full_context(portfolio_text: str) -> str:
    return (f"=== ESG POLICY ===\n{POLICY}\n\n"
            f"=== CLIENT PORTFOLIO ===\n{portfolio_text}\n\n"
            f"=== FULL CLIENT HISTORY ===\n{HISTORY}\n")


def _extract_json(text: str):
    """Parse JSON, tolerating markdown fences (live models often add them)."""
    cleaned = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.M).strip()
    return json.loads(cleaned)


async def _call(meter: Meter, context: str, role: str, label: str, prompt: str) -> str:
    import time
    t0 = time.time()
    print(f"   -> {label} ...", end="", flush=True)   # a long pause here in live
    # mode = model thinking time (2.5 Pro: 15-40s/call is NORMAL) or 429 backoff
    model, cb = model_and_callback("pro", role, meter, label)
    agent = Agent(
        name=f"default_{label}",
        model=model,
        instruction=context + "\nYou are a portfolio rebalancing assistant.",
        after_model_callback=cb,
        timeout=180,                           # fail loudly, don't hang forever
    )
    runner = InMemoryRunner(agent=agent, app_name="default_demo")
    session = await runner.session_service.create_session(
        app_name="default_demo", user_id="u1")
    out = ""
    msg = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for ev in runner.run_async(user_id="u1", session_id=session.id, new_message=msg):
        if ev.content and ev.content.parts and ev.content.parts[0].text:
            out = ev.content.parts[0].text
    print(f" done in {time.time() - t0:.1f}s", flush=True)
    return out


async def run_default(meter: Meter, portfolio_text: str, request: str) -> dict:
    ctx = _full_context(portfolio_text)

    intent = await _call(meter, ctx, "intent", "1_intent", request)
    plan = await _call(meter, ctx, "plan", "2_plan",
                       f"{request}\nIntent: {intent}\nMake a step-by-step plan.")
    score = await _call(meter, ctx, "score", "3_esg_score",
                        f"Plan: {plan}\nScore every holding against the policy.")
    risk = await _call(meter, ctx, "risk", "4_risk",
                       f"Scores: {score}\nEvaluate all risk constraints.")

    draft = await _call(meter, ctx, "synthesis_freeform", "5_synthesis",
                        f"Scores: {score}\nRisk: {risk}\n"
                        f"Produce the final rebalance recommendation.")
    for attempt in (1, 2):
        try:
            return _extract_json(draft)
        except (ValueError, TypeError):
            role = "synthesis_freeform" if attempt == 1 else "synthesis"
            draft = await _call(meter, ctx, role, f"5_synthesis_retry{attempt}",
                                f"Previous output was not valid JSON:\n{draft}\n"
                                f"Scores: {score}\nRisk: {risk}\n"
                                f"Return ONLY a JSON object with keys trades, "
                                f"waci_before, waci_after, summary, confidence.")
    try:
        return _extract_json(draft)
    except (ValueError, TypeError):
        return {"summary": draft, "note": "model never produced valid JSON"}


if __name__ == "__main__":
    portfolio = (Path(__file__).parent / "portfolios" / "84721.md").read_text()
    m = Meter("DEFAULT")
    asyncio.run(run_default(m, portfolio, "Rebalance ESG portfolio for client 84721."))
    print(m.breakdown())
    print(f"\nTotal: ${m.cost_usd:.5f} | {m.energy_wh:.3f} Wh | {m.carbon_g:.4f} gCO2e")
