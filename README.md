# traffic_video — can a VLM label traffic events well enough to be worth using?

An exploratory study, not a product. The question started as *where does a
vision-language model succeed and fail at grounding language to fixed-camera
intersection footage*, and narrowed under its own results into something with a
decision attached:

> **Can a VLM annotate traffic events accurately and repeatably enough to
> replace or bootstrap human labelling?**

The short answer so far is **no, and the reason is not the one you would guess**.
It does not invent events — negative controls hold — but it does invent
*state*: shown a police car with its lightbar dark, it reports the lights
flashing. Writing an event's boundaries into the query fixed the worst recall
failure (from one reported instance of eight to nearly all), yet roughly four
of five returned intervals still fail to land on the event they name.

Data is the COSMOS intersection footage: fixed multi-view cameras over
Amsterdam Ave at W 120 St, New York. Five 3-minute 4K clips from `12F-Ams`
(2026-08-25, at 09:00 / 13:30 / 17:00 / 17:30 / 22:00) are in `videos/`.

---

## 1. Results

Two experiments, both on the 17:00 clip against a hand-filled ground-truth
sheet (10 categories, 18 spans), run on `gemini-3.1-pro-preview` with interval
boundaries written into the three queries where the model and the sheet had
disagreed about where an event starts. Full per-answer tables with the IoU
each one earned: `experiment_results/<name>/result.md`.

| experiment | arm | presence | localised | mean IoU |
|---|---|---|---|---|
| **fps** | 1 fps (181 frames) | 36/50 (72%) | **13/55 (24%)** | 0.51 |
| | 2 fps (361 frames) | 32/50 (64%) | 7/32 (22%) | 0.58 |
| **scene** | no scene context | **41/50 (82%)** | 11/68 (16%) | 0.47 |
| | with scene context | 34/50 (68%) | 11/66 (17%) | 0.47 |

**`presence`** is whether the yes/no was right, per sample. **`localised`** is
how many of the returned intervals actually land on a real one at IoU ≥ 0.5.

**The `fps1` and `no-scene` arms are the same configuration run twice**, and
they differ by 5 answers on presence and 13 returned intervals. That spread is
the sampling noise at n=5; treat any smaller between-arm difference as nothing.

**Boundary definitions in the query text are what moved.** Three queries
carry an explicit boundary ("from stepping off the kerb until reaching the far
side") because the sheet and the model turned out to disagree about where an
event starts — both were marking what each considered the full extent.
Before the boundary was written in, `ped-midblock` (8 real spans) drew under
one interval per sample and zero localised hits, and no amount of
report-every-occurrence prompt wording changed that; with it, 6-7 intervals
per sample, of which 3-8 per run land at IoU ≥ 0.5. `turn-halt` intervals
narrowed from a 14 s median (approach included) to the 2 s of the halts
themselves. Two raters have to share an event's boundary before IoU measures
anything, and the model is a rater.

**Recall still fails wherever presence does.** `bus-dwell` has one clear
30-second instance; the model reports it in about one sample in five. Doubling
the frame rate lowered both headline numbers, and `ped-midblock`'s
localisation collapsed to zero at 2 fps.

**What works.** Negative controls held in every sample: no fabricated
collisions, no horse-drawn carriages. `roadworks` — visible for the whole
clip — stays at IoU 1.00, which is what a calibration item should do and is
not evidence of skill.

**The lights-flashing trap fails.** A police car crosses at 0:33 with its
lightbar dark — checked at 6 fps in native resolution, no lit strobe in any
of 11 consecutive frames. The model reports it as *flashing* in 3-5 samples
of 5 in every arm, while mostly missing the dark version that did occur: it
binds the object and invents the state. The car also appears in exactly one
frame at 1 fps, so at the default rate this pair rests on a single image.

## 2. What counts as a finding

**Not a finding:** "the model reaches 70% here." It does not survive a change of
clip and explains nothing.

**A finding:** a boundary with a mechanism, or a number that changes a decision.

- *"Vehicle signal state fails because the heads face away, not because they are
  small — they are the larger targets. The bottleneck is mounting geometry,
  which predicts that no crop or resolution tier recovers it."*
- *"Presence and localisation come apart, so a run that looks 70% correct
  returns usable intervals a fifth of the time."*

## 3. What the camera allows

Measured, not assumed. Method and the judgement calls in each: `measurements/`,
computed by `utils/measure.py`.

**Vehicle signal heads show only their backs.** Sampled every 6 s across a whole
clip they are pixel-for-pixel invariant. Vehicle phase is unavailable at any
resolution or model quality, so red-light running has no establishable truth
here and is not in the query set. Asking it would score the model wrong for a
question the data cannot answer.

**Pedestrian signal heads are legible.** The state is carried by an 8×10 patch of
the native frame at a 97-point `R − B` separation, and that separation survives
every downscale the probe applies — colour is low-frequency, glyph shape is not.
A phase timeline is therefore free, and three-state: the countdown flashes, and
a two-level threshold reports each dark flash as WALK.

**Traffic direction, in image space.** The vertical street is two-way, split by a
double yellow; lanes left of it run down the frame, right of it run up (r = 0.82
and 0.50, opposite signs — what right-hand driving must produce). The cross
street could not be recovered; the roadworks swamp the signal. It is recorded as
a failed measurement rather than a guess.

**Other constraints.** The east sidewalk is under a scaffolding shed, so nothing
there is observable. The intersection is under construction in all five clips.
The camera drifts between clips, so a fixed-box classifier needs re-locating per
clip. Timestamps come from container PTS, never from frame index.

## 4. The query set

`queries/events-key.txt` — one line per category, `name | description`. Eight
observable categories plus two negatives.

A query has to pass two tests.

**It must be precise enough that two people labelling the clip independently
would mark the same instances.** Most of the queries that were removed failed
here, not on difficulty. Examples that were actually tried:

| removed query | what was wrong with it |
|---|---|
| *a turning vehicle continuing through a crosswalk while a pedestrian is in it* | How near does the pedestrian have to be? In the vehicle's path, or anywhere on the paint? Two labellers answer differently, so it cannot be scored. |
| *a vehicle slowing down while making a turn* | Every vehicle slows into a turn. It scored 5/5 at every setting because it cannot be wrong, which means it measures nothing. Replaced by "stops, or almost stops". |
| *a vehicle stopped with part of its body on the crosswalk markings* | Nearly every car waiting at the line clips the paint. Frequent, and says nothing about what happened. |
| *a cyclist riding along the sidewalk in the direction it runs* | The qualifier was meant to exclude riders briefly crossing the kerb, but judging "in the direction it runs" is harder than the original question. |
| *a vehicle that has driven up onto the sidewalk* (negative) | Vehicles legally cross the sidewalk at kerb cuts, so a correct report would have been scored as a fabrication. |

**It should take more than an object detector to answer.** "A yellow taxi" is
detection, and COSMOS already ships boxes for 14 classes; a query only earns
its place if the answer needs some behaviour over time — stopping part-way
through a turn, a person getting out of a car, a bus dwelling at the kerb.
`skateboard` is the weakest line by this test, close to pure detection; it is
kept because skateboards are rare here, so it mostly measures whether the
model invents one.

Scoring added a third test: **a query that can match a span must say where the
event begins and ends** — "from stepping off the kerb until reaching the far
side". Without it, sheet and model each mark their own idea of the full
extent, and IoU measures that disagreement instead of localisation
(section 1).

The current set is not fully clean either. `ped-midblock` — "crossing the
roadway away from the crosswalk markings" — still leaves *away* to judgement:
someone stepping off a metre outside the paint is a coin flip between
labellers. Expect it to be tightened after the next labelling pass.

Two categories are instruments rather than targets: `roadworks` is visible for
the entire clip, so a wrong answer there means something upstream of the query
is broken; and `emergency` / `emergency-dark` are a pair about one vehicle — a
police car does pass, its lights are off, and exactly one of the two lines is
true of it. A model that answers "present" to both is matching the vehicle
without reading its state, which is a failure the totals would otherwise hide.

Vehicle-signal categories (red-light running, right turn on red) are absent
deliberately: no vehicle signal face is legible from this camera (section 3),
so they have no establishable truth here, and scoring the model on them would
be a category error rather than a measurement.

## 5. Running an experiment

```bash
./experiment_fps.sh                 # fps 1 and 2, no scene context, then score
./experiment_scene.sh               # no-scene vs with-scene at one rate
./experiment_scene.sh --rebuild     # re-measure the camera and rebuild the block first
./experiment_fps.sh --dry-run       # render frames, make no API calls
```

Each writes its arms into `experiment_results/<name>/arms/<arm>/` and scores
them. Re-running moves an existing arm aside rather than overwriting it, and the
probe refuses outright to append to a directory that already holds answers — a
comparison is worthless if it cannot be told which rows came from which run.

Or the probe directly:

```bash
python scripts/vlm_probe.py videos/<clip>.mp4 \
    --queries queries/events-key.txt --fps 1 --batch-queries --samples 5
```

| flag | why it exists |
|---|---|
| `--samples N` | N independent answers per query. At n=1 an answer cannot be told from a coin flip. Costs N×: the images are re-sent every call — `candidate_count` returns one output and chaining interactions re-bills the images, both tested. |
| `--batch-queries` | All queries in one call, so frames are sent once instead of once per query: 181 images instead of 1810. The cost is that the queries stop being independent. |
| `--scene FILE` | Supply measured camera facts in the system prompt. An ablation arm, never a default — supplied context can be echoed back as observation. |
| `--dry-run` | Render what would be sent, no API call. **If you cannot resolve the situation yourself in those frames, the model cannot either.** |

**Quota is the binding constraint, not cost.** The model is
`gemini-3.1-pro-preview`. Two failure modes look identical (both 429) and need
different responses: a rate-limit window passes on its own and the built-in
backoff rides it out, while depleted prepaid credits fail every retry until
the account is topped up — read the error body. Image requests draw on a
different quota from text, so a text probe tells you nothing about whether an
experiment can run: a key can refuse a single image while answering text
prompts without complaint.

## 6. Scoring

```bash
python scripts/score.py <arm-dir> ground-truth/<clip>.txt
python scripts/report.py experiment_results/fps ground-truth/<clip>.txt
```

`score.py` prints one arm's table; `report.py` writes the whole experiment's
`result.md`, including **every answer with the IoU it earned**. Scores are
computed from `results.jsonl` rather than stored, so changing the scoring
applies to every past run without re-querying anything.

Matching is one-to-one: without it a single interval covering the whole clip
would "hit" every span in the sheet at once, which is the opposite of
localisation. Three zeros are kept apart because they are different failures —
`no overlap` (intervals returned, none landed), `no answer` (nothing returned),
and `—` (a negative, where localisation does not apply).

How far IoU can be read is capped from both ends: the sheet's boundaries were
judged by eye to about a second, and the model can only place an edge on a
sampled frame. On a 6 s event that puts a correct answer near 0.8, not 1.0.

### The ground-truth sheet

```bash
python scripts/make_gt.py queries/events-key.txt videos/<clip>.mp4
```

Writes a blank sheet whose categories are the query file copied verbatim, so
scoring is a line-by-line comparison rather than a translation. It **refuses to
overwrite a sheet that already has entries** — that is hours of work and exists
nowhere else. When the vocabulary changes after labelling has started, the
sheet is edited in place around the existing entries, never regenerated; the
17:00 sheet went through several such edits, and the scorer parses loosely
enough (stray fields, seconds or MM:SS) to read it.

Fill it **blind**: ground truth read after seeing the model's answer is not
independent of it. Three states, not two — `yes`, `no`, `not-reviewed`. Only a
swept `no` turns a model hit into a fabrication, and a wrongly-ticked `no`
corrupts the score, which is worse than not scoring.

## 7. Scene context

```bash
python scripts/build_scene.py scene/12F-Ams.txt --video videos/<clip>.mp4
```

Measures the camera, folds the facts in with hand-written notes, has a model
tidy the result, and writes `scene/12F-Ams.built.md` for `--scene`.

The measurement runs inside the pipeline that consumes it, so there is no
intermediate file of "truth" to keep in step. **These measurements are inputs,
not judges** — reproducible is not the same as authoritative, and the only thing
that scores a run is the hand-filled sheet.

The tidying step is constrained to **add nothing**: it prints every word in the
rewrite that was not in the source, and refuses to write if the result grew more
than 40%. A detail invented while tidying becomes a confident wrong label on
every run afterwards.

Camera-constant facts only. A phase timeline belongs to one recording, and
putting it in a block reused across five would hand the model a confident
falsehood about four of them.

## 8. Repository layout

```
traffic_video/
|- videos/            source clips
|- queries/           events-key.txt -- the label vocabulary
|- ground-truth/      the hand-filled sheets runs are scored against
|- measurements/      camera facts, each with its method and its judgement calls
|- scene/             hand notes, and the built block --scene sends
|- experiment_results/
|   |- <name>/result.md      configuration, totals, and every answer's IoU
|   |- <name>/arms/<arm>/    summary.md, results.jsonl, run.json
|- runs/              the frames a run actually sent
|- experiment_*.sh    one per experiment: runs its arms and reports
|- scripts/
|   |- vlm_probe.py       the probe
|   |- score.py           one arm against the ground-truth sheet
|   |- report.py          a whole experiment into result.md
|   |- make_gt.py         blank ground-truth sheet from a query set
|   |- measure.py         camera measurements -> measurements/
|   |- build_scene.py     measure + notes -> the scene block
|   |- measure_signal_vlm.py  read the signal by asking a VLM, to compare
|   |                         against reading it arithmetically
|   |- clean_data.py      integrity check over a footage directory
|- utils/             library code only: no argument parsing, no import side effects
|- tests/test_pipeline.py  synthesises a clip with PyAV; no footage or key needed
```

**Naming.** A directory called `20260829-214844-scene` says when it ran and
nothing about what it was. Experiments are named for the question they ask;
arms are named for the condition.

**Scratch does not go in the repo.** Intermediate renders made while checking a
claim are working material, not output.

**A superseded run is deleted, not kept.** Its findings, if they survived
verification, belong in `measurements/` or a note. Keeping the directory keeps a
result nobody has checked.

## 9. Setup

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
users.

Keys come from `<repo root>/.env` via `utils/env.py`, which entry points call
explicitly. Shell variables win over the file. `.env` is gitignored.
`--backend claude` runs `claude-opus-5` through the same
`run(system, images, text, schema)` entry point and the same prompts, so the
comparison is like for like; it needs `ANTHROPIC_API_KEY`.
