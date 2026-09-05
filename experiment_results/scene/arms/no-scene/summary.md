# probe run: no-scene

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 1 | whole range, one call
- frames per call: 181 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/scene/no-scene`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| bus-dwell | 0/1 | 0/1 | 1/1 |  |
| emergency | 0/1 | 0/1 | 1/1 |  |
| emergency-dark | 0/1 | 0/1 | 1/1 |  |
| negative | 0/2 | 2/2 | 0/2 | ground truth known: all absent |
| ped-midblock | 1/1 | 0/1 | 0/1 |  |
| pickup-car | 0/1 | 0/1 | 1/1 |  |
| roadworks | 1/1 | 0/1 | 0/1 |  |
| skateboard | 1/1 | 0/1 | 0/1 |  |
| turn-halt | 1/1 | 0/1 | 0/1 |  |

### queries whose samples disagreed

- pickup-car — a person getting into or out of a stopped car, van or taxi
- bus-dwell — a bus stopped at the kerb with people getting on or off it; 
- emergency — an emergency vehicle with its lights flashing passing throug
- emergency-dark — an emergency vehicle passing through the intersection with i

## per query

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 1)

- **match** `exact` / conf `high` at 85.0-87.0s (clearest 86.0s)
  - subject: black car
  - A black car making a right turn from the vertical street onto the horizontal street stops at the crosswalk to allow a pedestrian to cross before continuing its turn.
- ruled out: Several other vehicles are seen making turns throughout the video, but they complete their turns without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **match** `exact` / conf `high` at 125.0-128.0s (clearest 126.0s)
  - subject: pedestrian
  - A person walks up to a black SUV parked at the curb on the lower left, opens the door, and gets inside, pulling the door shut.
- ruled out: Many pedestrians walk past parked cars on the sidewalks, but they do not interact with them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 1)

- **match** `exact` / conf `high` at 90.0-106.0s (clearest 98.0s)
  - subject: articulated bus
  - A long blue articulated bus arrives at the kerbside bus stop on the top left, boards/alights passengers, and then pulls away.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 1)

- **match** `exact` / conf `high` at 124.0-131.0s (clearest 127.0s)
  - subject: pedestrian
  - A pedestrian steps off the curb from between the parked cars on the lower left and walks diagonally across the middle of the active roadway to the right side.
- ruled out: Numerous pedestrians are seen crossing the intersection at the top using the marked crosswalks.

### [skateboard] a person riding a skateboard (sample 1)

- **match** `exact` / conf `high` at 169.0-175.0s (clearest 172.0s)
  - subject: person
  - A person riding a skateboard enters the frame from the top intersection, travelling down the middle of the vertical street before exiting at the bottom of the frame.
- ruled out: Bicycles and mopeds also use the roadway, but they have distinct rider postures and vehicle profiles from the skateboarder.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction site
  - The intersection in the top half of the frame features active construction, populated with orange barriers, cones, and workers in high-visibility vests throughout the entire video segment.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.0s)
  - subject: police SUV
  - A white police SUV crosses the intersection from left to right with its red and blue emergency roof lights flashing.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 1)

- **match** `exact` / conf `high` at 9.0-15.0s (clearest 12.0s)
  - subject: police car
  - An NYPD cruiser enters the intersection from the top left, executes a right turn, and drives down the vertical road. Its emergency lights remain turned off.
- ruled out: The police SUV appearing at 31 seconds has its flashing lights engaged, disqualifying it for this description.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: No collisions or other physical contact between vehicles occur in the footage.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: There are no horse-drawn carriages present; only motor vehicles and bicycles/skateboards traverse the roads.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 2)

- **match** `exact` / conf `high` at 31.0-33.0s (clearest 32.0s)
  - subject: white van
  - A white van turning left stops part-way through the turn to yield, then continues.
- **match** `exact` / conf `high` at 40.0-42.0s (clearest 41.0s)
  - subject: dark SUV
  - A dark SUV turning left stops in the intersection to yield to pedestrians, then moves off.
- **match** `exact` / conf `high` at 43.0-46.0s (clearest 44.0s)
  - subject: dark SUV
  - A dark SUV turning left pauses in the middle of the intersection to wait for the crosswalk to clear.
- **match** `exact` / conf `high` at 105.0-109.0s (clearest 107.0s)
  - subject: dark car
  - A dark car turning left stops for a few seconds part-way through its turn.
- **match** `exact` / conf `high` at 123.0-125.0s (clearest 124.0s)
  - subject: white van
  - A white van turning left stops midway through the turn before continuing.
- **match** `exact` / conf `high` at 141.0-143.0s (clearest 142.0s)
  - subject: black car
  - A black car making a left turn halts in the intersection to yield.
- **match** `exact` / conf `high` at 146.0-149.0s (clearest 147.0s)
  - subject: dark SUV
  - A dark SUV turning left comes to a stop in the crosswalk area before completing the turn.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **match** `exact` / conf `high` at 127.0-130.0s (clearest 128.0s)
  - subject: pedestrian
  - A person opens the driver's side door of a dark SUV parked on the left street and gets inside.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 2)

- **absent**
  - why not: No bus is clearly seen stopping with passengers actively boarding or alighting.
- ruled out: An articulated bus pulls over to the kerb on the far right at 91.03s and remains stopped for a while, but its doors are obscured by the scaffolding shed and no passengers can be seen getting on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 2)

- **match** `exact` / conf `high` at 9.0-13.0s (clearest 11.0s)
  - subject: construction worker
  - A worker in a high-visibility vest crosses the top right roadway from the median to the right kerb, away from any crosswalk.
- **match** `exact` / conf `high` at 17.0-21.0s (clearest 19.0s)
  - subject: pedestrian
  - A pedestrian crosses the top right roadway from the right kerb to the median.
- **match** `exact` / conf `high` at 24.0-28.0s (clearest 26.0s)
  - subject: construction worker
  - A worker crosses the top right roadway from the median to the right kerb.
- **match** `exact` / conf `high` at 44.0-47.0s (clearest 45.0s)
  - subject: pedestrian
  - A pedestrian crosses the top right roadway from the median to the right kerb.
- **match** `exact` / conf `high` at 50.0-53.0s (clearest 51.0s)
  - subject: two pedestrians
  - Two pedestrians cross the top right roadway side-by-side from the median to the right kerb.
- **match** `exact` / conf `high` at 53.0-56.0s (clearest 54.0s)
  - subject: pedestrian
  - A pedestrian crosses the left side street from the bottom kerb to the top kerb.
- **match** `exact` / conf `high` at 61.0-66.0s (clearest 63.0s)
  - subject: pedestrian
  - A pedestrian crosses the left side street diagonally from the top corner to the bottom kerb.
- **match** `exact` / conf `high` at 73.0-76.0s (clearest 74.0s)
  - subject: pedestrian
  - A pedestrian crosses the left side street from the bottom kerb to the top kerb.
- **match** `exact` / conf `high` at 78.0-81.0s (clearest 79.0s)
  - subject: pedestrian
  - A pedestrian crosses the left side street from the top kerb to the bottom kerb.
- **match** `exact` / conf `high` at 86.0-89.0s (clearest 87.0s)
  - subject: pedestrian
  - A pedestrian crosses the left side street from the bottom kerb to the top kerb.
- **match** `exact` / conf `high` at 100.0-104.0s (clearest 102.0s)
  - subject: pedestrian
  - A pedestrian crosses the left side street from the bottom kerb to the top kerb.
- **match** `exact` / conf `high` at 109.0-111.0s (clearest 110.0s)
  - subject: pedestrian
  - A pedestrian crosses the top right roadway from the median to the right kerb.
- **match** `exact` / conf `high` at 114.0-116.0s (clearest 115.0s)
  - subject: pedestrian
  - A pedestrian crosses the top right roadway from the right kerb to the median.
- **match** `exact` / conf `high` at 123.0-127.0s (clearest 125.0s)
  - subject: pedestrian
  - A pedestrian walks diagonally down the left side street from the corner to a parked car.
- **match** `exact` / conf `high` at 133.0-136.0s (clearest 134.0s)
  - subject: pedestrian
  - A pedestrian crosses the left side street from the top kerb to the bottom kerb.
- **match** `exact` / conf `high` at 138.0-141.0s (clearest 139.0s)
  - subject: pedestrian
  - A pedestrian crosses the left side street from the bottom kerb to the top kerb.
- **match** `exact` / conf `high` at 151.0-154.0s (clearest 152.0s)
  - subject: pedestrian
  - A pedestrian crosses the top right roadway from the median to the right kerb.
- **match** `exact` / conf `high` at 157.0-160.0s (clearest 158.0s)
  - subject: pedestrian
  - A pedestrian crosses the left side street from the bottom kerb to the top kerb.
- **match** `exact` / conf `high` at 161.0-168.0s (clearest 164.0s)
  - subject: pedestrian
  - A pedestrian steps off the median on the bottom main road, walks down the road, and crosses to the left kerb.

### [skateboard] a person riding a skateboard (sample 2)

- **match** `exact` / conf `high` at 45.0-48.0s (clearest 46.0s)
  - subject: skateboarder
  - A person pushing on a skateboard crosses the main road in the crosswalk.
- **match** `exact` / conf `high` at 153.0-156.0s (clearest 154.0s)
  - subject: skateboarder
  - A person rides a skateboard across the left side street in the crosswalk.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction zone
  - The roadway at the top of the intersection is an active construction zone with orange barriers, cones, and workers present for the duration of the clip.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 30.0-35.0s (clearest 32.0s)
  - subject: police car
  - A police car with flashing emergency lights passes straight through the intersection from right to left.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 2)

- **absent**
  - why not: No emergency vehicles pass through the intersection without their lights flashing.
- ruled out: A police car passes through the intersection between 30.03s and 35.03s, but its emergency lights are flashing.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: No collisions or vehicle contacts occur in the video.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: No horse-drawn carriage appears in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 3)

- **match** `exact` / conf `high` at 94.0-98.0s (clearest 96.0s)
  - subject: an articulated MTA bus
  - The bus halts entirely while part-way through turning left, then resumes its turn.
- **match** `exact` / conf `high` at 107.0-110.0s (clearest 108.0s)
  - subject: a white car
  - The white car pauses in the middle of the intersection to allow pedestrians to cross before completing its left turn.
- ruled out: Several other vehicles turn left or right during the clip, but they do so in one continuous motion without halting.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **match** `exact` / conf `high` at 66.0-68.0s (clearest 67.0s)
  - subject: the driver of a white van
  - The driver opens the door of the parked white van, steps out onto the roadway, and closes the door.
- **match** `exact` / conf `high` at 143.0-145.0s (clearest 144.0s)
  - subject: the driver of a white van
  - The driver opens the door, climbs back into the parked white van, and shuts the door before driving away.
- **match** `exact` / conf `high` at 173.0-175.0s (clearest 174.0s)
  - subject: the driver of a silver car
  - The driver opens the door of the newly parked silver car, steps out, and closes the door.
- ruled out: A delivery worker interacts with the open side-door of the parked white van around 106.03s to retrieve items, but does not actually get into the vehicle.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 3)

- **absent**
  - why not: No bus stops to pick up or drop off passengers within the video window.
- ruled out: Several buses (both standard and articulated) pass through the intersection and turn corners, but none stop at the kerb to let passengers board or alight.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 3)

- **match** `exact` / conf `high` at 118.0-124.0s (clearest 121.0s)
  - subject: a pedestrian in a white t-shirt and dark pants
  - The pedestrian steps off the left kerb and walks diagonally across the main roadway, entirely outside of any crosswalk markings, until reaching the far side.
- ruled out: Construction workers frequently stand and walk in the roadway, but they are working in an active construction zone rather than crossing the street as regular pedestrians.

### [skateboard] a person riding a skateboard (sample 3)

- **match** `exact` / conf `high` at 130.0-139.0s (clearest 134.0s)
  - subject: a person on a skateboard
  - A person riding a skateboard glides through the intersection and continues down the middle of the road.
- ruled out: There are several bicyclists and someone on a scooter, but they do not match the requirement of a skateboard.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: the intersection and roadway
  - The top half of the intersection is actively under construction, populated with orange traffic cones, physical barriers, and workers in high-visibility clothing.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **absent**
  - why not: No emergency vehicles with flashing lights are seen in the video.
- ruled out: A police vehicle passes through the intersection at 31.03s, but its emergency lights are not flashing.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 3)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.0s)
  - subject: a police car
  - A police car enters from the top left street, crosses the intersection, and exits to the right without its emergency lights activated.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: No vehicles crash or make contact with each other in the footage.
- ruled out: Vehicles occasionally pull up close behind one another when stopping (e.g. behind the bus at 95.03s or behind the turning white car at 108.03s), but they stop safely and no collisions occur.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: There are no horses or carriages anywhere in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 4)

- **match** `exact` / conf `high` at 93.0-102.0s (clearest 97.0s)
  - subject: articulated bus
  - An articulated bus begins a right turn but stops part-way through the turn, remaining halted before finally moving off.
- ruled out: Several other vehicles yield briefly while turning, but they do not come to a full, extended halt mid-turn like the bus does.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **match** `exact` / conf `high` at 125.0-129.0s (clearest 127.0s)
  - subject: person
  - A person approaches the driver's side of a dark car parked on the left side of the street, opens the door, and gets inside.
- ruled out: Other people walk near the parked cars throughout the video, but they do not get into or out of them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 4)

- **absent**
  - why not: No bus stops to pick up or drop off passengers.
- ruled out: Several buses pass through the intersection during the video, but none of them stop at the kerb to allow passengers to board or alight.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 4)

- **match** `exact` / conf `high` at 18.0-22.0s (clearest 20.0s)
  - subject: pedestrian
  - A pedestrian steps off the right kerb and crosses the roadway outside the crosswalk to reach the median.
- **match** `exact` / conf `high` at 33.0-36.0s (clearest 34.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses the roadway to the median.
- **match** `exact` / conf `high` at 62.0-65.0s (clearest 63.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses the roadway to the median.
- **match** `exact` / conf `high` at 70.0-74.0s (clearest 72.0s)
  - subject: pedestrian
  - A pedestrian steps off the median and crosses the roadway to the left kerb.
- **match** `exact` / conf `high` at 84.0-87.0s (clearest 85.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses the roadway to the median.
- **match** `exact` / conf `high` at 112.0-116.0s (clearest 114.0s)
  - subject: pedestrian
  - A pedestrian steps off the right kerb and crosses the roadway to the median.
- **match** `exact` / conf `high` at 123.0-126.0s (clearest 124.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses the roadway to the median.
- **match** `exact` / conf `high` at 128.0-132.0s (clearest 130.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses the roadway to the median.
- **match** `exact` / conf `high` at 138.0-142.0s (clearest 140.0s)
  - subject: pedestrian
  - A pedestrian steps off the median and crosses the roadway to the right kerb.
- ruled out: Pedestrians who cross entirely within the painted crosswalk lines are not included.

### [skateboard] a person riding a skateboard (sample 4)

- **match** `exact` / conf `high` at 53.0-58.0s (clearest 55.0s)
  - subject: person
  - A person riding a skateboard travels quickly down the left side of the street, alongside the parked cars.
- ruled out: Several people are seen riding bicycles through the intersection, but only one is on a skateboard.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction zone
  - A construction zone is set up in the upper section of the intersection, complete with orange cones, barriers, and workers in high-visibility vests standing in the roadway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **match** `exact` / conf `high` at 31.0-35.0s (clearest 33.0s)
  - subject: police SUV
  - A police SUV with its emergency lights flashing turns right into the intersection and drives upwards.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 4)

- **match** `exact` / conf `high` at 25.0-29.0s (clearest 27.0s)
  - subject: police car
  - A police car drives straight through the intersection from left to right without its emergency lights flashing.
- ruled out: The police vehicle at 31.03s is rejected for this query because its lights are flashing.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: No vehicles make contact with one another.
- ruled out: There are instances where turning vehicles must yield to others or pedestrians, but no physical contact or collision occurs.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: There are no horse-drawn carriages present in the footage.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 5)

- **match** `exact` / conf `high` at 16.0-17.0s (clearest 16.0s)
  - subject: a dark car
  - A dark car turns left from the bottom road to the right road, stopping in the intersection to yield to an oncoming car.
- **match** `exact` / conf `high` at 46.0-48.0s (clearest 47.0s)
  - subject: a dark SUV
  - A dark SUV turns left from the bottom road to the right road, stopping in the intersection to yield to oncoming traffic.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **absent**
  - why not: No person is seen getting into or out of a stopped vehicle during the video.
- ruled out: There are several parked cars on the left side of the bottom road, but no one is seen opening their doors or entering/exiting them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 5)

- **absent**
  - why not: Buses pass through the scene but none stop at a kerb to serve passengers.
- ruled out: A blue articulated bus travels down the bottom road from 85.03s to 102.03s, and another blue bus travels leftwards on the top road at 97.03s. Neither of them stops at a kerb to allow passengers to board or alight.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 5)

- **match** `exact` / conf `high` at 11.0-17.0s (clearest 14.0s)
  - subject: a pedestrian
  - A pedestrian steps off the left kerb of the bottom road, below the marked crosswalk, and crosses to the right side.
- **match** `exact` / conf `high` at 121.0-127.0s (clearest 124.0s)
  - subject: a pedestrian
  - A pedestrian steps off the left kerb of the bottom road, well below the crosswalk, and crosses to the right side.
- ruled out: Several pedestrians cross the roads, but they do so inside the painted crosswalk lines.

### [skateboard] a person riding a skateboard (sample 5)

- **match** `exact` / conf `high` at 161.0-169.0s (clearest 165.0s)
  - subject: a person
  - A person riding a skateboard enters from the left road, crosses the intersection, and rides down the middle of the bottom road until exiting the frame.
- ruled out: There are people riding bicycles through the intersection (e.g. at 35.03s and 114.03s), but they are not riding skateboards.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: the roadway
  - The top street and the top-left corner of the intersection feature orange barriers, cones, and construction workers standing in the roadway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **absent**
  - why not: No emergency vehicles with active flashing lights pass through the scene.
- ruled out: A police car passes through at 32.03s and an ambulance at 78.03s. Neither has its emergency lights flashing.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 5)

- **match** `exact` / conf `high` at 32.0-36.0s (clearest 34.0s)
  - subject: a police car
  - A police car enters from the left road, turns into the top road, and passes through the intersection with its lights inactive.
- **match** `exact` / conf `high` at 78.0-85.0s (clearest 81.0s)
  - subject: an ambulance
  - An ambulance travels up the bottom road and turns into the left road, passing through the intersection without its lights flashing.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: No vehicles collide or make contact with each other in the recording.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: No horse-drawn carriages are present in the video.

---

5 call(s) ok, 0 failed, 1005990 in / 50479 out tokens