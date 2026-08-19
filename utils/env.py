"""Loading API keys from a .env file at the repository root.

Called explicitly from entry points rather than on import -- utils/ modules
must stay side-effect free, and a library that silently mutates os.environ
when imported is hard to reason about in tests.
"""
import os
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent

# env vars each backend will accept, in precedence order
BACKEND_KEYS = {
    "gemini": ("GEMINI_API_KEY"),
    "claude": ("ANTHROPIC_API_KEY",),
}


def load_env(path: Optional[Path] = None, override: bool = False) -> Optional[Path]:
    """Load `.env` into os.environ. Returns the file used, or None.

    By default a key already exported in the shell wins over the file, so a
    one-off `GEMINI_API_KEY=... python scripts/...` behaves as expected.
    """
    path = Path(path) if path else REPO_ROOT / ".env"
    if not path.exists():
        return None
    try:
        from dotenv import load_dotenv
    except ImportError:  # keep the repo usable without the extra dep
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip("'\"")
            if v and (override or k not in os.environ):
                os.environ[k] = v
        return path
    load_dotenv(path, override=override)
    return path


def key_status(backend: str) -> str:
    """Human-readable, masked report of which key was picked up."""
    for name in BACKEND_KEYS.get(backend, ()):
        val = os.environ.get(name)
        if val:
            return f"{name}=***{val[-4:]}"
    return "no key found"


def require_key(backend: str) -> None:
    """Fail early with an actionable message rather than deep inside the SDK."""
    names = BACKEND_KEYS.get(backend, ())
    if any(os.environ.get(n) for n in names):
        return
    if backend == "claude":
        # the Anthropic SDK also reads an `ant auth login` profile, so a
        # missing env var is not conclusive -- let the SDK decide
        return
    raise SystemExit(
        f"No API key for backend '{backend}'.\n"
        f"  Set one of: {', '.join(names)}\n"
        f"  Either export it, or:  cp .env.example .env  and fill it in."
    )
