# probe run: events-key_0825-1700_fps2_n5_batch_0901-0459

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 2 | whole range, one call
- frames per call: 361 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/events-key_0825-1700_fps2_n5_batch_0901-0459`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| bus-dwell | 0/1 | 0/1 | 1/1 |  |
| negative | 0/3 | 2/3 | 1/3 | ground truth known: all absent |
| ped-midblock | 1/1 | 0/1 | 0/1 |  |
| pickup-car | 0/1 | 0/1 | 1/1 |  |
| roadworks | 1/1 | 0/1 | 0/1 |  |
| turn-halt | 1/1 | 0/1 | 0/1 |  |

### queries whose samples disagreed

- pickup-car — a person getting into or out of a stopped car, van or taxi
- bus-dwell — a bus stopped at the kerb with people getting on or off it
- negative — an emergency vehicle with its lights flashing passing throug

## per query

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 1)

- **match** `exact` / conf `high` at 28.5-32.0s (clearest 30.0s)
  - subject: white car
  - A white car enters the intersection from the right to turn left. It stops part-way through the turn to yield to an oncoming silver SUV, then continues its turn once the path is clear.
- ruled out: Examined many other vehicles making turns (e.g., the articulated buses at 90.03s and 104.03s, and the police SUV at 33.03s), but they all maintained their momentum through the turn without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **absent**
  - why not: No one is observed entering or exiting a vehicle during the footage.
- ruled out: Scanned the parked cars along the left curb and vehicles that pulled over or paused (such as the taxi at 178.53s), but while pedestrians walk past the parked cars, none are seen opening doors or getting into or out of any vehicle.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 1)

- **match** `exact` / conf `high` at 0.0-14.5s (clearest 5.0s)
  - subject: MTA city bus
  - An MTA bus is stopped at the kerb in the upper left corner of the frame, near a red awning. Passengers are clustered by the doors. The bus eventually pulls away at 14.53s.
- ruled out: Observed two articulated MTA buses passing through the intersection (around 90.03s and 104.03s), but they navigated turns without pulling over or stopping for passengers.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 1)

- **match** `exact` / conf `high` at 10.5-14.5s (clearest 12.5s)
  - subject: pedestrian in a blue shirt
  - A pedestrian emerges from between the parked cars on the lower left side of the street and crosses the roadway diagonally to the right, well away from the marked crosswalks at the intersection.
- ruled out: Many pedestrians cross correctly at the marked intersection lines, and some construction workers step into the street within the work zone, but only the individual crossing midway down the block clearly jaywalks across the active traffic lanes.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction zone
  - The top half of the intersection is an active construction site, delineated by bright orange barriers and traffic cones, with multiple workers in high-visibility vests standing in the roadway guiding traffic and working.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: No collisions or physical contact between vehicles occur in the sequence.
- ruled out: Observed instances where turning vehicles passed close to oncoming traffic (like the white car yielding at 29.53s), but all vehicles successfully avoided each other without making contact.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: There are no horse-drawn carriages present in the footage.
- ruled out: Observed many types of vehicles, including large buses and delivery trucks, but no animal-drawn vehicles.

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 31.5-35.0s (clearest 32.5s)
  - subject: NYPD police SUV
  - An NYPD police SUV with its roof light bar actively flashing enters the intersection from the left, executes a left turn, and heads down the vertical street.
- ruled out: Other municipal or utility vehicles were seen in the scene (like postal trucks), but none exhibited active, flashing emergency lights.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 2)

- **match** `exact` / conf `high` at 32.0-36.0s (clearest 33.5s)
  - subject: white police car
  - The police car begins a left turn in the intersection, stops to wait for oncoming traffic to clear, and then proceeds to complete the turn.
- ruled out: Other vehicles turning through the intersection were observed but they completed their turns smoothly without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **match** `exact` / conf `high` at 126.5-128.5s (clearest 127.5s)
  - subject: pedestrian and parked black SUV
  - A pedestrian approaches the driver's side of a black SUV parked in the diagonal spaces on the bottom left, opens the door, and gets inside.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 2)

- **absent**
  - why not: No bus stops at a kerb to allow passengers to board or alight during the video.
- ruled out: A bus stop with waiting passengers is visible in the top left, and two MTA buses pass through the intersection during the video, but neither stops to pick up or drop off passengers.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 2)

- **match** `exact` / conf `high` at 10.5-13.5s (clearest 11.5s)
  - subject: pedestrian
  - A pedestrian crosses the main vertical roadway from right to left, significantly further down the block than the marked crosswalk at the intersection.
- ruled out: Many pedestrians are seen crossing within the designated crosswalks at the intersection, which does not fit the query.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 84.0s)
  - subject: construction site
  - A section of the roadway in the upper part of the intersection is cordoned off with orange barriers and cones, and construction workers in high-visibility vests are actively working in the carriageway.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: No vehicles make physical contact or collide during the video.
- ruled out: Vehicles maneuver around each other and the construction zone, but all maintain separation.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: There are no horse-drawn carriages present in the footage.

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 31.5-36.5s (clearest 33.5s)
  - subject: white police car
  - A police vehicle with its roof lights flashing actively enters the intersection, stops briefly, and then passes through by turning left.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 3)

- **match** `exact` / conf `high` at 67.5-75.0s (clearest 70.5s)
  - subject: dark SUV turning left
  - A dark SUV turning left into the bottom-left roadway stops in the middle of the intersection to wait for an oncoming white SUV to pass before completing its turn.
- ruled out: A dark SUV turning left at 10.03s also stops part-way through its turn to yield to a pedestrian in the crosswalk.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **absent**
  - why not: No one gets into or out of a stopped vehicle in the scene.
- ruled out: Several vehicles are parked along the road on the left, but no one is seen opening a door to enter or exit them during the video.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 3)

- **absent**
  - why not: No buses stop at the kerb in this video.
- ruled out: An articulated bus passes through the intersection starting at 88.03s, but it is moving through traffic and does not stop at the curb.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 3)

- **match** `exact` / conf `high` at 24.0-37.0s (clearest 30.5s)
  - subject: pedestrian crossing the road
  - A pedestrian crosses the bottom-left roadway from the left sidewalk to the right side, walking completely outside the marked crosswalk area.
- ruled out: Another pedestrian crosses the same roadway outside the crosswalk starting around 115.53s.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction site in roadway
  - Throughout the entire video, a section of the upper roadway is closed off with orange barriers and cones, and construction workers wearing high-visibility vests are standing and working in the carriageway.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: No vehicles crash or make contact with one another.
- ruled out: Multiple vehicles navigate the intersection and yield to each other, but no collisions or contact occur.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: There are no horses or horse-drawn carriages in the scene.

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **absent**
  - why not: No emergency vehicles use flashing lights while passing through the frame.
- ruled out: Police vehicles pass through the intersection at 8.53s and 31.03s, but neither has its emergency lights flashing.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 4)

- **match** `exact` / conf `high` at 134.5-147.5s (clearest 140.0s)
  - subject: grey car
  - A grey car begins a left turn but stops in the middle of the intersection for several seconds to wait for a gap in oncoming traffic before completing the maneuver.
- **match** `exact` / conf `high` at 148.0-155.0s (clearest 151.5s)
  - subject: dark SUV
  - A dark SUV making a right turn stops part-way through the turn to yield to a pedestrian crossing the street, then continues.
- ruled out: A blue articulated bus takes a very long time to negotiate a left turn (78.53s-116.03s) and moves extremely slowly, but is generally inching forward continuously rather than coming to a clear stop.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **absent**
  - why not: No people enter or exit any vehicles during the video.
- ruled out: Several cars and a van are parked along the bottom left and top right edges of the roadway, and pedestrians walk near them, but no one is ever seen opening a door, getting in, or stepping out.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 4)

- **absent**
  - why not: No bus stops at a kerb to drop off or pick up passengers.
- ruled out: A blue MTA articulated bus slowly navigates the intersection from 78.53s to 116.03s, but it is turning and actively in traffic. There is a bus stop visible on the top left side of the street, but no bus pulls up to it.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 4)

- **match** `exact` / conf `high` at 107.0-125.0s (clearest 116.5s)
  - subject: pedestrian in light-coloured top
  - A pedestrian steps into the street well south of the marked crosswalk on the left side and walks diagonally across the intersection to the scaffolding on the right.
- ruled out: Other pedestrians can be seen briefly straying just outside the crosswalk lines while crossing, but are largely following the crosswalk path.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 0.0s)
  - subject: construction zone
  - The roadway approaching from the top is partially blocked off by orange cones and barriers, and construction workers wearing high-visibility vests are standing in the roadway.
- ruled out: The scaffolding structure over the sidewalk on the right is a related but separate construction element, but the active work in the street itself perfectly satisfies the query.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: No vehicles make contact with one another.
- ruled out: Traffic moves through the intersection normally, and vehicles occasionally come into close proximity (such as waiting behind crosswalks or passing the large turning bus), but no collisions occur.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: There are no horse-drawn carriages in the scene.
- ruled out: I looked for any animal-drawn vehicles mixed in with the motor traffic, but only standard motorised vehicles and bicycles were present.

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **absent**
  - why not: No emergency vehicle passes through with flashing lights.
- ruled out: Police vehicles pass through the intersection at 9.53s and 31.53s, but they are driving normally in traffic and their emergency lights are turned off.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 5)

- **match** `exact` / conf `high` at 176.5-180.0s (clearest 178.5s)
  - subject: yellow cab
  - A yellow cab enters the intersection to turn left, slows down significantly, and almost comes to a complete stop before continuing through the crosswalk.
- ruled out: Other turning vehicles, such as a blue bus turning right earlier, complete their turns without stopping or significantly hesitating in the intersection.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **absent**
  - why not: No one is observed getting into or out of a stopped vehicle in the provided frames.
- ruled out: Several vehicles are parked along the left side of the street and a white van is parked on the right, but no individuals are seen entering or exiting any of these stationary vehicles during the clip.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 5)

- **absent**
  - why not: No bus stops at the kerb for passengers in the provided frames.
- ruled out: An articulated bus drives straight through the intersection (t=88.53s to t=109.03s), stopping briefly for a traffic light, but it stays in the travel lanes and does not pull over to the kerb to pick up or drop off passengers.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 5)

- **match** `exact` / conf `high` at 144.0-150.0s (clearest 146.5s)
  - subject: pedestrian
  - A pedestrian enters the roadway from the right side, well below the marked crosswalk, and walks diagonally across the street towards the left side.
- ruled out: There are several instances of pedestrians walking in the roadway outside of crosswalks in this video. The one highlighted is a clear example of someone crossing from one side to the other away from the markings.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 0.0s)
  - subject: intersection
  - The upper portion of the intersection is actively under construction, marked by numerous orange traffic cones, orange mesh barriers, and workers wearing high-visibility vests.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: No collisions or contact between vehicles occur in the video.
- ruled out: Traffic flows through the intersection and vehicles stop for red lights, but all vehicles maintain distance from each other.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: There is no horse-drawn carriage visible in the video.
- ruled out: Various cars, vans, trucks, and a bus are seen passing through the intersection, but none are horse-drawn.

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **absent**
  - why not: While emergency vehicles are present, none of them have flashing lights active while passing through.
- ruled out: NYPD police vehicles pass through the intersection at t=9.53s and t=31.53s. However, their emergency lights are not flashing.

---

5 call(s) ok, 0 failed, 2003950 in / 22369 out tokens