# probe run: fps2

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 2 | whole range, one call
- frames per call: 361 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/fps/fps2`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| bus-dwell | 0/1 | 1/1 | 0/1 |  |
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
- skateboard — a person riding a skateboard
- emergency — an emergency vehicle with its lights flashing passing throug
- emergency-dark — an emergency vehicle passing through the intersection with i

## per query

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 1)

- **match** `exact` / conf `high` at 88.0-94.0s (clearest 91.0s)
  - subject: blue articulated bus
  - The bus part-way through a right turn stops completely to wait for traffic before resuming its turn.
- ruled out: Other turning vehicles complete their turns smoothly without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **match** `exact` / conf `high` at 126.0-128.0s (clearest 127.0s)
  - subject: pedestrian
  - A person approaches the driver's side of the black SUV parked at the bottom left, opens the door, and gets inside.
- ruled out: Pedestrians walking past parked cars on the sidewalk do not interact with them.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 1)

- **absent**
  - why not: No bus stops at a kerb to pick up or drop off passengers.
- ruled out: A bus passes through the intersection at 68s and another turns at 88s, but neither stops at the kerb to let passengers on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 1)

- **match** `exact` / conf `high` at 113.5-117.5s (clearest 115.5s)
  - subject: pedestrian
  - A person steps off the left kerb far below the marked crosswalk and walks directly across the empty traffic lanes to the scaffolding platform on the right.
- ruled out: Several pedestrians cross the street using the white-striped crosswalks; these do not fit the description.

### [skateboard] a person riding a skateboard (sample 1)

- **match** `exact` / conf `high` at 173.0-177.5s (clearest 175.5s)
  - subject: skateboarder
  - A person rides a skateboard downwards through the left side of the roadway, travelling past the parked cars.
- ruled out: Cyclists riding through the intersection are not riding skateboards.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: roadwork zone
  - A section of the intersection is continuously cordoned off with orange fencing and cones, and workers in yellow high-visibility vests are standing in the roadway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.5s)
  - subject: police SUV
  - A police SUV with flashing red and blue roof lights drives through the intersection from right to left.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 1)

- **absent**
  - why not: No emergency vehicle is seen operating without its flashing lights.
- ruled out: The police SUV passing through at 31s has its emergency lights actively flashing.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: There are no collisions or vehicles touching each other.
- ruled out: A car waits for the turning bus at 93s, but they do not make contact.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: There are no horse-drawn carriages present in the footage.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 2)

- **match** `exact` / conf `high` at 92.0-97.0s (clearest 94.5s)
  - subject: an articulated blue bus
  - The bus halts completely while part-way through turning into the near street. It remains stopped for several seconds before continuing its turn.
- ruled out: Numerous other vehicles pass through or turn at the intersection, but they do not stop during their turns.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **match** `exact` / conf `high` at 10.5-12.5s (clearest 11.5s)
  - subject: a person exiting a black SUV
  - The driver's door of the parked black SUV opens, and a person steps out onto the street before closing the door.
- **match** `exact` / conf `high` at 161.0-163.5s (clearest 162.0s)
  - subject: a person entering a white car
  - A person walks up to the driver's side of the parked white car, opens the door, and gets in.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 2)

- **absent**
  - why not: No buses stop at a kerb for passengers during the video window.
- ruled out: Several buses pass through the intersection, and one briefly halts in the middle of it, but none pull over to a kerb to allow passengers to board or alight.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 2)

- **match** `exact` / conf `high` at 11.0-16.0s (clearest 13.5s)
  - subject: a pedestrian in a light blue shirt
  - The pedestrian steps off the kerb north of the crosswalk and crosses diagonally across the roadway to the opposite corner.
- **match** `exact` / conf `high` at 34.0-38.0s (clearest 36.0s)
  - subject: a pedestrian
  - The pedestrian steps off the right kerb far below the crosswalk and walks directly across the road to the left side.
- **match** `exact` / conf `high` at 59.5-63.5s (clearest 61.5s)
  - subject: a pedestrian
  - The pedestrian crosses the main vertical street from right to left, outside the crosswalk area.
- **match** `exact` / conf `high` at 84.0-88.0s (clearest 86.0s)
  - subject: a pedestrian
  - The pedestrian crosses the main vertical street from left to right, far below the crosswalk.
- **match** `exact` / conf `high` at 108.5-113.0s (clearest 111.0s)
  - subject: a pedestrian in dark clothing
  - The pedestrian steps out from between the parked cars on the left and crosses to the right side of the street.
- **match** `exact` / conf `high` at 130.0-135.0s (clearest 132.5s)
  - subject: a pedestrian
  - The pedestrian crosses the main vertical street from right to left, away from the crosswalk markings.
- **match** `exact` / conf `high` at 142.5-145.5s (clearest 144.0s)
  - subject: a pedestrian
  - The pedestrian crosses the main vertical street from left to right, outside the crosswalk.
- **match** `exact` / conf `high` at 162.5-165.5s (clearest 164.0s)
  - subject: a pedestrian
  - The pedestrian crosses the main vertical street from left to right, well below the crosswalk.
- **match** `exact` / conf `high` at 174.5-177.5s (clearest 176.0s)
  - subject: a pedestrian
  - The pedestrian crosses the main vertical street from right to left, away from the marked crossing.

### [skateboard] a person riding a skateboard (sample 2)

- **match** `exact` / conf `high` at 168.0-174.0s (clearest 171.0s)
  - subject: a person on a skateboard
  - The person glides up the near lane of the vertical street on a skateboard, passing through the intersection before exiting the frame.
- ruled out: Several cyclists pass through the intersection, but they are riding bicycles rather than skateboards.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: a construction site in the roadway
  - An area of the intersection is fenced off with orange cones and barriers, and construction workers are present in the roadway throughout the entire clip.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **absent**
  - why not: No emergency vehicles use their flashing lights in this video window.
- ruled out: Police cars pass through the intersection at [8.53s - 12.53s] and [30.53s - 36.03s], but their emergency lights are not flashing.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 2)

- **match** `exact` / conf `high` at 8.5-12.5s (clearest 10.5s)
  - subject: a police car
  - A police car enters the intersection from the left, turns down into the near street, and exits the frame without using its flashing lights.
- **match** `exact` / conf `high` at 30.5-36.0s (clearest 33.0s)
  - subject: a police car
  - A police car enters from the left and makes a turn down the near street without its emergency lights activated.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: There are no vehicular collisions or instances of vehicles making contact in the video.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: No horse-drawn carriages appear in the recording.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 3)

- **match** `exact` / conf `high` at 143.0-150.5s (clearest 146.5s)
  - subject: dark SUV
  - A dark SUV making a left turn stops in the middle of the intersection to wait for pedestrians in the crosswalk, then resumes moving.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **absent**
  - why not: No one is seen getting into or out of any vehicle during the video.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 3)

- **absent**
  - why not: No buses stop to pick up or drop off passengers.
- ruled out: An articulated bus passes through the intersection from 86.53s to 101.53s, but it does not stop at the kerb to let passengers on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 3)

- **match** `exact` / conf `high` at 10.5-16.0s (clearest 13.0s)
  - subject: pedestrian
  - A pedestrian steps off the right kerb and crosses the vertical street diagonally, away from any crosswalks, until reaching the sidewalk on the left.

### [skateboard] a person riding a skateboard (sample 3)

- **absent**
  - why not: No skateboards or people riding them appear in the footage.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: construction area
  - An area of the intersection is cordoned off with orange barriers and cones, and construction workers are present throughout the video.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **match** `exact` / conf `high` at 31.0-36.0s (clearest 33.5s)
  - subject: police car
  - A police car drives straight down the vertical street with its emergency roof lights flashing.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 3)

- **absent**
  - why not: No emergency vehicles pass through without their lights flashing.
- ruled out: A police car passes through between 31.03s and 36.03s, but its emergency lights are flashing.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: No collisions or contact between vehicles occur in the video.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: There are no horse-drawn carriages in the scene.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 4)

- **match** `exact` / conf `high` at 111.5-113.5s (clearest 112.5s)
  - subject: a blue SUV
  - A blue SUV turns left and halts part-way through the turn to yield to pedestrians crossing the street, before resuming its turn.
- ruled out: An articulated MTA bus negotiates a slow left turn between 78.53s and 98.03s, but remains in motion the whole time and does not come to a stop.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **match** `exact` / conf `high` at 118.0-121.5s (clearest 119.5s)
  - subject: a person
  - A person walks up to a black SUV parked on the left side of the street, opens the driver's door, gets inside, and closes the door.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 4)

- **absent**
  - why not: No buses stop to pick up or drop off passengers during the video.
- ruled out: An articulated bus passes through the intersection starting at 78.53s, but it simply makes a left turn and does not stop at the kerb or let anyone on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 4)

- **match** `exact` / conf `high` at 167.0-173.5s (clearest 170.5s)
  - subject: a pedestrian
  - A pedestrian steps off the kerb at the bottom left and crosses the roadway diagonally towards the wooden platform on the bottom right, well away from any crosswalk.
- ruled out: Several other pedestrians cross the street during the video, but they all use the marked crosswalks.

### [skateboard] a person riding a skateboard (sample 4)

- **absent**
  - why not: No one is seen riding a skateboard in the footage.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: the roadway
  - The upper portion of the intersection is consistently cordoned off with orange barriers and traffic cones, and workers in high-visibility clothing are present on the roadway throughout the clip.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **match** `exact` / conf `high` at 31.5-34.5s (clearest 33.0s)
  - subject: a police car
  - A police car with its emergency lights flashing enters from the right and proceeds straight through the intersection.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 4)

- **absent**
  - why not: No emergency vehicles are seen passing through without their lights flashing.
- ruled out: A police car passes through the intersection between 31.53s and 34.53s, but its emergency lights are flashing.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: No vehicles make contact or collide with one another in the video.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: No horse-drawn carriages appear in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn; the interval is the halt itself, from the vehicle stopping to it moving off (sample 5)

- **absent**
  - why not: No vehicle halts mid-turn during the video.
- ruled out: Several vehicles are seen making turns through the intersection (e.g., a dark SUV turning right around 15s, a white car turning right around 12s, a white van turning left at 116s), but they all complete their turns smoothly without stopping or almost stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **absent**
  - why not: No one is seen getting into or out of a stopped vehicle.
- ruled out: Vehicles are parked or pull over to the kerb (such as a white van at 85s), but no individuals are seen opening doors and actively entering or exiting these vehicles.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it; the interval is the whole stop, from the bus halting to it pulling away (sample 5)

- **absent**
  - why not: The only bus stop lacks visibility of the doors and any boarding or alighting passengers.
- ruled out: An articulated bus pulls up and stops at the kerb between 93.53s and 102.03s. However, because the bus's doors are on its right side (facing away from the camera), it is impossible to see if anyone gets on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings, from stepping off the kerb until reaching the far side (sample 5)

- **match** `exact` / conf `high` at 11.0-16.0s (clearest 13.5s)
  - subject: a pedestrian
  - A pedestrian steps off the left kerb and crosses the near roadway diagonally to the right side, completely outside of any marked crosswalk.
- **match** `exact` / conf `high` at 123.0-131.0s (clearest 127.0s)
  - subject: a pedestrian
  - A pedestrian steps off the left kerb and walks across the near roadway to the right side, far from any crosswalk markings.

### [skateboard] a person riding a skateboard (sample 5)

- **absent**
  - why not: No one is seen riding a skateboard in the video.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: the intersection
  - The top half of the intersection is under construction, marked by orange cones and barriers, with workers in high-visibility vests moving around the carriageway throughout the entire video.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **match** `exact` / conf `high` at 28.5-35.0s (clearest 31.5s)
  - subject: a police SUV
  - A police SUV with its emergency lights flashing enters the intersection from the top-left road and makes a right turn into the near road.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 5)

- **match** `exact` / conf `high` at 10.0-14.0s (clearest 12.0s)
  - subject: a police car
  - A marked police car drives straight through the intersection from the top-left to the top-right road with its emergency lights turned off.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: There are no vehicle collisions in the video.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: No horse-drawn carriages appear in the video.

---

5 call(s) ok, 0 failed, 2003540 in / 34703 out tokens