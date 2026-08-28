# probe run: 20260828-071624-events-free

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `burn,list` (channels: burn, list, interleave, or none)
- fps: 0.5 | whole range, one call
- frames per call: 91 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/20260828-071624-events-free`

## by axis

| axis | answered present | note |
|---|---|---|
| block | 2/2 |  |
| conflict | 2/2 |  |
| detour | 2/2 |  |
| floor | 4/4 |  |
| negative | 0/3 | ground truth known: all absent |
| transit | 0/1 |  |
| worker | 2/2 |  |
| yield | 1/2 |  |

## per query

### [yield] a vehicle stopped in the roadway while a pedestrian crosses in front of it

- **match** `exact` / conf `high` at 110.0-118.0s (clearest 112.0s)
  - subject: a USPS truck and a pedestrian
  - A USPS truck turning right into the crosswalk on the right side of the intersection stops to allow a pedestrian to cross directly in front of it before proceeding.
- ruled out: A police car turning left stops in the intersection at 32.03s, but this appears to be to wait for oncoming traffic, not for a pedestrian. A white sedan turning left stops in the crosswalk at 10.03s, but no pedestrian crosses in front of it. Several vehicles are seen stopped at the stop line for a red light while pedestrians use the adjacent crosswalk (e.g., at 76.03s or 164.03s); while technically matching the words, these are routine stops for traffic signals rather than a vehicle yielding to a pedestrian in its path.

### [yield] a turning vehicle stopped part-way through its turn

- **absent**
  - why not: Although multiple vehicles make turns at this intersection during the provided timeframe, none of them come to a stop while in the middle of their turn.
- ruled out: I examined several turning vehicles, including the silver SUV (36.03s - 42.03s), the articulated bus (90.03s - 100.03s), and the USPS truck (112.03s - 116.03s). While they execute turns, they all maintain continuous motion and complete their maneuvers without stopping.

### [conflict] two road users close enough that one of them changes course or speed

- **match** `exact` / conf `high` at 12.0-24.0s (clearest 14.0s)
  - subject: pedestrian
  - A pedestrian jaywalking across the main road stops in the middle of the traffic lane to allow a white sedan to pass, then waits near the centerline for a second sedan before continuing.
- **match** `exact` / conf `high` at 58.0-64.0s (clearest 62.0s)
  - subject: black SUV
  - A black SUV proceeding up through the intersection brakes and comes to a halt just before the far crosswalk to yield to a pedestrian crossing in its path.
- ruled out: At t=170.03s - 174.03s, a pedestrian crosses the intersection while two cyclists pass very closely on either side of them. However, tracing the pedestrian's progress across the crosswalk stripes shows they maintain a steady walking pace without stopping or swerving, so no change in course or speed occurred. At t=88.03s - 94.03s, a black SUV waits for an articulated bus to complete its turn. This was rejected because the SUV is simply stopped at the intersection line following normal right-of-way rules, rather than changing its speed mid-maneuver due to unexpected proximity.

### [conflict] a cyclist passing close to a moving vehicle

- **match** `exact` / conf `high` at 124.0-128.0s (clearest 126.0s)
  - subject: cyclist and black SUV
  - A cyclist heading downwards and a black SUV heading upwards pass close to each other in opposite directions in the middle of the intersection.
- ruled out: 104.03s - 110.03s: A cyclist passes near a blue SUV that is turning left, but the SUV appears to be yielding, and they do not pass each other as closely.
112.03s - 116.03s: A cyclist waits for a grey SUV to cross their path, but they do not pass close to one another.

### [block] a vehicle unable to proceed because another vehicle is stopped in its lane

- **match** `exact` / conf `high` at 116.0-124.0s (clearest 118.0s)
  - subject: the dark SUV
  - A dark SUV encounters a white USPS truck that is stopped in its lane. The SUV comes to a halt directly behind the truck before eventually changing lanes to drive around the obstruction.
- ruled out: Vehicles waiting in normal queues at red lights were not considered matches. Other vehicles that later encounter the same stopped USPS truck (e.g., at 134.03s and 154.03s) change lanes smoothly well in advance without being forced to stop or wait in the blocked lane. Vehicles slowing down behind the moving food cart (e.g., 142.03s) are not matches because the lead vehicle is moving, not stopped.

### [block] a queue of vehicles waiting behind something stationary

- **match** `exact` / conf `high` at 84.0-102.0s (clearest 94.0s)
  - subject: a white van, a dark car, another white van, and a silver car
  - A line of vehicles forms on the road at the bottom of the frame, waiting behind a stationary white van.
- ruled out: I also observed a shorter queue forming between 130.03s and 138.03s in the same location, but chose the longer, more prominent example.

### [worker] a construction worker signalling to drivers

- **match** `exact` / conf `high` at 144.0-152.0s (clearest 148.0s)
  - subject: worker at the top-left crosswalk
  - A construction worker stands at the crosswalk and holds out his arm to signal a turning car.
- ruled out: There are workers visible in or near the crosswalks throughout much of the video, but they are generally observing or waiting rather than actively directing traffic.

### [worker] a construction worker standing in a live traffic lane

- **match** `exact` / conf `high` at 0.0-12.0s (clearest 2.0s)
  - subject: construction worker
  - A construction worker wearing a high-visibility vest stands near the middle of the road by the upper crosswalk while vehicles pass close by him in the live traffic lanes.
- ruled out: Other construction workers in the scene were examined, but they were either walking on the sidewalk or standing safely within the closed-off work zone behind orange barriers and cones, rather than in an active traffic lane.

### [detour] a pedestrian walking in the roadway alongside the closed sidewalk

- **match** `exact` / conf `high` at 158.0-178.0s (clearest 168.0s)
  - subject: pedestrian
  - A pedestrian steps off the crosswalk and walks south down the roadway, remaining in the street right next to the sidewalk scaffolding shed for the entire visible length of the block.
- ruled out: I scanned the construction zone at the top of the frame for pedestrians walking in the roadway to bypass the barriers, but found none. I also noted pedestrians entering the roadway on the left side of the street (e.g., around 124.03s), but they were accessing parked cars rather than walking along a closed sidewalk.

### [detour] a vehicle steering around cones or barriers in the roadway

- **match** `exact` / conf `high` at 0.0-4.0s (clearest 2.0s)
  - subject: white SUV
  - A white SUV approaches the intersection from the right on the cross street and steers leftward to navigate around a line of construction cones blocking the right lane.
- **match** `exact` / conf `high` at 14.0-18.0s (clearest 16.0s)
  - subject: dark sedan
  - A dark sedan travelling leftwards on the cross street shifts its path to the left to avoid the construction cones extending into the roadway.
- **match** `exact` / conf `high` at 32.0-36.0s (clearest 34.0s)
  - subject: police SUV
  - A police SUV drives leftwards on the cross street, steering left to maneuver around the construction cones before entering the intersection.
- **match** `exact` / conf `high` at 112.0-116.0s (clearest 114.0s)
  - subject: USPS truck
  - A USPS mail truck travelling from right to left on the cross street steers leftward to bypass the cones marking the construction area.
- ruled out: Vehicles turning right from the main road onto the cross street (such as the white NYPD van between 28.03s and 34.03s) pass near the construction barriers. However, they are simply following the natural curve of the turn and are not actively steering around an obstacle placed in an established travel lane, so these were not included as matches. The articulated bus turning left (86.03s - 104.03s) was also considered but does not interact with the cones.

### [transit] a bus stopped at the kerb with people getting on or off

- **absent**
  - why not: While buses are present in the scene, they are only seen driving through the intersection and do not stop to pick up or drop off passengers.
- ruled out: An articulated bus drives through the intersection and turns right between 86.03s and 110.03s. Another standard bus drives straight through the intersection between 110.03s and 114.03s. Neither bus stops at the kerb or has passengers boarding or alighting.

### [floor] a vehicle stopped with part of its body on the crosswalk markings

- **match** `exact` / conf `high` at 112.0-118.0s (clearest 114.0s)
  - subject: the white USPS box truck
  - A white USPS truck approaches the intersection from the right and stops to yield to a crossing scooter. While waiting, the truck's front wheels and bumper are stopped directly over the white crosswalk stripes.
- ruled out: Many vehicles are seen stopping at the intersection throughout the video (e.g., the white car approaching from the bottom around 28.03s, and the yellow cab approaching from the right at 160.03s), but they correctly stop behind the crosswalk lines. Vehicles that stop in the middle of the intersection while waiting to turn, such as the grey SUV at 108.03s, were also rejected because they are not stopped on the crosswalk markings.

### [floor] a pedestrian crossing the roadway outside the crosswalk markings

- **match** `exact` / conf `high` at 116.0-120.0s (clearest 118.0s)
  - subject: pedestrian
  - A pedestrian crosses the main roadway horizontally, walking completely outside of the painted crosswalk lines.
- **match** `exact` / conf `high` at 122.0-128.0s (clearest 124.0s)
  - subject: pedestrian in white shirt
  - A pedestrian steps off the median and crosses to the left sidewalk, walking outside the crosswalk area.
- ruled out: Multiple pedestrians are seen crossing the intersection at various times (e.g., at 12.03s, 44.03s, 100.03s, 162.03s), but they are using the designated, painted crosswalks, so they do not fit the criteria of crossing 'outside the crosswalk markings'.

### [floor] a cyclist or e-bike rider riding on the sidewalk

- **match** `exact` / conf `high` at 116.0-122.0s (clearest 118.0s)
  - subject: rider on a scooter or e-bike
  - A rider enters the frame from the bottom left, traveling upwards along the sidewalk, passes a pedestrian, and then exits the sidewalk into the crosswalk area.
- ruled out: Several cyclists and scooter riders are seen traveling through the intersection or using the crosswalks (e.g., around t=34.03, t=152.03, and t=172.03), but they remain on the roadway or within marked crosswalks rather than riding on the sidewalks.

### [floor] a vehicle stopped in a moving lane with traffic going around it

- **match** `exact` / conf `high` at 80.0-180.0s (clearest 86.0s)
  - subject: a white van towing a food cart
  - The van and food cart stop in the rightmost moving lane and remain parked there for the rest of the clip. Numerous vehicles approach from behind and change lanes to navigate around the stationary vehicle.
- ruled out: A USPS truck stops in the middle of the intersection from 114.03s to 116.03s before completing a turn, but it is yielding rather than parked, and no traffic goes around it. Other vehicles occasionally stop at the crosswalk to yield to pedestrians, but they do not cause traffic to route around them.

### [negative] a horse-drawn carriage

- **absent**
  - why not: The requested situation (a horse-drawn carriage) does not occur in this video clip. The intersection only sees motor vehicles (cars, buses, trucks, vans), bicycles, and pedestrians.
- ruled out: I examined all the vehicles moving through the intersection across the entire video window, including various cars, a large blue articulated bus (e.g., at t=86.03s to 104.03s), and a USPS truck (t=112.03s to 118.03s). None of these were horse-drawn carriages.

### [negative] a vehicle that has driven up onto the sidewalk

- **absent**
  - why not: Throughout the provided sequence, all visible vehicles remain within the designated roadway and crosswalk boundaries. No vehicle is observed driving up onto or parking on any of the visible sidewalks.
- ruled out: The white police SUV making a right turn at t=34.03s was examined as it turned closely to the curb, but it remained entirely on the roadway surface. Large vehicles like the articulated bus turning left around t=92.03s and the USPS truck turning left around t=114.03s were also considered due to their size and sweeping turns, but they both stayed within the roadway and did not mount the sidewalk.

### [negative] two vehicles making contact with each other

- **absent**
  - why not: No vehicles make contact with each other in this video window.
- ruled out: I examined all vehicles moving through the intersection, including tight maneuvers like the articulated bus making a left turn between 86.03s and 104.03s. At no point do any vehicles collide or touch.

---

18 call(s) ok, 0 failed, 1822303 in / 50358 out tokens