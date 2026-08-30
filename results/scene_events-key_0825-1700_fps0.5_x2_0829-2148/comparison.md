# scene — arm comparison

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- queries: `queries/events-key.txt` | fps 0.5 | 2 repeat(s) per arm

Held fixed and varied: `experiment.json`. A flip between arms at one repeat is not an effect; check the repeats column before reading anything into it.

## verdict per query

| axis | query | no-scene | with-scene |
|---|---|---|---|
| turn-fty | a turning vehicle continuing through a crosswalk while a p | present/present | present/present |
| right-hook | a vehicle turning across the path of a cyclist who is cont | present/present | present/absent |
| stop-crosswalk | a vehicle stopped with part of its body on the crosswalk m | absent/present | present/absent |
| pickup-car | a person getting into or out of a stopped car, van or taxi | absent/present | present/present |
| ped-conflict | a pedestrian in the crosswalk while vehicles are driving t | present/present | present/present |
| bike-sidewalk | a cyclist or e-bike rider riding along the sidewalk in the | absent/absent | absent/absent |
| bike-wrongway | a cyclist or e-bike rider riding against the direction of  | present/present | present/present |
| emergency | an emergency vehicle with lights flashing passing through  | present/present | present/absent |
| negative | two vehicles making contact with each other | absent/absent | absent/absent |
| negative | a horse-drawn carriage | absent/absent | absent/absent |

## flips between arms

- **stop-crosswalk** — a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to
  - `no-scene`: absent/present
  - `with-scene`: present/absent
- **pickup-car** — a person getting into or out of a stopped car, van or taxi
  - `no-scene`: absent/present
  - `with-scene`: present/present

## echo check

How often each arm's own prose uses wording that appears in a scene block. An arm that was given the block and uses this language far more than one that was not is repeating what it was told; the phrases are not evidence of having looked.

| arm | matches | phrases used |
|---|---|---|
| no-scene | 2 | left to right ×1, right to left ×1 |
| with-scene | 9 | left to right ×3, right to left ×5, up the frame ×1 |
