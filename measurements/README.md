# measurements/

Properties of the camera and the intersection, each with its derivation
written down. One file per topic.

**These are not "model-free".** A model chose where to put the measurement
bands, what threshold counted as motion, and which correlation was strong
enough to believe. Judgement is in every file here, and each one names where.

The distinction that actually matters is not whether a model was involved but
whether the claim can be **re-derived**:

| directory | holds | to disagree with it you… |
|---|---|---|
| `measurements/` | a number and the procedure that produced it | change the stated parameters and re-run; you get a number to argue about |
| `experiment_results/` | a model's free-text assertion about a moment | open the named second and look; there is nothing to re-run — the same prompt on the same frames has already produced different answers on different runs |
| `runs/` | the frames a run actually sent | — disposable |

So a measurement is falsifiable by re-running and a probe result is falsifiable
only by eye. That is why nothing in `experiment_results/` may be promoted into a
measurement without being checked against the frames first.

**These are inputs, not judges.** They decide what is worth asking --
`signal-legibility` is why no red-light query is in the vocabulary -- and they
feed the scene block via `utils/measure.py`. Nothing here scores a run; only the
hand-filled ground-truth sheet does. Reproducible and authoritative are
different things, and this is only the first.

Each file records `method` alongside `result`, a `judgement` field naming the
choices that were not forced by the data, and a `reliability` field saying
plainly what the number does and does not support. A measurement whose method
failed is kept and marked failed rather than deleted — that the cross-street
direction could not be recovered is itself worth having.

---

## Where things go

Four places, and nothing lands anywhere else.

```
measurements/<topic>.json     a measured fact, with its method and judgement calls
experiment_results/<name>/    one experiment: result.md, and arms/<arm>/ inside
runs/                         the frames a run actually sent.
ground-truth/                 the hand-filled sheets runs are scored against.
```

Regenerate with `python scripts/measure.py videos/<clip>.mp4`. The same
functions build the scene block, so a fix here cannot drift out of step with
what the pipeline uses.

**Scratch does not go in the repo.** Intermediate renders made while checking a
claim — fixed-box traces, zoomed crops, montages — are working material, not
output. They belong in a scratch directory outside the tree. Earlier they were
dropped into `runs/` next to the probe's own output, which is what made it hard
to tell what was an experiment and what was somebody looking at a frame.

Two consequences worth stating:

- **A run directory is never edited or appended to.** Re-running writes a new
  timestamped directory. A comparison between two conditions is worthless if it
  cannot be told which rows came from which.
- **A superseded run is deleted, not kept "just in case".** Its findings, if any
  survived verification, belong in `measurements/` or a note. Keeping the
  directory keeps a result that nobody has checked, which is worse than nothing.
