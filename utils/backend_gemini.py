"""Google Gemini backend (Interactions API).

Reads GEMINI_API_KEY or GOOGLE_API_KEY. Needs google-genai >= 1.51.0.

    pip install "google-genai>=1.51.0"

Two settings carry most of the quality here:

resolution
    Set per image, not globally: low / medium / high / ultra_high. It caps the
    token budget spent on that image, so whatever is in frame gets squeezed
    into it -- which is also why cropping to the subject matters. The objects
    that decide these verdicts are a handful of pixels in a 4K oblique frame,
    so this is pinned high.

thinking_level
    Adjudicating a violation is multi-factor reasoning over the frames, not a
    caption. Kept high; drop it to trade accuracy for cost.
"""
from typing import Any, Dict

from .render import to_b64



# The image quota that blocked the pro line recovered on 2026-09-04 (181
# images accepted, ~51 s/call vs flash's 26 s). 3.5-flash remains the
# fallback if pro 429s again mid-experiment.
DEFAULT_MODEL = "gemini-3.1-pro-preview"
# Pricing not pinned here: verify current rates before quoting a cost.
PRICE_IN = PRICE_OUT = None


def _inline_refs(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve $ref/$defs into a self-contained schema.

    pydantic emits nested models as $defs + $ref. Schema validators on the
    provider side are not guaranteed to follow references, so inline them.
    """
    defs = schema.pop("$defs", {})

    def walk(node):
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/$defs/"):
                target = defs.get(ref.split("/")[-1], {})
                merged = walk({k: v for k, v in target.items()})
                # keep any siblings alongside the $ref (description, title, ...)
                merged.update({k: walk(v) for k, v in node.items() if k != "$ref"})
                return merged
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v) for v in node]
        return node

    return walk(schema)


def _usage(interaction) -> Dict[str, Any]:
    """Token accounting off the Interactions API's `usage` object.

    Field names read off a real response on 2026-08-28, not guessed. The one
    that matters and is easy to miss: thinking is billed as output but reported
    separately from it, so `total_output_tokens` alone understates the cost of
    a call by a large factor at thinking_level=high. Reported `out` is the sum;
    the split is kept so a run can see where its output budget went.
    """
    u = getattr(interaction, "usage", None)
    if u is None:
        return {"in": None, "out": None, "price_in": None, "price_out": None}
    tin = getattr(u, "total_input_tokens", None)
    out = getattr(u, "total_output_tokens", None) or 0
    think = getattr(u, "total_thought_tokens", None) or 0
    if tin is None:
        return {"in": None, "out": None, "price_in": None, "price_out": None}
    return {"in": tin, "out": out + think, "answer_out": out, "thought": think,
            "cached": getattr(u, "total_cached_tokens", None) or 0,
            "price_in": PRICE_IN, "price_out": PRICE_OUT}


def _is_rate_limit(e) -> bool:
    """A 429 from any layer of the stack, however it is spelled."""
    s = f"{type(e).__name__} {e}".lower()
    return ("429" in s or "ratelimit" in s or "rate_limit" in s
            or "resource_exhausted" in s or "resource has been exhausted" in s
            or "exceeded a quota" in s or "too_many_requests" in s)


def _retry(call, attempts=6, base=30.0, label=""):
    """Retry 429s with long exponential backoff. Calls carry ~1M tokens of
    images and a per-minute window does not clear quickly. Only rate limits are
    retried; anything else would re-upload the images to fail the same way.
    """
    import random
    import sys
    import time

    for i in range(attempts):
        try:
            return call()
        except Exception as e:
            if not _is_rate_limit(e) or i == attempts - 1:
                raise
            wait = base * (2 ** i) * (0.8 + 0.4 * random.random())
            print(f"    rate limited{label}, waiting {wait:.0f}s "
                  f"(attempt {i + 1}/{attempts - 1})", file=sys.stderr, flush=True)
            time.sleep(wait)


class GeminiBackend:
    name = "gemini"

    def __init__(self, model: str = DEFAULT_MODEL,
                 resolution: str = "high",
                 thinking_level: str = "high"):
        from google import genai

        self.model = model
        self.resolution = resolution
        self.thinking_level = thinking_level
        self.client = genai.Client()

    def _image(self, img) -> dict:
        """One ImageContent entry.

        Sent as a plain dict rather than a typed object: the Interactions
        content classes live under google.genai._gaos, a private path, and the
        request body validates dicts against the same models.
        """
        return {"type": "image", "mime_type": "image/jpeg",
                "data": to_b64(img), "resolution": self.resolution}

    def parts(self, system, frames, text):
        """system + [(label, image)] + trailing text -> the `input` list.

        A label that is not None becomes its own text part immediately before
        its image, pairing each frame with its timestamp in the request
        structure rather than only in the pixels.
        """
        # Every element of a list-valued `input` must be an object carrying a
        # `type` discriminator; a bare string is only accepted when `input` is
        # itself a single string.
        parts = [{"type": "text", "text": system}]
        for label, img in frames:
            if label is not None:
                parts.append({"type": "text", "text": label})
            parts.append(self._image(img))
        # the varying part goes last, so the frames stay a stable prefix
        parts.append({"type": "text", "text": text})
        return parts

    def run(self, system, frames, text, schema, max_tokens=8000):
        """Generic call: system prompt + frames + text -> validated `schema`."""
        parts = self.parts(system, frames, text)
        interaction = _retry(lambda: self.client.interactions.create(
            model=self.model,
            input=parts,
            response_format={"type": "text", "mime_type": "application/json",
                             "schema": _inline_refs(schema.model_json_schema())},
            generation_config={"thinking_level": self.thinking_level,
                               "max_output_tokens": max_tokens},
        ), label=f" ({len(frames)} images)")
        text = getattr(interaction, "output_text", "") or ""
        if not text.strip():
            # An empty body usually means the reply was cut off before any JSON
            # was emitted -- high thinking levels consume the same output
            # budget. Say so, rather than letting a JSON parse error two frames
            # up the stack imply the schema was wrong.
            raise RuntimeError(
                f"{self.model} returned no output text "
                f"(status={getattr(interaction, 'status', '?')}, "
                f"max_output_tokens={max_tokens}, "
                f"thinking_level={self.thinking_level}). "
                f"Raise --max-output-tokens or lower thinking.")
        return schema.model_validate_json(text), _usage(interaction)
