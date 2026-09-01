# probe run: events-key_0825-1700_fps1_n5_batch_0901-0451

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 1 | whole range, one call
- frames per call: 181 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/events-key_0825-1700_fps1_n5_batch_0901-0451`

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

- **match** `exact` / conf `high` at 112.0-117.0s (clearest 114.0s)
  - subject: white box truck
  - The truck begins a left turn, stops in the middle of the intersection to wait for a pedestrian in the crosswalk, and then completes its turn once the path is clear.
- ruled out: A police SUV turning left at 32.03s and various cars making turns were considered, but they maintained continuous movement through the intersection without pausing.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **match** `exact` / conf `high` at 126.0-130.0s (clearest 128.0s)
  - subject: driver of a white van
  - A white van stops in the left-hand lane, and the driver opens the door, steps out onto the roadway, closes the door, and begins walking toward the curb.
- ruled out: Several parked vehicles in the designated spaces on the left were monitored, but no passengers were seen entering or exiting them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 1)

- **match** `superficial` / conf `high` at 104.0-124.0s (clearest 110.0s)
  - subject: blue articulated bus
  - A blue articulated bus pulls up to a bus stop on the far left side of the street and waits there for an extended period. However, due to the distance and the angle, no people can be clearly seen getting on or off.
- ruled out: Other buses that passed through the intersection without stopping were ruled out.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 1)

- **match** `exact` / conf `high` at 20.0-25.0s (clearest 22.0s)
  - subject: pedestrian
  - A pedestrian steps off the sidewalk and walks horizontally across the lower avenue, well away from the marked crosswalks at the intersection.
- ruled out: Other pedestrians were observed crossing the same lower section at different times (e.g., around 10.03s and 34.03s), which also represent valid instances of this behavior.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 0.0s)
  - subject: roadway
  - The upper part of the intersection contains a marked construction zone containing orange cones, barriers, and multiple workers moving around in the carriageway.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: Traffic flows normally through the intersection without any vehicles making physical contact with each other.
- ruled out: Vehicles maneuvering closely through the intersection, or pausing to avoid pedestrians, were examined for any potential collisions.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: No horses or horse-drawn carriages are present in the footage.
- ruled out: The sequence was broadly scanned for any non-motorized transport.

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **absent**
  - why not: Although an emergency vehicle appears, its flashing lights are not turned on.
- ruled out: A marked police SUV is seen turning left through the intersection from 32.03s to 34.03s, but it was ruled out because its roof lights are entirely inactive.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 2)

- **match** `exact` / conf `high` at 111.0-118.0s (clearest 114.0s)
  - subject: white box truck
  - A white box truck enters the intersection from the right, begins to turn left, but stops in the middle of the intersection to wait for a crossing pedestrian. It remains stationary for a few seconds before completing the turn.
- ruled out: Other vehicles turning through the intersection, such as the dark SUV at t=91.03s, complete their turns without stopping part-way through.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **match** `exact` / conf `high` at 169.0-178.0s (clearest 170.0s)
  - subject: driver of a black car
  - The driver's door of a black car parked in the angled parking lane opens. The driver steps out of the car, closes the door, and walks towards the sidewalk.
- ruled out: A white van pulls over on the bottom right side of the street around t=68.03s, but no one gets into or out of it.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 2)

- **absent**
  - why not: While buses are present, none stop to pick up or drop off passengers.
- ruled out: Several articulated blue buses drive through the intersection (e.g., passing from left to right at t=85.03s and driving straight top-to-bottom at t=95.03s). However, none of these buses stop at the kerb or allow passengers on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 2)

- **match** `exact` / conf `high` at 8.0-15.0s (clearest 11.0s)
  - subject: pedestrian in a white top
  - A pedestrian crosses the road with the angled parking diagonally, navigating between parked cars and a moving white car, completely outside of the designated crosswalk markings.
- **match** `exact` / conf `high` at 52.0-56.0s (clearest 54.0s)
  - subject: pedestrian in dark clothing
  - Another pedestrian walks across the same roadway from the angled parking side to the right sidewalk, well away from the marked crosswalk.
- ruled out: Pedestrians crossing within or immediately adjacent to the crosswalk markings were not counted as they were using the designated crossing area.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: the intersection roadway
  - The top-left crosswalk and part of the adjacent roadway are cordoned off with orange cones and barriers. Several construction workers in high-visibility yellow vests are standing and working in the roadway for the entire duration of the clip.
- ruled out: N/A

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: No physical contact or collision between any vehicles is observed in the footage.
- ruled out: Vehicles often pass closely by one another as they navigate the intersection or yield to turning traffic, but they do not hit each other.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: No horse-drawn carriages appear in the frames.
- ruled out: All vehicles passing through the intersection are modern motorized vehicles; no animal-drawn vehicles were observed.

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.0s)
  - subject: NYPD police vehicle
  - An NYPD police SUV enters the intersection from the left with its roof light bar visibly flashing. It turns right and proceeds up the top road.
- ruled out: Other service vehicles, like the white USPS box truck (t=112.03s), pass through but do not display flashing emergency lights.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 3)

- **match** `exact` / conf `high` at 92.0-97.0s (clearest 95.0s)
  - subject: a black SUV
  - The SUV turns right from the top street onto the left-heading street but stops midway through the turn, waiting for pedestrians to clear the crosswalk, before continuing.
- ruled out: I examined other turning vehicles throughout the sequence, but most completed their turns smoothly without stopping or significantly slowing down.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **absent**
  - why not: No one is seen entering or exiting any vehicles; all parked cars remain closed and inactive.
- ruled out: I checked the vehicles parked along the streets, particularly the ones on the left side, but no activity was observed around them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 3)

- **absent**
  - why not: While buses are present, none stop at a kerb or open their doors for passengers.
- ruled out: An articulated MTA bus passes through the intersection between 86.03s and 104.03s, and another standard bus is visible entering from the top right, but both move continuously without stopping at a kerb.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 3)

- **match** `exact` / conf `high` at 11.0-20.0s (clearest 15.0s)
  - subject: a pedestrian
  - A pedestrian steps into the bottom street well outside of the marked crosswalk and walks diagonally across the roadway, reaching the opposite side between parked cars.
- ruled out: I also observed another pedestrian crossing mid-block at the bottom of the frame between 33.03s and 39.03s, which was another exact match for the query.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: the top roadway area
  - Orange construction barriers, cones, and workers wearing high-visibility vests occupy a section of the roadway and crosswalk in the top street area for the duration of the clip.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: Traffic flows normally throughout the clip; no vehicles hit or scrape against one another.
- ruled out: I monitored close encounters, such as the articulated bus navigating the intersection alongside cars, but there were no collisions.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: Only motorized vehicles and bicycles are visible; there are no animal-drawn vehicles in the sequence.
- ruled out: I checked all moving vehicles crossing the intersection.

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **match** `exact` / conf `high` at 31.0-36.0s (clearest 32.0s)
  - subject: a police car
  - A police SUV with its rooftop emergency lights flashing enters from the right street and travels straight across the intersection to the left.
- ruled out: I checked for other emergency vehicles but this was the only one that appeared.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 4)

- **match** `exact` / conf `high` at 21.0-25.0s (clearest 23.0s)
  - subject: a white car
  - A white car turning left from the bottom-right road to the top-left road stops in the middle of the intersection to yield to pedestrians in the crosswalk before completing its turn.
- ruled out: Other turning vehicles, such as the articulated buses or vans, were considered, but they generally completed their turns smoothly or only slowed down without coming to a near or complete stop.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **absent**
  - why not: No person is seen entering or exiting a stopped car, van, or taxi during the video.
- ruled out: Several pedestrians are observed walking near the parked cars on the bottom-left road and the construction vehicles on the top-right, but none are seen opening a vehicle door or getting in or out.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 4)

- **match** `exact` / conf `high` at 0.0-10.0s (clearest 4.0s)
  - subject: a blue MTA bus
  - A blue public transit bus is stopped at the kerb on the top-left road. Passengers are visible waiting and moving near the doors before the bus eventually pulls away.
- ruled out: Other articulated buses pass through the intersection later in the video, but they do not stop at a kerb to load or unload passengers within the camera's view.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 4)

- **match** `exact` / conf `high` at 61.0-66.0s (clearest 63.0s)
  - subject: a pedestrian
  - A pedestrian in dark clothing walks diagonally across the very center of the intersection, cutting through the active roadway entirely outside of the marked crosswalks.
- ruled out: While many pedestrians cross using the designated crosswalks and construction workers move around the barricaded zone, this specific individual crosses straight through the middle of the intersection away from all markings.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: the roadway
  - An active construction zone is present in the top-right quadrant of the intersection for the entire duration of the video, featuring orange barriers, cones, and workers in high-visibility vests standing in the carriageway.
- ruled out: The construction is ongoing and stationary, so there was no need to reject any parts of the video; it is a continuous match.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: No vehicles are seen colliding or making contact with one another in the footage.
- ruled out: There are instances where long articulated buses or turning vehicles negotiate tight turns close to other traffic, but no physical contact or collision occurs at any point.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: There are no horse-drawn carriages visible in the intersection.
- ruled out: All observed traffic consists of motorized vehicles (cars, vans, buses, trucks, SUVs) and bicycles.

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **match** `exact` / conf `high` at 9.0-13.0s (clearest 11.0s)
  - subject: a police car
  - A white police car with its emergency lights flashing drives straight through the intersection, coming from the bottom-left road and continuing to the top-right road.
- ruled out: Another police SUV turns right through the intersection with its lights flashing around 31.03s, which also satisfies the query, but the first occurrence is an equally clear example.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 5)

- **match** `exact` / conf `high` at 107.0-112.0s (clearest 109.0s)
  - subject: a dark car turning left
  - The car begins a left turn from the top roadway but stops before the crosswalk to wait for pedestrians to finish crossing before proceeding.
- ruled out: Other turning vehicles, such as the police car at 32.03s or the white van at 30.03s, were considered but they completed their turns without needing to stop.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **match** `exact` / conf `high` at 14.0-18.0s (clearest 16.0s)
  - subject: a person in the dark car parked on the left
  - After backing into a diagonal parking spot on the left side of the street, the driver opens the door, steps out of the car, and walks away towards the sidewalk.
- ruled out: Several other cars are parked on the street, but no one is seen entering or exiting them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 5)

- **absent**
  - why not: No bus stops at the kerbside to pick up or drop off passengers during the video.
- ruled out: An articulated bus drives through the intersection starting at 85.03s. It stops due to traffic/signals, but it is not stopped at the kerb and no passengers board or alight.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 5)

- **match** `exact` / conf `high` at 121.0-127.0s (clearest 124.0s)
  - subject: a pedestrian
  - A pedestrian crosses the main roadway diagonally, walking well outside of the designated crosswalks, from the parked cars on the left to the sidewalk on the right.
- ruled out: Most pedestrians use the marked crosswalks near the intersection.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: the construction zone
  - There is a visible construction zone at the top of the intersection involving orange barriers, cones, and workers in high-visibility vests occupying the crosswalk and parts of the carriageway.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: No collisions or contact between vehicles occur in the footage.
- ruled out: The flow of traffic was monitored, but vehicles maintain appropriate distances or yield to each other successfully.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: There are no horse-drawn carriages present in the video.
- ruled out: All vehicles in the scene were examined, and all are motor vehicles (cars, vans, buses, trucks).

### [negative] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **absent**
  - why not: No emergency vehicles with active flashing lights pass through the scene.
- ruled out: A police vehicle drives through the intersection at 32.03s, but its roof lights are not illuminated or flashing.

---

5 call(s) ok, 0 failed, 1006400 in / 30430 out tokens