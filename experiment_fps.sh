#!/usr/bin/env bash
# EXPERIMENT: fps
# How does the frame rate change what the probe finds? One clip, one query set,
# everything else held fixed; each rate scored against the hand-filled ground
# truth.
#
#   ./experiment_fps.sh                      # fps 1 and 2, no scene context
#   ./experiment_fps.sh --scene              # same, with scene context supplied
#   ./experiment_fps.sh --fps "1 2"          # pick the rates
#   ./experiment_fps.sh --samples 3          # answers drawn per query
#   ./experiment_fps.sh --dry-run            # render frames, make no API calls
#
# Frame rate is the expensive axis: the clip is 180 s, so fps 1 and 2 send 181
# and 361 images per call, roughly 1M and 2M input tokens each. Samples
# multiply that -- the images are re-sent on every call, there being no
# multi-sample discount on this API.
#
# 5 fps is not in the default list. At 901 images a single call runs to about
# 5M input tokens, which is enough to exhaust a per-minute token quota on its
# own; the backoff in utils/backend_*.py cannot help with a limit that one
# request crosses by itself. Pass --fps "5" deliberately if you want to find
# out where that ceiling is.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

CLIP=${CLIP:-videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4}
QUERIES=${QUERIES:-queries/events-key.txt}
TRUTH=${TRUTH:-notes/ground-truth-2026-08-25-17_00_01.txt}
SCENE_FILE=${SCENE_FILE:-scene/12F-Ams.built.md}

FPS_LIST="1 2"
SAMPLES=5
EXTRA=""
LABEL="no-scene"

while [[ $# -gt 0 ]]; do
    case $1 in
        --scene)    EXTRA="$EXTRA --scene $SCENE_FILE"; LABEL="with-scene"; shift ;;
        --fps)      FPS_LIST="$2"; shift 2 ;;
        --samples)  SAMPLES="$2"; shift 2 ;;
        --dry-run)  EXTRA="$EXTRA --dry-run"; shift ;;
        --clip)     CLIP="$2"; shift 2 ;;
        *) echo "unknown option: $1" >&2; exit 2 ;;
    esac
done

# The project env, not whatever python is on PATH: the base conda install has
# none of the dependencies and fails deep inside an import instead of here.
# Refuse to start on top of a run that is already going. Two probes racing
# each other blow the per-minute token quota between them and both spend their
# retries waiting for the other -- and a killed probe does not stop the loop
# that spawned it, so an interrupted run can quietly still be going.
if pgrep -f "scripts/vlm_probe.py" >/dev/null; then
    echo "a probe is already running:" >&2
    pgrep -af "scripts/vlm_probe.py" | cut -c1-120 >&2
    echo >&2
    echo "wait for it, or stop it AND its parent loop:" >&2
    echo "  pkill -f experiment_fps.sh; pkill -f scripts/vlm_probe.py" >&2
    exit 1
fi

PY="$HOME/envs/traffic/bin/python"
[[ -x "$PY" ]] || { echo "no interpreter at $PY -- see README section 8" >&2; exit 1; }

for f in "$CLIP" "$QUERIES"; do
    [[ -f "$f" ]] || { echo "missing: $f" >&2; exit 1; }
done
[[ "$EXTRA" == *--scene* && ! -f "$SCENE_FILE" ]] && {
    echo "missing $SCENE_FILE -- build it first:" >&2
    echo "  $PY scripts/build_scene.py scene/12F-Ams.txt" >&2; exit 1; }

echo "clip     $CLIP"
echo "queries  $QUERIES  ($(grep -vc '^\s*#\|^\s*$' "$QUERIES") categories)"
echo "fps      $FPS_LIST"
echo "samples  $SAMPLES per query"
echo "scene    $LABEL"
echo

DIRS=()
for F in $FPS_LIST; do
    echo "───────── fps $F ─────────"
    # shellcheck disable=SC2086
    "$PY" scripts/vlm_probe.py "$CLIP" \
        --queries "$QUERIES" --fps "$F" \
        --batch-queries --samples "$SAMPLES" $EXTRA
    # newest matching directory is the one just written
    D=$(ls -dt results/*fps"$F"_n"$SAMPLES"_batch* 2>/dev/null | head -1)
    [[ -n "$D" ]] && DIRS+=("$D")
    echo
done

[[ "$EXTRA" == *--dry-run* ]] && exit 0

echo "═════════ scores ═════════"
for D in "${DIRS[@]}"; do
    [[ -f "$D/results.jsonl" ]] || { echo "no results in $D -- skipped"; continue; }
    echo "───────── $(basename "$D")"
    "$PY" scripts/score.py "$D" "$TRUTH" || true
    echo
done
