# Getting Started — Lean Agentic AI Demo on Google ADK

This guide takes you from zero to a running default-vs-lean comparison, in
simulation mode (no credentials) or against real Gemini.

---

## 1. Installation

Requires Python 3.10+.

```bash
# Unzip / clone, then from the project directory:
pip install -r requirements.txt        # installs google-adk (2.x)
```

That is the only dependency. Verify:

```bash
python -c "import google.adk; print(google.adk.__version__)"   # expect 2.x
```

## 2. First run (simulation mode — zero credentials)

```bash
python run_comparison.py
```

You'll see the DEFAULT pipeline run (7 heavyweight calls), the LEAN ADK
Workflow run (2 calls, one mostly cached), and a before/after table with cost,
energy, and SCI (gCO₂e per task) as parallel columns. A `report_84721.md` is
written alongside.

In simulation mode a deterministic `SimulatedGemini` — a real ADK `BaseLlm` —
stands in for the models. Token counts are computed from the **actual prompts
each pipeline builds** (chars/4), so the deltas are architectural, not scripted.
The run is fully reproducible: same inputs, same numbers, every time.

## 3. The three bundled portfolios

```bash
python run_comparison.py --list
```

| Client | Character | What it demonstrates |
|---|---|---|
| `84721` | Balanced book with fossil + governance flags | The standard REBALANCE path — both pipelines produce a plan |
| `91007` | Legacy energy-heavy book, multiple hard breaches | REBALANCE with the heaviest findings payload |
| `55210` | Fully compliant book | The **NO_ACTION fast path**: the lean workflow's router short-circuits and the synthesis model never runs (1 tiny call vs 7 heavy ones) |

Run any of them:

```bash
python run_comparison.py --client 91007
python run_comparison.py --client 55210
```

`55210` is the one worth showing people first — it makes the routing lever
visceral. The default pipeline burns seven full-context Pro calls to conclude
"nothing to do"; the lean workflow concludes the same thing with one
Flash-Lite call and pure code.

## 4. Running against real Gemini (live mode)

```bash
export GOOGLE_API_KEY=your-api-key      # from Google AI Studio
python run_comparison.py --client 84721
```

What changes in live mode:

- `make_model()`/`model_and_callback()` return plain model strings and ADK
  calls real Gemini. Defaults are the `-latest` aliases
  (`gemini-pro-latest`, `gemini-flash-latest`, `gemini-flash-lite-latest`).
  Override with env vars if your key needs specific versions:

  ```bash
  export LEAN_DEMO_PRO=gemini-2.5-pro
  export LEAN_DEMO_FLASH=gemini-2.5-flash
  export LEAN_DEMO_FLASH_LITE=gemini-2.5-flash-lite
  ```

- Token usage is captured from the **real** `usage_metadata` on every response,
  via ADK `after_model_callback`, and recorded into the same meter — so the
  report format is identical to simulation mode.

- Caching: the demo does not create an explicit cache in live mode. If the
  Gemini API applies **implicit caching** to the repeated policy prefix, the
  `cached_content_token_count` it reports flows straight into the "cached"
  column. If you want explicit caching, create one via `client.caches.create`
  and pass `cached_content` — see the deep-dive companion for the snippet.

- Expect variance. Live models produce different output lengths run-to-run,
  and the default pipeline's parse-retry count depends on whether the model's
  free-form answer happens to be valid JSON (retries are capped at 2 either
  way). The *shape* of the result — call count, input-token collapse, cached
  share — is stable; exact dollar figures wobble.

- Cost note: a live run of the DEFAULT pipeline makes 5–7 large-context calls
  to your Pro-tier model. It costs real money (order of $0.05–$0.15 per run
  at mid-2026 list prices). The LEAN run costs a fraction of a cent.

### 4b. Vertex AI mode (through your GCP project)

No API key needed — authenticate with Application Default Credentials:

```bash
gcloud auth application-default login
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
python run_comparison.py --client 84721
```

The demo detects Vertex mode and switches defaults to **concrete model IDs**
(`gemini-2.5-pro` / `gemini-2.5-flash` / `gemini-2.5-flash-lite`), because
the `-latest` aliases only exist on the Gemini API surface — using them on
Vertex produces a `404 Publisher model ... was not found`. If your project
or region has different models, override with the `LEAN_DEMO_*` env vars,
and confirm availability with `gcloud ai models list` or the Model Garden
page for your region.

## 5. Adding your own model portfolio

Drop a markdown file into `portfolios/` named `<client_id>.md`. The only hard
contract is the holdings table — six columns, in this order:

```markdown
| Ticker | Name | Sector | Weight % | Value USD | ESG Flag |
|--------|------|--------|----------|-----------|----------|
| MSFT   | Microsoft Corp | Technology | 12.4 | 353,090 | none |
| XOM    | Exxon Mobil    | Energy     |  7.2 | 205,020 | fossil |
```

Rules the parser and policy checks rely on:

- **Ticker**: capital letters (dots ok, e.g. `BRK.B`).
- **Sector**: single word (`Technology`, `Energy`, `Healthcare`, ... `Cash`).
  Cash rows are excluded from sector-cap math.
- **Weight %**: a number; weights should roughly total 100.
- **ESG Flag**: one of `none`, `fossil`, `governance`, `water`.

Which flags trigger which path (per `data/esg_policy.md`):

- Aggregate `fossil` weight **> 10%** → REBALANCE (policy s.2)
- Any single `fossil` position **> 4%** → REBALANCE (s.2)
- Any sector (ex-cash) **> 35%** → REBALANCE (s.5)
- None of the above → **NO_ACTION** fast path

Then run it:

```bash
python run_comparison.py --client <your_id>
```

Everything else on the page (client preferences, prose) is free-form — the
default pipeline stuffs the whole file into context (that's the point), while
the lean workflow parses only the table.

Tip for building demo portfolios: make one that sits *just* over a single
threshold (e.g. fossil at 10.5%) and one *just* under (9.8%) — flipping one
weight and re-running is a 20-second live demonstration of conditional
routing changing the cost profile.

## 6. Reading the output

> For a plain-language walkthrough of a real live run — where the default
> way wastes money and what the lean graph does differently — read
> **[ANALYSIS.md](ANALYSIS.md)** first.

```
metric                               DEFAULT          LEAN     delta
LLM calls per task                         7             2      -71%
Input tokens                           48891          4368      -91%
  of which cached                          0          4121
Cost per task (USD)                  0.10329       0.00209      -98%
Energy per task (Wh)                   5.021          0.04      -99%
SCI per task (gCO2e)                  2.1125        0.0402      -98%
```

- **Cost and SCI are parallel metrics** — the report never merges them.
- **SCI** follows ISO/IEC 21031: `(E × I) + M per R`, where R = one rebalance
  task, E from per-token model-class coefficients, I from the grid-intensity
  table, M a small amortized embodied-carbon constant per call.
- The annualized rows extrapolate to 10,000 tasks/day — edit `daily_volume`
  in `comparison_table()` to match your fleet.
- All coefficients (prices, joules/token, gCO₂/kWh, embodied) live in single
  tables at the top of `meter.py`. They are illustrative — update against
  current list prices and your region before quoting numbers externally.

## 7. Troubleshooting

- **Live mode appears to hang at the DEFAULT pipeline** — almost always API
  rate limiting, not a bug. The default run burns ~50K tokens across six
  Pro-tier calls; free-tier keys have low per-minute and per-day Pro quotas,
  and the client silently retries 429s with exponential backoff (which looks
  like a hang). Confirm with a one-line `generate_content("ping")` against
  your Pro model outside the demo. Fixes: wait for the quota window, enable
  billing on the key, or smoke-test plumbing with
  `export LEAN_DEMO_PRO=gemini-flash-latest` (don't quote dollar figures from
  that run — the meter still prices the tier as Pro). The demo prints a
  `-> <step> ...` line before each call and each agent has a 120–180s
  timeout, so a stall is visible and eventually fails loudly.
- **Cost safety**: a circuit breaker in `meter.py` aborts any single run
  that exceeds `LEAN_DEMO_MAX_CALLS` LLM calls (default 10; the demo's worst
  case is 7 default + 2 lean). Loops cannot run away: the default retry is a
  bounded `for` (max 7 calls total), the lean graph has no back-edges, and
  each agent carries a 120–180s timeout. Note 429-rejected requests are not
  billed — a rate-limit stall costs time, not money.
- **`unknown pricing model`** — you added a new model name; add a row to
  `PRICING` and `ENERGY_J_PER_TOKEN` in `meter.py`.
- **`404 Publisher model ... was not found` (Vertex)** — the `-latest`
  aliases don't exist on Vertex; the demo auto-switches to `gemini-2.5-*`
  IDs when `GOOGLE_GENAI_USE_VERTEXAI` is set, but if your project/region
  lacks those, set `LEAN_DEMO_*` to models your region actually has.
- **Live mode (API key): 404 / model not found** — set the `LEAN_DEMO_*`
  env vars to models `client.models.list()` shows for your key.
- **Live mode: nothing in the meter** — usage capture rides on
  `after_model_callback`; if you build your own agents, pass the callback
  from `model_and_callback()` through.
- **Your portfolio parses 0 holdings** — check the table has exactly six
  `|`-separated columns and numeric weights; run
  `python -c "from lean_agent import parse_holdings; print(parse_holdings(open('portfolios/X.md').read()))"`.

## 8. Where to go next

- `lean_agent.py` is annotated lever-by-lever — it's the file to read.
- The workflow graph is four pure-code nodes and two model calls; try adding
  a `deep_risk` branch behind the router, or a second breach type in
  `score_and_check_caps`, and watch the cost table respond.
- The deep-dive companion documents the same patterns against the managed
  platform services (Agent Runtime, Memory Bank, Batch API, explicit caching).
