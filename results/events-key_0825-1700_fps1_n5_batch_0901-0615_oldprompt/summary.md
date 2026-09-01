# probe run: events-key_0825-1700_fps1_n5_batch_0901-0615

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 1 | whole range, one call
- frames per call: 181 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/events-key_0825-1700_fps1_n5_batch_0901-0615`

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
| skateboard | 0/1 | 0/1 | 1/1 |  |
| turn-halt | 0/1 | 0/1 | 1/1 |  |

### queries whose samples disagreed

- turn-halt — a vehicle that stops, or almost stops, part-way through a tu
- pickup-car — a person getting into or out of a stopped car, van or taxi
- bus-dwell — a bus stopped at the kerb with people getting on or off it
- skateboard — a person riding a skateboard
- emergency — an emergency vehicle with its lights flashing passing throug
- emergency-dark — an emergency vehicle passing through the intersection with i

## per query

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 1)

- **absent**
  - why not: No turning vehicle was observed stopping or coming to a near-stop part-way through its maneuver.
- ruled out: I examined all vehicles making turns through the intersection, including several cars and SUVs turning left from the cross street onto the avenue (e.g., at 20s, 42s, 69s, 104s), and a white box truck at 112s-117s. All of them completed their turns continuously without pausing. The articulated bus at 90s-96s shifts lanes slightly but does not turn onto a different street.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **absent**
  - why not: No one was seen getting into or out of any stopped vehicle in the frames provided.
- ruled out: I checked the line of parked cars on the left side of the avenue and watched for any vehicles pulling over during the clip, but no activity around stationary vehicles occurred.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 1)

- **match** `exact` / conf `high` at 106.0-120.0s (clearest 112.0s)
  - subject: blue and white articulated MTA bus
  - The bus pulls up to the kerb at the bus shelter in the top left corner. It comes to a complete stop, and the cluster of people waiting there interacts with the bus doors, indicating boarding.
- ruled out: An earlier bus passes through the intersection around 86s-96s but does not stop at the kerb.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 1)

- **match** `exact` / conf `high` at 34.0-38.0s (clearest 36.0s)
  - subject: pedestrian in a light top and dark pants
  - A pedestrian steps off the right curb and walks horizontally across the traffic lanes of the avenue, far below the designated crosswalk, eventually reaching the left curb.
- ruled out: Other pedestrians were observed jaywalking in the exact same area, including one crossing left to right between 19s-23s, and another from left to right between 78s-83s.

### [skateboard] a person riding a skateboard (sample 1)

- **match** `exact` / conf `high` at 115.0-119.0s (clearest 117.0s)
  - subject: person on a skateboard
  - A person stands sideways on a skateboard and rolls rapidly down the crosswalk connecting the top-left to the bottom-left corner.
- ruled out: I checked cyclists passing through (e.g., at 105s, 133s) and running pedestrians, confirming they were not on skateboards.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: construction site in intersection
  - There is a permanent construction setup in the top-left quadrant of the intersection, featuring orange traffic cones, barriers, and workers in high-visibility vests standing on the roadway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 31.0-35.0s (clearest 32.0s)
  - subject: police car
  - A white police car with markings enters from the top right, turns left down the avenue, and drives away. Flashing blue and red lights are clearly visible on its roof bar.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 1)

- **absent**
  - why not: No emergency vehicles were observed driving through the intersection without their emergency lights engaged.
- ruled out: The only emergency vehicle that appears in the video is a police car between 31s-35s. I specifically checked it, and its light bar is actively flashing red and blue.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: No vehicles collided or made contact with one another.
- ruled out: I observed all interactions between passing cars, turning vehicles, buses, and cyclists. Traffic flowed continuously and vehicles safely yielded to one another.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: No horses or horse-drawn carriages appeared in any of the frames.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 2)

- **match** `exact` / conf `high` at 110.0-115.0s (clearest 112.0s)
  - subject: white box truck
  - A white box truck turning left from the right-hand road almost stops in the middle of the intersection, likely yielding to cross traffic or a cyclist, before completing its turn downwards.
- ruled out: Considered other vehicles turning left or right, but they maintain a steady speed throughout the turn without stopping or almost stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **match** `exact` / conf `high` at 114.0-118.0s (clearest 115.0s)
  - subject: driver in a high-vis vest
  - A white van parks on the right side of the bottom road, and the driver opens the door, steps out onto the roadway, and closes the door.
- ruled out: Considered vehicles parked on the left side of the bottom road, but no occupants are seen getting in or out.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 2)

- **absent**
  - why not: While buses pass through the intersection, none are observed stopping at the kerb to let people on or off.
- ruled out: Considered the articulated buses that pass through at 88.03s and 100.03s, but they are continuously moving through a turn and do not stop at the kerb to load or unload passengers.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 2)

- **match** `exact` / conf `high` at 130.0-136.0s (clearest 133.0s)
  - subject: pedestrian
  - A pedestrian steps off the kerb at the top-left corner and walks diagonally across the middle of the intersection to the bottom-right corner, away from any marked crosswalks.
- ruled out: Considered the driver exiting the white van around 115.03s who walks briefly on the roadway near the kerb, but he later uses the crosswalk marking to cross the street.

### [skateboard] a person riding a skateboard (sample 2)

- **absent**
  - why not: No one is seen riding a skateboard in the video.
- ruled out: Considered multiple cyclists seen travelling in the bike lanes or passing through the intersection, but none were riding skateboards.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction zone
  - Construction elements, including orange traffic cones, barriers, and workers wearing yellow high-vis vests, occupy the top crosswalk and portion of the top roadway for the entire duration of the clip.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 31.0-36.0s (clearest 33.0s)
  - subject: police SUV
  - A police SUV with its emergency lights flashing enters from the right road, crosses the intersection while turning left, and exits down the bottom road.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 2)

- **absent**
  - why not: No emergency vehicles are observed driving through the scene without flashing lights.
- ruled out: Considered the police SUV present at 33.03s, but its emergency lights were actively flashing.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: All vehicles navigate the intersection safely, with no collisions or contact occurring.
- ruled out: Considered the near interaction between the white box truck turning left and a cyclist at 112.03s, but the truck yields successfully and no contact is made.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: There are no horse-drawn carriages present in the scene.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 3)

- **match** `exact` / conf `high` at 155.0-162.0s (clearest 158.0s)
  - subject: silver SUV
  - A silver SUV enters the intersection to turn left, but stops mid-turn to yield to pedestrians in the crosswalk before completing its turn.
- ruled out: Checked other turning vehicles, such as a white van and an articulated bus, but they move continuously through their turns without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **absent**
  - why not: No person is observed getting into or out of any vehicle during the clip.
- ruled out: Checked parked cars along the avenue and the cross streets, as well as a USPS truck that pulls over, but no one is seen entering or exiting any of them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 3)

- **absent**
  - why not: No bus stops to pick up or drop off passengers in the video.
- ruled out: Several buses pass through the intersection, and there is a bus stop with waiting passengers on the left cross street, but no bus ever stops at the kerb.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 3)

- **match** `exact` / conf `high` at 115.0-119.0s (clearest 117.0s)
  - subject: pedestrian
  - A pedestrian crosses the avenue from left to right, significantly south of the intersection and the marked crosswalks.
- ruled out: Most pedestrians are seen using the marked crosswalks or remaining on the sidewalks.

### [skateboard] a person riding a skateboard (sample 3)

- **match** `exact` / conf `high` at 114.0-117.0s (clearest 115.0s)
  - subject: person on a skateboard
  - A person rides a skateboard south through the intersection and down the avenue.
- ruled out: Examined cyclists passing through the intersection, but their mode of transport is distinctly different from a skateboard.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: the roadway
  - Construction barriers, orange cones, an excavation area, and workers in high-visibility clothing are present in the left cross street for the entire duration of the clip.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **absent**
  - why not: No emergency vehicle is seen with active, flashing lights.
- ruled out: A police vehicle passes through the intersection, but its emergency lights are off.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 3)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.0s)
  - subject: police vehicle
  - A marked police vehicle crosses the intersection from right to left with its emergency light bar visibly turned off.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: No vehicles are seen colliding or making contact with each other in the video.
- ruled out: An articulated bus makes a tight right turn and passes near other vehicles, but no contact is made.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: There are no horse-drawn carriages present in the scene.
- ruled out: Checked all moving traffic on the avenue and cross streets.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 4)

- **match** `exact` / conf `high` at 177.0-180.0s (clearest 179.0s)
  - subject: yellow taxi
  - A yellow taxi enters the intersection from the bottom road, begins a left turn, and stops in the middle of the intersection to wait for pedestrians to finish crossing the crosswalk before completing the turn.
- ruled out: I observed several other vehicles making turns (e.g., an articulated bus at 91.03s, a white box truck at 154.03s), but they moved continuously through their turns without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **match** `exact` / conf `high` at 36.0-44.0s (clearest 41.0s)
  - subject: driver of a dark SUV
  - A dark SUV pulls into a parking spot on the left side of the bottom road. Shortly after stopping, the driver's side door opens and a person steps out, then walks towards the sidewalk.
- ruled out: A white van pulls over and stops on the bottom road at 64.03s, but no one is seen getting in or out of it. Another dark SUV parks at 123.03s and its driver also gets out around 126.03s, which would also match.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 4)

- **match** `exact` / conf `high` at 146.0-151.0s (clearest 148.0s)
  - subject: MTA bus
  - A blue and yellow city bus pulls up to the bus stop kerb on the top left street. It stops, and people can be seen boarding through the front doors before the bus pulls away.
- ruled out: Articulated buses pass through the intersection at 85.03s and 91.03s, but they are travelling in traffic lanes and do not stop at a kerb to load or unload passengers.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 4)

- **match** `exact` / conf `high` at 11.0-17.0s (clearest 14.0s)
  - subject: pedestrian
  - A pedestrian steps off the right curb of the bottom road well south of the marked crosswalk. They walk diagonally across the travel lanes to reach the parked cars on the left side.
- ruled out: Most pedestrians in the footage use the marked crosswalks, but there are multiple instances of jaywalking. Another pedestrian crosses the bottom road similarly between 32.03s and 37.03s.

### [skateboard] a person riding a skateboard (sample 4)

- **match** `exact` / conf `high` at 124.0-131.0s (clearest 128.0s)
  - subject: skateboarder
  - A person riding a skateboard enters the frame from the left road. They ride through the middle of the intersection and exit towards the top right.
- ruled out: Several cyclists pass through the intersection (e.g., at 35.03s and 135.03s), but this specific individual is clearly standing on a board and propelling themselves with one foot.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 1.0s)
  - subject: roadway construction site
  - The roadway approaching from the top is undergoing construction. Orange barriers, traffic cones, an excavated section, and workers in high-visibility vests are present throughout the entire clip.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **absent**
  - why not: No emergency vehicles with active, flashing lights are seen in the video.
- ruled out: An NYPD police SUV passes through the intersection between 32.03s and 34.03s, but its emergency light bar is not illuminated or flashing.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 4)

- **match** `exact` / conf `high` at 32.0-34.0s (clearest 33.0s)
  - subject: police SUV
  - An NYPD police SUV approaches from the right, crosses straight through the intersection, and exits to the left. Its roof-mounted light bar is clearly visible and is not flashing.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: Traffic flows smoothly through the intersection and no collisions or instances of vehicles touching each other occur.
- ruled out: I watched several vehicles perform parallel parking maneuvers (e.g., at 36.03s and 123.03s) where they come close to the parked cars behind them, but no physical contact is made.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: There are no horses or horse-drawn carriages present in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 5)

- **match** `exact` / conf `high` at 177.0-180.0s (clearest 178.0s)
  - subject: yellow taxi
  - A yellow taxi begins a right turn but stops part-way through in the crosswalk to yield to pedestrians before completing its turn.
- ruled out: Several other vehicles make turns throughout the video (such as a black SUV at 40.03s and a police car at 32.03s), but they proceed smoothly without stopping mid-turn.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **absent**
  - why not: No individuals are observed getting into or out of any stopped or parked vehicles during the sequence.
- ruled out: There is a line of parked cars along the left side of the vertical street, but none of their doors open and no one interacts with them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 5)

- **absent**
  - why not: Buses are seen passing through and stopping for traffic lights, but none stop at a kerb to allow people to board or alight.
- ruled out: An articulated MTA bus stops at the top left of the intersection from 86.03s to 91.03s, but it is waiting in the travel lane for a red light, not pulled over at the kerb for passengers.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 5)

- **match** `exact` / conf `high` at 11.0-15.0s (clearest 13.0s)
  - subject: pedestrian
  - A pedestrian walks across the vertical roadway from left to right, entirely outside of any crosswalk markings.
- ruled out: There are numerous instances of pedestrians crossing away from crosswalks throughout the video, such as at 19.03s, 34.03s, and 61.03s. The earliest clear instance was selected.

### [skateboard] a person riding a skateboard (sample 5)

- **match** `exact` / conf `high` at 132.0-137.0s (clearest 134.0s)
  - subject: person on a skateboard
  - A person riding a skateboard travels upwards from the bottom of the frame, passing straight through the intersection.
- ruled out: Several cyclists pass through the intersection, but their mode of transport has wheels and handlebars. The individual at 132.03s is standing in a sideways stance consistent with skateboarding.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 0.0s)
  - subject: construction area
  - Orange construction barriers, cones, and workers wearing high-visibility vests are continuously present in the roadway at the top left corner of the intersection.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.0s)
  - subject: police car
  - A police car enters the intersection from the right with its red and blue lights actively flashing, then turns left to head downwards.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 5)

- **absent**
  - why not: The only emergency vehicle present in the clip has its lights flashing. None pass through without active emergency lights.
- ruled out: A police car travels through the intersection at 31.03s, but its emergency lights are flashing.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: No vehicles are observed colliding or making physical contact with each other.
- ruled out: Vehicles occasionally yield to one another or pause for pedestrians (such as the taxi at 178.03s), but they do not collide or touch.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: There are no horses or horse-drawn carriages present in the video.

---

5 call(s) ok, 0 failed, 1006530 in / 39483 out tokens