#!/usr/bin/env bash
# EXPERIMENT: fps -- does the frame rate change what the probe finds?
#
#   ./experiment_fps.sh                 # fps 1 and 2, then score each arm
#   ./experiment_fps.sh --scene         # with scene context
#   ./experiment_fps.sh --fps "1" --samples 3 --dry-run
#
# Cost is per image: fps 1/2 = 181/361 images per call, x samples. 5 fps is
# excluded by default -- one 901-image call can exhaust the per-minute quota
# on its own, which no backoff can fix.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

CLIP=${CLIP:-videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4}
QUERIES=${QUERIES:-queries/events-key.txt}
TRUTH=${TRUTH:-ground-truth/2026-08-25-17_00_01.txt}
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
# Two probes racing each other exhaust the quota between them, and a killed
# probe does not stop the loop that spawned it.
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

EXP=experiment_results/fps
DIRS=()
for F in $FPS_LIST; do
    ARM="$EXP/arms/fps$F"
    [[ "$LABEL" == "with-scene" ]] && ARM="$EXP/arms/fps${F}-scene"
    if [[ -f "$ARM/results.jsonl" ]]; then
        # keep the old run, out of the way of the new one
        PREV="$ARM.prev-$(date +%m%d-%H%M)"
        echo "$ARM already holds a run -- moving it to $PREV"
        mv "$ARM" "$PREV"
    fi
    echo "───────── fps $F ─────────"
    # shellcheck disable=SC2086
    "$PY" scripts/vlm_probe.py "$CLIP" \
        --queries "$QUERIES" --fps "$F" \
        --batch-queries --samples "$SAMPLES" \
        --run-dir "$ARM" --out "runs/fps/fps$F" $EXTRA
    [[ -f "$ARM/results.jsonl" ]] && DIRS+=("$ARM")
    echo
done

[[ "$EXTRA" == *--dry-run* ]] && exit 0

echo "═════════ scores ═════════"
for D in "${DIRS[@]}"; do
    [[ -f "$D/results.jsonl" ]] || { echo "no results in $D -- skipped"; continue; }
    echo "───────── $(basename "$D")"
    "$PY" scripts/score.py "$D" "$TRUTH" --write "$D/score.md" || true
    echo
done
