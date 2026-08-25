# probe run: full-pro-wide

- clip: `data/12thFBotwinik/L12thFloorBotwinik-D-2025-11-03_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- roi: `wide` | fps: 0.5 | whole range, one call
- frames per call: 90 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/full-pro-wide`

## by axis

| axis | answered present | note |
|---|---|---|
| negative | 2/5 | **every hit here is a fabrication** |
| referential | 4/4 |  |
| relational | 3/4 |  |
| spatial | 3/4 |  |
| state | 2/2 |  |
| temporal | 3/3 |  |

## per query

### [referential] an articulated (bendy) city bus passing through the intersection

- **match** `exact` / conf `high` at 72.0-114.0s (clearest 90.0s)
  - subject: articulated city bus
  - An articulated city bus enters from the bottom of the frame, drives straight through the intersection, and exits at the top.
- **match** `exact` / conf `high` at 130.0-148.0s (clearest 140.0s)
  - subject: articulated city bus
  - An articulated city bus enters from the bottom of the frame, makes a left turn through the intersection, and exits to the left.
- **match** `exact` / conf `high` at 150.0-168.0s (clearest 158.0s)
  - subject: articulated city bus
  - An articulated city bus enters from the right side of the frame, drives straight across the far side of the intersection, and exits to the left.
- ruled out: The bus visible from t=0.00s to t=10.03s was considered but rejected because it is a standard, non-articulated bus.

### [referential] a yellow taxi

- **match** `exact` / conf `high` at 0.0-22.0s (clearest 14.0s)
  - subject: a yellow taxi
  - A yellow taxi travels straight through the intersection heading north, stopping briefly at the crosswalk before proceeding.
- **match** `exact` / conf `high` at 26.0-30.0s (clearest 28.0s)
  - subject: a yellow taxi
  - A yellow taxi turns right, heading east.
- **match** `exact` / conf `high` at 78.0-86.0s (clearest 82.0s)
  - subject: a yellow taxi
  - A yellow taxi turns left, heading west.
- **match** `exact` / conf `high` at 88.0-94.0s (clearest 90.0s)
  - subject: a yellow taxi
  - A yellow taxi travels straight through the intersection heading north, and then turns left.
- **match** `exact` / conf `high` at 120.0-128.0s (clearest 124.0s)
  - subject: a yellow taxi
  - A yellow taxi turns left, heading west.
- **match** `exact` / conf `high` at 132.0-140.0s (clearest 136.0s)
  - subject: a yellow taxi
  - A yellow taxi travels straight through the intersection heading north, and then turns left.
- **match** `exact` / conf `high` at 168.0-178.0s (clearest 174.0s)
  - subject: a yellow taxi
  - A yellow taxi travels straight through the intersection heading north.
- ruled out: There are no ambiguous cases; all instances of yellow taxis are clearly identifiable as such.

### [referential] a delivery van stopped at the kerb

- **match** `exact` / conf `high` at 0.0-178.0s (clearest 80.0s)
  - subject: white delivery van
  - A white delivery van remains parked at the kerb on the bottom left side of the street for the entire duration of the video segment.
- ruled out: A white box truck with blue stripes is visible on the cross street from t=112.03s to t=116.03s. While it briefly stops at the intersection, it is waiting in a travel lane, not stopped at the kerb.

### [referential] a cyclist or e-bike rider crossing the intersection

- **match** `exact` / conf `high` at 0.0-4.0s (clearest 2.0s)
  - subject: a cyclist
  - A cyclist crosses the intersection from the top left towards the bottom right.
- **match** `exact` / conf `high` at 16.0-22.0s (clearest 18.0s)
  - subject: an e-bike rider
  - An e-bike rider enters the intersection from the top right and crosses towards the top left.
- **match** `exact` / conf `high` at 94.0-98.0s (clearest 96.0s)
  - subject: an e-bike rider
  - An e-bike rider crosses the intersection from the top left towards the top right.
- **match** `exact` / conf `high` at 122.0-128.0s (clearest 124.0s)
  - subject: an e-bike rider
  - An e-bike rider with a bright headlight crosses the intersection from the top left towards the top right.
- **match** `exact` / conf `high` at 138.0-144.0s (clearest 140.0s)
  - subject: a cyclist
  - A cyclist crosses the intersection from the top left towards the top right.
- ruled out: Riders crossing on stand-up electric scooters between 44.03s - 48.03s and 60.03s - 64.03s were not included, as the prompt specifically asks for cyclists or e-bike riders.

### [spatial] a pedestrian still inside the crosswalk while a vehicle passes behind them

- **match** `exact` / conf `high` at 10.0-14.0s (clearest 12.0s)
  - subject: pedestrian in the top crosswalk
  - A pedestrian crosses the top crosswalk, and a silver car turning left passes directly behind them while they are still in the roadway.
- **match** `exact` / conf `high` at 168.0-172.0s (clearest 170.0s)
  - subject: pedestrian in the near crosswalk
  - A pedestrian crosses the near crosswalk from right to left, and a silver car driving straight through the intersection passes behind them.
- ruled out: Several instances of vehicles passing *in front* of pedestrians in crosswalks were rejected, such as at 30.03s (dark SUV in near crosswalk), 126.03s (taxi in top crosswalk), and 138.03s-144.03s (car and bus in top crosswalk). At 66.03s, a vehicle passes behind a person crossing on a scooter, but they are not a pedestrian walking.

### [spatial] a vehicle stopped with part of its body over the crosswalk markings

- **match** `exact` / conf `high` at 76.0-114.0s (clearest 90.0s)
  - subject: the articulated bus (number 5444)
  - An articulated bus stops at a red light. Its front end is clearly resting over the zebra stripes of the crosswalk.
- **match** `exact` / conf `high` at 136.0-140.0s (clearest 138.0s)
  - subject: an articulated bus
  - An articulated bus stops at the intersection before making a right turn. Its front section comes to rest over the crosswalk markings.
- **match** `exact` / conf `high` at 164.0-172.0s (clearest 168.0s)
  - subject: the blue and white bus
  - A blue and white bus traveling on the cross street stops at a red light, with its front end encroaching significantly onto the crosswalk markings.
- ruled out: The green and white bus stopped at the red light from 0.00s to 14.03s was considered, but its front bumper remains largely behind the stop line and does not meaningfully rest over the crosswalk markings. Another articulated bus that stops at the light from 118.03s to 132.03s was also rejected; it stops much further back than the first bus, with its front resting behind or directly on the stop line rather than over the crosswalk.

### [spatial] a cyclist riding on the sidewalk rather than in the roadway

- **absent**
  - why not: No cyclists were observed riding on any of the sidewalks in the provided frames. All visible cyclists are using the roadway.
- ruled out: Several cyclists are visible throughout the footage (e.g., crossing the intersection at 0.00s, 56.03s-60.03s, 122.03s, 138.03s-142.03s, and 168.03s-172.03s). However, all of these cyclists are riding in the roadway or within the crosswalks, not on the sidewalks.

### [spatial] a vehicle waiting inside the intersection box rather than behind the line

- **match** `exact` / conf `high` at 24.0-28.0s (clearest 26.0s)
  - subject: white SUV
  - A white SUV enters the intersection to make a left turn and waits inside the box for an oncoming yellow taxi to pass before completing its turn.
- ruled out: Several other vehicles turn left or pass through the intersection, such as the yellow taxi turning left between 82.03s and 88.03s, or the black sedan between 90.03s and 94.03s. However, these vehicles move continuously through the intersection and do not stop or wait inside the box.

### [temporal] the moment a stopped bus begins to move off

- **match** `exact` / conf `high` at 4.0-10.0s (clearest 6.0s)
  - subject: white and green bus
  - The bus, which was waiting at the intersection, begins to accelerate forward and cross the intersection.
- **match** `exact` / conf `high` at 88.0-94.0s (clearest 90.0s)
  - subject: articulated bus
  - An articulated bus that had been stopped at the crosswalk begins to pull forward into the intersection.
- **match** `exact` / conf `high` at 128.0-134.0s (clearest 130.0s)
  - subject: articulated bus
  - Another articulated bus (which has the same roof number) that was stopped at the crosswalk begins moving forward into the intersection.
- ruled out: Multiple blue buses travel along the cross street in the later part of the video, either going straight across or making turns. However, none of these buses come to a stop within the frame.

### [temporal] the moment a pedestrian steps off the kerb into the roadway

- **match** `exact` / conf `high` at 12.0-14.0s (clearest 14.0s)
  - subject: pedestrian on the bottom right corner
  - A pedestrian walks toward the street and steps off the kerb into the right crosswalk.
- **match** `exact` / conf `high` at 22.0-24.0s (clearest 24.0s)
  - subject: pedestrian on the bottom right corner
  - A pedestrian steps off the kerb into the right crosswalk.
- **match** `exact` / conf `high` at 58.0-60.0s (clearest 60.0s)
  - subject: pedestrian on the bottom left corner
  - A pedestrian steps off the kerb into the bottom crosswalk.
- **match** `exact` / conf `high` at 124.0-126.0s (clearest 126.0s)
  - subject: pedestrian on the bottom right corner
  - A pedestrian steps off the kerb into the right crosswalk.
- **match** `exact` / conf `high` at 166.0-168.0s (clearest 168.0s)
  - subject: two pedestrians on the bottom right corner
  - Two pedestrians step off the kerb into the bottom crosswalk.
- ruled out: Pedestrians who are already in the middle of a crosswalk (such as those in the top crosswalk around 36.03s) were excluded, as the specific action of stepping off the kerb is not captured.

### [temporal] a vehicle braking noticeably harder than the traffic around it

- **match** `exact` / conf `high` at 94.0-98.0s (clearest 96.0s)
  - subject: articulated bus
  - An articulated bus traveling upwards through the intersection is forced to brake hard and come to a sudden stop to avoid colliding with a black car that abruptly stops in its path.
- ruled out: I considered the vehicles coming to a stop at the red light at the bottom of the screen (e.g., the white car and yellow taxi from 0.00s to 30.03s). However, they decelerate gradually and normally for a traffic signal, which does not fit the description of braking 'noticeably harder' than surrounding traffic. I also considered the black SUV that causes the bus to brake (stops abruptly at 92.03s), but the bus's emergency braking is a more prominent and clear example of the described situation.

### [relational] a vehicle that entered the intersection and had to stop partway because someone was crossing in front of it

- **match** `exact` / conf `high` at 78.0-88.0s (clearest 82.0s)
  - subject: a yellow cab entering from the right and turning left
  - The cab enters the intersection to make a left turn, stops in the middle to yield to pedestrians crossing its path, and then continues once they have passed.
- **match** `exact` / conf `high` at 122.0-130.0s (clearest 124.0s)
  - subject: a yellow cab entering from the right and turning left
  - The cab enters the intersection and pauses its turn to allow a pedestrian to clear the crosswalk before proceeding.
- ruled out: The white car entering from the left at 172.03s stops in the intersection before making a left turn, but it is yielding to an oncoming vehicle, not someone crossing in front of it.

### [relational] a turning vehicle that waited for pedestrians to finish crossing before completing its turn

- **match** `exact` / conf `high` at 78.0-88.0s (clearest 84.0s)
  - subject: yellow taxi
  - A yellow taxi turns left into the bottom street, stops to yield to pedestrians in the crosswalk, and then completes its turn once the path is clear.
- ruled out: The black SUV turning left from 96.03s to 104.03s also waits for pedestrians, but the yellow taxi at 84.03s provides a clearer, more prominent example. The white SUV turning right around 126.03s passes in front of a pedestrian rather than waiting for them to cross.

### [relational] a pedestrian who started to cross, then stopped or stepped back because of an approaching vehicle

- **match** `exact` / conf `high` at 126.0-132.0s (clearest 128.0s)
  - subject: pedestrian starting to cross from the top right corner
  - A pedestrian steps off the curb into the top crosswalk, but stops their forward motion to allow a yellow cab to complete a right turn in front of them before resuming their crossing.
- ruled out: At 24.03s-28.03s, a pedestrian crosses the top crosswalk from right to left while a yellow cab turns right. However, the pedestrian continues walking without stopping, and the cab passes behind them. At 46.03s-50.03s, a pedestrian crosses the top crosswalk from left to right as a white car turns right, but again the pedestrian does not stop or hesitate.

### [relational] two road users passing close enough that one visibly changed course or speed

- **absent**
  - why not: While the intersection is busy, traffic flows smoothly, and drivers yield predictably. There are no observed instances of near-misses or unexpectedly close passes that force a road user to visibly alter their trajectory or suddenly change speed in evasion.
- ruled out: Several moments involve road users yielding to each other, but none depict an evasive maneuver (sudden swerving or hard braking) caused by passing too close. For instance, at 118.03s, a yellow cab turning left slows down to yield to a running pedestrian in the crosswalk. Between 126.03s and 130.03s, another left-turning yellow cab waits for a white car to cross the intersection. At 142.03s, a left-turning blue bus waits for a straight-traveling articulated bus. All these are standard, anticipated yielding behaviors rather than reactive changes in course or speed due to a close encounter.

### [state] a vehicle crossing the stop line while its signal was red

- **match** `exact` / conf `high` at 124.0-128.0s (clearest 126.0s)
  - subject: white SUV crossing left to right
  - A white SUV approaching from the left is shown behind the crosswalk while the light is yellow at 124.03s. By 126.03s, the light has turned red and the SUV is crossing the stop line, proceeding through the intersection.
- ruled out: Several other vehicles cross the intersection during the video, such as the white box truck around 112s and the articulated bus around 136s, but these entered the intersection while their signals were green.

### [state] pedestrians crossing while their signal was against them

- **match** `exact` / conf `high` at 12.0-18.0s (clearest 16.0s)
  - subject: a pedestrian on the left
  - A pedestrian crosses the cross-street in the left crosswalk while cross-street vehicles have the right-of-way and are actively driving through the intersection.
- **match** `exact` / conf `high` at 60.0-72.0s (clearest 68.0s)
  - subject: multiple pedestrians
  - Several pedestrians cross the avenue on both the upper and lower crosswalks while the avenue traffic has a green light and vehicles are actively flowing through the intersection.
- **match** `exact` / conf `high` at 122.0-130.0s (clearest 126.0s)
  - subject: a pedestrian on the left
  - A pedestrian walks downwards across the cross-street on the left side while cross-street traffic is actively moving through the intersection.
- ruled out: Pedestrians who enter the crosswalk just as the light changes were considered but rejected as matches, since they may have legally entered the intersection on a lagging walk or yellow signal. Only instances where pedestrians are crossing well into the green phase for conflicting traffic were included, making it unambiguous that the pedestrian signal was against them.

### [negative] a fire truck with flashing lights driving through the intersection

- **absent**
  - why not: A fire truck with flashing lights never appears in this sequence of frames.
- ruled out: Several large vehicles passed through the intersection during the video, including a standard transit bus and an articulated transit bus. A white box truck is also parked in the lower left corner. None of these vehicles are a fire truck.

### [negative] a horse-drawn carriage

- **absent**
  - why not: No horse-drawn carriage is present in this sequence.
- ruled out: I scanned all vehicles passing through the intersection, looking for a horse-drawn carriage. The vehicles present are primarily cars, taxis, buses, and delivery trucks.

### [negative] a collision in which two vehicles make contact

- **absent**
  - why not: No collisions occurred in the provided frames. All visible vehicles passed through the intersection or navigated around each other without any physical contact.
- ruled out: I reviewed the entire sequence, paying close attention to moments where vehicles crossed paths or turned near each other (e.g., around 46.03s, 86.03s, and 168.03s). However, in all instances, the vehicles maintained separation and navigated the intersection safely without making physical contact.

### [negative] a vehicle driving the wrong way against the flow of traffic

- **match** `exact` / conf `high` at 0.0-12.0s (clearest 4.0s)
  - subject: city bus
  - A city bus drives northbound, bypassing a stopped line of traffic by driving entirely within the southbound lane (to the left of the double yellow line), before proceeding through the intersection.
- **match** `exact` / conf `high` at 72.0-146.0s (clearest 100.0s)
  - subject: articulated city bus
  - An articulated bus drives northbound in the southbound oncoming traffic lane to bypass stopped vehicles. It waits at the intersection in the wrong lane and then executes a wide right turn across the correct northbound lanes.
- ruled out: The dark sedan that turns left and drives 'down' the main street from t=166.03s to t=178.03s was evaluated. However, based on the orientation of the parked cars on that side of the street and the presence of a traffic signal for 'downward' moving vehicles, the street is two-way. The sedan is traveling in the correct southbound lane, not against traffic flow.

### [negative] a person lying in the roadway

- **match** `exact` / conf `high` at 70.0-72.0s (clearest 70.0s)
  - subject: pedestrian
  - A pedestrian is seen lying on the ground in the crosswalk, with another person standing over them and appearing to assist. The person then gets up and walks towards the sidewalk.
- ruled out: A cyclist crosses the intersection around t=62.03s - 66.03s but remains upright.

---

22 call(s) ok, 0 failed, 0 in / 0 out tokens