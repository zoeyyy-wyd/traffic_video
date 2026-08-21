# probe run: full-pro

- clip: `data/12thFBotwinik/L12thFloorBotwinik-D-2025-11-03_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- roi: `0.28,0.00,0.40,0.42` | fps: 0.5 | whole range, one call
- frames per call: 90 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/full-pro`

## by axis

| axis | answered present | note |
|---|---|---|
| negative | 2/5 | **every hit here is a fabrication** |
| referential | 3/4 |  |
| relational | 4/4 |  |
| spatial | 3/4 |  |
| state | 2/2 |  |
| temporal | 3/3 |  |

## per query

### [referential] an articulated (bendy) city bus passing through the intersection

- **match** `exact` / conf `high` at 136.0-156.0s (clearest 144.0s)
  - subject: articulated city bus
  - An articulated city bus enters the intersection from the left, makes a left turn (clearly showing its flexible middle section), and exits the frame to the top left.
- ruled out: A large white box truck passes through the intersection between 112.03s and 116.03s, but it was ruled out as it is not a bus and is not articulated.

### [referential] a yellow taxi

- **match** `exact` / conf `high` at 26.0-28.0s (clearest 26.0s)
  - subject: a yellow taxi
  - A yellow taxi enters the intersection from the left, turns right, and exits at the bottom edge of the frame.
- **match** `exact` / conf `high` at 78.0-86.0s (clearest 80.0s)
  - subject: a yellow taxi (sedan)
  - A yellow sedan taxi enters from the left and drives straight across the intersection, exiting to the right.
- **match** `exact` / conf `high` at 78.0-88.0s (clearest 82.0s)
  - subject: a yellow taxi (SUV)
  - A yellow SUV taxi enters the intersection from the right, turns left, and drives upwards away from the camera.
- **match** `exact` / conf `high` at 118.0-130.0s (clearest 124.0s)
  - subject: a yellow taxi
  - A yellow taxi enters from the right and proceeds straight through the intersection, eventually exiting to the left.
- ruled out: There are transient appearances of a yellow taxi at the bottom edge of the frame (e.g., at 42.03s and 88.03s), but they are only briefly visible for a single frame without showing a full traversal or action, so they were excluded in favor of the more complete sequences.

### [referential] a delivery van stopped at the kerb

- **absent**
  - why not: A box truck is seen driving through the intersection, but no delivery van is ever observed stopping or parked at the kerb.
- ruled out: The white box truck (Penske) crossing the intersection from right to left between 112.03s and 116.03s. It was rejected because it drives straight through and does not stop at the kerb.

### [referential] a cyclist or e-bike rider crossing the intersection

- **match** `exact` / conf `high` at 14.0-20.0s (clearest 16.0s)
  - subject: an e-bike rider
  - An e-bike rider enters from the left side of the frame and crosses the intersection horizontally to the right.
- **match** `exact` / conf `high` at 94.0-100.0s (clearest 98.0s)
  - subject: a delivery worker on an e-bike
  - A delivery worker riding an e-bike with a yellow cargo box crosses the intersection from left to right along the bottom crosswalk area.
- **match** `exact` / conf `high` at 136.0-144.0s (clearest 140.0s)
  - subject: a rider on a moped or e-bike
  - A rider on a moped or e-bike enters the frame from the left and crosses the intersection to the right side.
- **match** `exact` / conf `high` at 160.0-168.0s (clearest 164.0s)
  - subject: a cyclist
  - A cyclist enters from the right side of the intersection and crosses over to the left side.
- ruled out: Considered the person crossing the south crosswalk between 38.03s and 42.03s, but they appear to be a pedestrian pushing a cart or stroller rather than a cyclist riding. Also noted a cyclist entering the left crosswalk at 48.03s, but they turn and move off-screen quickly without crossing the main intersection in a clear trajectory.

### [spatial] a pedestrian still inside the crosswalk while a vehicle passes behind them

- **match** `exact` / conf `high` at 24.0-30.0s (clearest 28.0s)
  - subject: a pedestrian and a dark SUV
  - A pedestrian crosses the top crosswalk from right to left. As they near the left sidewalk, a dark SUV driving straight through the intersection passes through the crosswalk directly behind them.
- **match** `exact` / conf `high` at 34.0-40.0s (clearest 38.0s)
  - subject: a pedestrian and a black car
  - A pedestrian crosses the top crosswalk from left to right. As they approach the right side, a black car going straight passes through the crosswalk behind them.
- **match** `exact` / conf `high` at 42.0-46.0s (clearest 44.0s)
  - subject: a pedestrian and a white car
  - A pedestrian crosses the left crosswalk heading downwards. A white car driving straight from right to left passes through the intersection behind the pedestrian's path.
- **match** `exact` / conf `high` at 90.0-96.0s (clearest 94.0s)
  - subject: a pedestrian and a black car
  - A pedestrian is near the end of the top crosswalk, moving left to right, when a black car traveling straight passes through the crosswalk behind them.
- **match** `exact` / conf `high` at 98.0-104.0s (clearest 102.0s)
  - subject: a pedestrian and a black SUV
  - A pedestrian crosses the top crosswalk from left to right. As they near the right sidewalk, a black SUV traveling straight passes behind them.
- **match** `exact` / conf `high` at 168.0-172.0s (clearest 170.0s)
  - subject: a pedestrian and a black SUV
  - A pedestrian is about halfway across the top crosswalk (moving left to right) when a black SUV traveling straight passes through the crosswalk behind them.
- **match** `exact` / conf `high` at 174.0-178.0s (clearest 176.0s)
  - subject: a pedestrian and a white car
  - A pedestrian crosses the top crosswalk from left to right. A white car turning left passes through the crosswalk behind the pedestrian.
- ruled out: Several instances were rejected because a vehicle passed in front of a crossing pedestrian, causing them to wait or yield, rather than passing behind them. Examples include a black SUV at 16.03s, a silver SUV at 48.03s, a black SUV at 136.03s, and a silver car at 150.03s.

### [spatial] a vehicle stopped with part of its body over the crosswalk markings

- **match** `exact` / conf `high` at 118.0-126.0s (clearest 124.0s)
  - subject: yellow taxi
  - A yellow taxi is stopped at the red light on the right-hand crosswalk, with its front end extending over the white crosswalk markings.
- **match** `exact` / conf `high` at 162.0-168.0s (clearest 166.0s)
  - subject: blue and yellow bus
  - A blue and yellow bus is stopped at the left-hand crosswalk, with its front bumper resting over the crosswalk markings.
- ruled out: The Penske truck between 110.03s and 114.03s passes over the crosswalk but does not stop. Several vehicles stop at the top crosswalk (e.g., the dark minivan at 28.03s and the dark SUV at 80.03s), but they stop correctly behind the stop line and do not block the crosswalk markings.

### [spatial] a cyclist riding on the sidewalk rather than in the roadway

- **match** `exact` / conf `high` at 150.0-162.0s (clearest 154.0s)
  - subject: cyclist on the right sidewalk
  - A cyclist appears in the lower right corner and rides upwards along the right sidewalk, remaining completely on the pedestrian path between the buildings and the parked cars.
- ruled out: Several other cyclists appear in the video, but they are all riding in the roadway or bike lanes. For example, a cyclist with green underglow rides in the bike lane on the left side of the road between 18.03s and 20.03s, and another cyclist with a very bright headlight crosses the intersection in the roadway from 120.03s to 126.03s.

### [spatial] a vehicle waiting inside the intersection box rather than behind the line

- **absent**
  - why not: Throughout the video, all vehicles that are required to stop for a red light or traffic do so behind the marked stop lines. No vehicle is seen entering the intersection box and coming to a stop to wait inside it.
- ruled out: A white SUV stops briefly at t=24.03s with its door open, apparently to discharge a passenger, but it stops primarily on the crosswalk rather than pulling fully into the intersection box to wait. Several other vehicles stop for traffic signals (e.g., a dark SUV from t=6.03s to t=16.03s, and other vehicles around t=28.03s), but they all stop correctly behind the designated stop lines.

### [temporal] the moment a stopped bus begins to move off

- **match** `exact` / conf `high` at 166.0-172.0s (clearest 168.0s)
  - subject: the articulated bus
  - The bus, which had been waiting stationary on the cross street, pulls away and drives out of the frame.
- ruled out: I looked for other instances of buses stopping and starting, but this is the only bus that appears in the video.

### [temporal] the moment a pedestrian steps off the kerb into the roadway

- **match** `exact` / conf `high` at 8.0-12.0s (clearest 10.0s)
  - subject: a pedestrian
  - A pedestrian on the right side of the intersection approaches the crosswalk and steps off the kerb into the roadway.
- **match** `exact` / conf `high` at 32.7-36.0s (clearest 34.0s)
  - subject: a pedestrian
  - A pedestrian on the left side of the intersection steps off the kerb into the crosswalk.
- ruled out: Pedestrians who are already in the middle of the roadway (such as those crossing at 28.03s or 160.03s) were not selected, as the decisive moment they step off the kerb is less clear or happens outside a concise window. Several other valid instances occur in the video; representative clear examples were chosen.

### [temporal] a vehicle braking noticeably harder than the traffic around it

- **match** `exact` / conf `high` at 156.0-162.0s (clearest 158.0s)
  - subject: a dark grey car
  - A dark grey car driving left to right brakes suddenly in the middle of the intersection, illuminating its brake lights, to avoid a person on a scooter crossing directly in its path.
- ruled out: The black car at 90.03s appears to stop abruptly at the crosswalk line with bright brake lights, but this is a normal stop for the intersection rather than an unexpected or unusually hard brake compared to surrounding traffic flow. The dark grey SUV at 28.03s slows down normally to a stop, which does not constitute hard braking.

### [relational] a vehicle that entered the intersection and had to stop partway because someone was crossing in front of it

- **match** `exact` / conf `high` at 140.0-148.0s (clearest 144.0s)
  - subject: the articulated bus turning left
  - The bus enters the intersection to turn left, but has to stop in the middle of the intersection to wait for a pedestrian crossing in front of its path.
- **match** `exact` / conf `high` at 170.0-176.0s (clearest 174.0s)
  - subject: the white car turning left
  - The white car enters the intersection to turn left, then stops partway through to yield to a pedestrian crossing the crosswalk before completing its turn.
- ruled out: Several vehicles turn right (e.g., the dark car at 34.03s) but yield to pedestrians before entering the intersection, which does not match the prompt's requirement to stop 'partway' in the intersection. Other vehicles (like the yellow taxi turning left at 126.03s) enter and complete their turns without having to stop for pedestrians.

### [relational] a turning vehicle that waited for pedestrians to finish crossing before completing its turn

- **match** `exact` / conf `high` at 124.0-128.0s (clearest 126.0s)
  - subject: yellow taxi
  - A yellow taxi turns right from the right road to the top road. It pauses mid-turn in the intersection to allow a pedestrian crossing the top road to clear its path before completing the turn.
- ruled out: A yellow taxi turns right from the top road to the right road between 78.03s and 82.03s. While there is a pedestrian in the crosswalk, the taxi does not noticeably stop or wait; it completes the turn as the pedestrian is already out of its immediate path.

### [relational] a pedestrian who started to cross, then stopped or stepped back because of an approaching vehicle

- **match** `exact` / conf `high` at 90.0-96.0s (clearest 92.0s)
  - subject: pedestrian on the top-left corner
  - A pedestrian steps off the curb to cross the top crosswalk from left to right, but sees an approaching black car and steps back onto the sidewalk.
- **match** `exact` / conf `high` at 166.0-174.0s (clearest 170.0s)
  - subject: pedestrian on the right crosswalk
  - A pedestrian begins crossing the right crosswalk from top to bottom, but stops in the middle of the lane to yield to a turning car before resuming their crossing.
- ruled out: The pedestrian at the top-right corner at t=146.03 waits for the articulated bus to turn left before entering the crosswalk, rather than starting to cross and then aborting.

### [relational] two road users passing close enough that one visibly changed course or speed

- **match** `exact` / conf `high` at 168.0-172.0s (clearest 170.0s)
  - subject: grey car and cyclist
  - A cyclist crosses the intersection from right to left, passing closely in front of a grey car traveling straight up the avenue. The grey car visibly swerves to its right to avoid the cyclist before continuing.
- ruled out: At t=16.03s to t=20.03s, two cyclists cross paths in the intersection, but neither visibly alters their course or speed to avoid the other; they just pass cleanly.
At t=122.03s to t=126.03s, a cyclist crosses in front of a yellow taxi, but neither road user visibly swerves or changes speed.
At t=136.03s to t=140.03s, a cyclist stops to wait for an articulated bus to complete its turn, which is a standard yield rather than a dynamic evasive maneuver during a close pass.

### [state] a vehicle crossing the stop line while its signal was red

- **match** `exact` / conf `high` at 108.0-112.0s (clearest 110.0s)
  - subject: a dark SUV from the side street
  - The SUV crosses the stop line on the side street and proceeds straight across the intersection while the traffic signal facing it clearly displays a red light.
- ruled out: I observed a white SUV turning right from the side street at t=22.03 while facing a red signal, and several yellow taxis entering the intersection from the main road around t=78.03-82.03 when their signal appeared to be red. However, the dark SUV proceeding straight through the intersection at t=110.03 provides a more unambiguous and complete example of a vehicle crossing the stop line on a red signal.

### [state] pedestrians crossing while their signal was against them

- **match** `exact` / conf `high` at 22.0-28.0s (clearest 26.0s)
  - subject: a pedestrian in dark clothing
  - A pedestrian walks across the top crosswalk of the main road from left to right while a light SUV and a yellow taxi drive through on the main road, indicating the pedestrian signal is red.
- **match** `exact` / conf `high` at 38.0-44.0s (clearest 40.0s)
  - subject: two pedestrians
  - Two pedestrians cross the side street's left crosswalk from the median to the sidewalk while a dark SUV drives straight down the side street through the intersection, showing they are crossing against their signal.
- **match** `exact` / conf `high` at 88.0-94.0s (clearest 90.0s)
  - subject: a pedestrian with an orange bag or clothing
  - A pedestrian crosses the main street's top crosswalk from right to left while a black car drives past them on the main street, indicating they are crossing against a red pedestrian signal.
- **match** `exact` / conf `high` at 130.0-136.0s (clearest 132.0s)
  - subject: a pedestrian in dark clothing
  - A pedestrian walks across the top crosswalk of the main road from left to right just as a black car and an articulated bus drive through the intersection on the main road.
- ruled out: Pedestrians crossing the left crosswalk around 28.03s to 32.73s were rejected because the main road traffic was flowing, meaning the side street was red, so these pedestrians likely had a 'walk' signal to cross the side street. Similarly, a pedestrian crossing the bottom crosswalk from 34.03s to 38.03s was rejected; a dark SUV was entering the intersection from the side street, indicating the side street had a green light and the pedestrian likely had a 'walk' signal to cross the main road.

### [negative] a fire truck with flashing lights driving through the intersection

- **absent**
  - why not: No fire truck appears in this video sequence.
- ruled out: A white box truck crosses from right to left between 112.03s and 116.03s, and a long blue-and-white articulated city bus makes a right turn through the intersection between 136.03s and 148.03s. Neither of these is a fire truck.

### [negative] a horse-drawn carriage

- **absent**
  - why not: No horse-drawn carriage entered or passed through the intersection during this time window.
- ruled out: I scanned the footage specifically for a horse-drawn carriage. The vehicles present in the intersection are standard cars, taxis, SUVs, delivery trucks, bicycles, scooters, and an articulated bus.

### [negative] a collision in which two vehicles make contact

- **absent**
  - why not: All vehicles navigate the intersection without making contact with one another; no collisions occur in the provided video segment.
- ruled out: No vehicles ever appear to be on a collision course or interact closely in this video.

### [negative] a vehicle driving the wrong way against the flow of traffic

- **match** `exact` / conf `high` at 152.0-158.0s (clearest 154.0s)
  - subject: an articulated bus
  - An articulated bus traveling left-to-right (eastbound) enters and crosses the intersection while driving entirely in the lanes designated for oncoming (westbound) traffic, clearly visible above the double yellow line.
- ruled out: The silver mapping car at 0.00s traveling left-to-right is in the correct lane (below the implied median). The articulated bus at 144.03s approaches the intersection in the correct lane before turning right. The regular bus at 168.03s travels straight through in the correct lane.

### [negative] a person lying in the roadway

- **match** `exact` / conf `high` at 48.0-48.0s (clearest 48.0s)
  - subject: cyclist with a blue cart
  - A cyclist falls and is seen down on the roadway surface within the crosswalk.
- ruled out: At t=96.03s, a delivery worker's cart tips over, but the person themselves remains standing and does not end up lying in the roadway.

---

22 call(s) ok, 0 failed, 0 in / 0 out tokens