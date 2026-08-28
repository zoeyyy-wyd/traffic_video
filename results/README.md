# results/

One directory per probe run, created by `scripts/vlm_probe.py`:

```
results/<YYYYmmdd-HHMMSS>-<label>/
  summary.md      what was asked and what came back, with the parameters
  results.jsonl   one row per call, written as each answer arrives (gitignored)
  run.json        every parameter of the run, machine-readable
  frames -> ../../runs/<same name>/    the images the model was actually sent
```

`<label>` is `--name`, or `<query set>-fps<fps>` when that is not given.
The timestamp makes the directory unique, which is what stops a re-run of the
same command from appending to the previous run's rows.

Frames stay under `runs/` rather than in here: they are large and reproducible,
while `summary.md` and `run.json` are neither. The symlink keeps them one hop
away.

The runs that predate this layout have been removed.
