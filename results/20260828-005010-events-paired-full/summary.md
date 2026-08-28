# probe run: 20260828-005010-events-paired-full

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `burn,list` (channels: burn, list, interleave, or none)
- fps: 0.5 | whole range, one call
- frames per call: 91 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/20260828-005010-events-paired-full`

## by axis

| axis | answered present | note |
|---|---|---|
| floor | 2/3 |  |
| negative | 0/3 | ground truth known: all absent |
| pair-cause | 2/2 |  |
| pair-conflict | 2/2 |  |
| pair-direct | 1/2 |  |
| pair-hesitate | 2/2 |  |
| pair-turn | 2/2 |  |
| pair-yield | 2/2 |  |

## per query

### [pair-yield] a vehicle that stopped to let a pedestrian cross in front of it, and moved off only after they had passed

- **match** `exact` / conf `high` at 126.0-138.0s (clearest 132.0s)
  - subject: dark SUV turning left
  - A dark SUV enters the intersection to turn left, but stops to let a pedestrian in the crosswalk pass in front of it. After the pedestrian clears its path, the SUV resumes its turn.
- ruled out: I considered the police SUV turning right at t=32.03, but it completes its turn before the nearby pedestrian crosses its path, without stopping. I also checked the dark SUV turning left at t=104.03, but no pedestrian was in the crosswalk, so it did not need to yield.

### [pair-yield] a vehicle that was stopped because the traffic in front of it was not moving, while a pedestrian happened to pass nearby

- **match** `exact` / conf `high` at 40.0-50.0s (clearest 48.0s)
  - subject: the silver car
  - A silver car stops in a queue behind a dark SUV. While it is waiting, a pedestrian walking along the adjacent sidewalk passes by it.
- **match** `exact` / conf `high` at 66.0-78.0s (clearest 74.0s)
  - subject: the dark SUV
  - A dark SUV comes to a stop behind a silver SUV. While waiting in the queue, pedestrians on the nearby sidewalk walk past the vehicle.
- **match** `exact` / conf `high` at 104.0-110.0s (clearest 106.0s)
  - subject: the grey car
  - A grey car stops because an articulated bus in front of it is navigating the intersection. While the car is stationary, a pedestrian crosses the street directly in front of it on the crosswalk.
- **match** `exact` / conf `high` at 136.0-146.0s (clearest 142.0s)
  - subject: the silver car
  - A silver car stops in traffic behind a white box truck. A pedestrian on the sidewalk passes next to the car while it waits.
- ruled out: The dark SUV that stops at 34.03 and the silver SUV that stops at 64.03 both have pedestrians pass near them while they are waiting. However, these are the lead vehicles stopping at the intersection line for a red light, not vehicles stopping because the traffic in front of them is not moving.

### [pair-cause] a vehicle that entered the intersection and had to stop partway because someone was crossing in front of it

- **match** `exact` / conf `high` at 142.0-150.0s (clearest 146.0s)
  - subject: dark car
  - A dark car entering from the right turns left and stops in the intersection to allow pedestrians to finish crossing the street before completing its turn.
- ruled out: The grey SUV turning left around 104.03s was considered, but it does not clearly come to a stop for pedestrians. The articulated bus turning left from 86.03s to 104.03s was also considered, but it appears to proceed slowly through the intersection without coming to a complete stop for crossing pedestrians.

### [pair-cause] a vehicle that came to a stop partway through the intersection with nobody in front of it

- **match** `exact` / conf `high` at 60.0-72.0s (clearest 64.0s)
  - subject: dark SUV
  - A dark SUV enters the intersection from the upper right, comes to a complete stop in the middle of the intersection for several seconds despite having a clear path ahead, and then eventually continues on its way.
- ruled out: Several other vehicles were observed passing through the intersection (e.g., a silver SUV around 36s, an articulated bus around 90s), but they all maintained continuous movement without stopping partway through.

### [pair-hesitate] a pedestrian who started to step into the roadway, then stopped or stepped back because a vehicle was approaching

- **match** `exact` / conf `high` at 114.0-120.0s (clearest 116.0s)
  - subject: pedestrian at the top-right corner
  - The pedestrian steps off the curb into the vertical crosswalk, then stops and waits near the edge of the roadway as a grey SUV turns right in front of them.
- **match** `exact` / conf `high` at 134.0-140.0s (clearest 136.0s)
  - subject: pedestrian at the top-right corner
  - The pedestrian steps off the curb into the horizontal crosswalk toward the median, then stops and waits as a white van turns right. They resume crossing after it passes.
- ruled out: Pedestrians crossing the bottom crosswalk at 64.03s and 160.03s stopped to let vehicles pass, but they were already well into the travel lane rather than just starting to step into the roadway. A pedestrian crossing the top horizontal crosswalk at 24.03s stopped for a turning white car, but they were also already far into the roadway.

### [pair-hesitate] a pedestrian who waited at the kerb until the road was clear and then crossed without breaking stride

- **match** `exact` / conf `high` at 12.0-22.0s (clearest 16.0s)
  - subject: pedestrian on the left crosswalk
  - A pedestrian waits at the bottom-left curb while a white car passes, then proceeds to cross the left crosswalk in one continuous movement without stopping.
- **match** `exact` / conf `high` at 132.0-140.0s (clearest 136.0s)
  - subject: pedestrian on the left crosswalk
  - A pedestrian waits at the top-left curb as a dark car crosses the intersection, then steps into the left crosswalk and crosses without breaking stride.
- ruled out: Pedestrians cross the left crosswalk starting around 62.03 and 76.03, but they walk straight into the intersection without pausing at the curb first. A pedestrian at 98.03 waits for a bus and an SUV before crossing the bottom crosswalk, which is another valid instance of this behavior, though the left crosswalk examples are slightly clearer to observe.

### [pair-direct] a construction worker signalling to drivers, with a driver visibly doing what they were signalled to do

- **absent**
  - why not: While construction workers are present near the intersection throughout the video, none are observed actively signalling drivers (such as waving them on or holding up a hand to stop them), and no driver is seen visibly changing their behavior in response to a worker.
- ruled out: I considered several moments where vehicles pass near construction workers, such as the articulated bus turning left (86.03s - 104.03s), the USPS truck turning right (112.03s - 116.03s), and various cars passing through the intersection (e.g., 22.03s, 32.03s). However, in all these instances, the workers are either working or standing passively near the cones. They are not actively directing traffic, and the drivers are simply following normal traffic patterns rather than responding to a worker's signal.

### [pair-direct] a construction worker standing in or beside the roadway while traffic passes, without signalling to anyone

- **match** `exact` / conf `high` at 24.0-34.0s (clearest 30.0s)
  - subject: construction worker in yellow vest in the upper crosswalk
  - A construction worker stands in the upper crosswalk next to traffic cones, holding his position without gesturing or signaling, while several vehicles (including a white van and a police SUV) pass near him.
- ruled out: Workers standing completely inside the orange barricaded area in the top right corner were not considered, as they are fully separated from the active roadway and passing traffic.

### [pair-conflict] two road users who came close enough that one of them visibly changed course or speed to avoid the other

- **match** `exact` / conf `high` at 170.0-174.0s (clearest 172.0s)
  - subject: a pedestrian and a cyclist
  - A pedestrian crossing the street stops walking to avoid a collision with a cyclist who passes very closely in front of them.
- ruled out: The interaction between the articulated bus and the black SUV (92.03s - 96.03s) was examined. While the bus makes a wide turn in front of the SUV, the SUV is already stopped and waiting at the intersection; this is standard yielding behavior rather than an evasive maneuver.

### [pair-conflict] two road users passing close to one another with neither changing course or speed

- **match** `exact` / conf `high` at 112.0-116.0s (clearest 114.0s)
  - subject: the cyclist and the white box truck
  - A cyclist proceeding straight and a white box truck turning right pass extremely close to each other in the intersection, with neither appearing to yield, change course, or adjust their speed.
- ruled out: I considered the interaction between a turning white car and a crossing pedestrian from 34.03s to 38.03s, but the car appears to yield to the pedestrian. I also looked at the white van turning near a pedestrian from 140.03s to 144.03s, but they do not pass particularly close to one another.

### [pair-turn] a turning vehicle that waited for pedestrians to finish crossing before completing its turn

- **match** `exact` / conf `high` at 176.0-180.0s (clearest 178.0s)
  - subject: yellow taxi
  - A yellow taxi enters the intersection to make a left turn, pauses to yield to a pedestrian in the destination crosswalk, and then completes the turn once the pedestrian is clear.
- ruled out: A dark SUV turning left at 46.03s completes its turn while pedestrians are crossing on the other side of the intersection, but it does not need to wait for them. A silver SUV turning left at 38.03s and a USPS truck turning right at 112.03s both complete their turns without having to yield to pedestrians.

### [pair-turn] a turning vehicle that completed its turn across a crosswalk while pedestrians were still in it

- **match** `exact` / conf `high` at 170.0-176.0s (clearest 174.0s)
  - subject: dark car turning left
  - A dark car turning left completes its maneuver across the crosswalk while a pedestrian, who had just begun to cross, is still actively walking in the crosswalk.
- ruled out: The dark car turning left between 54.03s and 58.03s crosses the crosswalk just after the pedestrian steps onto the sidewalk, so it does not complete the turn while the pedestrian is still in the crosswalk. The dark car turning left between 144.03s and 152.03s waits correctly for the pedestrian to fully clear the crosswalk before proceeding. The yellow taxi beginning a left turn at 178.03s enters the intersection while a pedestrian is in the crosswalk, but the video ends before the turn is completed.

### [floor] a vehicle stopped with part of its body on the crosswalk markings

- **absent**
  - why not: Several vehicles stop to wait at the intersection throughout the video, but all of them stop correctly behind the stop lines. No vehicle comes to a halt while positioned over the striped crosswalk markings.
- ruled out: The white car waiting from 14.03s to 26.03s, the dark SUV waiting from 46.03s to 54.03s, and the silver car waiting from 118.03s to 128.03s on the bottom road were all examined as they are stopped at the intersection. However, in all cases, the vehicle correctly stops behind the solid stop line and does not rest any part of its body on the striped crosswalk markings. The articulated buses turning right from the left road (around 88.03s and 108.03s) were also considered, but they are in continuous motion while passing over the crosswalk markings and do not stop on them.

### [floor] a pedestrian crossing the roadway outside the crosswalk markings

- **match** `exact` / conf `high` at 12.0-20.0s (clearest 16.0s)
  - subject: pedestrian
  - A pedestrian crosses the southbound lanes diagonally, walking from near the center line towards the top-left corner, outside the marked crosswalks.
- **match** `exact` / conf `high` at 34.0-40.0s (clearest 36.0s)
  - subject: pedestrian
  - A pedestrian crosses the northbound lanes, walking from the center of the road towards the scaffolding on the right side, below the marked crosswalks.
- **match** `exact` / conf `high` at 74.0-86.0s (clearest 80.0s)
  - subject: pedestrian
  - A pedestrian walks diagonally across the entire intersection, starting from the parked cars on the lower left and heading towards the top right, completely outside the crosswalk markings.
- **match** `exact` / conf `high` at 166.0-172.0s (clearest 168.0s)
  - subject: pedestrian
  - A pedestrian crosses the southbound lanes diagonally, moving from the intersection area towards the parked cars on the lower left, outside the crosswalk markings.
- ruled out: Several pedestrians cross the street using the marked crosswalks at the top of the intersection (e.g., around 44s-52s); these were rejected as they are within the markings. A pedestrian is seen walking south down the middle of the road along the double yellow line from 124.03s to 130.03s; this was rejected because the person is walking along the roadway rather than crossing it.

### [floor] a cyclist or e-bike rider riding on the sidewalk rather than in the roadway

- **match** `exact` / conf `high` at 34.0-36.0s (clearest 34.0s)
  - subject: cyclist in the top right
  - A cyclist rides along the top-right sidewalk before transitioning into the crosswalk.
- ruled out: Several other cyclists and e-bike riders are visible throughout the video (e.g., at 104.03s, 110.03s, 130.03s, and a group at 172.03s), but they are riding in the roadway or designated crosswalks, not on the pedestrian sidewalks.

### [negative] a horse-drawn carriage

- **absent**
  - why not: A horse-drawn carriage does not appear at any point in this video.
- ruled out: Examined all vehicles passing through the intersection, including cars, SUVs, vans, a large articulated bus, and a yellow taxi. No horse-drawn vehicles were present among them.

### [negative] a collision in which two vehicles make contact

- **absent**
  - why not: Throughout the provided frames, traffic flows through the intersection normally. There is no moment where two vehicles crash or make contact with one another.
- ruled out: I paid close attention to the articulated MTA bus making a tight left turn between 88.03s and 100.03s, as its rear section swung wide, but it successfully completed the maneuver without contacting any other vehicle. I also monitored various vehicles passing close to each other in the intersection, but none resulted in a collision.

### [negative] a vehicle that has driven up onto the sidewalk

- **absent**
  - why not: Throughout the video, all vehicles remain on the marked road surfaces, within designated lanes, or in official street parking spots. No vehicle is ever seen driving onto or resting upon any of the pedestrian sidewalks.
- ruled out: I examined the vehicles parked along the bottom left side of the street, but they are in designated street parking spaces, not on the sidewalk. I also observed vehicles maneuvering near the construction zone in the top half of the frame (e.g., the white truck at t=90.03s and the flatbed truck at t=92.03s), but they remained on the roadway while navigating the work area.

---

18 call(s) ok, 0 failed, 1822405 in / 55667 out tokens