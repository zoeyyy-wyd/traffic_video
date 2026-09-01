"""Anthropic backend. Reads ANTHROPIC_API_KEY, or an `ant auth login` profile."""
from .render import to_b64

DEFAULT_MODEL = "claude-opus-5"
# USD per million tokens
PRICE_IN, PRICE_OUT = 5.0, 25.0


def _is_rate_limit(e) -> bool:
    """A 429 from any layer of the stack, however it is spelled."""
    s = f"{type(e).__name__} {e}".lower()
    return ("429" in s or "ratelimit" in s or "rate_limit" in s
            or "resource_exhausted" in s or "resource has been exhausted" in s
            or "exceeded a quota" in s or "too_many_requests" in s)


def _retry(call, attempts=6, base=30.0, label=""):
    """Retry a rate-limited call with exponential backoff.

    Calls here carry hundreds of images and run to ~1M input tokens each, so a
    handful fired back to back will cross a per-minute token quota even when
    the account has plenty of credit left. The waits start long for that
    reason: a per-minute window does not clear in two seconds, and retrying
    faster than the window just burns the remaining attempts.

    Only 429s are retried. A malformed request or a schema failure is not going
    to fix itself, and retrying it wastes the images all over again.
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


class ClaudeBackend:
    name = "claude"

    def __init__(self, model: str = DEFAULT_MODEL):
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic()

    @staticmethod
    def content(frames, text):
        """[(label, image)] + trailing text -> a user content list.

        A label that is not None is sent as its own text block immediately
        before its image. Nothing else can express the pairing: an image block
        carries only its source, with no caption or metadata field, so a frame
        is bound to its timestamp either in its pixels or by an adjacent block.
        """
        content = []
        for label, img in frames:
            if label is not None:
                content.append({"type": "text", "text": label})
            content.append({"type": "image", "source": {
                "type": "base64", "media_type": "image/jpeg",
                "data": to_b64(img)}})
        # the varying part goes last, so the frames stay a stable prefix
        content.append({"type": "text", "text": text})
        return content

    def run(self, system, frames, text, schema, max_tokens=8000):
        """Generic call: system prompt + frames + text -> validated `schema`.

        Task-specific callers build on this so every task shares one place
        where retries, caching and model options are configured.
        """
        content = self.content(frames, text)
        resp = _retry(lambda: self.client.messages.parse(
            model=self.model,
            max_tokens=max_tokens,
            thinking={"type": "adaptive"},
            # stable prefix: the system prompt never varies within a task
            system=[{"type": "text", "text": system,
                     "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": content}],
            output_format=schema,
        ), label=f" ({len(frames)} images)")
        usage = {"in": resp.usage.input_tokens, "out": resp.usage.output_tokens,
                 "price_in": PRICE_IN, "price_out": PRICE_OUT}
        return resp.parsed_output, usage
