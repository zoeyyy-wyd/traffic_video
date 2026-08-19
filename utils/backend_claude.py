"""Anthropic backend. Reads ANTHROPIC_API_KEY, or an `ant auth login` profile."""
from .render import to_b64

DEFAULT_MODEL = "claude-opus-5"
# USD per million tokens
PRICE_IN, PRICE_OUT = 5.0, 25.0


class ClaudeBackend:
    name = "claude"

    def __init__(self, model: str = DEFAULT_MODEL):
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic()

    def run(self, system, images, text, schema, max_tokens=8000):
        """Generic call: system prompt + images + text -> validated `schema`.

        Task-specific callers build on this so every task shares one place
        where retries, caching and model options are configured.
        """
        content = [{"type": "image", "source": {
            "type": "base64", "media_type": "image/jpeg", "data": to_b64(img)}}
            for img in images]
        content.append({"type": "text", "text": text})
        resp = self.client.messages.parse(
            model=self.model,
            max_tokens=max_tokens,
            thinking={"type": "adaptive"},
            # stable prefix: the system prompt never varies within a task
            system=[{"type": "text", "text": system,
                     "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": content}],
            output_format=schema,
        )
        usage = {"in": resp.usage.input_tokens, "out": resp.usage.output_tokens,
                 "price_in": PRICE_IN, "price_out": PRICE_OUT}
        return resp.parsed_output, usage
