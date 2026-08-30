# The same question, the same frames, five different answers

Three runs on one clip, at three sampling rates. The finding is not about any
category: **at n=1 this probe's verdict is close to a coin flip on most of the
label set, and raising the frame rate does not fix it.**

| run | fps | frames | sampling | tokens in |
|---|---|---|---|---|
| `scene_..._fps0.5_x2_0829-2148` | 0.5 | 91 | 2 whole-run repeats, one call per query | 4.06M |
| `events-key_..._fps1_n5_batch_0830-0549` | 1 | 181 | 5 samples per query, all queries in one call | 1.01M |
| `events-key_0825-1700_fps2_n5_batch_0830-0813` | 2 | 361 | same, at 2 fps | 2.00M |

Clip `2026-08-25 17:00`, `queries/events-key.txt` (10 categories),
`gemini-3.1-pro-preview`, resolution high, thinking high, timestamps
`interleave`.

## 1. Most categories have no stable answer

Five independent answers to each query, same frames, same prompt:

```
                 1 fps            2 fps
turn-fty         nYYYY  4/5       nYnnY  2/5
right-hook       nnYYn  2/5       nnnnn  0/5
stop-crosswalk   nYnnY  2/5       nnnYn  1/5
pickup-car       nnnYn  1/5       nnnYn  1/5
ped-conflict     YYYYY  5/5       YYYYY  5/5
bike-sidewalk    Ynnnn  1/5       nnnnn  0/5
bike-wrongway    nnnYY  2/5       nYnnn  1/5
emergency        YnYnY  3/5       nYnYY  3/5
negative x2      nnnnn  0/5       nnnnn  0/5
```

At 1 fps, seven of nine axes disagree with themselves. Four sit at 2/5 or 3/5,
which is not a weak signal — it is no signal.

Two things are stable in both runs, and they are the two ends of the range:

- `ped-conflict` at 5/5. It is also the most frequent situation in the clip —
  pedestrians and vehicles share a crosswalk many times in three minutes, so
  almost any window supports it.
- both negative controls at 0/5. **No fabrication in ten opportunities.** The
  instability is not the model inventing things; it is the model failing to
  commit.

## 2. Raising the frame rate makes it answer "no" more, not "yes" better

Matches returned per sample:

```
1 fps:  3, 3, 4, 8, 5    mean 4.6
2 fps:  2, 4, 1, 4, 3    mean 2.8
```

Doubling the frames cut reported events by 40%. Per category, five went down,
three stayed level, **none went up** — a sign test on the five non-ties gives
p = 0.031, which is small-sample but points one way only.

So the two categories that "became stable" at 2 fps (`right-hook`, 2/5 → 0/5;
`bike-sidewalk`, 1/5 → 0/5) did not become better judged. They collapsed onto
"absent". Counting split categories (7 → 5) as an improvement would be reading
the wrong number.

The direction is the opposite of what more evidence should buy, and points at
attention rather than evidence: at 361 images an event occupies a smaller share
of the payload than at 181, and gets passed over.

## 3. Correction to the previous report

`results/scene_.../report.md` §2 attributed the instability to 0.5 fps being
too coarse — a third of reported events last <= 4 s and so spanned 1-2 frames.
That explanation is now dead. Going 0.5 → 1 → 2 fps did not reduce the
disagreement, and the hit rate moved monotonically the wrong way. The duration
argument was sound about the sampling floor and wrong about the cause.

## 4. What is still confounded

The 0.5 fps run asked each query in its own call; both later runs put all ten
in one call. Two facts point at that mattering:

- match totals swing as a block (`3,3,4,8,5`) — sample 4 returned 8 matches
  where sample 1 returned 3. Ten independent calls cannot swing together like
  that; ten queries inside one call can.
- the per-sample totals are the natural unit of that swing, not any category.

So "the model is unstable" and "batching makes it unstable" are not yet
separated. The arm that separates them is one run of `--fps 1 --samples 5`
without `--batch-queries`: same everything, ten calls per sample instead of
one. It costs 10M tokens because the frames are re-sent per query, which is
exactly the saving that batching bought.

## 5. What this means for annotation

A single answer from this probe cannot be used as a label. That is not a
statement about accuracy — accuracy has not been measured, because the ground
truth sheet is unfilled — it is a statement about repeatability, which is
cheaper to measure and comes first.

Two usable consequences:

- **Report n/5, not present/absent.** A category at 5/5 and one at 2/5 are
  different kinds of claim and should not both be called a detection.
- **The negative controls hold.** Whatever is wrong here, it is not
  hallucination; ten chances to invent a collision or a horse-drawn carriage,
  taken zero times.

Both are visible without any labelling, which is why they came first.
