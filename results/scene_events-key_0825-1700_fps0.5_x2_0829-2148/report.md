# Does supplying scene facts change what the probe finds?

**Answer: cannot tell. Run-to-run variance is larger than any difference
between the arms.** The experiment measured its own noise floor instead, which
is worth having — every earlier comparison in this repo was made at n=1.

- clip `2026-08-25 17:00`, 180 s, **0.5 fps → 91 frames**, whole clip in one call
- `queries/events-key.txt`, 10 categories
- `gemini-3.1-pro-preview`, resolution high, thinking high, timestamps `interleave`
- 2 arms x 2 repeats = 4 runs, **4.06M in / 95k out tokens**
- arms: `no-scene` (nothing supplied) vs `with-scene` (`scene/12F-Ams.built.md`
  in the system prompt — street directions in image space, occlusions, which
  signal heads are legible)

## 1. The arms are not separable at n=2

Two queries flipped between arms. Both also flipped **inside** an arm:

| query | no-scene | with-scene |
|---|---|---|
| `stop-crosswalk` | absent / present | present / absent |
| `pickup-car` | absent / present | present / present |

`stop-crosswalk` disagrees with itself in both arms. A difference between arms
cannot be read off a comparison whose within-arm variance is the same size.

The other 8 queries agreed everywhere, including both negative controls
(absent in all 4 runs) and `bike-sidewalk` (absent in all 4).

## 2. The unstable queries are the short ones

Median duration of the intervals the model itself reported:

| category | median | frames at 0.5 fps | stable across runs |
|---|---|---|---|
| `stop-crosswalk` | 4.0 s | **2** | no |
| `emergency` | 4.0 s | **2** | no |
| `ped-conflict` | 6.0 s | 3 | yes |
| `turn-fty` | 6.0 s | 3 | yes |
| `right-hook` | 6.0 s | 3 | yes |
| `pickup-car` | 8.0 s | 4 | no |
| `bike-wrongway` | 12.0 s | 6 | yes |

32% of reported events last <= 4 s, so at 2 s spacing they are 1-2 frames.
The two least stable categories are the two shortest. That is consistent with
sampling, not with the model: an event that falls between frames is not
"missed", it is absent from the payload.

**0.5 fps is below what this category set needs.** Three to four frames inside
an event is the minimum for placing its start and end, which puts the floor at
1 fps and comfortable at 2 fps. This is the confound to remove before the scene
question is asked again.

(The durations are the model's own claims, not ground truth. They bound the
scale of the events being looked for, which is all they are used for here.)

## 3. The with-scene arm repeats what it was told

Phrases lifted from the supplied block, counted in the model's own prose:

| arm | uses | which |
|---|---|---|
| `no-scene` | 2 | left to right x1, right to left x1 |
| `with-scene` | **9** | right to left x5, left to right x3, up the frame x1 |

4.5x more. The count alone cannot separate "used the fact" from "echoed the
sentence" — supplying vocabulary should raise its use even when the model is
looking properly. What settles it is whether a direction claim is *correct*,
and that needs the one thing the answers omit: `bike-wrongway` matched in every
run, always described as travelling "toward the top right", never saying which
side of the double yellow the rider was on. Both sides of that line exist and
carry opposite directions
(`measurements/flow-direction.json`), so the claim is unadjudicable as written
whether or not the model was given the map.

## 4. What this changes

1. **Raise fps before re-running this.** At 0.5 fps a third of the target
   events are 1-2 frames, and the noise that creates is larger than the effect
   being looked for.
2. **n=1 is not evidence.** Two of ten queries were unstable across identical
   runs. Every claim in this repo made from a single run should be read with
   that in mind.
3. **Ask the model which side of the line.** A wrong-way answer without it
   cannot be scored, so `bike-wrongway` needs re-wording rather than re-running.
4. **Sampling now happens per query** (`--samples N`), not by repeating the
   whole run: same information, one decode. Combined with `--batch-queries`,
   which sends the frames once for all ten queries instead of once each, five
   samples cost about what this two-repeat experiment did.
