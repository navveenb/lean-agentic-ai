"""run_comparison.py — run DEFAULT and LEAN against the same portfolio,
print the before/after table, and write report_<client>.md.

Usage:
    python run_comparison.py                    # default client 84721, simulation
    python run_comparison.py --client 91007     # fossil-heavy book
    python run_comparison.py --client 55210     # compliant book (NO_ACTION path)
    python run_comparison.py --list             # show available portfolios
    GOOGLE_API_KEY=... python run_comparison.py # live Gemini mode
"""

import argparse
import asyncio
from pathlib import Path

from meter import Meter, comparison_table
from default_agent import run_default
from lean_agent import run_lean
from sim_models import is_live

PORTFOLIOS = Path(__file__).parent / "portfolios"


def list_portfolios():
    return sorted(p.stem for p in PORTFOLIOS.glob("*.md"))


async def main(client: str):
    path = PORTFOLIOS / f"{client}.md"
    if not path.exists():
        raise SystemExit(f"No portfolio '{client}'. Available: {', '.join(list_portfolios())}")
    portfolio = path.read_text()
    request = f"Rebalance ESG portfolio for client {client}."
    mode = "LIVE GEMINI" if is_live() else "SIMULATION (deterministic, zero-credential)"

    print("=" * 78)
    print(f"LEAN AGENTIC AI — DEFAULT vs LEAN on Google ADK   [{mode}]")
    print(f"Task: '{request}'")
    print("=" * 78)

    default_meter = Meter("DEFAULT")
    print("\n[1/2] DEFAULT pipeline (everything -> Pro, full context, retries)...")
    await run_default(default_meter, portfolio, request)
    print(default_meter.breakdown())

    lean_meter = Meter("LEAN")
    print("\n[2/2] LEAN workflow (ADK graph, funnel, cache, schema, routing)...")
    await run_lean(lean_meter, portfolio, request)
    print(lean_meter.breakdown())
    if not any(c.label == "2_synthesis" for c in lean_meter.calls):
        print(">> NO_ACTION fast path: portfolio within all policy constraints — "
              "the synthesis model was never invoked.")

    print("\n" + "=" * 78)
    print("BEFORE / AFTER — cost and carbon as parallel metrics")
    print("=" * 78)
    table = comparison_table(default_meter, lean_meter)
    print(table)

    out = Path(f"report_{client}.md")
    out.write_text(
        f"# Default vs Lean — client {client} ({mode})\n\n"
        f"## Default pipeline calls\n\n```\n{default_meter.breakdown()}\n```\n\n"
        f"## Lean workflow calls\n\n```\n{lean_meter.breakdown()}\n```\n\n"
        f"## Comparison\n\n```\n{table}\n```\n")
    print(f"\n{out} written.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", default="84721",
                    help="portfolio id (a file in portfolios/<id>.md)")
    ap.add_argument("--list", action="store_true", help="list available portfolios")
    args = ap.parse_args()
    if args.list:
        print("Available portfolios:", ", ".join(list_portfolios()))
    else:
        asyncio.run(main(args.client))
