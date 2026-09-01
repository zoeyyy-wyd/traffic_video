# probe run: events-key_0825-1700_fps1_n5_batch_0901-0321

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 1 | whole range, one call
- frames per call: 181 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/events-key_0825-1700_fps1_n5_batch_0901-0321`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| emergency | 0/1 | 0/1 | 1/1 |  |
| negative | 0/2 | 2/2 | 0/2 | ground truth known: all absent |
| over-yellow | 1/1 | 0/1 | 0/1 |  |
| ped-midblock | 1/1 | 0/1 | 0/1 |  |
| pickup-car | 0/1 | 0/1 | 1/1 |  |
| roadworks | 1/1 | 0/1 | 0/1 |  |
| turn-slow | 1/1 | 0/1 | 0/1 |  |

### queries whose samples disagreed

- pickup-car — a person getting into or out of a stopped car, van or taxi
- emergency — an emergency vehicle with its lights flashing passing throug

## per query

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 1)

- **match** `exact` / conf `high` at 105.0-108.0s (clearest 107.0s)
  - subject: a black SUV
  - A black SUV making a left turn stops in the intersection to yield to pedestrians crossing the crosswalk before completing its turn.
- ruled out: Other vehicles make turns throughout the video, but most proceed smoothly without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **match** `exact` / conf `high` at 101.0-105.0s (clearest 103.0s)
  - subject: a construction worker
  - A worker in a high-visibility vest walks up to the driver's side of the parked white van, opens the door, and gets inside.
- ruled out: A white van is parked for a long time in the lower left lane, but for most of the video no one interacts with it.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 1)

- **match** `exact` / conf `high` at 95.0-101.0s (clearest 98.0s)
  - subject: an articulated blue bus
  - In order to overtake a parked white van and cart, the bus drives with its left side clearly over the solid double yellow center line.
- ruled out: Most vehicles stay within their lanes, but several vehicles (including a white van around 108.03s and a silver car at 113.03s) also cross the center line to pass the obstacle.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 1)

- **match** `exact` / conf `high` at 130.0-136.0s (clearest 133.0s)
  - subject: a pedestrian
  - A pedestrian steps off the lower left sidewalk and walks straight across all the driving lanes to the opposite sidewalk, completely avoiding the crosswalks.
- ruled out: Pedestrians are frequently seen using the marked crosswalks at the top of the intersection.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 0.0s)
  - subject: a construction zone
  - A section of the intersection is cordoned off with orange barriers and traffic cones, and workers in high-visibility clothing are present in the roadway for the entirety of the video.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 31.0-35.0s (clearest 32.0s)
  - subject: a police car
  - A white police vehicle with its roof lights actively flashing enters from the right and passes straight through the intersection.
- ruled out: Other service vehicles pass through, but do not have flashing emergency lights active.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: No collisions or contact between vehicles occur in this sequence.
- ruled out: Vehicles occasionally pass quite close to the parked van or each other when turning, but none make physical contact.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: There are no horse-drawn carriages present in any of the frames.
- ruled out: The sequence contains many cars, vans, SUVs, and buses, but no horse-drawn vehicles.

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 2)

- **match** `exact` / conf `high` at 85.0-105.0s (clearest 93.0s)
  - subject: blue articulated bus
  - A blue articulated bus enters the intersection from the left and slows to a near crawl as it carefully navigates a tight right turn around the construction area.
- ruled out: I also considered the police SUV at 31.03s, which slows down to turn, and a dark SUV at 38.03s turning left. However, the articulated bus provides a much clearer and more definitive example of a vehicle significantly slowing down to safely complete a turn.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **match** `exact` / conf `high` at 121.0-125.0s (clearest 123.0s)
  - subject: driver of the parked white van
  - A person opens the driver's side door of a white van parked on the left side of the street, steps out into the roadway, and walks towards the rear of the vehicle.
- ruled out: I observed all the other parked vehicles on the left side of the street throughout the video, but no other occupants entered or exited them.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 2)

- **match** `exact` / conf `high` at 136.0-139.0s (clearest 137.0s)
  - subject: white van
  - A white van driving down the street steers over the double yellow center line, partially entering the opposing traffic lane, to give a wide berth to a parked food cart and another van.
- ruled out: I checked other vehicles driving down the road past the parked cars, such as the dark SUV at 116.03s, which comes very close to the line, but the white van crossing at 137.03s is the most undeniable instance.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 2)

- **match** `exact` / conf `high` at 132.0-137.0s (clearest 134.0s)
  - subject: pedestrian
  - A pedestrian steps off the sidewalk on the right side of the street and jaywalks directly across the middle of the road, over the double yellow lines, far away from any crosswalks.
- ruled out: Many pedestrians are seen crossing the intersection at the top of the frame, but they are all using the designated crosswalk areas.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 0.0s)
  - subject: intersection
  - The upper part of the intersection is under active construction, featuring orange cones, barriers, and workers wearing high-visibility vests standing in the roadway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.0s)
  - subject: police SUV
  - A police SUV with its emergency lightbar flashing brightly enters the intersection from the left side and turns left to head up the street.
- ruled out: No other emergency vehicles appear in the sequence.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: There are no collisions or physical contacts between any vehicles in the provided frames.
- ruled out: I closely monitored several tight maneuvers, including the blue articulated bus navigating the construction zone at 89.03s and the white van passing the parked cars at 137.03s. In all instances, the drivers successfully avoided making contact with other vehicles or barriers.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: The traffic consists entirely of motorized vehicles, bicycles, and pedestrians. There is no horse-drawn carriage in the scene.
- ruled out: I scanned the street and intersection for any non-motorized transport. Bicycles and an attached food cart are visible, but no horses are present.

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 3)

- **match** `exact` / conf `high` at 177.0-180.0s (clearest 179.0s)
  - subject: yellow taxi
  - A yellow taxi approaching from the right enters the intersection to turn left, but slows to a stop in the middle of the intersection to yield to an oncoming white car before completing the turn.
- ruled out: A dark SUV turning left at 42.03s and a blue bus turning right at 90.03s were considered, but neither came to a clear stop or significantly slowed down due to traffic while making their turns.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **match** `exact` / conf `high` at 124.0-130.0s (clearest 127.0s)
  - subject: a pedestrian
  - A pedestrian walks from the sidewalk into the street toward a black car parked in an angled spot on the left side, opens the driver's side door, and gets inside.
- ruled out: A white van that pulls over and parks in the travel lane at 70.03s was closely examined, but no person is clearly seen getting into or out of it while it is stopped.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 3)

- **match** `exact` / conf `high` at 74.0-78.0s (clearest 76.0s)
  - subject: dark SUV
  - A dark SUV driving up the bottom roadway encounters a white van stopped in its lane. The SUV steers to the left, crossing its left wheels over the double yellow centre line to pass the van, before merging back into its lane.
- ruled out: All other vehicles driving up or down the bottom roadway were observed to remain entirely within their lanes, without crossing the double yellow line.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 3)

- **match** `exact` / conf `high` at 173.0-177.0s (clearest 175.0s)
  - subject: a pedestrian
  - A pedestrian steps off the curb on the left side of the bottom street, far away from the intersection crosswalks, and walks straight across the roadway to the sidewalk on the right.
- ruled out: Pedestrians navigating around the construction site at the top of the intersection were considered, but they are walking near the marked (though closed) crosswalk areas rather than jaywalking mid-block.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: the roadway construction site
  - Throughout the entire sequence, a section of the upper intersection and crosswalk is cordoned off with orange barriers and cones, with workers in high-visibility vests actively working in the carriageway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **match** `exact` / conf `high` at 31.0-36.0s (clearest 33.0s)
  - subject: police car
  - A police car approaches from the right side of the intersection with its roof emergency lights flashing, turns left, and proceeds down the bottom street.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: At no point in the video do any vehicles make contact or collide with one another.
- ruled out: A dark SUV passing very close to a parked white van at 76.03s was considered, but it successfully avoids a collision.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: There are no horses or horse-drawn carriages visible in the scene at any time; only motor vehicles, bicycles, and pedestrians are present.

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 4)

- **match** `exact` / conf `high` at 81.0-86.0s (clearest 84.0s)
  - subject: white van
  - A white van turning left slows down and comes to a brief stop in the middle of the intersection to yield to an oncoming silver car before completing its turn.
- ruled out: A police car turning right between 31.03s and 35.03s slows down slightly to negotiate the turn but does not come to a stop.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **absent**
  - why not: While there are several cars parked along the side of the road on the left, no individuals are seen opening doors or getting into or out of any vehicles during the video.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 4)

- **match** `exact` / conf `high` at 17.0-20.0s (clearest 18.0s)
  - subject: dark SUV
  - A dark SUV approaching the intersection from the top left crosses completely over the double yellow center line into the oncoming lane to drive around the active construction zone.
- ruled out: Vehicles moving through the intersection often pass near the center line, but vehicles approaching from the top left are specifically forced to cross the double yellow line due to the lane closure.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 4)

- **match** `exact` / conf `high` at 13.0-21.0s (clearest 17.0s)
  - subject: pedestrian
  - A pedestrian steps off the left sidewalk and crosses the main roadway diagonally to the right side, walking well away from the marked crosswalks.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 0.0s)
  - subject: construction zone
  - An active construction zone is present on the road entering from the top left, marked by orange cones, barriers, an open excavation, and workers wearing high-visibility vests standing in the carriageway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **absent**
  - why not: No emergency vehicles with active flashing lights are seen passing through the intersection.
- ruled out: A marked police vehicle approaches and turns right through the intersection between 31.03s and 35.03s, but its roof lights are not flashing.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: Vehicles are observed navigating the intersection smoothly and yielding when necessary; no collisions or contact between vehicles occur.
- ruled out: At 84.03s, a white van turning left gets close to an oncoming silver car heading straight, but the van yields in time and no contact is made.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: The traffic consists entirely of motor vehicles, buses, bicycles, and pedestrians. There are no horse-drawn carriages present in the scene.

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 5)

- **match** `exact` / conf `high` at 38.0-43.0s (clearest 41.0s)
  - subject: grey SUV
  - A grey SUV turning from the left cross street onto the top street slows down as it approaches the crosswalk, yielding to other road users, before completing its turn.
- ruled out: Many vehicles make turns without significantly slowing down. The grey SUV is chosen because it noticeably decelerates during the maneuver.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **match** `exact` / conf `high` at 116.0-122.0s (clearest 119.0s)
  - subject: passenger of black SUV
  - A black SUV pulls over and stops on the left side of the bottom street. The rear street-side door opens, and a passenger gets out and walks away.
- ruled out: Pedestrians walking near parked cars were examined, but no others were observed actually interacting with the doors or entering/exiting vehicles.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 5)

- **match** `exact` / conf `high` at 94.0-103.0s (clearest 98.0s)
  - subject: articulated bus
  - An articulated bus turns right into the bottom street. Due to its length, the rear section of the bus tracks over the painted double yellow centre line during the turn.
- ruled out: Most cars turning into the street briefly approach the line but stay within their lanes. The articulated bus is the clear exception.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 5)

- **match** `exact` / conf `high` at 12.0-18.0s (clearest 15.0s)
  - subject: pedestrian
  - A pedestrian crosses the bottom street laterally, walking through the travel lanes far below the marked crosswalk at the intersection.
- ruled out: Another pedestrian crosses diagonally outside the crosswalk at 5.03s, but the one at 12.03s provides a completely unambiguous case of crossing mid-block.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: construction zone
  - The cross street leading upward from the intersection is an active construction zone, containing orange cones, barriers, exposed areas, and multiple workers standing in the carriageway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **absent**
  - why not: No emergency vehicles with their lights actively flashing are seen in the footage.
- ruled out: A white police SUV passes through the intersection between 31.03s and 34.03s. It is an emergency vehicle, but its roof lights are not flashing.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: No vehicles make contact with one another.
- ruled out: Vehicles maneuver closely around each other during turns and yielding events, but there are no collisions or instances of physical contact between any road users.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: No horse-drawn carriages are present in the video.
- ruled out: All vehicles observed are motorized.

---

5 call(s) ok, 0 failed, 1006400 in / 37438 out tokens