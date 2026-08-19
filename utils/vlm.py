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

_SCENE = """The camera is fixed, mounted high on a building, and looks down obliquely across an intersection in New York City. A large part of the frame is the wall of the host building, a sidewalk scaffolding shed, and street trees; those areas contain no road users. Frames are given in chronological order, each captioned with its timestamp in seconds."""

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


def frames_text(frames: Sequence[Tuple[float, Image.Image]],
                t0: float, t1: float) -> str:
    stamps = ", ".join(f"{t:.2f}" for t, _ in frames)
    return (f"Window {t0:.2f}s - {t1:.2f}s of the recording, "
            f"{len(frames)} frames in chronological order.\n"
            f"Timestamps (seconds into the recording): {stamps}\n"
            f"Each frame is captioned with its own timestamp.")


def open_prompt(frames, t0: float, t1: float) -> str:
    return (frames_text(frames, t0, t1) +
            "\n\nReport any traffic events. Use these timestamps for "
            "t_start_sec / t_end_sec.")


def query_prompt(frames, t0: float, t1: float, query: str) -> str:
    return (frames_text(frames, t0, t1) +
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
