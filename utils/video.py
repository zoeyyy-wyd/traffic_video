"""Frame extraction and container probing.

Timestamps always come from the container's PTS, never from frame_index/fps.
The COSMOS footage is recorded off a network stream via GStreamer and is very
likely variable-frame-rate; an index-derived clock drifts silently against the
signal phase, which inverts red-light verdicts without any visible error.
"""
from typing import List, Optional, Tuple

from PIL import Image

Frame = Tuple[float, Image.Image]


def probe(video: str) -> dict:
    """Container metadata, including a variable-frame-rate flag."""
    import av

    container = av.open(video)
    stream = container.streams.video[0]
    info = {
        "width": stream.codec_context.width,
        "height": stream.codec_context.height,
        "duration_s": float(stream.duration * stream.time_base) if stream.duration else None,
        "avg_rate": str(stream.average_rate),
        "base_rate": str(stream.base_rate),
        "nb_frames": stream.frames or None,
        # average_rate diverging from base_rate is the usual VFR tell
        "likely_vfr": str(stream.average_rate) != str(stream.base_rate),
    }
    container.close()
    return info


def extract(video: str, t0: float, t1: float, fps: float) -> List[Frame]:
    """Decode frames in [t0, t1] at `fps`, returned as (pts_seconds, image)."""
    import av

    container = av.open(video)
    stream = container.streams.video[0]
    stream.thread_type = "AUTO"

    if stream.time_base is None:
        raise RuntimeError(f"{video}: stream has no time_base; timestamps untrustworthy")

    # seek early -- seeking lands on the preceding keyframe
    container.seek(max(0, int((t0 - 2.0) / stream.time_base)), stream=stream)

    out: List[Frame] = []
    next_due, step = t0, 1.0 / fps
    for frame in container.decode(stream):
        if frame.pts is None:
            continue
        t = float(frame.pts * stream.time_base)
        if t < t0 - 1e-6:
            continue
        if t > t1 + 1e-6:
            break
        if t + 1e-6 >= next_due:
            out.append((t, frame.to_image()))
            # advance past t rather than by one step, so a gap of dropped
            # frames does not leave a backlog of due-times emitted back to back
            while next_due <= t + 1e-6:
                next_due += step
    container.close()
    return out


def windows(start: float, end: float, length: float, overlap: float):
    """Yield (t0, t1) covering [start, end], overlapping so that an event
    straddling a boundary is fully visible in at least one window."""
    step = max(0.1, length - overlap)
    t = start
    while t < end:
        yield t, min(t + length, end)
        t += step


# --- integrity ----------------------------------------------------------

def verify(path: str, deep: bool = False) -> dict:
    """Classify one video file. Never raises.

    Returns {"path", "size", "status", "detail"} where status is one of:

    ok           opens, reports a duration, and (with deep) decodes a frame
    empty        zero bytes
    unreadable   the container will not open -- for mp4 this usually means a
                 truncated file, since the moov atom sits at the end and a
                 partial upload loses it
    no_duration  opens but carries no duration; playable but unusable here,
                 since every script needs an end time to walk windows to
    undecodable  headers fine, but no frame comes out (deep only)
    """
    import os

    try:
        size = os.path.getsize(path)
    except OSError as e:
        return {"path": path, "size": 0, "status": "unreadable", "detail": str(e)}

    if size == 0:
        return {"path": path, "size": 0, "status": "empty", "detail": "zero bytes"}

    try:
        import av

        container = av.open(path)
        try:
            stream = container.streams.video[0]
            dur = float(stream.duration * stream.time_base) if stream.duration else None
            if dur is None and container.duration:
                dur = container.duration / 1_000_000
            if not dur:
                return {"path": path, "size": size, "status": "no_duration",
                        "detail": "no duration in container"}
            if deep:
                got = False
                stream.codec_context.skip_frame = "NONKEY"
                for frame in container.decode(stream):
                    got = frame is not None
                    break
                if not got:
                    return {"path": path, "size": size, "status": "undecodable",
                            "detail": "no frame decoded"}
            return {"path": path, "size": size, "status": "ok",
                    "detail": f"{dur:.1f}s {stream.codec_context.width}x"
                              f"{stream.codec_context.height}"}
        finally:
            container.close()
    except Exception as e:
        return {"path": path, "size": size, "status": "unreadable",
                "detail": f"{type(e).__name__}: {e}"}
