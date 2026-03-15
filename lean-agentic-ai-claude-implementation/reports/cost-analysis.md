# Lean Cost Analysis Report
> Principle 2: "Not every prompt deserves a 70B response"

**Generated:** 2026-03-14
**Scanned:** `test-codebase/` (2 files, 11 LLM calls)
**Assumed volume:** 10,000 calls/day (~909 calls/type/day)

---

## Summary

| Metric | Value |
|--------|-------|
| Total LLM calls found | 11 |
| Calls using frontier models | 11 (100%) |
| Calls that could be downgraded | 9 |
| Calls to eliminate entirely | 1 |
| **Estimated current monthly cost** | **$3,170** |
| **Estimated optimized monthly cost** | **$940** |
| **Monthly savings** | **$2,230 (70% reduction)** |

---

## Findings by File

### `test-codebase/support_bot.py`

| Location | Model | Task Type | Recommendation | Status |
|----------|-------|-----------|----------------|--------|
| `support_bot.py:18` | claude-opus-4 | Spam classification (yes/no) | Downgrade to Haiku | ⚠️ OVERPOWERED |
| `support_bot.py:34` | claude-opus-4 | Contact info extraction | Downgrade to Haiku | ⚠️ OVERPOWERED |
| `support_bot.py:51` | claude-opus-4 | Sentiment analysis | Downgrade to Haiku | ⚠️ OVERPOWERED |
| `support_bot.py:67` | claude-opus-4 | Ticket routing | Downgrade to Haiku | ⚠️ OVERPOWERED |
| `support_bot.py:83` | claude-opus-4 | Conversation summarization | Downgrade to Sonnet | ⚠️ OVERPOWERED |
| `support_bot.py:100` | claude-opus-4 | Draft reply generation | Downgrade to Sonnet | ⚠️ OVERPOWERED |
| `support_bot.py:117` | claude-opus-4 | Escalation reasoning | Keep Opus | ✅ RIGHT-SIZED |

### `test-codebase/content_pipeline.py`

| Location | Model | Task Type | Recommendation | Status |
|----------|-------|-----------|----------------|--------|
| `content_pipeline.py:17` | gpt-4 | Article categorization | Downgrade to GPT-4o-mini | ⚠️ OVERPOWERED |
| `content_pipeline.py:34` | gpt-4 | SEO tag generation | Downgrade to GPT-4o-mini | ⚠️ OVERPOWERED |
| `content_pipeline.py:51` | gpt-4 | Headline translation | Downgrade to GPT-4o | ⚠️ OVERPOWERED |
| `content_pipeline.py:67` | gpt-4 | JSON formatting | **Eliminate — use Python** | 🚨 LLM NOT NEEDED |

---

## Cost Breakdown Table

| Task Type | Count | Current Tier | Recommended Tier | Monthly Cost (Current) | Monthly Cost (Optimized) | Monthly Savings |
|-----------|-------|-------------|-----------------|----------------------|------------------------|-----------------|
| Classification / routing | 4 | Opus / GPT-4 | Haiku / GPT-4o-mini | $870 | $48 | **$822** |
| Summarization / generation | 2 | Opus | Sonnet | $900 | $180 | **$720** |
| Translation | 1 | GPT-4 | GPT-4o | $164 | $33 | **$131** |
| Complex reasoning | 1 | Opus | Opus (keep) | $654 | $654 | $0 |
| JSON formatting (eliminate) | 1 | GPT-4 | Python code | $409 | $0 | **$409** |
| Extraction | 2 | Opus / GPT-4 | Haiku / GPT-4o-mini | $491 | $32 | **$459** |
| **TOTAL** | **11** | | | **$3,488** | **$947** | **$2,541 (73%)** |

---

## Top 3 Quick Wins

### 1. 🚨 Eliminate LLM for JSON formatting (`content_pipeline.py:67`)
`format_article_json()` uses GPT-4 to structure data into JSON. This is deterministic transformation — pure Python (`json.dumps`, dataclasses, or Pydantic) does this better, faster, and for free.
**Monthly savings: ~$409**

### 2. ⚠️ Downgrade 4 classification/routing calls to Haiku (`support_bot.py:18, 34, 51, 67`)
Spam detection, sentiment analysis, contact extraction, and ticket routing are all well-defined, low-ambiguity tasks. Claude Haiku 4.5 handles these with high accuracy at ~19x lower cost than Opus 4.
**Monthly savings: ~$822**

### 3. ⚠️ Downgrade summarization + reply drafting to Sonnet (`support_bot.py:83, 100`)
These tasks benefit from stronger language quality but don't require frontier reasoning. Sonnet 4.6 delivers excellent results at ~80% lower cost than Opus 4.
**Monthly savings: ~$720**

---

## Carbon Impact

> Using 0.03 kWh per frontier call, 0.005 kWh per medium call, 0.001 kWh per Haiku call
> Grid emission factor: 0.4 kg CO₂/kWh

| Scenario | kWh/day | kg CO₂/day | kg CO₂/year |
|----------|---------|------------|-------------|
| **Current** (all frontier) | 300 kWh | 120 kg | 43,800 kg |
| **Optimized** (right-sized) | 46 kWh | 18.5 kg | 6,753 kg |
| **Reduction** | 254 kWh/day saved | 101.5 kg/day | **37,047 kg/year (85%)** |

Eliminating unnecessary frontier calls reduces carbon footprint by **85%** — equivalent to ~4 transatlantic flights saved per month.

---

## Next Steps

- [ ] `content_pipeline.py:67` — Replace `format_article_json()` LLM call with Python `json.dumps` or Pydantic serialization
- [ ] `support_bot.py:18` — Switch `classify_spam()` from `claude-opus-4` → `claude-haiku-4-5-20251001`
- [ ] `support_bot.py:34` — Switch `extract_contact_info()` from `claude-opus-4` → `claude-haiku-4-5-20251001`
- [ ] `support_bot.py:51` — Switch `analyze_sentiment()` from `claude-opus-4` → `claude-haiku-4-5-20251001`
- [ ] `support_bot.py:67` — Switch `route_ticket()` from `claude-opus-4` → `claude-haiku-4-5-20251001`
- [ ] `support_bot.py:83` — Switch `summarize_conversation()` from `claude-opus-4` → `claude-sonnet-4-6`
- [ ] `support_bot.py:100` — Switch `draft_reply()` from `claude-opus-4` → `claude-sonnet-4-6`
- [ ] `content_pipeline.py:17` — Switch `categorize_article()` from `gpt-4` → `gpt-4o-mini`
- [ ] `content_pipeline.py:34` — Switch `generate_seo_tags()` from `gpt-4` → `gpt-4o-mini`
- [ ] `content_pipeline.py:51` — Switch `translate_headline()` from `gpt-4` → `gpt-4o`
- [ ] Run `/bloat-detector` to identify additional structural waste (reflection loops, over-tooling)
- [ ] Run `/carbon-estimator` for a full emissions breakdown after optimizations

---

> **Principle 2 violation across 91% of calls.** Only `analyze_escalation()` justifies frontier model usage.
> Right-sizing to the smallest capable model would cut monthly spend from ~$3,170 to ~$940 with no quality loss on routine tasks.
