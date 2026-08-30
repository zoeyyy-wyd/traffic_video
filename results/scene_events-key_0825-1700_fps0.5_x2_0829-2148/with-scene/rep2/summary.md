# probe run: rep2

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 0.5 | whole range, one call
- frames per call: 91 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `/home/yw4636/traffic_video/runs/20260829-214844-scene/with-scene/rep2`

## by axis

| axis | answered present | note |
|---|---|---|
| bike-sidewalk | 0/1 |  |
| bike-wrongway | 1/1 |  |
| emergency | 0/1 |  |
| negative | 0/2 | ground truth known: all absent |
| ped-conflict | 1/1 |  |
| pickup-car | 1/1 |  |
| right-hook | 0/1 |  |
| stop-crosswalk | 0/1 |  |
| turn-fty | 1/1 |  |

## per query

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it

- **match** `exact` / conf `high` at 142.0-148.0s (clearest 146.0s)
  - subject: silver SUV
  - A silver SUV turns left into a crosswalk that a pedestrian is actively crossing.
- ruled out: A white USPS truck turns left at 114.03s, but there are no pedestrians in the crosswalk it passes through (there is a pedestrian in an adjacent crosswalk). An articulated bus turns right at 90.03s, but the crosswalk it enters is empty.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight

- **absent**
  - why not: While there are multiple cyclists who travel straight through the intersection, and several vehicles that make turns at various times, at no point does a vehicle turn across the path of a moving cyclist.
- ruled out: A white box truck turns left onto the vertical street (108.03s - 112.03s) shortly before a cyclist travels straight down that same street, but the truck merges into the lane ahead of the cyclist rather than turning across their path. A yellow taxi turns right (176.03s - 180.03s) near a cyclist, but the cyclist is stationary at the side of the road. A cyclist crosses in front of a car traveling straight (144.03s - 148.03s), but the vehicle is not turning.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to

- **absent**
  - why not: While there are several instances of vehicles stopping to yield to pedestrians in crosswalks throughout the video, in all clearly visible cases, the drivers stop their vehicles behind the stop lines and do not block the crosswalk markings with their vehicles.
- ruled out: I examined instances where vehicles yielded to crossing pedestrians, particularly at the top crosswalk (horizontal street). Between 146.03s and 156.03s, multiple pedestrians cross the street. A dark sedan approaching from the left stops (visible from 148.03s to 154.03s), and a white car approaching from the right stops (visible from 150.03s to 156.03s). However, both vehicles appear to stop correctly behind the stop line and their bodies do not encroach onto the zebra-striped crosswalk markings. I also reviewed a white van turning right between 114.03s and 118.03s while a pedestrian was in the bottom crosswalk, but the van kept moving and did not stop on the crosswalk.

### [pickup-car] a person getting into or out of a stopped car, van or taxi

- **match** `exact` / conf `high` at 44.0-52.0s (clearest 48.0s)
  - subject: the driver of the dark SUV
  - The driver opens the door of the newly parked dark SUV on the left side of the street, steps out of the vehicle, and walks away.
- ruled out: Between t=122.03s and t=128.03s, a pedestrian walks very close to the driver's side door of the highest parked black car on the left, making it look briefly as if they might be getting in. However, they do not open the door or enter the vehicle; they simply continue walking past it.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk

- **match** `exact` / conf `high` at 16.0-22.0s (clearest 20.0s)
  - subject: a pedestrian crossing the lower crosswalk
  - A pedestrian crosses the lower crosswalk from left to right while several vehicles traveling down the vertical street drive through the same crosswalk behind them.
- **match** `exact` / conf `high` at 36.0-42.0s (clearest 40.0s)
  - subject: a pedestrian crossing the lower crosswalk
  - A pedestrian crosses the lower crosswalk from right to left as a dark SUV and a white car traveling down the vertical street drive through the same crosswalk.
- **match** `exact` / conf `high` at 46.0-52.0s (clearest 48.0s)
  - subject: two pedestrians crossing the lower crosswalk
  - Two pedestrians walk together across the lower crosswalk from left to right while multiple vehicles traveling down the vertical street pass through the crosswalk concurrently.
- **match** `exact` / conf `high` at 78.0-84.0s (clearest 80.0s)
  - subject: a pedestrian crossing the lower crosswalk
  - A pedestrian crosses the lower crosswalk from right to left while a dark car and a white van traveling down the vertical street drive through the crosswalk.
- ruled out: During the first 10 seconds, several construction workers are standing in the upper crosswalk while vehicles pass through it. While this technically involves people on foot in a crosswalk simultaneously with vehicles, they are stationary workers occupying a closed lane rather than pedestrians actively using the crosswalk to cross the street. The matches selected represent clearer, less ambiguous examples of the requested situation, which occurs repeatedly in the lower crosswalk throughout the video.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians

- **absent**
  - why not: While cyclists are present in the intersection and roadways, no cyclist is observed riding along a sidewalk in the direction it runs, nor weaving among pedestrians on a sidewalk.
- ruled out: Several cyclists are visible in the video, but they are all riding in the roadway or crossing at crosswalks, not riding along a sidewalk. Examples include a cyclist travelling right-to-left on the horizontal street at t=34.03s-38.03s, a cyclist riding up the left side of the vertical street in the roadway at t=102.03s-108.03s, and another cyclist moving up the vertical street in the roadway at t=120.03s-126.03s.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic

- **match** `exact` / conf `high` at 104.0-112.0s (clearest 108.0s)
  - subject: cyclist
  - A cyclist travels from right to left through the intersection in the lower lanes of the horizontal street, riding against the left-to-right flow of traffic.
- **match** `exact` / conf `high` at 156.0-166.0s (clearest 160.0s)
  - subject: cyclist
  - A cyclist travels from right to left through the intersection in the lower lanes of the horizontal street, riding against the left-to-right flow of traffic.
- ruled out: Several other cyclists are seen navigating the intersection throughout the video (e.g., at 36s, 144s, and 150s). However, these riders are either positioned in the correct lane for their direction of travel or are using the pedestrian crosswalks.

### [emergency] an emergency vehicle with lights flashing passing through the intersection

- **absent**
  - why not: While an emergency vehicle (a police car) does pass through the intersection, it does not have its lights flashing as described in the prompt.
- ruled out: A police car travels through the intersection on the horizontal street from left to right between t=32.03s and t=36.03s. However, its emergency lights are not flashing.

### [negative] two vehicles making contact with each other

- **absent**
  - why not: No vehicles are observed colliding with or otherwise making contact with each other in the provided sequence.
- ruled out: Between t=92.03s and t=96.03s, a long articulated bus turns left through the intersection and passes close to several stopped cars, but no contact occurs.

### [negative] a horse-drawn carriage

- **absent**
  - why not: A horse-drawn carriage did not appear in the scene during this timeframe.
- ruled out: I scanned all the frames for a horse-drawn carriage. The intersection and roadways are occupied by various motor vehicles (cars, vans, buses, trucks) and pedestrians/cyclists, but no horse-drawn carriage appears at any point in the provided window.

---

10 call(s) ok, 0 failed, 1016414 in / 25219 out tokens