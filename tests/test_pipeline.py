"""Smoke tests that do not need the real footage or any API key.

Synthesises a short video with PyAV, then exercises the extraction and
rendering path against it. The point is to pin down the timestamp handling in
utils/video.py -- a silent one-second drift there flips red-light verdicts, and
it is not the kind of bug the real footage will make obvious.

    python tests/test_pipeline.py
"""
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw

from utils.render import LONG_EDGE, contact_sheet, fit, stamp, to_b64
from utils.schema import Detected, QueryMatch, QueryResult, WindowResult
from utils.video import extract, probe, windows

FPS, DURATION, W, H = 30, 10, 640, 360


def make_video(path: str) -> None:
    """A 10 s CFR clip whose every frame is tinted by its own frame number,
    so a decoded frame can be traced back to the time it should carry."""
    import av

    container = av.open(path, mode="w")
    stream = container.add_stream("libx264", rate=FPS)
    stream.width, stream.height, stream.pix_fmt = W, H, "yuv420p"
    stream.codec_context.time_base = Fraction(1, FPS)

    for i in range(FPS * DURATION):
        img = Image.new("RGB", (W, H), (i % 256, (i * 3) % 256, 40))
        d = ImageDraw.Draw(img)
        d.text((20, 20), f"frame {i}  t={i / FPS:.3f}s", fill=(255, 255, 255))
        frame = av.VideoFrame.from_image(img)
        frame.pts = i
        frame.time_base = Fraction(1, FPS)
        container.mux(stream.encode(frame))
    container.mux(stream.encode(None))
    container.close()


def check(label, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
    if not cond:
        check.failed += 1
check.failed = 0


def main():
    tmp = Path(tempfile.mkdtemp())
    video = str(tmp / "synth.mp4")
    make_video(video)
    print(f"synthesised {DURATION}s @ {FPS}fps -> {video}\n")

    print("probe()")
    info = probe(video)
    check("width/height", (info["width"], info["height"]) == (W, H), str(info["width"]))
    check("duration ~= 10s", abs((info["duration_s"] or 0) - DURATION) < 0.2,
          f"{info['duration_s']:.3f}s")
    check("CFR not flagged as VFR", info["likely_vfr"] is False,
          f"avg={info['avg_rate']} base={info['base_rate']}")

    print("\nextract() -- 1 fps over [2.0, 8.0]")
    frames = extract(video, 2.0, 8.0, 1.0)
    ts = [t for t, _ in frames]
    check("frame count", len(frames) == 7, f"got {len(frames)}: {[f'{t:.2f}' for t in ts]}")
    check("starts at/after t0", ts and ts[0] >= 2.0 - 1e-6, f"{ts[0]:.3f}")
    check("ends at/before t1", ts and ts[-1] <= 8.0 + 1e-6, f"{ts[-1]:.3f}")
    check("timestamps strictly increasing", all(b > a for a, b in zip(ts, ts[1:])))
    check("spacing ~1s (no backlog burst)",
          all(abs((b - a) - 1.0) < 0.05 for a, b in zip(ts, ts[1:])),
          f"gaps={[round(b - a, 3) for a, b in zip(ts, ts[1:])]}")

    print("\nextract() -- 5 fps over a 2 s window")
    fast = extract(video, 3.0, 5.0, 5.0)
    check("frame count ~11", len(fast) == 11, f"got {len(fast)}")

    print("\nextract() -- seek does not leak pre-roll frames")
    late = extract(video, 7.0, 9.0, 1.0)
    check("no frame before t0", all(t >= 7.0 - 1e-6 for t, _ in late),
          f"min={min(t for t, _ in late):.3f}")

    print("\nwindows()")
    ws = list(windows(0, 10, 6, 2))
    check("overlapping cover", ws[0] == (0, 6) and ws[1] == (4, 10), str(ws))
    check("last window clipped to end", ws[-1][1] == 10, str(ws[-1]))

    print("\nrender")
    img = frames[0][1]
    check("fit caps long edge", max(fit(img.resize((4000, 2000))).size) == LONG_EDGE)
    check("stamp preserves size", stamp(img.copy(), "t=1.00s").size == img.size)
    sheet = contact_sheet(frames, 3)
    check("sheet is 3 cols x 3 rows", sheet.width == (LONG_EDGE // 3) * 3, str(sheet.size))
    check("base64 non-empty", len(to_b64(img)) > 100)

    # Each timestamp channel is meant to be switchable on its own, so what is
    # worth pinning is that they stay independent: an arm must not describe a
    # channel it did not send, and the interleaved blocks must land next to
    # the frame they name rather than merely somewhere in the message.
    print("\ntimestamp channels")
    from utils.vlm import frames_text, parse_encoding
    check("default arm is burn+list",
          parse_encoding("burn,list") == frozenset({"burn", "list"}))
    check("'none' clears every channel", parse_encoding("none") == frozenset())
    try:
        parse_encoding("burn,pixels")
        check("unknown channel rejected", False)
    except ValueError as e:
        check("unknown channel rejected", "pixels" in str(e))

    two = frames[:2]
    listed = frames_text(two, 2.0, 3.0, parse_encoding("list"))
    inter = frames_text(two, 2.0, 3.0, parse_encoding("interleave"))
    check("list arm enumerates the timestamps", "Timestamps (seconds" in listed)
    check("interleave arm does not enumerate", "Timestamps (seconds" not in inter)
    check("interleave arm says frames are preceded", "immediately preceded" in inter)
    check("neither arm promises a caption it did not burn",
          "burnt into" not in inter and "burnt into" not in listed)
    check("empty arm admits it", "No timestamps are supplied"
          in frames_text(two, 2.0, 3.0, parse_encoding("none")))

    from utils.backend_claude import ClaudeBackend
    labelled = [(f"t={t:.2f}s", im) for t, im in two]
    c = ClaudeBackend.content(labelled, "the query")
    check("content alternates text/image and ends on the query",
          [b["type"] for b in c] == ["text", "image", "text", "image", "text"],
          str([b["type"] for b in c]))
    check("each label sits immediately before its own frame",
          c[0]["text"] == f"t={two[0][0]:.2f}s"
          and c[2]["text"] == f"t={two[1][0]:.2f}s",
          f"{c[0]['text']} / {c[2]['text']}")
    check("the varying query goes last", c[-1]["text"] == "the query")
    check("labels off -> plain image run",
          [b["type"] for b in ClaudeBackend.content([(None, im) for _, im in two],
                                                    "q")]
          == ["image", "image", "text"])

    print("\nschema")
    r = WindowResult(events=[], signal_head_visible=False, scene_notes="quiet",
                     unreadable_reasons=["signal facing away"])
    check("empty event list is valid", r.events == [])
    d = Detected(event_type="red_light_running", t_start_sec=1, t_end_sec=2,
                 actors="white van", what_happened="crossed on red",
                 signal_state_claimed="red", signal_state_basis="inferred_from_behaviour",
                 severity="moderate", confidence="low")
    check("signal_state_basis round-trips", d.model_dump()["signal_state_basis"]
          == "inferred_from_behaviour")

    q = QueryResult(matches=[], considered_and_rejected="two vans, neither stopped",
                    why_not_found="no vehicle stopped mid-crossing",
                    unreadable_reasons=[])
    check("empty match list is valid", q.matches == [])
    m = QueryMatch(t_start_sec=3, t_end_sec=7, subject="white van",
                   clearest_frame_sec=5, what_happens="stopped for a pedestrian",
                   match_quality="superficial", confidence="low")
    check("match_quality round-trips",
          m.model_dump()["match_quality"] == "superficial")

    from utils.backend_gemini import _inline_refs
    import json
    for name, model in (("WindowResult", WindowResult), ("QueryResult", QueryResult)):
        schema = json.dumps(_inline_refs(model.model_json_schema()))
        check(f"{name} schema has no $ref/$defs",
              "$ref" not in schema and "$defs" not in schema)

    from utils.render import overview_grid
    g = overview_grid([(t, im) for t, im in frames], cols=4)
    check("overview grid tiles 4 wide", g.width == 320 * 4, str(g.size))

    # A run directory that does not carry its condition leaves an ablation
    # loop as a pile of directories separable only by timestamp, and one that
    # is not unique lets a re-run append to the previous run's rows.
    print("\nrun directory naming")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "vlm_probe", Path(__file__).resolve().parent.parent / "scripts" / "vlm_probe.py")
    probe_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe_mod)

    class Args:
        name = queries = query = None
        fps = 0.5

    a = Args()
    a.queries = "queries/events-paired.txt"
    check("label carries query set and fps",
          probe_mod.run_label(a) == "events-paired-fps0.5", probe_mod.run_label(a))
    b = Args()
    check("no query set -> open mode label",
          probe_mod.run_label(b) == "open-fps0.5", probe_mod.run_label(b))
    c = Args()
    c.name = "minimal pairs #4 / yielding"
    check("--name wins and is slugged",
          probe_mod.run_label(c) == "minimal-pairs-4-yielding", probe_mod.run_label(c))
    check("slug never returns an empty component", probe_mod.slug("///") == "run")

    link_root = tmp / "linktest"
    (link_root / "results" / "r1").mkdir(parents=True)
    (link_root / "runs" / "r1").mkdir(parents=True)
    (link_root / "runs" / "r1" / "a.jpg").write_bytes(b"x")
    probe_mod.link_frames(link_root / "results" / "r1", link_root / "runs" / "r1")
    check("frames symlink resolves to the rendered frames",
          (link_root / "results" / "r1" / "frames" / "a.jpg").exists())
    probe_mod.link_frames(link_root / "results" / "r1", link_root / "runs" / "r1")
    check("linking twice is not an error", True)

    print("\nbackend key lookup")
    import os as _os
    from utils.env import BACKEND_KEYS, key_status, require_key
    for backend, names in BACKEND_KEYS.items():
        # a bare string here iterates as characters, which silently matched
        # the shell's $_ and made the pre-flight key check a no-op
        check(f"{backend} key list is a tuple, not a string",
              isinstance(names, tuple), repr(names))
    saved = {n: _os.environ.pop(n, None) for n in BACKEND_KEYS["gemini"]}
    try:
        require_key("gemini")
        check("missing gemini key is caught before the SDK call", False)
    except SystemExit:
        check("missing gemini key is caught before the SDK call", True)
    _os.environ[BACKEND_KEYS["gemini"][0]] = "0123456789abcdef"
    require_key("gemini")
    check("key_status reports the variable that was actually found",
          key_status("gemini") == f"{BACKEND_KEYS['gemini'][0]}=***cdef",
          key_status("gemini"))
    for n, v in saved.items():
        _os.environ.pop(n, None)
        if v is not None:
            _os.environ[n] = v

    # Construct each backend and exercise everything short of the network
    # call. A previous refactor left a dangling name in GeminiBackend.__init__
    # that syntax checks and schema tests both passed straight over.
    print("\nbackends")
    from utils.env import load_env
    load_env()
    for name in ("gemini", "claude"):
        try:
            from utils.vlm import get_backend
            b = get_backend(name)
        except ImportError:
            print(f"  SKIP  {name}: sdk not installed")
            continue
        except Exception as e:
            check(f"{name} constructs", False, f"{type(e).__name__}: {e}")
            continue
        check(f"{name} constructs", True, f"{b.model}")
        check(f"{name} exposes run()", callable(getattr(b, "run", None)))
        if hasattr(b, "parts"):
            ps = b.parts("system", [(f"t={t:.2f}s", im) for t, im in frames[:2]],
                         "the query")
            check(f"{name} interleaves its parts",
                  [p["type"] for p in ps]
                  == ["text", "text", "image", "text", "image", "text"],
                  str([p["type"] for p in ps]))
        if hasattr(b, "_image"):
            try:
                d = b._image(img)
                check(f"{name} builds an image block",
                      d["type"] == "image" and d["resolution"] == b.resolution
                      and len(d["data"]) > 100)
            except Exception as e:
                check(f"{name} builds an image block", False, str(e))

    print(f"\n{'all passed' if not check.failed else str(check.failed) + ' FAILED'}")
    return 1 if check.failed else 0


if __name__ == "__main__":
    sys.exit(main())
