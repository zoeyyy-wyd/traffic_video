# probe run: with-scene

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 1 | whole range, one call
- frames per call: 181 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/scene/with-scene`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| bus-dwell | 0/1 | 0/1 | 1/1 |  |
| emergency | 1/1 | 0/1 | 0/1 |  |
| emergency-dark | 0/1 | 0/1 | 1/1 |  |
| negative | 0/2 | 2/2 | 0/2 | ground truth known: all absent |
| ped-midblock | 1/1 | 0/1 | 0/1 |  |
| pickup-car | 0/1 | 0/1 | 1/1 |  |
| roadworks | 1/1 | 0/1 | 0/1 |  |
| skateboard | 0/1 | 0/1 | 1/1 |  |
| turn-halt | 1/1 | 0/1 | 0/1 |  |

### queries whose samples disagreed

- pickup-car — a person getting into or out of a stopped car, van or taxi
- bus-dwell — a bus stopped at the kerb with people getting on or off it; 
- skateboard — a person riding a skateboard
- emergency-dark — an emergency vehicle passing through the intersection with i

## per query

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 1)

- **match** `exact` / conf `high` at 58.0-61.0s (clearest 59.0s)
  - subject: dark grey SUV
  - A dark grey SUV turns left from the vertical street onto the horizontal street, stopping mid-turn to wait for pedestrians before continuing.
- **match** `exact` / conf `high` at 86.0-88.0s (clearest 87.0s)
  - subject: black SUV
  - A black SUV turns left from the horizontal street to go down the vertical street, stopping in the crosswalk area before completing the turn.
- ruled out: Various vehicles make turns throughout the video without stopping mid-turn. They are ignored.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **absent**
  - why not: No one gets into or out of a stopped vehicle during the video.
- ruled out: Parked cars line the left side of the vertical street, but no one is seen opening doors or entering/exiting them at any point.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 1)

- **absent**
  - why not: No bus stops at a kerb to pick up or drop off passengers.
- ruled out: An articulated MTA bus passes through the intersection between 91.03s and 105.03s, but it merely navigates the turn and continues down the street without stopping at a kerb.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 1)

- **match** `exact` / conf `high` at 18.0-25.0s (clearest 21.0s)
  - subject: pedestrian
  - A pedestrian steps out from between parked cars on the left and walks across the vertical street, far below the crosswalk, reaching the right kerb.
- **match** `exact` / conf `high` at 109.0-116.0s (clearest 112.0s)
  - subject: skateboarder
  - A person riding a skateboard crosses the vertical street from right to left, well outside the marked crosswalks.
- **match** `exact` / conf `high` at 129.0-135.0s (clearest 132.0s)
  - subject: skateboarder
  - A person riding a skateboard crosses the vertical street from right to left, away from the crosswalk markings.
- **match** `exact` / conf `high` at 159.0-164.0s (clearest 161.0s)
  - subject: pedestrian
  - A pedestrian steps out from between parked cars on the left and walks across the vertical street, well below the crosswalk.
- ruled out: Pedestrians use the marked crosswalks at various times; they do not match the query as they are crossing at designated areas.

### [skateboard] a person riding a skateboard (sample 1)

- **match** `exact` / conf `high` at 109.0-116.0s (clearest 112.0s)
  - subject: skateboarder
  - A person is seen actively pushing and coasting on a skateboard, traveling right to left across the vertical street.
- **match** `exact` / conf `high` at 129.0-135.0s (clearest 132.0s)
  - subject: skateboarder
  - A person rides a skateboard, pushing with one foot and coasting across the vertical street from right to left.
- ruled out: Several cyclists pass through the intersection, but their posture and motion clearly indicate they are on bicycles, not skateboards.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: road construction
  - The upper part of the intersection is actively under construction, enclosed by orange mesh barriers and cones, with workers in high-visibility vests standing in the roadway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 32.0-35.0s (clearest 33.0s)
  - subject: police car
  - A white police vehicle with its emergency roof lights actively flashing passes straight through the intersection on the horizontal street.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 1)

- **absent**
  - why not: No emergency vehicles pass through without their lights flashing.
- ruled out: A police car passes through at 32.03s, but it has its lights flashing, which disqualifies it for this query.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: No vehicle collisions occur in the video.
- ruled out: Various vehicles navigate turning paths simultaneously, but none come into physical contact with each other.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: There are no horse-drawn carriages present in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 2)

- **match** `exact` / conf `high` at 55.0-56.0s (clearest 55.0s)
  - subject: black SUV
  - A black SUV traveling up the vertical street stops in the intersection part-way through a left turn before continuing.
- **match** `exact` / conf `high` at 74.0-75.0s (clearest 74.0s)
  - subject: dark SUV
  - A dark SUV traveling down the vertical street stops at the crosswalk mid-way through a right turn before moving off.
- **match** `exact` / conf `high` at 92.0-97.0s (clearest 95.0s)
  - subject: articulated bus
  - An articulated bus stops in the middle of the intersection while part-way through a left turn, waiting for clearance before continuing.
- **match** `exact` / conf `high` at 136.0-142.0s (clearest 139.0s)
  - subject: black SUV
  - A black SUV turning right stops part-way through the turn, waiting in the crosswalk for a pedestrian before completing the turn.
- ruled out: Several other vehicles are seen making turns (e.g., a white van at 29.03s, a black SUV at 162.03s) but they drive continuously through the turn without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **match** `exact` / conf `high` at 172.0-176.0s (clearest 174.0s)
  - subject: pedestrian
  - A person on the sidewalk steps down to a parked black car, opens the driver's side door, gets in, and closes the door.
- ruled out: Several cars are parked along the left side of the street throughout the video, and pedestrians walk past them, but no one interacts with them outside of the noted interval.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 2)

- **absent**
  - why not: No bus stops at the kerb to let passengers on or off at any point in the video.
- ruled out: An articulated bus stops in the intersection at 92.03s but is in the middle of a turn, not at the kerb, and no boarding happens. A standard bus drives straight through at 106.03s without stopping.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 2)

- **match** `exact` / conf `high` at 10.0-14.0s (clearest 12.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb mid-block and crosses to the right side, walking under the scaffolding.
- **match** `exact` / conf `high` at 15.0-19.0s (clearest 17.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb mid-block and crosses to the right side.
- **match** `exact` / conf `high` at 18.0-22.0s (clearest 20.0s)
  - subject: pedestrian
  - A pedestrian emerges from the right-side scaffolding mid-block and crosses the roadway to the left side.
- **match** `exact` / conf `high` at 33.0-37.0s (clearest 35.0s)
  - subject: pedestrian
  - A pedestrian leaves the right kerb mid-block and crosses the street to the parked cars on the left.
- **match** `exact` / conf `high` at 83.0-87.0s (clearest 85.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb mid-block and crosses the road, disappearing under the right-side scaffolding.
- **match** `exact` / conf `high` at 90.0-94.0s (clearest 92.0s)
  - subject: pedestrian
  - A pedestrian emerges from the scaffolding on the right mid-block and crosses to the left kerb.
- **match** `exact` / conf `high` at 122.0-126.0s (clearest 124.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb mid-block and crosses to the right side.
- **match** `exact` / conf `high` at 129.0-133.0s (clearest 131.0s)
  - subject: pedestrian
  - A pedestrian steps off the right kerb mid-block and crosses to the left side.
- **match** `exact` / conf `high` at 142.0-146.0s (clearest 144.0s)
  - subject: pedestrian
  - A pedestrian emerges from the right-side scaffolding and crosses mid-block to the left kerb.
- **match** `exact` / conf `high` at 155.0-159.0s (clearest 157.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb mid-block and crosses the street to the right.
- **match** `exact` / conf `high` at 164.0-168.0s (clearest 166.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb mid-block and crosses the street to the right side.
- **match** `exact` / conf `high` at 168.0-172.0s (clearest 170.0s)
  - subject: pedestrian
  - A pedestrian emerges from the right-side scaffolding mid-block and crosses to the left kerb.
- ruled out: Several pedestrians are seen crossing the streets at the marked crosswalks near the top of the intersection. These instances do not match the criteria of crossing away from the markings.

### [skateboard] a person riding a skateboard (sample 2)

- **match** `exact` / conf `high` at 111.0-118.0s (clearest 115.0s)
  - subject: skateboarder
  - A person on a skateboard rides up the vertical street in the leftward lane, pushing themselves across the intersection.
- ruled out: Several pedestrians and bicyclists are seen passing through the frame, but they are walking or cycling.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: intersection construction
  - Orange traffic barriers, cones, an active excavation area, and workers wearing high-visibility vests are situated directly on the roadway at the top of the intersection.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 31.0-35.0s (clearest 33.0s)
  - subject: police SUV
  - A police SUV drives across the intersection from right to left with its roof lights actively flashing.
- ruled out: Civilian vehicles traverse the intersection regularly, but without flashing lights.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 2)

- **absent**
  - why not: No emergency vehicles are seen passing through without their lights flashing.
- ruled out: A police SUV is observed moving through the intersection between 31.03s and 35.03s, but its emergency lights are flashing.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: No vehicular collisions or contact occurred in the video.
- ruled out: Vehicles are frequently seen steering around the central construction zone and waiting for pedestrians or crossing traffic, but none collide or make physical contact.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: No horses or horse-drawn carriages appear in this video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 3)

- **match** `exact` / conf `high` at 6.0-8.0s (clearest 7.0s)
  - subject: red car
  - A red car turning left comes to a complete stop in the middle of the intersection to wait for a pedestrian before moving off.
- **match** `exact` / conf `high` at 56.0-59.0s (clearest 57.0s)
  - subject: grey car
  - A grey car making a left turn halts in the intersection to yield to pedestrians in the crosswalk before continuing.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **match** `exact` / conf `high` at 124.0-127.0s (clearest 125.0s)
  - subject: driver
  - The driver's door of a black SUV parked on the left side of the street opens, and a person steps out and walks toward the sidewalk.
- **match** `exact` / conf `high` at 144.0-147.0s (clearest 146.0s)
  - subject: person
  - A person walks from the sidewalk, opens the driver's side door of the parked black SUV, gets in, and closes the door.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 3)

- **absent**
  - why not: No bus is visibly engaged in picking up or dropping off passengers.
- ruled out: A bus is stopped at the kerb in the top left from 0.00s to 11.03s, but no passengers are seen boarding or alighting. An articulated bus pulls over to the left kerb at 104.03s and remains there, but its doors are completely hidden by the tree canopy, making it impossible to confirm the boarding or alighting state.
- unreadable: The tree canopy on the left entirely blocks the view of the bus doors and the adjacent sidewalk, preventing any observation of passenger activity there.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 3)

- **match** `exact` / conf `high` at 21.0-27.0s (clearest 24.0s)
  - subject: pedestrian
  - A pedestrian steps off the top right kerb and crosses diagonally through the middle of the intersection, far from the crosswalk markings.
- **match** `exact` / conf `high` at 106.0-111.0s (clearest 108.0s)
  - subject: pedestrian
  - A pedestrian steps into the roadway below the middle crosswalk and walks diagonally across the vertical street to the opposite side.
- **match** `exact` / conf `high` at 114.0-120.0s (clearest 117.0s)
  - subject: pedestrian
  - A pedestrian steps out from between parked cars on the left and crosses the vertical street mid-block to reach the scaffolding on the right.
- **match** `exact` / conf `high` at 123.0-128.0s (clearest 125.0s)
  - subject: pedestrian
  - A pedestrian leaves the sidewalk under the scaffolding on the right and crosses the vertical street to the left side.
- **match** `exact` / conf `high` at 151.0-157.0s (clearest 154.0s)
  - subject: two pedestrians
  - Two people step into the roadway from the right and walk across the vertical street together, reaching the parked cars on the left.
- **match** `exact` / conf `high` at 164.0-168.0s (clearest 166.0s)
  - subject: pedestrian
  - A pedestrian weaves between parked cars on the left, enters the roadway, and crosses the vertical street to the right side.

### [skateboard] a person riding a skateboard (sample 3)

- **match** `exact` / conf `high` at 99.0-118.0s (clearest 108.0s)
  - subject: person on a skateboard
  - A person rides a skateboard into the intersection from the right, travels through the crosswalk, and then rolls down the vertical street before exiting the frame.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: intersection construction zone
  - The intersection is actively under construction, evident from the ongoing presence of orange cones, barriers, and several workers in high-visibility vests standing in the roadway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **match** `exact` / conf `high` at 30.0-34.0s (clearest 32.0s)
  - subject: police SUV
  - An NYPD SUV drives into the intersection with its roof light bar flashing actively and makes a left turn.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 3)

- **match** `exact` / conf `high` at 138.0-142.0s (clearest 140.0s)
  - subject: ambulance
  - A white and red ambulance passes straight across the top horizontal street through the intersection, and its emergency lights are dark.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: At no point during the video do any two vehicles collide or make contact with each other.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: There are no horse-drawn carriages present in the footage.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 4)

- **match** `exact` / conf `high` at 91.0-94.0s (clearest 92.0s)
  - subject: blue articulated bus
  - A long blue articulated bus turning left into the vertical street drastically slows down and comes to a complete halt mid-turn, before slowly resuming its motion to complete the turn.
- ruled out: Several other vehicles, such as a white USPS truck and a grey sedan, make turns at the intersection, but they do not stop part-way through their maneuvers.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **match** `exact` / conf `high` at 28.0-32.0s (clearest 29.0s)
  - subject: driver of a black SUV
  - The driver's door of a recently parked black SUV opens, a person steps out onto the roadway, pushes the door closed, and walks away towards the sidewalk.
- ruled out: Pedestrians are seen walking past other parked cars along the left side of the street, but they do not open doors or get in or out.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 4)

- **absent**
  - why not: No bus stops at a kerb with people getting on or off in the video.
- ruled out: City buses, including blue articulated models, pass through the intersection, and pedestrians are gathered at a bus shelter on the upper left corner, but no bus actually pulls over to the kerb and stops to board or alight passengers.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 4)

- **match** `exact` / conf `high` at 11.0-22.0s (clearest 16.0s)
  - subject: pedestrian in light clothing
  - A pedestrian steps off the left kerb far below the intersection and walks straight across the entire roadway, reaching the sidewalk scaffolding on the far side.
- **match** `exact` / conf `high` at 116.0-126.0s (clearest 121.0s)
  - subject: pedestrian in dark clothing
  - A pedestrian steps off the left kerb midway down the block and crosses both directions of traffic, arriving at the right-hand sidewalk under the scaffolding.
- **match** `exact` / conf `high` at 135.0-144.0s (clearest 139.0s)
  - subject: pedestrian in a light top
  - A pedestrian leaves the left sidewalk mid-block and crosses the entire width of the vertical street to the far side.
- **match** `exact` / conf `high` at 162.0-172.0s (clearest 167.0s)
  - subject: pedestrian in dark clothing
  - A pedestrian emerges from under the scaffolding on the right-hand side, far below the intersection, and walks across the roadway to reach the left kerb.
- ruled out: Pedestrians are observed crossing at the top left of the intersection, but they are doing so near or within the designated crosswalk markings, avoiding the construction zone rather than jaywalking mid-block.

### [skateboard] a person riding a skateboard (sample 4)

- **match** `exact` / conf `high` at 132.0-141.0s (clearest 136.0s)
  - subject: person on a skateboard
  - A person riding a skateboard travels down the left sidewalk, rides off the kerb into the roadway, and continues skating down the street until exiting the bottom of the frame.
- ruled out: Numerous pedestrians walk and jog along the sidewalks and crosswalks, but only this one individual is riding a skateboard.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: intersection construction zone
  - The upper portion of the intersection is an active construction site with orange barriers, cones, excavation equipment, and workers in safety vests operating in the carriageway for the entire duration of the clip.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **match** `exact` / conf `high` at 29.0-35.0s (clearest 32.0s)
  - subject: NYPD police SUV
  - An NYPD police vehicle with its roof lights visibly flashing enters from the right, travels through the intersection, and exits to the left.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 4)

- **absent**
  - why not: No emergency vehicles are seen operating with their lights turned off.
- ruled out: An NYPD police vehicle is seen passing through the intersection, but its emergency light bar is actively flashing.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: No collisions or contact between vehicles occur in the video.
- ruled out: Vehicles occasionally get close to one another—such as an articulated bus slowing down for oncoming traffic during a turn—but no vehicles collide or make physical contact at any point.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: A horse-drawn carriage never appears in the video.
- ruled out: Many different types of motor vehicles traverse the intersection, but there are no animal-drawn carriages.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 5)

- **match** `exact` / conf `high` at 35.0-36.0s (clearest 35.0s)
  - subject: dark car
  - A dark car turning left almost stops in the intersection to yield before completing the turn.
- **match** `exact` / conf `high` at 43.0-44.0s (clearest 43.0s)
  - subject: white SUV
  - A white SUV turning left stops midway through the intersection before resuming its turn.
- **match** `exact` / conf `high` at 93.0-97.0s (clearest 95.0s)
  - subject: articulated bus
  - An articulated bus turning left stops entirely in the middle of the intersection for several seconds before continuing.
- **match** `exact` / conf `high` at 111.0-112.0s (clearest 111.0s)
  - subject: silver car
  - A silver car turning left halts briefly in the intersection before continuing.
- **match** `exact` / conf `high` at 139.0-140.0s (clearest 139.0s)
  - subject: silver SUV
  - A silver SUV making a left turn almost comes to a complete stop before moving off.
- ruled out: Many vehicles make turns smoothly without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **absent**
  - why not: No one is seen getting into or out of a stopped vehicle at any point in the footage.
- ruled out: People are seen walking near parked cars at times (e.g., at 65.03s), but they do not open the doors or get inside.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 5)

- **match** `exact` / conf `high` at 0.0-15.0s (clearest 5.0s)
  - subject: bus
  - A bus is stopped at the kerbside bus stop structure at the top left of the frame. It remains stopped while passengers board or alight, and finally pulls away at 15.03s.
- ruled out: Other buses pass through the intersection, but they do not stop at the kerb to let passengers on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 5)

- **match** `exact` / conf `high` at 5.0-12.0s (clearest 8.0s)
  - subject: pedestrian
  - A pedestrian crosses the vertical street from left to right, walking over the diagonal hashes well below the marked crosswalk.
- **match** `exact` / conf `high` at 15.0-25.0s (clearest 20.0s)
  - subject: pedestrian in blue shirt
  - A pedestrian in a blue shirt steps off the left kerb and walks across the hash marks to the scaffolding on the right.
- **match** `exact` / conf `high` at 35.0-42.0s (clearest 38.0s)
  - subject: pedestrian
  - A pedestrian emerges from the right side and crosses to the left kerb outside of the crosswalk.
- **match** `exact` / conf `high` at 48.0-56.0s (clearest 52.0s)
  - subject: pedestrian in white
  - A pedestrian in a white top crosses from the scaffolding side to the left side.
- **match** `exact` / conf `high` at 58.0-65.0s (clearest 61.0s)
  - subject: pedestrian
  - A pedestrian crosses left to right, walking over the diagonal hashes below the crosswalk.
- **match** `exact` / conf `high` at 108.0-116.0s (clearest 112.0s)
  - subject: pedestrian
  - A pedestrian steps off the left kerb and crosses to the right side underneath the scaffolding.
- **match** `exact` / conf `high` at 120.0-128.0s (clearest 124.0s)
  - subject: pedestrian
  - A pedestrian walks left to right across the roadway, outside the crosswalk lines.
- **match** `exact` / conf `high` at 131.0-139.0s (clearest 135.0s)
  - subject: pedestrian
  - A pedestrian comes out from the scaffolding on the right and crosses the street to the left side.
- **match** `exact` / conf `high` at 162.0-171.0s (clearest 166.0s)
  - subject: pedestrian
  - A pedestrian crosses the road left to right well away from the marked pedestrian crossing.
- **match** `exact` / conf `high` at 172.0-180.0s (clearest 176.0s)
  - subject: pedestrian carrying a bag
  - A pedestrian walks right to left across the vehicular lanes, reaching the kerb just as the video ends.
- ruled out: Many pedestrians are seen crossing legally inside the marked crosswalk lines at the intersection, which does not match the prompt.

### [skateboard] a person riding a skateboard (sample 5)

- **absent**
  - why not: No one on a skateboard appears in the video.
- ruled out: People are seen walking and occasionally a cyclist rides past, but none ride a skateboard.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: roadway intersection
  - The intersection has an active construction zone with orange cones, safety barriers, and workers in high-vis vests standing in the roadway. This event is underway at the start of the video and continues until the video ends.
- ruled out: None

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **match** `exact` / conf `high` at 30.0-34.0s (clearest 32.0s)
  - subject: police car
  - An NYPD police vehicle drives through the intersection from left to right with its emergency roof lights flashing.
- ruled out: No other emergency vehicles were seen with their flashing lights active.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 5)

- **absent**
  - why not: No emergency vehicles are seen passing through the intersection without their lights flashing.
- ruled out: A police car passes through at 30.03s, but its emergency lights are flashing.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: No vehicle collisions occur in the video.
- ruled out: Multiple vehicles make turns in the intersection and sometimes yield to one another, but no vehicles collide or make contact.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: No horse-drawn carriages are present.
- ruled out: Various cars, buses, and trucks drive through the area, but no horse-drawn carriage passes through.

---

5 call(s) ok, 0 failed, 1007790 in / 54956 out tokens