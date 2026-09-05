#!/usr/bin/env bash
# EXPERIMENT: scene -- does supplying measured camera facts change what the
# probe finds? Two arms, identical except for --scene.
#
#   ./experiment_scene.sh                 # fps 1, 5 samples, both arms
#   ./experiment_scene.sh --rebuild       # re-measure and rebuild the block first
#   ./experiment_scene.sh --only with-scene --fps 2 --samples 3
#
# Always run the no-scene arm too: supplied context can be echoed back as
# observation, and only the contrast makes that visible.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

CLIP=${CLIP:-videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4}
QUERIES=${QUERIES:-queries/events-key.txt}
TRUTH=${TRUTH:-ground-truth/2026-08-25-17_00_01.txt}
NOTES=${NOTES:-scene/12F-Ams.txt}
SCENE=${SCENE:-scene/12F-Ams.built.md}

FPS=1
SAMPLES=5
ARMS="no-scene with-scene"
REBUILD=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --fps)     FPS="$2"; shift 2 ;;
        --samples) SAMPLES="$2"; shift 2 ;;
        --only)    ARMS="$2"; shift 2 ;;
        --rebuild) REBUILD=1; shift ;;
        --clip)    CLIP="$2"; shift 2 ;;
        *) echo "unknown option: $1" >&2; exit 2 ;;
    esac
done

# Two probes racing each other exhaust the quota between them, and a killed
# probe does not stop the loop that spawned it.
if pgrep -f "scripts/vlm_probe.py" >/dev/null; then
    echo "a probe is already running:" >&2
    pgrep -af "scripts/vlm_probe.py" | cut -c1-120 >&2
    echo "stop it AND its parent loop:" >&2
    echo "  pkill -f experiment_ ; pkill -f scripts/vlm_probe.py" >&2
    exit 1
fi

PY="$HOME/envs/traffic/bin/python"
[[ -x "$PY" ]] || { echo "no interpreter at $PY -- see README section 9" >&2; exit 1; }
for f in "$CLIP" "$QUERIES"; do
    [[ -f "$f" ]] || { echo "missing: $f" >&2; exit 1; }
done

if [[ $REBUILD -eq 1 ]]; then
    echo "═════════ rebuilding the scene block ═════════"
    "$PY" scripts/build_scene.py "$NOTES" --video "$CLIP"
    echo
fi
[[ "$ARMS" == *with-scene* && ! -f "$SCENE" ]] && {
    echo "missing $SCENE -- build it first:" >&2
    echo "  $PY scripts/build_scene.py $NOTES --video $CLIP" >&2; exit 1; }

echo "clip     $CLIP"
echo "queries  $QUERIES  ($(grep -vc '^\s*#\|^\s*$' "$QUERIES") categories)"
echo "fps      $FPS   samples  $SAMPLES per query"
echo "arms     $ARMS"
[[ "$ARMS" == *with-scene* ]] && \
    echo "scene    $SCENE  ($(wc -w < "$SCENE") words)"
echo

EXP=experiment_results/scene
DIRS=()
for ARM in $ARMS; do
    D="$EXP/arms/$ARM"
    if [[ -f "$D/results.jsonl" ]]; then
        PREV="$D.prev-$(date +%m%d-%H%M)"
        echo "$D already holds a run -- moving it to $PREV"
        mv "$D" "$PREV"
    fi
    echo "───────── $ARM ─────────"
    EXTRA=()
    [[ "$ARM" == "with-scene" ]] && EXTRA=(--scene "$SCENE")
    "$PY" scripts/vlm_probe.py "$CLIP" \
        --queries "$QUERIES" --fps "$FPS" \
        --batch-queries --samples "$SAMPLES" \
        --run-dir "$D" --out "runs/scene/$ARM" "${EXTRA[@]}"
    [[ -f "$D/results.jsonl" ]] && DIRS+=("$D")
    echo
done

echo "═════════ scores ═════════"
for D in "${DIRS[@]}"; do
    [[ -f "$D/results.jsonl" ]] || { echo "no results in $D -- skipped"; continue; }
    echo "───────── $(basename "$D")"
    "$PY" scripts/score.py "$D" "$TRUTH" --write "$D/score.md" || true
    echo
done

# Wording lifted from the supplied block, counted in the model's own prose. An
# arm that was given the block and uses this language far more than one that was
# not is repeating what it was told; the phrases are not evidence of looking.
if [[ ${#DIRS[@]} -eq 2 ]]; then
    echo "═════════ echo check ═════════"
    "$PY" - "${DIRS[@]}" <<'PYEOF'
import json, sys
from pathlib import Path
PHRASES = ["up the frame", "down the frame", "right to left", "left to right",
           "double yellow", "scaffolding shed", "tree canopy", "pedestrian signal"]
print(f"{'arm':<28} {'uses':>5}   phrases")
for d in sys.argv[1:]:
    hits = {}
    for line in (Path(d) / "results.jsonl").read_text().splitlines():
        r = json.loads(line)
        for m in (r.get("matches") or []):
            t = (m.get("what_happens", "") + " " + m.get("subject", "")).lower()
            for p in PHRASES:
                if p in t:
                    hits[p] = hits.get(p, 0) + 1
    print(f"{Path(d).name.split('_')[0]:<28} {sum(hits.values()):>5}   "
          + (", ".join(f"{k} x{v}" for k, v in sorted(hits.items())) or "—"))
PYEOF
fi
