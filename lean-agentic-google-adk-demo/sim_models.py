"""sim_models.py — model factory for both modes.

SIMULATION MODE (default, zero credentials):
    SimulatedGemini, a real ADK BaseLlm, returns deterministic responses and
    records token usage derived from actual prompt length (chars/4).

LIVE MODE (GOOGLE_API_KEY set):
    Returns the plain model string; ADK calls real Gemini. Usage is captured
    from response.usage_metadata via an after_model_callback and recorded to
    the same Meter — so the before/after report works identically both ways.

Model names in live mode are env-overridable:
    LEAN_DEMO_PRO / LEAN_DEMO_FLASH / LEAN_DEMO_FLASH_LITE
"""

import os
from typing import AsyncGenerator, Optional

from google.adk.models import BaseLlm, LlmRequest, LlmResponse
from google.genai import types

from meter import Meter, PRICING

CHARS_PER_TOKEN = 4

# Live-mode model strings. Defaults depend on the surface:
#   * Gemini API (GOOGLE_API_KEY): '-latest' aliases work.
#   * Vertex AI (GOOGLE_GENAI_USE_VERTEXAI): aliases DON'T exist there —
#     concrete publisher model IDs are required.
# LEAN_DEMO_* env vars override either surface.
_ON_VERTEX = bool(os.environ.get("GOOGLE_GENAI_USE_VERTEXAI"))
_DEFAULTS = (
    {"pro": "gemini-2.5-pro", "flash": "gemini-2.5-flash",
     "lite": "gemini-2.5-flash-lite"}
    if _ON_VERTEX else
    {"pro": "gemini-pro-latest", "flash": "gemini-flash-latest",
     "lite": "gemini-flash-lite-latest"}
)
LIVE_MODELS = {
    "pro":        os.environ.get("LEAN_DEMO_PRO",        _DEFAULTS["pro"]),
    "flash":      os.environ.get("LEAN_DEMO_FLASH",      _DEFAULTS["flash"]),
    "flash-lite": os.environ.get("LEAN_DEMO_FLASH_LITE", _DEFAULTS["lite"]),
}


CANNED = {
    "intent": '{"client_id": "{CID}", "scope": "equity", "urgency": "scheduled", '
              '"esg_lens": ["carbon", "governance"], "confidence": 0.94}',
    "plan": "Plan: 1) load holdings 2) score ESG per policy s.8 3) evaluate caps "
            "s.2/s.3/s.5 4) propose trades within s.6/s.7 5) client summary. "
            "I will begin by loading the full holdings table and history...",
    "score": "Scores computed for all holdings against policy s.8 composite "
             "methodology. Fossil-flagged names fall below the divestment "
             "threshold; governance-flagged names are on watch; remaining "
             "holdings are compliant. Detailed table follows in synthesis.",
    "risk": "Risk: post-trade ex-ante vol within 1.15x benchmark cap. Turnover "
            "under the 25% cap. Sector caps evaluated per s.5. Position count "
            "and cash band both within policy limits.",
    "synthesis": '{"trades": [{"ticker": "XOM", "action": "reduce", "from_pct": 7.2, '
                 '"to_pct": 3.6}, {"ticker": "CVX", "action": "reduce", "from_pct": 5.1, '
                 '"to_pct": 3.9}, {"ticker": "NEE", "action": "increase", "from_pct": 6.4, '
                 '"to_pct": 9.0}, {"ticker": "ENPH", "action": "increase", "from_pct": 3.8, '
                 '"to_pct": 6.2}], "waci_before": 134.2, "waci_after": 108.7, '
                 '"summary": "Reduced fossil exposure per policy s.2 glide path; '
                 'proceeds to clean-energy names. Post-trade WACI 108.7 (limit 120), '
                 'turnover within cap.", "confidence": 0.91}',
    "synthesis_freeform": "Here is my recommendation. I suggest reducing the "
                          "fossil-flagged positions toward their policy caps, "
                          "with proceeds to clean-energy names, which brings the "
                          "weighted carbon intensity back under the limit. "
                          "Overall I am fairly confident in this direction. "
                          "Let me know if you would like the trades as JSON.",
}


class SimulatedGemini(BaseLlm):
    """Deterministic Gemini stand-in with realistic token accounting."""

    role: str = "intent"
    meter_ref: object = None
    cached_chars: int = 0
    label: str = "call"
    display: str = ""

    model_config = {"arbitrary_types_allowed": True}

    @classmethod
    def supported_models(cls):
        return [r".*"]

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        n_chars = len(llm_request.config.system_instruction or "") if llm_request.config else 0
        for c in llm_request.contents or []:
            for p in c.parts or []:
                n_chars += len(p.text or "")

        text = CANNED[self.role]
        tokens_in = n_chars // CHARS_PER_TOKEN
        tokens_out = len(text) // CHARS_PER_TOKEN
        tokens_cached = min(self.cached_chars // CHARS_PER_TOKEN, tokens_in)

        if self.meter_ref is not None:
            self.meter_ref.record(self.label, self.model, tokens_in, tokens_out,
                                  tokens_cached, actual=self.display or self.model)

        yield LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text=text)]),
            usage_metadata=types.GenerateContentResponseUsageMetadata(
                prompt_token_count=tokens_in,
                candidates_token_count=tokens_out,
                cached_content_token_count=tokens_cached,
                total_token_count=tokens_in + tokens_out,
            ),
            turn_complete=True,
        )


def is_live() -> bool:
    return bool(os.environ.get("GOOGLE_API_KEY")
                or os.environ.get("GOOGLE_GENAI_USE_VERTEXAI"))


def _metering_callback(meter: Meter, pricing_model: str, label: str):
    """after_model_callback for live mode: read real usage_metadata."""
    actual = LIVE_MODELS[pricing_model]
    def _cb(callback_context, llm_response: LlmResponse) -> Optional[LlmResponse]:
        um = llm_response.usage_metadata
        if um is not None and (um.prompt_token_count or um.candidates_token_count):
            meter.record(
                label,
                pricing_model,                     # price against the intended tier
                um.prompt_token_count or 0,
                um.candidates_token_count or 0,
                um.cached_content_token_count or 0,   # implicit caching, if any
                actual=actual,                     # concrete model that ran
            )
        return None                                # don't modify the response
    return _cb


def model_and_callback(pricing_model: str, role: str, meter: Meter,
                       label: str, cached_chars: int = 0):
    """Returns (model, after_model_callback) for Agent construction.

    pricing_model must be a key in meter.PRICING — it drives the cost table.
    """
    assert pricing_model in PRICING, f"unknown pricing model {pricing_model}"
    if is_live():
        return LIVE_MODELS[pricing_model], _metering_callback(meter, pricing_model, label)
    sim = SimulatedGemini(model=pricing_model, role=role, meter_ref=meter,
                          label=label, cached_chars=cached_chars,
                          display=f"{pricing_model} (simulated)")
    return sim, None
