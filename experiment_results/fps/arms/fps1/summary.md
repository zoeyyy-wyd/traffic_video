# probe run: fps1

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 1 | whole range, one call
- frames per call: 181 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/fps/fps1`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| bus-dwell | 0/1 | 0/1 | 1/1 |  |
| emergency | 1/1 | 0/1 | 0/1 |  |
| emergency-dark | 0/1 | 0/1 | 1/1 |  |
| negative | 0/2 | 2/2 | 0/2 | ground truth known: all absent |
| ped-midblock | 1/1 | 0/1 | 0/1 |  |
| pickup-car | 1/1 | 0/1 | 0/1 |  |
| roadworks | 1/1 | 0/1 | 0/1 |  |
| skateboard | 0/1 | 0/1 | 1/1 |  |
| turn-halt | 1/1 | 0/1 | 0/1 |  |

### queries whose samples disagreed

- bus-dwell — a bus stopped at the kerb with people getting on or off it; 
- skateboard — a person riding a skateboard
- emergency-dark — an emergency vehicle passing through the intersection with i

## per query

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 1)

- **match** `exact` / conf `high` at 178.0-180.0s (clearest 179.0s)
  - subject: yellow taxi
  - A yellow taxi begins a left turn from the cross street but stops partway through the turn in the middle of the intersection, remaining halted until the video ends.
- ruled out: Other turning vehicles, such as the white van at 30.03s or the articulated bus at 90.03s, slow down to make the turn but do not come to a stop partway through it.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **match** `exact` / conf `high` at 112.0-114.0s (clearest 113.0s)
  - subject: driver of white van
  - A person opens the driver-side door of a parked white van on the left side of the street, steps out, and shuts the door.
- ruled out: A few other vehicles park along the street during the video, but no one gets into or out of them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 1)

- **absent**
  - why not: No bus stops at a kerb to load or unload passengers during the time window.
- ruled out: A standard blue bus passes through at 85.03s and an articulated bus turns through at 90.03s, but neither stops at the kerb to let passengers on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 1)

- **match** `exact` / conf `high` at 15.0-18.0s (clearest 17.0s)
  - subject: pedestrian
  - A pedestrian steps off the right kerb well away from the crosswalk markings and walks across the main road, reaching the left kerb.
- **match** `exact` / conf `high` at 120.0-125.0s (clearest 123.0s)
  - subject: pedestrian
  - A pedestrian steps off the right kerb mid-block and crosses the main road, arriving at the left kerb near a parked white van.
- **match** `exact` / conf `high` at 133.0-137.0s (clearest 135.0s)
  - subject: pedestrian
  - A pedestrian steps off the right kerb midway down the block and walks straight across to the left kerb.
- **match** `exact` / conf `high` at 163.0-167.0s (clearest 165.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb between parked cars and crosses the road directly to the right kerb.
- ruled out: Many pedestrians cross the street within the designated crosswalk markings, which does not match the query.

### [skateboard] a person riding a skateboard (sample 1)

- **match** `exact` / conf `high` at 121.0-134.0s (clearest 128.0s)
  - subject: person on a skateboard
  - A person riding a skateboard enters the top of the frame, glides straight through the intersection, and rolls down the right-hand traffic lane until leaving the shot.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction zone
  - Orange traffic cones, barriers, and workers wearing high-visibility safety vests occupy parts of the intersection and the cross street for the duration of the video.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 30.0-35.0s (clearest 32.0s)
  - subject: police car
  - An NYPD police car with its emergency lights flashing enters from the right and drives straight through the intersection, exiting out the left side.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 1)

- **absent**
  - why not: No emergency vehicles are seen traversing the intersection with their lights off.
- ruled out: The police car at 30.03s is an emergency vehicle, but its lights are flashing.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: No vehicles collide or make contact with each other in the video.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: There are no horses or carriages visible in the clip.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 2)

- **match** `exact` / conf `high` at 64.0-66.0s (clearest 65.0s)
  - subject: black car
  - A black car making a left turn stops in the middle of the intersection before resuming its movement to complete the turn.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **match** `exact` / conf `high` at 74.0-76.0s (clearest 75.0s)
  - subject: person and white van
  - A person opens the driver's door of the parked white van and steps out onto the roadway.
- **match** `exact` / conf `high` at 124.0-128.0s (clearest 126.0s)
  - subject: person and white van
  - A person approaches the parked white van, opens the driver's door, gets in, and closes the door.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 2)

- **absent**
  - why not: No bus stops at a kerb during the video.
- ruled out: Blue transit buses are seen passing through the intersection between 86.03s - 95.03s and 100.03s - 105.03s, but they are actively turning and do not stop at the kerb to let passengers board or alight.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 2)

- **match** `exact` / conf `high` at 9.0-17.0s (clearest 13.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses the roadway outside of the marked crosswalk, walking until they reach the scaffolding platform on the right.
- **match** `exact` / conf `high` at 111.0-117.0s (clearest 114.0s)
  - subject: pedestrian
  - A pedestrian steps off the right scaffolding platform and crosses the roadway entirely outside the crosswalk lines, arriving at the left kerb.
- **match** `exact` / conf `high` at 129.0-135.0s (clearest 132.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses the road below the marked crosswalk, walking until they reach the right scaffolding platform.
- **match** `exact` / conf `high` at 160.0-166.0s (clearest 163.0s)
  - subject: pedestrian
  - A pedestrian steps off the right scaffolding platform and walks straight across the roadway, outside the crosswalk, until reaching the left kerb.

### [skateboard] a person riding a skateboard (sample 2)

- **absent**
  - why not: No one is seen riding a skateboard at any point in the video.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction zone
  - The top half of the intersection is actively under construction, clearly marked with orange cones, barriers, and workers standing in the carriageway for the duration of the video.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 31.0-35.0s (clearest 33.0s)
  - subject: police vehicle
  - A police SUV drives straight through the intersection from left to right with its emergency roof lights flashing.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 2)

- **absent**
  - why not: No emergency vehicle passes through the intersection without its lights flashing.
- ruled out: A police vehicle passes through the intersection between 31.03s and 35.03s, but its emergency lights are actively flashing, failing the requirement that the lights NOT be flashing.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: No vehicles make contact or collide with each other in the video.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: There are no horse-drawn carriages present in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 3)

- **match** `exact` / conf `high` at 93.0-98.0s (clearest 95.0s)
  - subject: articulated bus
  - An articulated bus turning left into the lower street stops part-way through the turn, waiting before it moves off again.
- **match** `exact` / conf `high` at 106.0-108.0s (clearest 107.0s)
  - subject: dark SUV
  - A dark SUV turning left into the lower street comes to a stop in the middle of the intersection before continuing.
- **match** `exact` / conf `high` at 110.0-111.0s (clearest 110.0s)
  - subject: silver car
  - A silver car turning left briefly halts behind a white van in the intersection before moving off.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **match** `exact` / conf `high` at 111.0-115.0s (clearest 113.0s)
  - subject: person and white van
  - A person walks up to a parked white van, opens the driver's side door, gets in, and pulls the door shut.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 3)

- **absent**
  - why not: Buses pass through the intersection, but none stop at a kerb to allow passengers to get on or off.
- ruled out: The articulated bus that stops in the intersection at 93.03s does so due to traffic, not at a kerb, and no one boards or alights.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 3)

- **match** `exact` / conf `high` at 11.0-21.0s (clearest 16.0s)
  - subject: pedestrian in blue shirt
  - A pedestrian steps off the left kerb and crosses the lower street to the right side, far from the crosswalk markings.
- **match** `exact` / conf `high` at 34.0-41.0s (clearest 37.0s)
  - subject: pedestrian in grey shirt
  - A pedestrian steps off the right kerb and crosses the lower street to the left side, away from any crosswalk.
- **match** `exact` / conf `high` at 52.0-59.0s (clearest 55.0s)
  - subject: pedestrian in black shirt
  - A pedestrian steps off the left kerb and crosses the lower street to the right side, outside the crosswalk.
- **match** `exact` / conf `high` at 62.0-67.0s (clearest 64.0s)
  - subject: pedestrian in white shirt
  - A pedestrian steps off the right kerb and crosses to the left side of the lower street.
- **match** `exact` / conf `high` at 81.0-88.0s (clearest 84.0s)
  - subject: pedestrian in grey shirt
  - A pedestrian crosses the lower street from the left kerb to the right.
- **match** `exact` / conf `high` at 120.0-125.0s (clearest 122.0s)
  - subject: pedestrian in white shirt
  - A pedestrian crosses the lower street from the right kerb to the left.
- **match** `exact` / conf `high` at 130.0-136.0s (clearest 133.0s)
  - subject: pedestrian in dark shirt
  - A pedestrian crosses the lower street from the left kerb to the right.
- **match** `exact` / conf `high` at 138.0-144.0s (clearest 141.0s)
  - subject: pedestrian in dark shirt
  - A pedestrian crosses the lower street from the left kerb to the right.
- **match** `exact` / conf `high` at 153.0-159.0s (clearest 156.0s)
  - subject: pedestrian in black shirt
  - A pedestrian crosses the lower street from the right kerb to the left.
- **match** `exact` / conf `high` at 166.0-171.0s (clearest 168.0s)
  - subject: pedestrian in white shirt
  - A pedestrian crosses the lower street from the left kerb to the right.

### [skateboard] a person riding a skateboard (sample 3)

- **match** `exact` / conf `high` at 121.0-127.0s (clearest 124.0s)
  - subject: skateboarder
  - A person rides a skateboard smoothly across the intersection along the left crosswalk.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction zone
  - The intersection has cones, barriers, and workers present in the roadway for the entire duration of the clip.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **match** `exact` / conf `high` at 31.0-36.0s (clearest 33.0s)
  - subject: police car
  - A police car passes through the intersection, turning left, with its emergency light bar flashing brightly.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 3)

- **absent**
  - why not: The only emergency vehicle passing through has its emergency lights turned on and flashing.
- ruled out: The police car at 31.03s is an emergency vehicle, but its lights are actively flashing, so it fails the 'NOT flashing' condition.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: No vehicles collide or make contact with each other in the intersection.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: There are no horses or carriages seen in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 4)

- **match** `exact` / conf `high` at 134.0-137.0s (clearest 135.0s)
  - subject: white box truck
  - A white box truck turning left halts in the crosswalk to allow pedestrians to cross, before continuing its turn.
- ruled out: A black SUV turns left at 51.03s, but completes the turn in one continuous motion without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **match** `exact` / conf `high` at 110.0-113.0s (clearest 111.0s)
  - subject: driver of the white SUV
  - A person opens the driver's side door of a parked white SUV, steps out into the roadway, and closes the door.
- **match** `exact` / conf `high` at 138.0-141.0s (clearest 139.0s)
  - subject: driver of the black car
  - A person opens the door of a parked black car, gets out, and shuts the door behind them.
- **match** `exact` / conf `high` at 177.0-179.0s (clearest 178.0s)
  - subject: pedestrian
  - A person opens the driver's side door of the black car parked closest to the intersection, gets in, and closes the door.
- ruled out: Many vehicles pass through the intersection, but no one gets into or out of them while they are moving.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 4)

- **match** `exact` / conf `high` at 0.0-2.0s (clearest 1.0s)
  - subject: white and blue city bus
  - A city bus is stopped at the bus shelter kerb at the start of the video. It pulls away from the kerb and enters the intersection at 3.00s.
- ruled out: Several buses cross the intersection (e.g., at 86.03s, 98.03s, and 148.03s), but they are moving continuously in traffic and do not stop at a kerb.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 4)

- **match** `exact` / conf `high` at 121.0-127.0s (clearest 124.0s)
  - subject: pedestrian
  - A pedestrian steps off the kerb near the parked cars on the left and walks diagonally across the middle of the road to the scaffolding on the right, entirely outside the crosswalks.
- **match** `exact` / conf `high` at 160.0-165.0s (clearest 162.0s)
  - subject: pedestrian
  - A pedestrian steps off the top right kerb and walks diagonally through the middle of the intersection to the parked cars on the left, completely avoiding the marked crosswalks.
- ruled out: A pedestrian crosses the road at 20.03s, but they are using the marked crosswalk.

### [skateboard] a person riding a skateboard (sample 4)

- **match** `exact` / conf `high` at 110.0-118.0s (clearest 114.0s)
  - subject: person riding a skateboard
  - A person riding a skateboard travels up the road from the bottom edge of the frame, passing straight through the intersection towards the top right.
- ruled out: A person rides a bicycle through the intersection at 42.03s, not a skateboard.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: roadway construction zone
  - Construction barriers, traffic cones, and workers wearing high-visibility vests occupy the top-left road and crosswalk area continuously throughout the entire window.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.0s)
  - subject: police car
  - An NYPD police car with its roof lightbar actively flashing drives through the intersection, turning right.
- ruled out: A police car passes through at 9.03s, but its emergency lights are dark and not flashing.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 4)

- **match** `exact` / conf `high` at 9.0-11.0s (clearest 10.0s)
  - subject: police car
  - An NYPD police car passes straight through the intersection without its emergency roof lights flashing.
- ruled out: A police car drives through the intersection at 31.03s, but its lights are flashing.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: Traffic flows smoothly and no vehicles make contact or collide with each other in the video.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: No horses or horse-drawn carriages appear in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 5)

- **match** `exact` / conf `high` at 106.0-109.0s (clearest 107.0s)
  - subject: dark SUV
  - A dark SUV part-way through a left turn stops in the intersection, waits for a few seconds, and then moves off to complete the turn.
- ruled out: A dark SUV at 86.03s stops before entering the intersection to allow an articulated bus to make a wide left turn, but the SUV has not yet begun a turn itself.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **match** `exact` / conf `high` at 67.0-71.0s (clearest 68.0s)
  - subject: person
  - A person on the sidewalk approaches a dark SUV parked on the kerb, opens the door, and gets inside.
- ruled out: There are people walking past parked cars throughout the video, but they do not interact with them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 5)

- **absent**
  - why not: No event showing people actually boarding or alighting a stopped bus occurs within the video window.
- ruled out: A local bus pulls up to the bus stop in the top-left at 178.03s and stops, but the video ends before its doors open or anyone is seen getting on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 5)

- **match** `exact` / conf `high` at 11.0-22.0s (clearest 16.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses the roadway diagonally to the right, outside of any crosswalk markings.
- **match** `exact` / conf `high` at 34.0-45.0s (clearest 40.0s)
  - subject: pedestrian
  - A pedestrian crosses the roadway from the left kerb to the right side, outside the crosswalk.
- **match** `exact` / conf `high` at 50.0-55.0s (clearest 53.0s)
  - subject: pedestrian
  - A pedestrian quickly crosses the roadway from left to right, outside the marked crosswalk.
- **match** `exact` / conf `high` at 61.0-67.0s (clearest 64.0s)
  - subject: pedestrian
  - A pedestrian steps onto the roadway from the right side and crosses to the left kerb.
- **match** `exact` / conf `high` at 73.0-79.0s (clearest 76.0s)
  - subject: pedestrian
  - A pedestrian crosses the lower roadway from the left kerb to the right side.
- **match** `exact` / conf `high` at 101.0-105.0s (clearest 103.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses to the middle of the road before continuing out of view.
- **match** `exact` / conf `high` at 118.0-126.0s (clearest 122.0s)
  - subject: pedestrian
  - A pedestrian crosses the lower portion of the road from the right side to the left.
- **match** `exact` / conf `high` at 120.0-126.0s (clearest 123.0s)
  - subject: pedestrian
  - A pedestrian crosses the roadway from left to right.
- **match** `exact` / conf `high` at 131.0-138.0s (clearest 134.0s)
  - subject: pedestrian
  - A pedestrian crosses the lower roadway from right to left.
- ruled out: Many pedestrians cross within the marked crosswalks near the construction zone.

### [skateboard] a person riding a skateboard (sample 5)

- **match** `exact` / conf `high` at 133.0-138.0s (clearest 135.0s)
  - subject: person
  - A person on a skateboard rides down the center of the avenue, crossing through the intersection.
- ruled out: A bicyclist rapidly crosses the crosswalk at 35.03s, but they are riding a bicycle, not a skateboard.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 60.0s)
  - subject: construction area
  - A section of the road in the top-left crosswalk area is cordoned off with orange cones and barriers, and construction workers in yellow vests are standing and working in the carriageway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.0s)
  - subject: police car
  - A police car drives straight through the intersection with its roof emergency lights flashing.
- ruled out: Civilian vehicles drive through the intersection throughout the video, none having flashing emergency lights.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 5)

- **absent**
  - why not: No emergency vehicles without active flashing lights are seen passing through the intersection.
- ruled out: Several white vans and a mail truck pass through the intersection, but they are commercial vehicles rather than emergency vehicles.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: No collisions or vehicles making contact occur in the video.
- ruled out: At 86.03s, a dark SUV stops close to an articulated bus making a wide left turn, but the vehicles do not make contact.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: No horse-drawn carriages are present.

---

5 call(s) ok, 0 failed, 1005990 in / 50273 out tokens