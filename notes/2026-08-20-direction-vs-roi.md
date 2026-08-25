# Direction, not resolution

Record of four probe runs and one controlled ablation on a single clip, and what
survived verification against the frames.

- **Clip** `data/12thFBotwinik/L12thFloorBotwinik-D-2025-11-03_T-17_00_01.mp4`
  (3840x2160, VFR, 180 s, evening peak)
- **Model** `gemini-3.1-pro-preview`, `resolution=high`, `thinking=high`
  (one run on `gemini-3.5-flash` for contrast)
- **Date** 2026-08-20
- **Ground truth** established by eye from locally decoded frames, no API calls;
  the frames it rests on are in `notes/figures/`.

---

## 0. Runs

| # | run | ROI | window | fps | frames/call | queries | artifacts |
|---|---|---|---|---|---|---|---|
| 1 | `full-flash` | `junction` | 0-180 s | 0.5 | 90 | 20/22 (interrupted) | not kept -- jsonl only, gitignored |
| 2 | `full-pro` | `junction` | 0-180 s | 0.5 | 90 | 22/22 | `results/full-pro/` |
| 3 | `full-pro-wide` | `wide` | 0-180 s | 0.5 | 90 | 22/22 | `results/full-pro-wide/` (+ an aborted partial, rows 1-2) |
| 4 | ROI ablation | `none` / `junction` / `wide` | 130-166 s | 0.5 | 18 | 3 x 3 | `results/roi-{none,junction,wide}-bus/` |

Query sets: `queries/starter.txt` (runs 1-3), `queries/bus-direction.txt` (run 4).
Rendered frames for every run under `runs/<name>/`.

Image actually sent, per ROI (after `fit()` to a 1568 px long edge):

| ROI | crop | sent | linear resolution on the junction box |
|---|---|---|---|
| `none` | 3840x2160 | 1568x882 | 0.41x |
| `junction` (0.28,0.00,0.40,0.42) | 1536x907 | 1536x907 | 1.00x |
| `wide` (0.17,0.00,0.54,1.00) | 2074x2160 | 1505x1568 | 0.73x |

Not cropping is the *lowest* resolution condition on the subject, not the
highest-information one. What each crop keeps and drops:
`notes/figures/roi-extent.jpg` (red box = `junction`).

### 0.1 Two process notes

**Free-tier accounts cannot run the default backend.** On the education/free
key, `gemini-3.1-pro-preview` returns `429 exceeded your current quota` on a
10-token text call, while `gemini-3.5-flash`, `gemini-3-flash-preview` and
`gemini-3.1-flash-lite` succeed. Probe with a one-line call before spending a
run. Runs 2-4 were made after the account was upgraded.

**`0.28,0.00,0.40,0.42` is the `junction` preset**, which `utils/render.py`
documents as "not recommended as a default -- it cuts the southbound approach
and both sidewalks". The script's own default is `wide`. Runs 1 and 2 inherited
the junction coordinates from the README usage example, which the README itself
flags as a placeholder. Run 3 exists to correct that.

**Token accounting is broken.** All summaries report `0 in / 0 out`;
`backend_gemini._usage()` does not find the usage field on the Interactions API
response, so cost per run is unrecorded.

---

## 1. Ground truth for the 130-166 s event

Verified by decoding the clip locally at 2 fps and cropping suspect regions at
native 4K resolution. No model involved.

- **One** articulated bus, MTA 5444. It travels **north** up the avenue
  (rolling, never stationary, 122-144 s), **turns left** onto the east-west
  street, and comes to rest at the **north kerb** around 148 s. It is still
  parked there at 166 s.
- The yellow end of the bus is its **rear** -- tail lights and rear window are
  resolvable at native resolution.
- Dark vehicles west of the double yellow line at 134-142 s are travelling
  **south**, in the southbound lanes. Legal. Their headlights face the camera.
- **No** vehicle travels against the flow of traffic anywhere in the clip.
- **No** bus starts from rest within the window.

Evidence: `notes/figures/bus-5444-trajectory.jpg` (132-160 s at 4 s spacing),
`notes/figures/southbound-cars-134-142.jpg` (native resolution, the cars the
`wide` ablation called wrong-way).

Two further situations checked, for the negative controls in runs 2 and 3:

- **48 s** -- a tarp-covered cargo trike with its rider, ~50x30 px, low and
  horizontal, moving west. Nobody falls, nobody is on the ground.
- **70 s** -- an adult crouching toward a small child or dog **on the sidewalk**
  near the corner, standing up again by 72 s. Not the roadway, not a crosswalk.
- **0-12 s** -- a bus travelling **south** in the southbound lane, alongside a
  stationary queue in the adjacent northbound lane.

Evidence: `notes/figures/sidewalk-crouch-68-74.jpg`,
`notes/figures/southbound-bus-0-12.jpg`.

---

## 2. Results

### 2.1 Runs 2 and 3: same 22 queries, ROI is the only difference

| axis | `junction` answered present | `wide` answered present |
|---|---|---|
| referential | 3/4 | 4/4 |
| spatial | 3/4 | 3/4 |
| temporal | 3/3 | 3/3 |
| relational | 4/4 | 3/4 |
| state | 2/2 | 2/2 |
| **negative** (all known absent) | **2/5** | **2/5** |
| total matches | 36 | 42 |

### 2.2 The negative controls, side by side

| control | `junction` | `wide` |
|---|---|---|
| fire truck with flashing lights | absent | absent |
| horse-drawn carriage | absent | absent |
| collision between two vehicles | absent | absent |
| **vehicle driving the wrong way** | **MATCH** (bus, 152-158 s) | **MATCH** (bus 0-12 s; bus 72-146 s) |
| **person lying in the roadway** | **MATCH** (cyclist, 48 s) | **MATCH** (pedestrian, 70-72 s) |

The same two controls fail under both ROIs, and the same three hold. The
fabrication target moves (different object, different timestamp) but the
*queries* that provoke it do not.

Every fabricated claim carried `match_quality: exact` and `confidence: high`,
and every one arrived with a filled-in `considered_and_rejected` field. That
field produces discrimination-shaped prose whether or not discrimination
happened; it is not a guard.

### 2.3 Run 4: ROI ablation on one event

Same 36 s window, same three queries, same model, ROI the only variable.
Truth from section 1.

| query | truth | `none` | `junction` | `wide` |
|---|---|---|---|---|
| a vehicle driving the wrong way | absent | absent | absent | **MATCH** (black SUV "northbound in the southbound lanes", "flashing lights") |
| an articulated city bus | one, north then left turn | **two buses**, first "straight through" | **one, left turn** | **two buses**, "5444 northbound straight through" + "another eastbound" |
| a stopped bus begins to move off | absent | **MATCH** | absent | **MATCH** |
| | | 1/3 | **3/3** | 0/3 |

---

## 3. What survived

**F1. Near-miss capture.** A negative control holds when the scene contains no
analogue of the queried situation (horse-drawn carriage, fire truck, collision:
3/3 correct under both ROIs). It fails when the scene contains an ambiguous
near-analogue, which the model then resolves *toward the query*. Four
independent instances:

| what is really there | what was reported |
|---|---|
| low tarp-covered cargo trike, 50x30 px, moving | "a cyclist falls and is down on the roadway" |
| adult crouching over a child/dog on the sidewalk | "a pedestrian lying in the crosswalk, another standing over them" |
| bus northbound, east of the double yellow, turning left | "driving entirely in the oncoming lanes" |
| dark car southbound, west of the double yellow | "black SUV northbound in the southbound lanes, flashing lights" |

The object is real in every case. The invented part is the state the query asked
about.

**F2. Heading inversion is the motion-shaped special case of F1, and the lane
evidence is read correctly.** In all three wrong-way fabrications the model
locates the vehicle relative to the double yellow line accurately, then assigns
the opposite direction of travel, then resolves the resulting contradiction as a
violation rather than as its own error. Direction is what it cannot recover from
stills at 0.5 fps; lane geometry is static and it reads that well.

**F3. Wider framing splits one object into two.** `none` and `wide` both report
two articulated buses where there is one, and give the phantom a direction the
real bus does not have. `junction` does not. Same mechanism as F2: cross-frame
association fails, so "arriving" and "departing" become separate individuals.

**F4. The self-report fields are saturated.** 36/36 and 42/42 matches are
`exact` + `high`; `unreadable_reasons` is empty in all 44 query results. As
implemented these fields carry no information. `match_quality` was supposed to
separate exact from superficial (README section 6) and does not.

**F5. Answers are query-conditioned, not read off a stable scene.** In run 2 the
collision control is answered absent on the grounds that "no vehicles ever
appear to be on a collision course or interact closely", while the relational
axis reports, in the same clip, two road users passing close enough that one
changed course. The same bus is described as turning left, turning right, and
driving straight in three different answers. Each answer is `exact`/`high`.

**F6. The state axis fails circularly, and the stated reason for expecting it to
fail is wrong.** All five state-axis matches rest on wording of the form
"traffic is moving, therefore the pedestrian signal was red" -- the inference
the prompt forbids. But signal heads are ~20-30 px in the native frame and at
least two of them show a **resolvable green lens**
(`notes/figures/signal-head-near.jpg`, `notes/figures/signal-head-far.jpg`,
both cropped from the native 4K frame at t=48 s). The README predicts failure from
missing pixels; the pixels are there. This makes the state axis a testable
question rather than a flat negative, via a dedicated signal-head crop.

---

## 4. Hypotheses killed

**"The wrong-way call came from cropping away the southbound approach."**
Plausible after run 2 -- the bus's approach leg is outside `junction`, and
direction is exactly what was got wrong. Run 4 refutes it: `junction` is the
only condition that answered that query correctly and described the bus's
trajectory correctly, while both conditions that *do* show the approach failed.
The run 2 vs run 3 comparison that suggested it also confounds window length
(180 s vs 36 s) with ROI.

**"ROI is the lever that matters."** Runs 2 and 3 differ by 6 matches out of 22
queries and by nothing at all on the negative controls. Whatever separates a
good answer from a fabricated one here, it is not the crop.

---

## 5. Limits

- One clip, one three-minute window, one time of day.
- One sample per cell. No repeated sampling, so model variance is unmeasured and
  the 3/3 vs 1/3 vs 0/3 of run 4 (nine calls total) could invert on a re-run.
  **Run 4 does not license "junction is better".** It licenses only the claim
  that the crop does not explain the failure.
- Ground truth is one observer reading frames at 2 fps. A sub-2 s pause or
  contact is not excluded; VFR means even PTS-derived times carry some slack.
- Runs 1-3 sample at 0.5 fps, so every direction judgement rests on 2 s spacing.
  That is the variable section 6 tests, and it is confounded into every result
  above.
- Cost per run is unknown (token accounting returns zero).

---

## 6. Next experiment

Fix ROI, vary sampling rate. Same 130-166 s window, `--roi junction`, queries
whose truth depends on direction of travel; conditions `--fps 0.5` (18 frames)
and `--fps 2` (72 frames); at least three repeats per cell so that variance is
visible.

Prediction, from F2 and F3: at 2 fps the heading inversions and the
double-counting both disappear, because the model gains the cross-frame evidence
it currently lacks. If they persist, the model is not associating objects across
frames at all, and direction has to be supplied externally -- which promotes the
Phase 3 geometry work from a scoring instrument to a model input.

Either outcome is a finding in the sense of README section 3: a capability
boundary with a mechanism, stated so that it survives a change of dataset.

---

## Appendix: commands

```bash
CLIP=data/12thFBotwinik/L12thFloorBotwinik-D-2025-11-03_T-17_00_01.mp4

# run 2 -- junction crop, full query set
python scripts/vlm_probe.py $CLIP --queries queries/starter.txt \
    --roi 0.28,0.00,0.40,0.42 --fps 0.5 --name full-pro

# run 3 -- same, wide crop
python scripts/vlm_probe.py $CLIP --queries queries/starter.txt \
    --roi wide --fps 0.5 --name full-pro-wide

# run 4 -- ROI ablation on one event
for R in none junction wide; do
  python scripts/vlm_probe.py $CLIP --queries queries/bus-direction.txt \
      --start 130 --end 166 --fps 0.5 --roi "$R" --name "roi-$R-bus"
done
```

These were run before the per-run directory existed, when `--out` and
`--results` named a frames path and a file prefix and two runs of the same
command appended into one jsonl. Their output has since been moved to
`results/<name>/summary.md`; the commands above are the current equivalents.
