# probe run: rep1

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 0.5 | whole range, one call
- frames per call: 91 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `/home/yw4636/traffic_video/runs/20260829-214844-scene/with-scene/rep1`

## by axis

| axis | answered present | note |
|---|---|---|
| bike-sidewalk | 0/1 |  |
| bike-wrongway | 1/1 |  |
| emergency | 1/1 |  |
| negative | 0/2 | ground truth known: all absent |
| ped-conflict | 1/1 |  |
| pickup-car | 1/1 |  |
| right-hook | 1/1 |  |
| stop-crosswalk | 1/1 |  |
| turn-fty | 1/1 |  |

## per query

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it

- **match** `exact` / conf `high` at 62.0-68.0s (clearest 66.0s)
  - subject: dark SUV turning left
  - A dark SUV turns left from the horizontal street to travel down the vertical street. As it completes the turn, it drives through the lower crosswalk while a pedestrian is walking across it.
- **match** `exact` / conf `high` at 112.0-118.0s (clearest 116.0s)
  - subject: dark SUV turning left
  - A dark SUV turning left onto the vertical street passes through the lower crosswalk while a pedestrian is actively walking in it.
- **match** `exact` / conf `high` at 122.0-128.0s (clearest 126.0s)
  - subject: dark SUV turning left
  - A dark SUV makes a left turn onto the vertical street, continuing through the lower crosswalk while two pedestrians are crossing.
- ruled out: Several other vehicles make turns through crosswalks, but without pedestrians present in them at the time. For instance, the articulated bus turning right at 90.03s, the mail truck turning left at 136.03s, and the yellow taxi turning right at 178.03s all pass through empty crosswalks.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight

- **match** `exact` / conf `high` at 34.0-38.0s (clearest 36.0s)
  - subject: grey SUV and cyclist
  - A cyclist travels straight (left to right) across the intersection on the horizontal street. A grey SUV traveling the same direction turns right onto the vertical street, cutting directly across the cyclist's path just behind them.
- ruled out: I also considered the interactions at 112.03-116.03 (dark sedan) and 148.03-154.03 (dark SUV), where a vehicle on the vertical street intended to turn left while a cyclist approached from the opposite direction. These were rejected because the turning vehicles yielded, waiting for the cyclist to pass through the intersection before completing their turn, so they did not actively turn across the cyclist's path.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to

- **match** `exact` / conf `high` at 146.0-154.0s (clearest 148.0s)
  - subject: dark SUV
  - A dark SUV descending the vertical street stops with its front tires on the crosswalk markings while a pedestrian crosses right in front of it.
- **match** `exact` / conf `high` at 176.0-180.0s (clearest 178.0s)
  - subject: dark car
  - A dark car descending the vertical street stops with its front end on the crosswalk markings while a pedestrian waits on the right curb to cross.
- ruled out: At 96.03s, the tail end of a left-turning articulated bus blocks the top crosswalk while a pedestrian crosses behind it, but the bus is stuck mid-turn in the intersection rather than stopping at the crosswalk approach. At 134.03s, a white USPS truck stops for pedestrians at the top crosswalk, but it stops properly behind the line and does not encroach on the markings.

### [pickup-car] a person getting into or out of a stopped car, van or taxi

- **match** `exact` / conf `high` at 46.0-54.0s (clearest 50.0s)
  - subject: a person and a black SUV
  - A black SUV stops in the downward-traveling lanes. A person approaches the driver's side door, gets inside the vehicle, and the SUV then drives away.
- ruled out: A yellow taxi turns right and stops at the crosswalk between 176.03s and 180.03s. It is only yielding to a pedestrian; no one gets into or out of the vehicle.
- unreadable: The camera's low framerate means the precise moment the car door is open and the person steps inside falls in the gap between 50.03s and 52.03s, but the sequence of events is clear from the surrounding frames.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk

- **match** `exact` / conf `high` at 118.0-124.0s (clearest 122.0s)
  - subject: a pedestrian and two SUVs
  - A pedestrian is crossing the lower crosswalk from right to left. While they are in the crosswalk, a white SUV turning left and a black SUV going straight drive through the downward lanes of that same crosswalk.
- ruled out: At 54.03s - 58.03s, a pedestrian is in the lower crosswalk while a white car makes a turn, but the car drives through the left crosswalk, not the same one as the pedestrian. At 162.03s - 168.03s, another pedestrian uses the lower crosswalk, but no vehicles drive through it while they are there.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians

- **absent**
  - why not: The video shows numerous cyclists and e-bike riders, but all of them are using the roadway or marked crosswalks. No rider is observed traveling along the length of a sidewalk among pedestrians.
- ruled out: Cyclists are present at 36.03-38.03s, 112.03-122.03s, and frequently between 136.03-176.03s. In all these cases, they are either riding in the roadway with vehicular traffic or using the marked crosswalks to cross the intersection. None are seen riding longitudinally along the sidewalks.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic

- **match** `exact` / conf `high` at 112.0-126.0s (clearest 118.0s)
  - subject: cyclist
  - A cyclist travels up the frame in the left-hand lanes of the vertical street, against the designated downward flow of traffic for those lanes.
- ruled out: Cyclists can be seen exhibiting potentially irregular or brief wrong-way behavior within the horizontal street and intersection around 36.03s - 40.03s. However, the sequence starting at 112.03s is a much clearer and prolonged instance of a cyclist traveling a significant distance in the opposing traffic lane.

### [emergency] an emergency vehicle with lights flashing passing through the intersection

- **match** `exact` / conf `high` at 32.0-36.0s (clearest 34.0s)
  - subject: Police vehicle
  - A police vehicle with its emergency lights flashing enters the intersection from the right on the horizontal street and travels through to the left.
- ruled out: No other emergency vehicles were seen in this sequence.

### [negative] two vehicles making contact with each other

- **absent**
  - why not: The frames show normal traffic flow with vehicles maintaining safe distances from one another. No collision or contact between any two vehicles occurs.
- ruled out: I reviewed the frames for any interacting vehicles, particularly at the central intersection where paths cross. Several vehicles, including cars, trucks, and articulated buses, navigate the intersection, but none of them collide or make contact.

### [negative] a horse-drawn carriage

- **absent**
  - why not: No horse-drawn carriages appear in this video window. Only motor vehicles, bicycles, and pedestrians are present.
- ruled out: I scanned all frames for a horse-drawn carriage.

---

10 call(s) ok, 0 failed, 1016414 in / 29595 out tokens