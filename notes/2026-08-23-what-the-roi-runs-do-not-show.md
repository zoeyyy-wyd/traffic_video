# What the ROI runs do not show, and what to run instead

Read of the state of the repo on 2026-08-23, after
[`2026-08-20-direction-vs-roi.md`](2026-08-20-direction-vs-roi.md). Nothing new
was run for this; it is an audit of the existing runs, the query sets and the
instrument, and an ordered list of what to do next.

---

## 0. TODO, and the gate on everything below

**Establish the legibility boundary on one clip, before running any further
ablation.** Not "does cropping help" — *at what apparent object size does an
answer stop being recoverable at all*, expressed in pixels of the native
3840x2160 frame.

Everything in sections 1-4 is currently guessing at this number. The ROI
presets are guesses about it (`none` puts 0.41x the pixels on a target that
`junction` does; whether that crosses the boundary is unknown). The size bands
in `queries/resolution-limited.txt` are guesses about it. The prediction in
README section 2 that the state axis fails for want of pixels is a guess about
it, and F6 already suggests the guess was wrong.

### Why it has to come first

Once the boundary is a number in pixels, it stops being a property of a crop
and becomes a property of a *target*, and then every configuration is
**derivable rather than ablated**: compute how many pixels a given ROI and
resolution tier put on a given object, compare against the boundary, and you
have a prediction. An ablation table gives you three data points; a boundary
gives you the function. That is also the difference README section 3 draws
between a number and a finding.

It also decides which questions are askable at all. A query whose evidence sits
below the boundary everywhere is not a failed grounding test — it is a question
with no answer in the data, and scoring it as a model failure is a category
error.

### Why one clip is enough

The boundary is a property of the camera geometry and the encode, not of the
traffic. One clip, one frame, is enough to locate it; further clips test
whether it moves (night, a different bitrate, a different date).

### Method

Model-free first. The whole first half needs no API calls.

1. One frame, native 3840x2160, from one clip.
2. Pick instances spanning the depth range — the same class near the camera,
   mid-intersection, and across the junction. **Signal heads are the ideal
   target**: fixed, present in every frame, and both a near and a far instance
   are already captured in `notes/figures/signal-head-{near,far}.jpg`. Add
   pedestrians, riders and vehicles for a second and third class.
3. **Measure each instance's box in native pixels.** By hand for a first pass;
   from the COSMOS YOLO annotations once `data/` is back, which gives it for
   free across 14 classes and removes the hand measurement entirely.
4. **Establish the ceiling first.** For each instance, can the attribute be
   resolved at native resolution at all? README section 6 already states the
   rule — "if you cannot resolve the situation yourself, the model cannot
   either" — so this is the ceiling. A failure below it is not a finding; a
   failure *above* it is. The next subsection is how to get this without
   hand-labelling.
5. Only then the probe, at each ROI, and find the size at which the answer
   flips.

### Generating the questions instead of writing them

The task is deliberately simple — does this situation occur, and when — so the
questions can be produced by a model rather than by hand. What makes that sound
rather than circular is one asymmetry:

**the generator must see more than the answerer.**

- The **generator** is shown a tight, native-resolution crop of one instance,
  and returns a question, its answer, and the time it holds. At 1.00x on a
  single object the evidence is as unambiguous as it gets in this footage, and
  the instance's box — hence its pixel size — is known because the crop defines
  it.
- The **answerer** is shown the ordinary probe payload: the whole ROI, at
  whatever resolution the condition specifies, with the object at 0.41x or
  0.73x among everything else.
- The **boundary** is where the two stop agreeing, plotted against the measured
  pixel size. Fully automatic, and it is exactly step 4-5 above with the
  hand-labelling removed.

Three properties this has to carry to be worth anything:

1. **It measures a boundary relative to the ceiling condition, not to truth.**
   Say so wherever the number is quoted. Validate it by hand-checking a sample
   of generated items — the hand-written set in
   `queries/resolution-limited.txt` exists for exactly this, as the control the
   generator is scored against before it is trusted.
2. **Negative controls come free, and stop being clip-specific.** A question
   generated from window A, asked about window B, is a negative by
   construction. That removes the defect in `starter.txt` — that its negatives
   were verified on one clip and silently assumed everywhere else — and gives
   an unlimited supply of them.
3. **Never show the generator the low-resolution view.** It would only ask
   questions that survive it, and the boundary would collapse to nothing.

### Score localisation, not just presence

Every answer already carries `t_start_sec`, `t_end_sec` and
`clearest_frame_sec`, and no run so far has checked any of them. README's
Phase 2 section already makes the point about the timestamp-encoding ablation:
*"the measure is not whether an event is found but whether the returned
t_start_sec / clearest_frame_sec land on the right frame, which is checkable
against the jpgs in `runs/` without a human labelling anything."*

With generated questions the generator supplies the true time, so temporal
localisation error is free on every item — a second score per call, at no extra
cost, and the one that makes this a grounding measurement rather than a
recognition one. Presence alone is the weaker half: a model can be right that
something happened and wrong about when by twenty seconds, and the current
summary records that as a hit.

Spatial IoU is the rung after, and it is a bigger change: the schema returns no
box, so it needs the Set-of-Mark path README's Phase 2 describes — numbered
tiles, the model names an index, out-of-range indices are dropped. Not now.
Present/absent plus time is the right first rung precisely because it needs
neither boxes nor annotation.

### What it outputs

A threshold in native pixels per attribute type, roughly:

    signal lens colour        readable above ~N px of head width
    rider vehicle type        above ~M px
    presence of a stroller    above ~K px

with N, M, K measured rather than assumed, and with the human ceiling recorded
next to each. Express it in **apparent object size, never in ROI names** — that
is what makes it transfer to a different crop, a different resolution tier, and
a different camera.

### Consequences to expect

- Some of `queries/starter.txt` will turn out to be unanswerable in principle
  on this camera. That is a result, and a better one than a low score.
- The hand-written query sets stop being the instrument. `starter.txt` becomes
  the historical baseline that runs 2 and 3 are comparable to,
  `resolution-limited.txt` becomes the generator's control, and
  `contradiction-pairs.txt` keeps its own job — it needs no truth at all, so it
  is orthogonal to whether the generator works.
- The ROI question (section 1) may become arithmetic rather than an experiment.
- The state-axis prediction in README section 2 gets settled either way.

---

## 1. The ROI experiment tests the right lever with the wrong targets

The intent of run 4 is clear and correct: ROI is the *treatment*. Crop to the
intersection, spend the model's fixed per-image budget on the subject instead
of on brick wall, and see whether queries that failed before now succeed.
Losing the approaches is not a confound in that question — it is the price the
treatment charges, and a result of the form "cropping helps, crop your frames"
would be a real, usable answer that needs no decomposition.

The problem is elsewhere. **Nothing in the query set is resolution-limited.**

| ROI | field of view | linear px across the junction box |
|---|---|---|
| `none` | 100% of the frame | 0.41x |
| `wide` (0.17,0.00,0.54,1.00) | 54% | 0.73x |
| `junction` (0.28,0.00,0.40,0.42) | 17% | 1.00x |

`queries/bus-direction.txt` asks three questions, all about an articulated bus.
An articulated bus is eighteen metres long and spans hundreds of pixels in the
native frame; at `none` it is still hundreds of pixels. It is legible in every
condition, so no amount of extra resolution can move it from "cannot see it" to
"can see it" — there is no unrecognised state to recover. Raising n would not
change that. The experiment varies a lever the queries are insensitive to.

The failures it did surface confirm this. F2 (heading inverted) and F3 (one bus
reported as two) are not "the object was too small to see" — the model located
the bus accurately against the double yellow line every time. They are
cross-frame association failures, and pixels-per-frame is not the lever on
those; sampling rate is.

**The observed ordering says so too.** If resolution were driving the result,
the ranking should follow the pixel column: `junction` > `wide` > `none`. What
came back was `junction` 3/3, `none` 1/3, `wide` 0/3 — `wide` worse than
`none` despite carrying nearly twice the pixels on the subject. At n=1 that is
most likely noise, but it is not the shape the resolution hypothesis predicts.

### What the experiment needs

**Queries whose targets sit at the legibility boundary.** The hypothesis is
about objects that are lost at 0.41x and recovered at 1.00x, so the targets have
to be in the size range where that happens — roughly 10-60 px in the native
frame. Signal lenses are ~20-30 px (F6). A cargo trike was ~50x30 px. A stroller,
a dog, an e-scooter versus a bicycle, a lit brake light, a taxi roof light, a
bus route number: all near that boundary, all in or adjacent to the annotation
ontology. `queries/resolution-limited.txt` is that set, ordered by approximate
native pixel size, with a large-object control at the top whose answer must not
change — if the bus flips, the run is noise.

Most of those are also checkable from a **single native frame**, so ground truth
costs minutes rather than the hour an exhaustive clip labelling costs.

**Score flips, not totals.** The claim is "previously unrecognised, now
recognised". That is a per-item paired comparison — same query, same moment,
different ROI — counted in both directions: how many items `none` got wrong and
`junction` got right, against how many went the other way. Comparing 3/3 with
1/3 throws that structure away and is far less sensitive to the effect being
looked for.

**Three repeats per cell.** Still true, and unchanged: every conclusion in the
2026-08-20 note rests on one sample.

### The separate question: is it resolution, or is it decluttering?

Worth stating because README section 3 makes it the point. The example finding
there is *"raising effective resolution via ROI cropping moves accuracy from A
to B, which locates the bottleneck in perception rather than reasoning"* — and
that sentence is a claim about the mechanism, not about whether cropping helps.
Cropping does two things at once: it adds pixels, and it deletes the brick wall
and the swaying canopy that README section 5 says "generate spurious motion
energy and detections". An improvement is consistent with either.

Separating them costs one extra arm, not a redesign: hold the crop fixed and
vary the visual budget alone. On Gemini that budget is `resolution`
(`low` / `medium` / `high` / `ultra_high`), a per-image token cap rather than a
pixel count, so it moves pixels-on-subject at *constant* field of view — the
one arm the ROI presets cannot produce. It is hard-coded to `high` in
`utils/backend_gemini.py` and not reachable from the command line;
`LONG_EDGE = 1568` in `utils/render.py` is fixed the same way, and `fit()` only
ever downscales.

| | `junction` | `wide` | `none` |
|---|---|---|---|
| resolution=`medium` | | | |
| resolution=`high` | | | |

Run the ROI row first — it is the question actually being asked. The second row
is what turns "cropping helps" into "cropping helps *because* of resolution",
and is only worth paying for if the first row shows an effect.

---

## 2. The query sets

**Only the negatives score.** Every positive in `starter.txt` has unknown ground
truth until a clip is hand-labelled, so runs 2 and 3 produced 78 matches that
nobody can mark right or wrong. The negatives produced the entire finding.

Two new sets address this from different directions.
`queries/resolution-limited.txt` (§1) buys cheap ground truth by choosing
targets settled from a single native frame rather than from the whole clip.
`queries/contradiction-pairs.txt` closes the gap a second way, for a subset. Each pair asks
for two properties one road user cannot hold at once — northbound and
southbound, left turn and right turn, stopped and never stopped. If a match on
one side overlaps in time with a match on the other, the run contradicted
itself, and that is checkable from `results.jsonl` alone with no labelling. It
targets F2 and F3 directly, because both are failures of cross-frame
association, and it carries a single-frame control pair and a verbatim-repeat
pair to separate a real contradiction from run-to-run variance.

**The referential axis is not testing what the README says it tests.** README
section 6 argues that asking a model to find "a fire truck" tests object
recognition and says nothing about grounding; section 2 defines the referential
failure mechanism as "confusion among same-class instances". But three of the
four referential queries in `starter.txt` are bare object queries — "a yellow
taxi", "an articulated city bus". The one that matters would name an instance
among several of its class: *the* taxi that turned right, not the one that went
straight. The result shows why — "a yellow taxi" returned four matches, and
scoring that needs a hand count of every taxi in the clip.

**The negative controls are clip-specific and the file did not say so.** Absence
was verified on the 2025-11-03 17:00 clip only. Run the same file against any
other clip and a fire truck really can drive past, at which point a correct
answer is scored as a fabrication. The header now says this.

**The three self-report fields are dead** (F4: all 78 matches came back
`exact` + `high`, and `unreadable_reasons` was empty in all 44 query results). They were the instrument for
separating a real match from a surface one, and they measure nothing as
implemented. The cheapest replacement is a field the model cannot fill without
committing to something falsifiable: the list of frame timestamps in which the
evidence is visible. That is checkable against the jpgs in `runs/<name>/` by
eye, unlike a self-assessed quality label.

---

## 3. Instrument problems that block the next run

1. **Token accounting returns zero on Gemini.** `_usage()` in
   `utils/backend_gemini.py` probes three attribute-name pairs on the
   Interactions response and finds none, so every summary says `0 in / 0 out`.
   A repeats-and-cells design is a few hundred calls; running it blind to cost
   is not sensible. Fix by dumping the response's usage object once and reading
   the real field names off it.
2. **`--resolution` and `--long-edge` are not exposed** (§1).
3. **No `--repeat N`.** Every ablation needs it, and every conclusion so far is
   n=1. Repeats are also the only way to know whether a contradiction pair
   caught a real inconsistency or sampling noise.
4. **`utils/env.py` had the gemini key list as a bare string** rather than a
   one-element tuple, so `require_key` iterated its characters, matched the
   shell's `$_`, and passed with no key set — the exact failure the function
   exists to prevent — while `key_status` printed `_=***…` into the run log
   instead of naming the key. Fixed 2026-08-23.
5. **The clip every finding rests on is not on disk.** There is no `data/`
   directory at all; the
   only footage present is `L12thFloorBotwinik-D-2026-08-17_T-17_30_02.mp4` in
   the repo root — 3840x2160, 180.1 s, 5404 frames, VFR, and a **different
   clip** with no ground truth. Nothing in the 2026-08-20 note can be
   reproduced or extended until the 2025-11-03 clip is back.
6. **That new clip is ~0.86 Mbit/s at 4K** (19.4 MB of payload for 180 s, ~3.6
   kB per frame). Before reusing the "signal lenses are resolvable at native
   resolution" finding (F6), check it on this clip specifically: at that
   bitrate a 20-30 px signal head can be destroyed by compression before any
   model downscaling happens, and legibility then varies clip to clip rather
   than being a property of the camera.

---

## 4. Order of work

**Section 0 comes before all of this.** The steps below are written as though
the boundary were known; until it is, most of them cannot be designed properly,
and steps 5-8 in particular may not be worth running in the form given.

1. Restore the 2025-11-03 clip, or accept that the baseline moves to the
   2026-08-17 clip and re-establish ground truth on it by eye.
2. **Section 0: measure the legibility boundary.** Steps 1-3 of its method need
   no API calls at all, so this can start immediately after step 1 above. Then
   the question generator, validated against `queries/resolution-limited.txt`
   before it is trusted, and the probe scored on both presence and time.
3. Fix token accounting. One call, and it gates knowing what anything costs.
4. Expose `--resolution`, `--long-edge`, `--repeat N`.
5. Run `contradiction-pairs.txt` x 3 repeats on one 36 s window, `--roi
   junction`, current settings. Cheap (36 calls), needs no annotation, and
   measures the variance that every existing single-sample comparison is
   missing. **Do this before the ROI run** — if the verbatim-repeat pair
   disagrees with itself, no ablation cell can be read either.
6. **Re-run the ROI ablation properly**: `resolution-limited.txt`, three ROIs,
   three repeats, one window chosen because the named objects are in it (135
   calls). Establish the truth for each item from native frames first, then
   count flips in both directions per §1. This is the experiment that was
   intended all along; only its targets and its n change.
7. Only if step 6 shows an effect, the second row of the §1 table
   (`resolution=medium` at fixed crop). That is what turns "cropping helps"
   into "cropping helps because of resolution", and it is not worth paying for
   until there is an effect to explain.
8. The fps arm the earlier note proposed (0.5 vs 2 fps). Independent of all the
   above and well motivated on its own — F2 and F3 are cross-frame association
   failures, and pixels-per-frame is not the lever on those, sampling rate is.
   It multiplies the frame count by four, so it wants working cost accounting.
9. The dedicated signal-head crop for the state axis. The `px-15` block of
   `resolution-limited.txt` is the cheap version of this and may settle it
   first; §3.6 (this clip's bitrate) has to be checked either way.
