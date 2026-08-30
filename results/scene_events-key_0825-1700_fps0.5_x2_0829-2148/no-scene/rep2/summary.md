# probe run: rep2

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 0.5 | whole range, one call
- frames per call: 91 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `/home/yw4636/traffic_video/runs/20260829-214844-scene/no-scene/rep2`

## by axis

| axis | answered present | note |
|---|---|---|
| bike-sidewalk | 0/1 |  |
| bike-wrongway | 1/1 |  |
| emergency | 1/1 |  |
| negative | 0/2 | ground truth known: all absent |
| ped-conflict | 1/1 |  |
| pickup-car | 1/1 |  |
| right-hook | 1/1 |  |
| stop-crosswalk | 1/1 |  |
| turn-fty | 1/1 |  |

## per query

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it

- **match** `exact` / conf `high` at 120.0-126.0s (clearest 124.0s)
  - subject: a turning vehicle and a pedestrian
  - A dark SUV turning right passes through the crosswalk while a pedestrian is walking in it, passing just behind the pedestrian.
- ruled out: At 144.03s - 148.03s, a dark SUV turning right approaches a crosswalk with a pedestrian in it. However, the SUV stops and waits for the pedestrian to reach the sidewalk before continuing through the crosswalk, so it does not meet the description.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight

- **match** `exact` / conf `high` at 114.0-122.0s (clearest 118.0s)
  - subject: silver car and cyclist
  - A silver car traveling straight makes a right turn, crossing directly in front of the path of a cyclist who is continuing straight in the adjacent lane.
- ruled out: At 36.03s - 40.03s, a cyclist travels straight through the intersection while a grey SUV turns left. However, the SUV turns onto the same street the cyclist is traveling on, not across the cyclist's path. At 110.03s - 114.03s, a cyclist travels straight while a silver car turns left, but their paths do not intersect in the manner described.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to

- **match** `exact` / conf `high` at 178.0-180.0s (clearest 180.0s)
  - subject: yellow cab and a pedestrian
  - A yellow cab approaches the intersection from the right road and comes to a stop with its front end resting on the crosswalk markings. At the same time, a pedestrian walks up to the corner and waits to cross the blocked crosswalk.
- ruled out: At 46.03s, a dark SUV stops in the intersection to yield to a pedestrian crossing the left crosswalk, but the SUV is in the middle of the intersection and not stopped on the crosswalk markings. Between 92.03s and 98.03s, buses navigate the intersection, but they do not stop on a crosswalk while pedestrians are waiting.

### [pickup-car] a person getting into or out of a stopped car, van or taxi

- **match** `exact` / conf `high` at 102.0-106.0s (clearest 104.0s)
  - subject: a pedestrian
  - A person walks up to a white van stopped on the left side of the street, opens the driver's side door, and gets inside.
- ruled out: A second white van stops in a similar location later in the video (around 132.03s), but no one gets into or out of it. There are also several parked cars on the left side of the street throughout the video, but no individuals are seen interacting with their doors or getting inside.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk

- **match** `exact` / conf `high` at 60.0-64.0s (clearest 62.0s)
  - subject: a pedestrian and a black SUV
  - A pedestrian is crossing the top crosswalk on the right side while a black SUV drives straight down through the left side of the same crosswalk.
- ruled out: From 44.03s to 48.03s, pedestrians are in the top crosswalk while a black car drives horizontally through the intersection. However, the black car passes through the left and right crosswalks, not the top crosswalk where the pedestrians are.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians

- **absent**
  - why not: No cyclist or e-bike rider is seen riding along any of the visible sidewalks at any point in the video.
- ruled out: Several cyclists are visible in the video, but they are either crossing the intersection in the crosswalks (e.g., at 36.03s and 154.03s) or riding in the street (e.g., at 114.03s and 162.03s). I examined these candidates, but none of them are riding on a sidewalk.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic

- **match** `exact` / conf `high` at 110.0-122.0s (clearest 114.0s)
  - subject: cyclist
  - A cyclist rides down the avenue in the lane designated for traffic moving in the opposite direction.
- ruled out: Several cyclists are seen using the crosswalks to cross the intersection (e.g., at 46.03s, 102.03s, 126.03s, 144.03s, 154.03s). These instances were rejected because crossing at a crosswalk is not the same as riding against the flow of traffic in a vehicular lane.

### [emergency] an emergency vehicle with lights flashing passing through the intersection

- **match** `exact` / conf `high` at 30.0-34.0s (clearest 32.0s)
  - subject: police car
  - A police car with its emergency lights flashing travels through the intersection from right to left.
- ruled out: No other emergency vehicles are seen in the video.

### [negative] two vehicles making contact with each other

- **absent**
  - why not: While there is a major vehicle failure in the scene, there is no instance of two distinct vehicles colliding or otherwise making physical contact with each other.
- ruled out: Between 094.03s and 100.03s, an articulated bus taking a right turn breaks in half, leaving its rear section stranded in the intersection. This was rejected because it involves a single vehicle experiencing a structural failure, rather than two separate vehicles making contact (colliding) with each other.

### [negative] a horse-drawn carriage

- **absent**
  - why not: No horse-drawn carriage appears in the video.
- ruled out: I looked for a horse-drawn carriage throughout the video. I saw many vehicles, including cars, vans, an articulated bus, a USPS truck, and a yellow taxi, as well as bicycles and pedestrians, but no horse-drawn carriages appeared at any point.

---

10 call(s) ok, 0 failed, 1013274 in / 20784 out tokens