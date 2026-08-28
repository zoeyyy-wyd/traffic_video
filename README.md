# traffic_video — What can a VLM actually ground in fixed-camera traffic video?

An exploratory study, not a product. The question is where vision-language
models succeed and fail at grounding language to a fixed-camera intersection
recording — which objects, which moments, which relations they can resolve, and
**why** they fail where they do.

The deliverable is a characterisation with mechanisms attached, plus a small set
of reusable techniques for getting verifiable output out of a VLM. It is not a
violation-detection system, and no part of this repo should be read as one.

Data is the COSMOS intersection footage
(`ProjectTrafficIntersection.COSMOS.V2/annotations/spring2025.4_view.Annotation`):
fixed multi-view cameras, YOLO-format boxes over 14 classes (`car, bike, truck,
motorcycle, pedestrian, van, city-bus, school-bus, e-bikes, taxi, e-scooter,
stroller, pet, emergency-vehicle`), with a 3-minute 1 fps pilot segment from
`12F-Ams` and the raw recordings behind it.

---

## 1. Why this setting is worth studying

Published VLM video benchmarks are dominated by ego-view dashcam footage and
web video. This is neither. A camera on the 12th floor looking down obliquely
across an intersection is a distinct visual regime, and its failure modes do
not transfer from the benchmark setting:

- **Severe perspective compression.** The view is oblique, not nadir. Near the
  camera a pixel spans centimetres; across the intersection it spans tens of
  centimetres. Any spatial judgement degrades non-uniformly with distance.
- **Most of the frame is not the scene.** Roughly a third is the host
  building's brick wall; more is facade and tree canopy. The intersection
  occupies a minority of the pixels.
- **Structural, not incidental, occlusion.** A sidewalk scaffolding shed hides
  an entire sidewalk from this camera. Tree canopy hides part of a crosswalk,
  and seasonally so. Vehicles occlude each other badly at shallow angles.
- **The decisive evidence is often sub-pixel.** A signal head is a few pixels
  after the downscaling every VLM applies, and for some approaches the signal
  face points away from the camera entirely.
- **Vulnerable road users are the subject.** The class list singles out
  `stroller`, `pet`, `e-bikes`, `e-scooter` — this is a study of pedestrians and
  micromobility, not of vehicle throughput. Those are the smallest, most
  occluded objects in frame.

That last pair is what makes the setting interesting rather than merely hard:
the objects the research cares about are precisely the ones the model can least
afford to lose.

---

## 2. Decomposing the question

"Can a VLM do grounding here?" is not answerable as posed. It separates into
axes that fail for unrelated reasons, and conflating them produces an accuracy
number that explains nothing.

| Axis | Question form | Expected | Failure mechanism |
|---|---|---|---|
| **Referential** | "the white box truck" → which object | good | confusion among same-class instances |
| **Spatial** | "in the crosswalk", "past the stop line" | mixed | oblique perspective; depth misread as distance |
| **Temporal** | "when did it cross" | poor | sampling rate; an instant between samples |
| **Relational** | "the van that failed to yield" | possibly strong | — |
| **State** | "while the signal was red" | splits — see below | vehicle heads face away; pedestrian heads are legible |

The state axis was the sharpest prediction in this repo — that it fails for
information reasons, because a signal head spanning three or four pixels cannot
be read at any level of model quality. **That has been measured, and it is half
wrong.** The axis splits in two, and the split is decided by how a head is
mounted rather than by how many pixels it spans
(measured 2026-08-27; evidence in `notes/figures/2026-08-27-*.png`):

- **Vehicle** heads present only their tops and backs to this camera. Sampled
  across a whole clip they are pixel-for-pixel invariant, so their state is
  unavailable at any resolution or tier. They are the *larger* targets, which
  is why the pixel-count argument was the wrong one.
- **Pedestrian** heads do show an illuminated face. The state is carried by an
  8 x 10 patch of the native frame at a 97-point `R − B` separation, and that
  separation survives every downscale the probe applies — colour is
  low-frequency, so averaging preserves it while destroying glyph shape. It is
  resolvable by eye in every condition, night included.

So on the pedestrian phase the pixels are *present*, which makes it a clean
experiment rather than a flat negative: a wrong answer there cannot be blamed
on missing evidence. The failure mode still worth instrumenting is the model
inferring colour from behaviour — "traffic is stopped, so it must be red" —
which is circular, confidently stated, and wrong exactly on the marginal cases
that matter. `utils/schema.py` catches it directly: every reported event must
declare `signal_state_basis` as `read_directly`, `inferred_from_behaviour`, or
`unknown`, and every window reports `signal_head_visible`. Vehicle-phase
questions (red-light running) remain unanswerable from this view and need the
fallbacks in section 5.

---

## 3. What counts as a finding

This governs how the experiments are designed, so it is stated before them.

**Not a finding:** "Model X reaches 72% on traffic event detection." It does not
survive a change of dataset and explains nothing to anyone.

**A finding:** a capability boundary with a mechanism.

- *"Signal-state judgements fail because the vehicle heads face away from the
  camera entirely, while the pedestrian heads do not — which locates the
  bottleneck in mounting geometry rather than in resolution or reasoning, and
  predicts which of the two remains answerable after any downscaling."*
- *"Constraining the model to select from a supplied index set drives
  hallucinated locations to zero, because an out-of-range index is rejected
  programmatically rather than trusted."*
- *"Relational judgements survive aggressive downsampling that destroys
  referential ones, which suggests the two draw on different visual evidence."*

The second kind generalises past this dataset. The first does not.

---

## 4. Phases

### Phase 0 — pick clips, not a window

The corpus is 189 clips of **three minutes each**, sampled at a few times of day
across many dates. It is not continuous: the 17:00 clip ends at 17:03 and the
next begins at 17:30. There is no ten-minute stretch anywhere, so the unit of
work is one clip.

Several clips beat one long window regardless. A single stretch risks a result
that reflects that afternoon's traffic and light; five clips across times and
dates give a spread rather than a point estimate, and show whether a finding
survives a change of conditions. Suggested first sample:

```
3 x 17:00 / 17:30   evening peak, highest event density (68 clips available)
1 x 09:00           morning, sun from the opposite side
1 x 22:00           night
```

The night clip earns its place twice over. The finding that signal faces are
unreadable here was measured on daytime footage; an illuminated lens at night
has an order of magnitude more contrast against its surroundings, so the
conclusion may invert. If it does, the state axis becomes testable under a
stated condition, which is a better result than a flat negative.

Exhaustive hand-labelling of one clip is under an hour, so five clips is about
half a day and yields perhaps 40-80 situations. **But it is not the first
step** — see the negative controls in section 6, which score without any
annotation at all.

### Phase 1 — capability probes

A battery of targeted questions across the five axes, **run against the same
clips**, so that a wrong answer is attributable to an axis rather than to
general difficulty. Asking one clip five different kinds of question is worth
more than asking five clips one kind.

Emergency-vehicle passage is the best target to start with, ahead of red-light
running:

- it needs no scene state outside the frame, so it has no blocking dependency;
- the object is unmistakable at any scale, so a failure is a real reasoning
  failure rather than missing pixels — which makes it a clean experiment;
- it is already class 13 in the annotation ontology;
- if this is the Amsterdam Ave corridor near Mount Sinai Morningside, incidence
  should be high enough to find samples;
- it is the canonical exculpating circumstance for any later violation call.

### Phase 2 — ablations over the two design levers

This is where a reusable contribution lives, because it answers *how to use*
a VLM rather than whether one works.

**Output constraint.** Free-text answers versus selection from a supplied index
set (Set-of-Mark style: numbered boxes, numbered tiles). Measures hallucination
rate. The constrained form is not implemented yet: it would have the model name
a tile number, drop indices outside the grid, and derive timestamps from the
index rather than take them from the model.

**Visual budget.** Resolution tier; sampling rate; tiled contact sheet versus
separate full-resolution frames. Measures where the perception bottleneck sits.
Frames are sent whole, fitted to a 1568 px long edge; cropping was removed as a
variable because the properties these queries turn on are low-frequency and
survive downscaling intact (measured 2026-08-27).

**Timestamp encoding.** Every answer here is a time interval, so how a frame is
bound to its own timestamp is a lever in its own right. `--time-encoding` takes
any subset of three independent channels:

| channel | where the timestamp is | how the model must bind it to a frame |
|---|---|---|
| `burn` | drawn into the frame's pixels | it is *in* the frame |
| `list` | one text block naming every timestamp in order | positionally: count to the k-th number |
| `interleave` | one text block immediately before its own frame | adjacency in the message itself |

`burn,list` is the default and reproduces every run made before the flag
existed. The interesting arms are `burn` alone, `interleave` alone, and
`burn,interleave`: the measure is not whether an event is found but whether the
returned `t_start_sec` / `clearest_frame_sec` land on the right frame, which is
checkable against the jpgs in `runs/` without a human labelling anything. Note
that an image content block has no caption or metadata field on either
provider, so these two are the only places a per-frame timestamp can go.

### Phase 3 — geometry as an instrument

Only here, and **only on the evaluation window** — not over the corpus.

The purpose is not to do the model's job. It is to provide objective reference
values so that error can be quantified rather than eyeballed: ground-plane
speeds, post-encroachment time, the frame at which a stop line was crossed.
That turns "the model's account seems off" into "the model reported 1.5 s where
the measured value is 3.2 s".

Most VLM video evaluation cannot do this. A fixed calibrated camera with
existing box annotations can, and it is a large part of what this dataset
offers.

What it needs, all one-time per view: a ground-plane homography (the project's
autocalibration), hand-annotated scene polygons (crosswalks, stop lines, lane
directions, intersection box), and a signal-phase timeline. On phase reading, a
fixed-box classifier plus a state machine over legal phase transitions is both
cheaper and more accurate than asking a model per frame — but see §5 on whether
the signal faces are visible at all.

**Reliability must be bounded, not assumed.** Under this obliquity, homography
error grows sharply with distance. Measure it against known dimensions
(crosswalk stripe spacing, lane width) at near, mid and far range, then define
a polygon within which metric claims are made and mark everything outside it
`metrics_reliable: false`. Reporting a PET value with unstated error is worse
than reporting none.

---

## 5. Site constraints that shape every experiment

These are facts about this camera, not about method. If the view changes, this
section is rewritten and the rest stands.

**Sampling asymmetry.** Annotation is 1 fps; the raw recordings are not. At 1 fps
a vehicle travels 10–15 m between samples, so a stop-line crossing can fall
entirely between frames, deceleration and TTC cannot be estimated from two
consecutive points, and the yellow-to-red transition can be missed. Use the 1 fps
annotation to locate roughly where something is; do anything timing-dependent
against the raw video.

**Timestamp alignment must be verified, not derived.** The capture is a
GStreamer network recording, so variable frame rate and dropped frames are
likely. `t = frame_index / fps` is a hypothesis, not a fact. A one-second drift
puts a crossing in the wrong signal phase and silently inverts the verdict.
`utils/video.py` reads PTS from the container throughout and never derives time
from an index; `probe()` flags a VFR mismatch. Confirm the mapping empirically
by checking annotated boxes against raw frames at the start, middle and end of a
segment — a constant offset shows as uniform mismatch, drift as mismatch that
grows.

**Camera motion.** A tall building sways. If one homography is to serve a whole
recording, verify stability by tracking static background features across frames
first.

**Signal-face visibility is a prerequisite, not a detail.** Signals facing the
approach that runs toward the camera present only their backs. Before any
experiment that depends on phase, establish which approaches have a legible
signal face in which of the four views. If some approach is legible in none,
the fallbacks in order are: infer from phase coupling with an approach that is
visible; detect queue-discharge onset as the green edge; obtain the timing plan
from NYC DOT.

Measured for the 12F-Ams view on 2026-08-27: **no vehicle head is legible, both
pedestrian heads are.** The pedestrian phase can therefore be read off a fixed
box directly — the timeline for one clip is in the note — while every
vehicle-phase question on this view needs one of the fallbacks above. Note that
the pedestrian countdown *flashes*, so a two-level classifier reports each dark
flash as WALK; three states are needed, not two.

**Multi-view is a coverage requirement, not a nicety.** Some regions are
visible from only certain cameras. Scene annotations should carry
`visible_from: [view_ids]`, and detection rates must be reported per view —
otherwise "not visible from this camera" reads as "nothing happens here".

**Frames are sent whole.** Models downscale to a fixed long edge, so a frame
that is two-thirds wall spends two-thirds of its budget on wall, and cropping
to the intersection would buy back roughly a 2× linear gain on the subject.
Cropping was nevertheless removed: the properties the queries here turn on —
where a road user is, which way it went, whether two of them interacted — are
low-frequency and survive downscaling intact, so the crop bought resolution
nothing needed while deciding what was in frame at all. That second effect is
the one that matters, and it cuts the wrong way: the approach legs, where
deceleration is the evidence for "did it yield", are the first thing a tight
crop loses. Measured basis:
the 2026-08-27 measurement, evidence in `notes/figures/`.

---

## 6. The probe

One script, `scripts/vlm_probe.py`, in two modes over the same frames.

### Query mode — the experiment

```bash
python scripts/vlm_probe.py videos/<clip>.mp4 \
    --queries queries/events-paired.txt --fps 0.5
```

Queries live in `queries/*.txt`, one per line as `axis | situation`:

```
relational | a vehicle that entered the intersection and had to stop partway
             because someone was crossing in front of it
negative   | a fire truck with flashing lights driving through the intersection
```

The axis tags which capability a failure should be attributed to and is broken
out in the run summary, so a wrong answer points at a mechanism instead of at
"it did not work".

Asking a model to find "a fire truck" tests object recognition. A detector
already does that, and the answer says nothing about grounding. The question
worth asking is whether a model can locate a **situation** — several actors,
over several seconds, with an outcome — for which no detector has a class.
That is the only capability a VLM plausibly adds here.

**Start with the negative controls.** Axis `negative` marks situations that did
not occur. They score with **no annotation at all**: the answer is already
known to be "absent", so every hit is a fabrication and every miss is correct
restraint. That makes the first real measurement available on day one, before
any labelling, and it is the measurement that matters most — a probe that never
answers "absent" cannot be trusted when it answers "present".

The remaining axes have unknown ground truth until a clip is labelled. Run them
anyway: the answers say where to look, and the frames written under `runs/`
let a claim be checked by eye in a couple of minutes.

Three fields in `QueryResult` exist to make failure visible rather than to
carry information:

- `match_quality` separates `exact` from `superficial`. A situation query can
  be answered by matching surface features — "a van and a pedestrian are both
  present" is not "the van stopped for the pedestrian". Fluent prose hides that
  difference; this field does not.
- `considered_and_rejected` shows whether the model discriminated. If the scene
  contains near-misses of the query and this comes back empty, the match was
  luck rather than reasoning.
- `why_not_found` separates "did not happen" from "happened but was not
  legible" — different results that a bare negative conflates.

**No sliding window by default.** A clip is three minutes; at 0.5 fps that is
90 frames, which fits in context as one call. Asking *where in the clip* a
situation occurs is a stronger test of temporal localisation than asking
whether it is present in each eight-second slice, and it costs less — sliding
windows re-send their overlap. `--window N` opts back into splitting, which
makes haystack size an ablation variable: how does localisation degrade as the
searched span grows?

Frames are decoded once and reused across every query in a batch.

**One run, one directory.** Every invocation writes
`results/<YYYYmmdd-HHMMSS>-<label>/` holding `summary.md` (what was asked and
what came back), `results.jsonl` (one row per call, written as each answer
arrives), `run.json` (every parameter, machine-readable) and a `frames`
symlink to the images that were actually sent, under `runs/<same name>/`.

`<label>` is `--name`, or `<query set>-fps<fps>` when that is not given, so an
ablation loop over one flag separates its own arms as long as `--name` carries
the condition. The timestamp is what stops a re-run of the same command from
appending to the previous run's rows — a comparison between two conditions is
worthless if it cannot be told which rows came from which.
`run.json` exists for the same reason: ablations are read across runs, and
grepping a dozen markdown headers is not a comparison.

### Open mode — no hint

```bash
python scripts/vlm_probe.py data/clip.mp4 --start 40 --end 100
```

Same frames, nothing named. Measures what the model surfaces unprompted, and
reports the two diagnostics that test the state-axis prediction in section 2:
how many windows had no legible signal face, and how many reported events rest
on a signal state that was not read directly.

Two provisions in the prompts are load-bearing and should not be edited away:
inferring signal colour from traffic behaviour is forbidden, and an empty
result is stated to be a correct answer. Without the second, a model asked to
find violations will produce them.

### Before spending a run

```bash
# whole recording as one grid -- what the camera covers, at a glance
python scripts/vlm_probe.py data/clip.mp4 --overview runs/overview.jpg

# render what the model would receive, no API call, no key needed
python scripts/vlm_probe.py data/clip.mp4 --start 40 --end 100 --dry-run
```

Open the frames. If you cannot resolve the situation yourself, the model
cannot either, and the run is wasted. Frames are written on every run, not
only dry ones — when a probe misses something the first question is whether
the evidence was legible at all.

Default backend is `gemini-3.1-pro-preview` at `media_resolution_high`
(1120 tokens per image — the tier matters when the subject is a few pixels);
`--backend claude` runs `claude-opus-5`. Both go through one
`run(system, images, text, schema)` entry point and share the prompts in
`utils/vlm.py`, so the comparison is like for like.

## 7. Repository layout

```
traffic_video/
|- data/          # source video, frames, exports (gitignored)
|- runs/          # rendered windows and grids, one dir per run (gitignored)
|- results/       # one dir per run: summary.md, results.jsonl, run.json
|- utils/         # library code only -- importable, no side effects on import
|   |- video.py       # PTS-based extraction, container probing, windowing
|   |- render.py      # timestamp stamping, downscaling, overview grids, base64
|   |- schema.py      # pydantic schemas for every model-facing task
|   |- vlm.py         # shared prompts (open + query) + backend factory
|   |- backend_gemini.py   # gemini-3.1-pro-preview, Interactions API
|   |- backend_claude.py   # claude-opus-5, Messages API
|   |- env.py         # .env loading, key checks
|- queries/       # query sets, one situation per line, tagged by axis
|- scripts/       # runnable entry points -- argument parsing, orchestration
|   |- clean_data.py   # integrity check + removal of unusable video files
|   |- vlm_probe.py   # the probe: query mode and open mode
|- tests/
|   |- test_pipeline.py   # synthesises a clip with PyAV; no footage or key needed
|- requirements.txt
```

**Convention:** `utils/` holds library code only — no argument parsing, no
progress output, no side effects at import. Anything runnable goes in
`scripts/`; tests in `tests/`.

Backends expose a generic `run(system, images, text, schema)`; task-specific
callers build on it, so adding a probe does not mean touching provider details.

## 8. Setup

```bash
conda create -p ~/envs/traffic --override-channels -c conda-forge python=3.11 -y
conda activate ~/envs/traffic
pip install -r requirements.txt

cp .env.example .env        # then fill in the key for the backend you use
python tests/test_pipeline.py
```

`--override-channels -c conda-forge` is required, not stylistic: without it
conda resolves against `repo.anaconda.com`, which refuses to proceed until its
Terms of Service are accepted and carries licensing conditions for institutional
users. That flag cannot be expressed in an `environment.yml` `channels:` list
alone, which is why there isn't one — `requirements.txt` is the single
dependency list and those three lines are all conda contributes.

Python is pinned to 3.11 for the Phase 3 stack's sake (torch, ultralytics and
fiftyone lag new CPython releases). Everything in `requirements.txt` also
resolves on 3.14, so the pin is about what comes later.

Keys are read from `<repo root>/.env` by `utils/env.py`, which entry points call
explicitly. Shell variables take precedence over the file. `.env` is gitignored.

## 9. Open questions

0. **The legibility boundary — TODO, and the one that gates the rest.** At what
   apparent object size, in pixels of the native 3840x2160 frame, does an
   attribute stop being recoverable at all? Every design decision below is
   currently a guess about this number: which resolution tier, which queries
   are even askable. Measure it on **one clip** —
   instances of one class at near, mid and far depth, boxes measured rather
   than assumed, and the *human* boundary established first at native
   resolution, since §6's rule ("if you cannot resolve the situation yourself,
   the model cannot either") makes that the ceiling. Once it is a number in
   pixels it stops being a property of the payload and becomes a property of a
   target, and every configuration becomes derivable instead of ablated.
   The one method that avoids hand-labelling: a **generator** shown a tight
   native-resolution crop of one instance produces the question, its answer and
   its time; the **answerer** gets the ordinary downscaled payload; the boundary
   is where the two stop agreeing. The generator must never see the downscaled
   view, or it will only ask questions that survive it.

   **Partly answered, 2026-08-27**, for the signal-state target: the ceiling is
   established, and the boundary turned out not to be a size at all. Colour
   survives every downscale because it is low-frequency; shape survives
   none of them. So the useful axis for this attribute is *what kind of
   evidence* an answer rests on, not how many pixels the target spans — which
   is a better-transferring result than the threshold that was being looked
   for, but it means the thresholds for the other attribute types (whole small
   road users, attached objects, lit parts) are still unmeasured. The model
   half of the measurement has not been run at all.
1. **Signal-face visibility per approach per view** — **answered for 12F-Ams**
   (§5, measured 2026-08-27): no vehicle head
   legible, both pedestrian heads legible, in all five clips including night
   and the lowest-bitrate one. Still open for the other three views, and the
   head inventory was made by eye — an automatic sweep found only the
   intersection's roadworks.
2. **Track IDs in `labels/all_raw`** — CVAT interpolated annotations usually
   carry them; determines whether Phase 3 association is trivial or a multi-day
   task.
3. **Timestamp alignment between the 1 fps frames and the raw recordings** (§5).
4. **Which axes to probe first.** Referential and relational are where a VLM
   plausibly contributes. State was expected to fail for information reasons
   and no longer is, on the pedestrian phase — it is now the *cheapest* axis to
   score, because §2's measurement supplies ground truth for it with no
   labelling and no model. Spending effort proportional to expectation is still
   a choice worth making deliberately; the expectation has changed.
