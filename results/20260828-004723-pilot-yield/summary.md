# probe run: 20260828-004723-pilot-yield

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `burn,list` (channels: burn, list, interleave, or none)
- fps: 0.5 | whole range, one call
- frames per call: 91 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/20260828-004723-pilot-yield`

## by axis

| axis | answered present | note |
|---|---|---|
| pair-yield | 2/2 |  |

## per query

### [pair-yield] a vehicle that stopped to let a pedestrian cross in front of it, and moved off only after they had passed

- **match** `exact` / conf `high` at 120.0-126.0s (clearest 122.0s)
  - subject: a silver SUV and a pedestrian
  - A silver SUV turns right and stops at the crosswalk to allow a pedestrian to cross in front of it. The vehicle remains stationary until the pedestrian has safely passed, then resumes driving.
- ruled out: I also observed a pedestrian crossing in front of a dark SUV around 158.03s, but the vehicle did not need to stop or adjust its speed as the pedestrian had already cleared its path by the time it approached.

### [pair-yield] a vehicle that was stopped because the traffic in front of it was not moving, while a pedestrian happened to pass nearby

- **match** `exact` / conf `high` at 110.0-114.0s (clearest 110.0s)
  - subject: white SUV
  - A white SUV stops in a queue behind a USPS truck on the cross street. While the SUV is stopped, a pedestrian on the adjacent sidewalk walks past it toward the intersection.
- ruled out: The black SUV that stops at the intersection line at 94.03s after an articulated bus turns in front of it. While a pedestrian crosses in front of the SUV shortly after, the vehicle is first in line and stopped for the traffic light, rather than being queued behind non-moving traffic. The black SUV that stops behind a silver SUV at 40.03s was also considered, but there are no pedestrians walking near it while it is queued.

---

2 call(s) ok, 0 failed, 202503 in / 8365 out tokens