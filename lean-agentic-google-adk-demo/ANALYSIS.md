# What Just Happened? — A Plain-Language Walkthrough

This document explains a **real run against live Google Gemini** of the same
task built two ways. If the comparison table felt like a wall of numbers,
read this first. No prior agent experience assumed.

---

## The task

One sentence: *"Rebalance ESG portfolio for client 84721."*

Behind that sentence, some work has to happen: read the client's holdings,
check them against an ESG policy document, figure out which rules are broken,
and propose trades that fix it.

We built this twice. Same task, same data files, same models available to both.

## The result (real numbers from a live Gemini run)

| | DEFAULT way | LEAN way |
|---|---|---|
| AI calls made | 6 | 2 |
| Words sent to the AI (input tokens) | 48,427 | 3,725 |
| ...of which served from cache | 0 | **3,327 (90%)** |
| Cost for this one task | **$0.171** | **$0.006** |
| Electricity used | 8.3 Wh | 0.1 Wh |
| Carbon footprint (SCI) | 3.4 gCO₂e | 0.07 gCO₂e |
| Wall-clock time | ~3.8 minutes | seconds |
| If you ran 10,000 of these per day, per year | **$623,544** | **$22,204** |

Same answer. 96% less money, 98% less carbon — and the answer arrived
in seconds instead of four minutes. Nothing got smarter — the work
just went to the right place. Here's where the difference comes from.

---

## Where the DEFAULT way wastes money (4 habits)

### Habit 1: It sends the whole filing cabinet with every question

Look at the first line of the default run:

```
1_intent    gemini-2.5-pro    6725 in    1432 out    $0.031
```

The actual question was 8 tokens: *"Rebalance ESG portfolio for client 84721."*
So why did we send 6,725? Because the default code pastes the **entire ESG
policy + the entire portfolio + three past client conversations** into every
single call — even the call whose only job is to figure out what the user wants.

> **Analogy:** it's like attaching the complete employee handbook to every
> text message you send a coworker. The handbook doesn't change. They've
> seen it. You're paying to send it anyway.

And it does this **six times**. That's why input tokens total 49,098 for a
task whose real question was 8 tokens long.

### Habit 2: It uses the most expensive model for everything

Every default call goes to the Pro-tier model (~$2 per million input tokens).
Including the trivial first step — "what is the user asking?" — which a model
20× cheaper answers just as well. Ferrari, pizza.

### Habit 3: It asks the AI to do spreadsheet math

Three of the six calls — *plan, ESG scoring, risk* — cost about **$0.087
combined**. What do they actually compute? Things like "add up the weights of
fossil-flagged holdings and check if the total is over 10%."

That's not AI work. That's a `for` loop and an `if` statement.

### Habit 4: It doesn't control its own output, then pays to retry

The default asks for the recommendation in free-form prose, then tries to
parse it as JSON. Look what happened in the live run:

```
5_synthesis          8400 in       0 cached    $0.032
5_synthesis_retry1   9729 in    6126 cached    $0.015
```

The model answered in prose (models do that when you don't constrain them),
the JSON parse **failed**, and the code paid again — this time with the failed
answer stacked on top of the already-huge prompt, so the retry was *bigger*
than the original. Retries don't just repeat cost, they compound it.

**One instructive detail:** in an earlier run of this same default code,
Google's *implicit caching* spontaneously discounted the retry (it noticed
the repeated giant prefix). In this run it didn't fire at all — the cached
column reads 0 on every default call. That's the point about implicit
caching: it's opportunistic, not guaranteed. The lean version doesn't hope
for a discount — it **creates an explicit cache** and gets one every time.

---

## What the LEAN way does differently (5 moves)

The lean version is an **ADK Workflow — a graph**. Instead of one loop that
calls a big model over and over, the task is drawn as a map of steps, where
each step is either code or a model — whichever the step actually needs:

```
             (AI: Flash-Lite,          (pure code — costs nothing)
              45 tokens, $0.00002)
                    │
START ──► classify ──► load_portfolio ──► check_caps ──► risk_router
                          (code)            (code)          (code)
                                                              │
                                       ┌──────────────────────┴───────┐
                                  route: NO_ACTION              route: REBALANCE
                                       │                              │
                                  "nothing to do,               build_prompt (code)
                                   done — $0.00002                    │
                                   total"                        synthesizer
                                                          (AI: Flash + cached policy,
                                                           3,675 tokens, $0.011)
```

This picture **is** the code. In `lean_agent.py`:

```python
Workflow(
    name="lean_esg_rebalance",
    retry_config=RetryConfig(max_attempts=2),
    edges=[
        (START, classifier, load_portfolio, check_caps, risk_router),
        (risk_router, {"NO_ACTION": no_action, "REBALANCE": build_prompt}),
        (build_prompt, synthesizer),
    ],
)
```

Each name in `edges` is a node. `classifier` and `synthesizer` are `Agent`s
(AI). The other four are plain Python functions — ADK runs them as
**FunctionNodes** in the graph, and they cost zero tokens. The dict after
`risk_router` is **conditional routing**: the router returns a route name,
and the graph takes that branch.

The five moves, mapped to the numbers:

**Move 1 — Small model answers the small question.**
`1_classify` = 45 tokens on Flash-Lite = **$0.00002**. The default spent
$0.031 on the same step. That's a 1,500× difference, for identical value.

**Move 2 — Code does the code-shaped work.**
The default's plan + scoring + risk calls ($0.087) don't exist in the lean
table *at all*. `check_caps()` is arithmetic; `risk_router()` is an `if`.
The cheapest AI call is the one you never make.

**Move 3 — Send the findings, not the filing cabinet.**
The synthesis prompt is a compact summary built by code — "fossil 12.3%,
breach=True; top sector Technology 36.1%, breach=True; holdings: ..." —
plus the policy. 3,675 tokens instead of 8,400+.

**Move 4 — Cache what never changes.**
The 16K-character policy is the same on every request, so the code creates
an explicit **context cache** (`_try_create_policy_cache()`) before the
synthesis call. You can see it in the run log:

```
[context cache created: projects/.../cachedContents/78317... ]
2_synthesis   gemini-2.5-flash   3680 in   3327 cached   $0.00606
```

**90% of the synthesis input was served from cache**, billed at roughly a
tenth of the normal input rate. That single move nearly halved the lean
cost ($0.0106 → $0.0061 per task).

**Move 5 — Make the output format impossible to get wrong.**
`output_schema=RebalancePlan` tells Gemini the exact JSON shape via
constrained decoding. The answer *is* valid JSON, always. Notice the lean
table has **no retry row** — the failure mode wasn't handled better, it was
designed out.

---

## The bonus demo: the portfolio with nothing wrong

Run the compliant portfolio:

```bash
python run_comparison.py --client 55210
```

The graph's router sees no breaches and takes the **NO_ACTION** branch —
the expensive synthesis model **never runs**:

| | DEFAULT | LEAN |
|---|---|---|
| AI calls | 7 | **1** |
| Cost | $0.103 | **$0.00002** |

The default way spent ten cents and seven frontier-model calls to conclude
*"nothing to do."* The lean graph concluded the same thing with one tiny
call and some arithmetic. This is what conditional routing buys you: the
cost of a task scales with how much the task actually needs.

---

## The one-sentence takeaway

> **Lean isn't a cheaper model or a clever prompt. It's putting each step of
> the work in the right layer — code for code-shaped work, small models for
> small questions, the big model only where judgment is genuinely needed —
> and the graph is what makes those choices explicit and enforceable.**

Cost and carbon moved together (-94% and -97%) because they share the same
root cause: tokens processed. Every token you don't send is money *and*
watts *and* grams of CO₂ you don't spend. That's the whole discipline.

---

*Numbers in this document are from a real live-Gemini run (July 2026) of
`python run_comparison.py --client 84721`, with explicit context caching
active. One pricing caveat: the meter prices calls by intended tier
(the tables in `meter.py`); if your env vars map a tier to a different
concrete model (e.g. `gemini-2.5-flash`), align `PRICING` to that model's
list price before quoting dollar figures externally. Your exact figures will vary
run-to-run — live models produce different output lengths — but the shape
(call count collapse, input-token collapse, no-retry lean path) is stable.
Pricing/energy/carbon coefficients are the editable tables in `meter.py`.*
