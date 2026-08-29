# probe run: 20260829-002257-events-key

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `burn,list` (channels: burn, list, interleave, or none)
- fps: 0.5 | whole range, one call
- frames per call: 91 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/20260829-002257-events-key`

## by axis

| axis | answered present | note |
|---|---|---|
| bike-crosswalk | 1/1 |  |
| bike-sidewalk | 0/1 |  |
| bike-wrongway | 1/1 |  |
| negative | 0/2 | ground truth known: all absent |
| ped-jaywalk | 1/1 |  |
| ped-signal | 1/1 |  |
| ped-standing | 1/1 |  |
| stop-box | 1/1 |  |
| stop-crosswalk | 1/1 |  |
| stop-lane | 1/1 |  |
| stop-midturn | 0/1 |  |
| stop-pickup | 0/1 |  |
| transit-dwell | 0/1 |  |

## per query

### [stop-pickup] a vehicle stopped at the kerb with a person getting in or out of it

- **absent**
  - why not: While several vehicles pull over and stop at the curb during the sequence, no person is ever observed opening a door to get in or out of any of them.
- ruled out: A red car pulls over to the curb on the bottom-left street around t=8.03s, stops briefly, and then drives away at t=12.03s, but no one gets in or out. A white van pulls over to the right curb of the bottom street at t=80.03s and remains parked there (followed by a food cart), but no one is seen getting out of or into the van.

### [stop-midturn] a vehicle stopped part-way through a turn

- **absent**
  - why not: Several vehicles are observed making turns throughout the video, but all complete their maneuvers without stopping part-way through.
- ruled out: A blue articulated bus is seen making a left turn from 86.03s to 98.03s, and a white box truck makes a similar turn from 112.03s to 116.03s. While both maneuvers are slow due to the size of the vehicles, continuous progress is visible across the frames, and neither vehicle comes to a stop mid-turn.
- unreadable: The 2-second gap between frames means a very brief hesitation during a turn might not be captured, but a clear stop would likely be visible.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings

- **match** `exact` / conf `high` at 30.0-32.0s (clearest 32.0s)
  - subject: white van
  - A white van turning right stops with its front wheels and bumper resting on the crosswalk markings.
- ruled out: Several other vehicles stop at the various crosswalks in this scene (e.g., the white SUV at 0.00s, the silver SUV at 38.03s, and the black car at 122.03s), but they all come to a halt behind the crosswalk lines, not on them.

### [stop-box] a vehicle stopped inside the intersection, blocking it

- **match** `exact` / conf `high` at 96.0-102.0s (clearest 98.0s)
  - subject: an articulated bus
  - An articulated bus turning left stops while still partially in the intersection, with its rear section blocking the crosswalk and part of the box, before resuming its movement.
- ruled out: A grey car at 106.03s to 110.03s stops inside the intersection while waiting to turn left. However, this is a normal yielding maneuver for a pedestrian in the crosswalk, not an instance of a vehicle blocking the intersection.

### [stop-lane] a vehicle stopped in a moving lane with traffic going around it

- **match** `exact` / conf `high` at 80.0-180.0s (clearest 92.0s)
  - subject: white box truck
  - A white box truck stops in the southbound moving lane and remains parked there for the duration of the clip. Multiple vehicles, including an articulated bus, a standard bus, vans, and cars, are forced to cross the center line into the oncoming lane to navigate around it.
- ruled out: The food truck parked near the bottom left is in a designated parking or loading lane, not a moving lane, so traffic simply passes it without having to change lanes. Vehicles that briefly pause in the intersection to make turns are yielding to oncoming traffic or pedestrians, which is normal operation and not considered being 'stopped in a moving lane' in this context.

### [transit-dwell] a bus stopped at the kerb with people getting on or off

- **absent**
  - why not: While there is a bus stop shelter visible on the top-left corner of the intersection, no bus ever pulls up to it or stops at any other kerb to load or unload passengers during this video.
- ruled out: A blue articulated bus enters the intersection at 86.03s and turns right to travel down the vertical street, exiting at 104.03s. However, it does not stop at the kerb, and no people get on or off.

### [ped-jaywalk] a pedestrian crossing the roadway outside the crosswalk markings

- **match** `exact` / conf `high` at 12.0-22.0s (clearest 18.0s)
  - subject: a pedestrian
  - A pedestrian crosses the main roadway from the left side to the right side, completely outside of any crosswalk markings.
- **match** `exact` / conf `high` at 110.0-120.0s (clearest 114.0s)
  - subject: a pedestrian
  - A pedestrian walks diagonally through the intersection, starting from the right side and ending on the bottom left, without using the marked crosswalks.
- **match** `exact` / conf `high` at 122.0-132.0s (clearest 126.0s)
  - subject: a pedestrian
  - A pedestrian crosses the main roadway from left to right, well below the intersection and outside the crosswalk.
- **match** `exact` / conf `high` at 160.0-168.0s (clearest 164.0s)
  - subject: a pedestrian
  - A pedestrian crosses the main roadway from the right side to the left side, just below the intersection and outside the marked crosswalk.
- ruled out: Several pedestrians are observed crossing the street within the marked crosswalks (e.g., around 34s, 76s, 108s, 138s). These were rejected as the query specifically asks for crossings outside the crosswalk markings. Construction workers are also seen in the roadway, but they are stationary or moving within a work zone, not crossing the street.

### [ped-standing] a pedestrian standing still in the roadway or crosswalk while traffic moves around them

- **match** `exact` / conf `high` at 88.0-102.0s (clearest 96.0s)
  - subject: pedestrian in the bottom crosswalk
  - A pedestrian crossing the street from right to left stops and stands still in the middle of the crosswalk to yield to an articulated bus turning right, waiting for the bus to fully pass before resuming their crossing.
- ruled out: Construction workers standing in the cordoned-off work zone at the top left were considered, but they are working in a protected area rather than acting as pedestrians navigating active traffic. Other pedestrians crossing the street throughout the video (e.g., at 18s, 68s, 110s, 128s, 158s) were also considered, but they cross continuously without having to stop and stand still in the roadway for moving vehicles.

### [ped-signal] a pedestrian crossing while the pedestrian signal for that crosswalk shows the red raised hand

- **match** `exact` / conf `high` at 12.0-22.0s (clearest 16.0s)
  - subject: pedestrian
  - A pedestrian enters the bottom crosswalk from the left and crosses to the right side while the pedestrian signal displays a red hand.
- **match** `exact` / conf `high` at 52.0-64.0s (clearest 58.0s)
  - subject: pedestrian
  - A pedestrian enters the bottom crosswalk from the right and crosses to the left side while the pedestrian signal displays a red hand.
- **match** `exact` / conf `high` at 106.0-116.0s (clearest 110.0s)
  - subject: pedestrian
  - A pedestrian enters the bottom crosswalk from the left and crosses to the right side while the pedestrian signal displays a red hand.
- **match** `exact` / conf `high` at 124.0-132.0s (clearest 128.0s)
  - subject: pedestrian
  - A pedestrian enters the bottom crosswalk from the left and crosses to the right side while the pedestrian signal displays a red hand.
- **match** `exact` / conf `high` at 134.0-142.0s (clearest 138.0s)
  - subject: pedestrian
  - A pedestrian enters the bottom crosswalk from the right and crosses to the left side while the pedestrian signal displays a red hand.
- **match** `exact` / conf `high` at 170.0-180.0s (clearest 176.0s)
  - subject: pedestrian
  - A pedestrian enters the bottom crosswalk from the left and crosses to the right side while the pedestrian signal displays a red hand.
- ruled out: Pedestrians who cross while the pedestrian signal displays the white 'walk' icon (for example, people crossing the top crosswalk at the beginning of the video) were not included. Additionally, a pedestrian who begins crossing the bottom crosswalk at 8.03s while the signal is white, and finishes crossing after it turns red, was excluded in favor of clearer examples where the pedestrian initiates the crossing against a red signal.

### [bike-sidewalk] a cyclist or e-bike rider riding on the sidewalk

- **absent**
  - why not: While multiple cyclists are observed in the street, no cyclists or e-bike riders are seen riding on any of the visible sidewalks during this timeframe.
- ruled out: Several cyclists and e-bike riders are visible in the footage, but all are using the roadway or designated bike lanes. For example, a cyclist rides down the avenue's bike lane from 104.03s to 110.03s, and pairs of riders cross the intersection on the cross street around 152.03s and 172.03s. These were rejected because they are not riding on the sidewalk.
- unreadable: The sidewalk on the right side of the avenue is completely covered by a scaffolding shed, making it impossible to see if any road users are present in that area.

### [bike-crosswalk] a cyclist or e-bike rider riding across a pedestrian crosswalk rather than walking the bike

- **match** `exact` / conf `high` at 34.0-38.0s (clearest 36.0s)
  - subject: cyclist
  - A cyclist rides from right to left across the northern pedestrian crosswalk.
- **match** `exact` / conf `high` at 110.0-114.0s (clearest 112.0s)
  - subject: cyclist
  - A cyclist rides from left to right across the southern pedestrian crosswalk.
- **match** `exact` / conf `high` at 152.0-156.0s (clearest 154.0s)
  - subject: cyclist
  - A cyclist rides from top to bottom across the western pedestrian crosswalk.
- **match** `exact` / conf `high` at 170.0-174.0s (clearest 172.0s)
  - subject: cyclist
  - A cyclist rides from left to right across the northern pedestrian crosswalk.
- ruled out: Cyclists riding straight through the intersection in the vehicle lanes (traveling with traffic) cross over the crosswalk markings but are not using the crosswalk as a pedestrian path; examples include 106.03-108.03 and 132.03-136.03. Between 122.03 and 128.03, a person crosses the western crosswalk, but they are walking and pushing their bike rather than riding it.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic in the roadway

- **match** `exact` / conf `high` at 108.0-114.0s (clearest 112.0s)
  - subject: a cyclist
  - A cyclist rides towards the top-right in the lanes closest to the camera. Because these lanes are designated for traffic moving towards the bottom-left, the cyclist is riding against the flow of traffic.
- ruled out: Cyclists observed at 36.03s, 120.03s, 126.03s, 132.03s, and 140.03s were checked, but all were riding in the correct designated lanes and directions for traffic.

### [negative] a vehicle that has driven up onto the sidewalk

- **absent**
  - why not: Throughout the video, all vehicles (cars, trucks, buses) remain on the designated roadways. No vehicle is observed driving up onto or parking on any of the pedestrian sidewalks.
- ruled out: I examined the white flatbed truck that enters the frame on the far right at 90.03s; due to the camera angle, it appears close to the corner, but it is driving on the roadway, not the sidewalk. I also observed the construction equipment in the top left quadrant (visible throughout), but this is operating within a cordoned-off work zone, not an active pedestrian sidewalk. Finally, I checked the vehicles parked along the curbs (e.g., bottom left, top right), and all appear to be parked in the roadway, not on the sidewalk.

### [negative] two vehicles making contact with each other

- **absent**
  - why not: Throughout the provided frames, traffic flows normally and vehicles successfully navigate the intersection without any collisions or physical contact with each other.
- ruled out: I examined multiple instances of vehicles navigating the intersection at the same time and passing close to one another. Notable examples include the articulated bus turning through the intersection between 84.03s and 104.03s while other vehicles were present, and the white box truck moving through around 112.03s to 116.03s. In all of these cases, the vehicles maintained proper clearance and no contact occurred.

---

14 call(s) ok, 0 failed, 1417380 in / 45048 out tokens