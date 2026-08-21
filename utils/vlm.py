"""Prompts and the backend factory.

Two probes share one set of frames:

open    no hint given -- what does the model find on its own?
query   a described situation -- can it locate that, and say so when absent?

The query probe is the one that matters. Asking a model to find "a fire truck"
tests object recognition, which a detector already does and which says nothing
about grounding. Asking it to find "a vehicle that entered the intersection and
had to stop partway because someone was crossing" asks for something no
detector has a class for: a situation, composed of several actors over several
seconds. If a VLM contributes anything here, that is where.

Provider-specific request shapes live in backend_*.py. Everything shared lives
here so the backends are compared on identical wording.
"""
from typing import Sequence, Tuple

from PIL import Image

_SCENE = """The camera is fixed, mounted high on a building, and looks down obliquely across an intersection in New York City. A large part of the frame is the wall of the host building, a sidewalk scaffolding shed, and street trees; those areas contain no road users. Frames are given in chronological order; how each frame's timestamp is supplied is stated in the user message."""

SYSTEM_OPEN = f"""You review fixed-camera footage of an urban intersection and report traffic events.

{_SCENE}

Report only what the imagery supports. Two rules matter more than completeness:

1. Never infer the traffic signal colour from how vehicles are behaving. If you cannot see an illuminated signal face, set signal_state_basis to "inferred_from_behaviour" or "unknown" and say so. A red-light violation whose signal state was inferred from stopped traffic is circular reasoning and is the most damaging error available here.

2. Returning an empty events list is a correct and expected answer. Most windows contain no violation. Do not manufacture an event to have something to report.

Local rules: right turn on red is prohibited in NYC unless a sign permits it. Cyclists and e-bikes may not ride on the sidewalk.

List in unreadable_reasons anything you needed but could not resolve (signal facing away, object too small, occluded by the shed or tree canopy, motion blur)."""

SYSTEM_QUERY = f"""You are given frames from fixed-camera intersection footage and a description of a situation. Decide whether that situation occurs in these frames, and if so, when and to whom.

{_SCENE}

The description names a situation, not an object. It may involve several road users, a sequence over several seconds, or an outcome. Matching it means the sequence actually happened -- not that the pieces are visible somewhere in frame.

Rules:

1. "Not present" is a correct and expected answer, and many queries are deliberately for situations that did not occur. Return an empty matches list and explain in why_not_found what was absent. Never stretch a partial resemblance into a match to be helpful.

2. Distinguish what you matched on. If the described sequence is visible, that is "exact". If part of it is visible but the decisive moment is not, that is "partial". If the actors and setting are present but the described interaction is not something you actually observed, that is "superficial" -- report it as such rather than as a match.

3. Fill considered_and_rejected with the candidates you examined and ruled out, and why. If the scene contains near-misses of the query, they belong here.

4. Judge only from the frames. Do not assume that a plausible sequence occurred between two frames; if the decisive moment falls in a gap, say so in unreadable_reasons."""


# How a frame's timestamp reaches the model. Three independent channels, so
# each can be switched on alone and the arms compared on the same frames:
#
#   burn        drawn into the frame's own pixels (survives whatever cropping
#               and tiling the provider does internally, and is the only
#               channel a person sees when opening the saved jpg)
#   list        one text block naming every timestamp in the window, in order;
#               binding a frame to its time is then positional -- the model has
#               to count to the k-th number
#   interleave  a text block carrying one timestamp immediately before its own
#               frame, so the pairing is in the message structure itself
#
# `burn,list` is what every run before this flag existed used, and stays the
# default so an old command reproduces its earlier result.
CHANNELS = ("burn", "list", "interleave")
DEFAULT_ENCODING = "burn,list"


def parse_encoding(spec: str) -> frozenset:
    """'burn,interleave' or 'none' -> the set of active channels."""
    spec = (spec or "").strip()
    if spec in ("", "none"):
        return frozenset()
    got = frozenset(p.strip() for p in spec.split(",") if p.strip())
    bad = got - set(CHANNELS)
    if bad:
        raise ValueError(f"unknown timestamp channel(s) {sorted(bad)} -- "
                         f"pick from {list(CHANNELS)}, or 'none'")
    return got


def frames_text(frames: Sequence[Tuple[float, Image.Image]],
                t0: float, t1: float, enc: frozenset) -> str:
    """The text half of the payload. It describes only the channels actually
    in use: telling the model a frame is captioned when it is not invites it
    to invent the caption it was promised."""
    lines = [f"Window {t0:.2f}s - {t1:.2f}s of the recording, "
             f"{len(frames)} frames in chronological order."]
    if "list" in enc:
        stamps = ", ".join(f"{t:.2f}" for t, _ in frames)
        lines.append(f"Timestamps (seconds into the recording): {stamps}")
    if "interleave" in enc:
        lines.append("Each frame is immediately preceded by a line giving "
                     "that frame's own timestamp.")
    if "burn" in enc:
        lines.append("Each frame carries its own timestamp burnt into its "
                     "top-left corner.")
    if not enc:
        lines.append("No timestamps are supplied. Give times in seconds from "
                     "the start of the window, and say in unreadable_reasons "
                     "that they are estimated from frame order.")
    return "\n".join(lines)


def open_prompt(frames, t0: float, t1: float, enc: frozenset) -> str:
    return (frames_text(frames, t0, t1, enc) +
            "\n\nReport any traffic events. Use these timestamps for "
            "t_start_sec / t_end_sec.")


def query_prompt(frames, t0: float, t1: float, query: str,
                 enc: frozenset) -> str:
    return (frames_text(frames, t0, t1, enc) +
            f"\n\nSituation to locate:\n  {query}\n\n"
            f"Does it occur in these frames? Use these timestamps for "
            f"t_start_sec / t_end_sec / clearest_frame_sec.")


def get_backend(name: str, model: str = None):
    """Factory. Backends are imported lazily so neither SDK is a hard dep."""
    if name == "gemini":
        from .backend_gemini import GeminiBackend
        return GeminiBackend(model) if model else GeminiBackend()
    if name == "claude":
        from .backend_claude import ClaudeBackend
        return ClaudeBackend(model) if model else ClaudeBackend()
    raise ValueError(f"unknown backend: {name}")
