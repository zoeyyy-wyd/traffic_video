#!/usr/bin/env bash
# Remove unusable clips from the footage directory.
#
#   empty       zero-byte placeholders left by the archived date range
#   unreadable  non-zero but will not open -- an mp4 keeps its index at the
#               end of the file, so a truncated transfer looks fine in a
#               directory listing and fails only when something opens it
#
# clean_data.py prints everything it is about to remove before removing it.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

# Bare `python` is the base conda install, which has none of the dependencies.
# Prefer the project env; fall back to whatever is active only if it can import av.
ENV_PY="$HOME/envs/traffic/bin/python"
if [[ -x "$ENV_PY" ]]; then
    PY="$ENV_PY"
elif python -c 'import av' 2>/dev/null; then
    PY=python
else
    echo "error: no interpreter with PyAV." >&2
    echo "  expected $ENV_PY, or run 'conda activate traffic' first." >&2
    exit 1
fi

DIR="${1:-data/12thFBotwinik}"
exec "$PY" scripts/clean_data.py "$DIR" --apply --status empty,unreadable
