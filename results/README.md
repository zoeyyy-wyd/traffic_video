# results/

One directory per probe run, created by `scripts/vlm_probe.py`:

```
results/<YYYYmmdd-HHMMSS>-<label>/
  summary.md      what was asked and what came back, with the parameters
  results.jsonl   one row per call, written as each answer arrives (gitignored)
  run.json        every parameter of the run, machine-readable
  frames -> ../../runs/<same name>/    the images the model was actually sent
```

`<label>` is `--name`, or `<query set>-roi-<roi>-fps<fps>` when that is not
given, so an ablation loop separates itself without the caller naming each arm.
The timestamp makes the directory unique, which is what stops a re-run of the
same command from appending to the previous run's rows.

Frames stay under `runs/` rather than in here: they are large and reproducible,
while `summary.md` and `run.json` are neither. The symlink keeps them one hop
away.

`full-pro`, `full-pro-wide` and `roi-{none,junction,wide}-bus` predate this
layout. They are the runs written up in
[`notes/2026-08-20-direction-vs-roi.md`](../notes/2026-08-20-direction-vs-roi.md)
and carry only a `summary.md`; their `run.json` was never written, so their
parameters live in the summary header alone.
