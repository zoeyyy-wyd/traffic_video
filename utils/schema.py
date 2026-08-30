"""Schemas for every model-facing task.

Constraining output to a schema is not only convenience. Several fields exist
to make a specific failure visible rather than to carry information: whether a
signal colour was read or inferred, whether alternatives were considered before
answering, whether a match is genuine or merely surface-level. A model that
answers well and a model that pattern-matches produce the same prose; they do
not produce the same values in these fields.
"""
from typing import List, Literal

from pydantic import BaseModel

# --- open-ended scanning ----------------------------------------------------

EventType = Literal[
    "red_light_running", "pedestrian_against_signal", "failure_to_yield_turning",
    "wrong_way", "blocking_the_box", "double_parking", "stopping_in_crosswalk",
    "micromobility_wrong_space", "near_miss", "collision", "other",
]


class Detected(BaseModel):
    """One event the model found without being told what to look for."""

    event_type: EventType
    t_start_sec: float
    t_end_sec: float
    actors: str
    what_happened: str
    signal_state_claimed: str
    # The measurement that settles whether signal-dependent judgements are
    # viable here: did it read an illuminated face, or infer colour from
    # traffic behaviour -- circular, and confidently wrong on edge cases?
    signal_state_basis: Literal["read_directly", "inferred_from_behaviour", "unknown"]
    severity: Literal["minor", "moderate", "severe"]
    confidence: Literal["high", "medium", "low"]


class WindowResult(BaseModel):
    events: List[Detected]
    signal_head_visible: bool
    scene_notes: str
    unreadable_reasons: List[str]


# --- query grounding --------------------------------------------------------

class QueryMatch(BaseModel):
    """One moment in the window that matches the described situation."""

    t_start_sec: float
    t_end_sec: float
    subject: str                  # which road user, described well enough to identify
    clearest_frame_sec: float     # where a human should look to check this
    what_happens: str             # the observed sequence, in the model's own words
    # A situation query can be answered by matching surface features rather
    # than the situation: "a van and a pedestrian are both present" is not
    # "the van stopped for the pedestrian". Forcing this distinction makes the
    # difference visible in the output instead of hidden in fluent prose.
    match_quality: Literal["exact", "partial", "superficial"]
    confidence: Literal["high", "medium", "low"]


class QueryResult(BaseModel):
    """Answer to 'is this described situation in this window, and where?'"""

    matches: List[QueryMatch]     # empty means not present -- a valid answer
    # What it looked at and ruled out. A model that discriminated will have
    # something here when the scene contains near-misses of the query; one that
    # pattern-matched will not. Distinguishes reasoning from lucky agreement.
    considered_and_rejected: str
    # When nothing matched: what was absent. Separates "did not happen" from
    # "happened but could not be seen", which are different results.
    why_not_found: str
    unreadable_reasons: List[str]


class QueryAnswer(QueryResult):
    """One query's answer inside a batched call.

    `query_index` is what makes the batch usable: the model is asked several
    questions in one request and must say which answer belongs to which, rather
    than relying on list order, which it is free to permute or truncate.
    """

    query_index: int


class BatchQueryResult(BaseModel):
    """Answers to every query in one call, over one set of frames.

    Sending the frames once instead of once per query is the difference between
    paying for N x M images and paying for M. The cost is that the queries are
    no longer independent -- the model sees all of them at once and can let one
    answer inform another. That is a real change in what is being measured, not
    a free optimisation, so it is a flag rather than the default.
    """

    answers: List[QueryAnswer]
