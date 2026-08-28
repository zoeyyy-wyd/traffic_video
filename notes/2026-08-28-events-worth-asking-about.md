# Events worth asking about, and what each one is for

A catalogue of intersection events, sorted by the question that decides what a
result on one *means*:

> Given a detector, a tracker, hand-drawn scene polygons (crosswalks, stop
> lines, lane directions, the junction box) and a signal phase timeline —
> could a rule answer it?

The answer does **not** decide whether to ask it. It decides two other things,
and they pull in opposite directions:

- **"Yes, a rule could" means the event is scorable.** Build the rule once and
  every clip gets objective ground truth, for presence *and* for timing, at no
  labelling cost. That is the scarcest thing in this repo: of the 78 matches
  the first runs produced, not one could be marked right or wrong, and the
  entire finding rested on five negative controls. A rule is not the model's
  competitor here, it is the scorer — README §3's "geometry as an instrument",
  which exists to turn "the model's account seems off" into "the model said
  1.5 s, the measured value is 3.2 s".
- **"Yes, a rule could" also means a correct answer proves little.** The model
  getting "a vehicle is stopped on the crosswalk" right says nothing about
  whether it can tell yielding from queueing. So these events establish a floor
  and a scoring instrument, not the capability claim.

And the counterfactual cuts the other way too: **none of that infrastructure
exists yet.** There is no homography, no polygon set, no tracker, no
calibration — Phase 3 is unwritten. A model that answers these zero-shot,
without any of it, is itself a result, because it means the stack can be
skipped.

So the split below is by **role**, not by permission:

| role | what it is for |
|---|---|
| **floor** (§1) | scorable on presence and timing; establishes whether the easy end works at all, and supplies the measuring stick |
| **discriminating** (§2) | where the research question lives; needs paired queries to be interpretable |
| **unaskable** (§0) | no establishable ground truth on this camera — the only genuine exclusion |

**Nothing here is verified to occur in these clips.** This is the menu to check
against during a clip review, not a set of claims. Ground truth per event comes
from that review, or from the rule where one can be built.

---

## 0. What this site allows and forbids

Established by measurement on 2026-08-27, model-free, from the pixels
themselves. The write-up has since been removed; the surviving evidence is the
figures in `notes/figures/2026-08-27-*.png`, and the method is restated in §0.1
so the claims below are not left unsupported.

| | status |
|---|---|
| pedestrian signal phase | **available free**, model-free, per clip |
| vehicle signal phase | **not readable** from this camera at any resolution |
| east sidewalk | **hidden** by a scaffolding shed — nothing there is observable |
| the intersection | **under construction** in these clips: cones, barriers, plated excavation, workers in the roadway |
| all four approaches, both crosswalks, the junction box | visible |

Two consequences that decide what can be written:

- **Any event whose truth depends on the vehicle signal cannot be scored here,
  and that is the one real exclusion in this document.** Red-light running,
  stopping on yellow, right-turn-on-red: nothing establishes what the light was,
  so a model answer can be neither confirmed nor refuted. It is not that the
  question is uninteresting — it is that it has no answer in this data, and
  scoring it as a model failure would be a category error. The vehicle phase may
  yet be recoverable by *coupling* — inferring it from the pedestrian phase,
  which shares a controller — in which case this block opens up. That coupling
  is established by watching which traffic moves during which pedestrian phase,
  which costs one clip review and no API calls.
- **Events whose truth depends on the pedestrian signal are the cheapest in the
  repo**, because the phase timeline costs no labelling and no API call.

---

## 1. The floor: events a rule can also answer, and therefore score

These are worth asking, and they are the only events that can be scored
**automatically, on every clip, for both presence and timing**. The rule that
could answer them is what supplies the ground truth.

Two of them are the strongest starting points in the whole catalogue, because
their truth is a *duration* rather than a yes/no:

- **a pedestrian crossing against their signal** — needs the pedestrian phase
  timeline (already built, model-free) plus a hand-drawn crosswalk polygon. One
  afternoon of one-time work and every clip is scored forever.
- **a vehicle occupying the crosswalk for too long** — same polygon, plus "is
  it stationary". The answer is an interval, so the model's `t_start_sec` /
  `t_end_sec` can be scored against a measured interval instead of only being
  marked hit or miss. That is the localisation score no run has ever produced,
  and the threshold on "too long" is itself a variable worth sweeping.

The rest, with what a rule needs for each:

| event | what a rule needs |
|---|---|
| a vehicle stopped over the crosswalk markings | box ∩ polygon |
| a vehicle waiting inside the junction box | box ∩ polygon |
| a cyclist riding on the sidewalk | box ∩ polygon |
| a pedestrian crossing outside the crosswalk | box ∩ polygon |
| a vehicle in the bike lane | box ∩ polygon |
| a vehicle driving the wrong way | track heading vs lane direction |
| the moment a stopped vehicle begins to move | track speed crossing zero |
| a vehicle braking harder than its neighbours | track acceleration |
| a pedestrian stepping off the kerb | track ∩ polygon boundary |
| a bus / taxi / fire truck is present | detector class |
| a pedestrian crossing against their signal | polygon ∩ phase timeline |
| double parking, stopping in a travel lane | track dwell + polygon |

**What a correct answer here does and does not license.** Getting these right
shows the model can bind language to objects and to scene geometry, which is
worth knowing and is the precondition for everything in §2. It does not show it
can tell yielding from queueing, because nothing in this list requires that.
Read the two blocks as a floor and a ceiling on the same run: a model that
fails §1 makes §2 uninterpretable, and a model that passes §1 but fails §2 has
been located precisely.

**Build the rule for a subset only.** The point is a measuring stick, not a
detection system. Two polygons (the two crosswalks) and the phase timeline
cover both starred events above; stop lines, lane directions and the junction
box can wait until something needs them.

---

## 2. The discriminating set: events a rule cannot answer

What they have in common: the evidence is not a position or a velocity. It is a
**relation between actors that has to be inferred**, and the pixels are
consistent with more than one relation.

### 2.1 Causation — one actor's behaviour explained by another

- a vehicle that entered the intersection and had to stop partway **because**
  someone was crossing in front of it
- a queue that formed **because** a delivery vehicle blocked the lane
- a pedestrian who changed their path **to avoid** the construction plates
- a cyclist who left the bike lane **because** it was obstructed

A rule sees "stopped vehicle" and "pedestrian present" and cannot assert the
link. This is the sharpest category and the one the existing failures point at:
the model already reports the objects correctly and invents the relation
between them (F1).

### 2.2 Intent and counterfactual — what would have happened otherwise

- a turning vehicle that **waited for** pedestrians to finish crossing before
  completing its turn
- a driver who **yielded** to a bus pulling out from the stop
- a vehicle that **gave way** to another at an ambiguous point of conflict
- a vehicle that **failed to yield** while turning across a crosswalk

"Waited" is not "was stationary". A vehicle stationary in a queue with a
pedestrian nearby produces the same tracks as a vehicle yielding.

### 2.3 Hesitation and abandoned action

- a pedestrian who **started to cross, then stopped or stepped back** because
  of an approaching vehicle
- a vehicle that **began a turn and aborted it**
- a cyclist who **slowed, looked, and then went** through a gap
- someone who **approached the kerb and decided not to cross**

Requires recognising that an action was initiated and not completed — a
negative event, which no detector has a representation for.

### 2.4 Social and normative roles — purpose, not class

- a **worker directing traffic** through the construction zone, and whether
  drivers complied
- a driver **waving a pedestrian across**
- a **delivery rider** stopped to make a drop-off, as distinct from stopped in
  traffic
- passengers **boarding or alighting** a bus, and a pedestrian crossing in
  front of or behind it
- other vehicles **making way for an emergency vehicle**, or failing to

The detector sees a person in a hi-vis vest. Whether they are *directing
traffic* is about what everyone else is doing in response.

### 2.5 Multi-actor outcomes over time

- **two road users passing close enough that one visibly changed course or
  speed** — the near-miss, which is the safety-relevant unit
- a **right hook**: a vehicle turning right across a cyclist continuing straight
- pedestrians and a turning vehicle **negotiating** the same crosswalk space
- a group crossing that **holds up** turning traffic

Note that the near-miss is partly measurable — post-encroachment time from
calibrated tracks — which is exactly why it is worth asking a model about: the
geometry gives an objective reference value to score the answer against
(README §4, Phase 3).

### 2.6 Construction-specific, and unusually rich here

This intersection is dug up in every clip, which supplies event types a normal
intersection does not:

- a **pedestrian detoured into the roadway** because the sidewalk is closed
- a vehicle **threading between cones**, or driving over the coned-off zone
- a worker **stepping into a live lane** and traffic responding
- a vehicle **stopping short** for a plated excavation

These are worth listing separately because they are rare in any benchmark, and
because they will dominate this particular corpus.

---

## 3. How to turn this into a query set

A list of events is not yet an experiment. Two hypotheses have to be separated:

- **H1** the model understands the relation
- **H2** the model recognises the objects and writes a fluent sentence about
  whatever relation the query named

Every query in §2 is answerable by H2, because each names a situation whose
objects are present. So each positive needs a **twin**: identical objects,
different relation.

```
A | a vehicle that stopped to let a pedestrian cross, then moved off once they had passed
B | a vehicle stopped in a queue while a pedestrian happened to pass alongside it
```

H1 predicts one match and one absent. H2 predicts two matches. **Only one of
the pair can be true of a given moment, so the pair scores itself** — no
labelling needed to detect the failure, exactly as
a mechanical check on `results.jsonl` can find.

Grounding comes after, and is cheap: every answer already carries
`t_start_sec` and `clearest_frame_sec`, and the frames it was shown are on disk
under `runs/<name>/`. Checking whether a claimed event is at the claimed second
takes about two minutes by eye, and only for the answers that came back
present.

## 4. Order

The two blocks are independent, so they can run in either order or in parallel.
§1 is cheaper and needs no clip review, so it is the one that can start today.

**The floor (§1), no clip review needed:**

1. Pedestrian phase timeline for all five clips — model-free, one script,
   already demonstrated on the 17:00 clip. Re-locate the head box per clip
   (G6: the camera drifts between recordings).
2. Hand-draw the two crosswalk polygons on one native frame. One-time, minutes.
3. That is enough to score "pedestrian crossing against the signal" and
   "vehicle occupying the crosswalk for N seconds" automatically, with a
   measured interval to compare the model's interval against.
4. Run those queries. Score presence **and** timing. This is the first
   grounding measurement the repo will have produced.

**The discriminating set (§2), gated on the clip review:**

5. Clip review: walk the clips and record which of §2 actually occur, with
   times and actors.
6. While reviewing, note which direction of traffic moves during which
   pedestrian phase. If the coupling is consistent, the vehicle phase becomes
   inferable and §0's exclusion relaxes.
7. Write the paired query set from the reviewed events — every positive with a
   surface-matched twin (§3).
8. Presence/absence on the pairs, three repeats. Then time-grounding on the
   hits, checked by eye against the frames in `runs/<name>/`.
