# probe run: events-key_0825-1700_fps2_n5_batch_0901-0328

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 2 | whole range, one call
- frames per call: 361 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/events-key_0825-1700_fps2_n5_batch_0901-0328`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| emergency | 1/1 | 0/1 | 0/1 |  |
| negative | 0/2 | 2/2 | 0/2 | ground truth known: all absent |
| over-yellow | 1/1 | 0/1 | 0/1 |  |
| ped-midblock | 1/1 | 0/1 | 0/1 |  |
| pickup-car | 0/1 | 1/1 | 0/1 |  |
| roadworks | 1/1 | 0/1 | 0/1 |  |
| turn-slow | 1/1 | 0/1 | 0/1 |  |

## per query

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 1)

- **match** `exact` / conf `high` at 88.5-107.0s (clearest 97.0s)
  - subject: an articulated bus
  - An articulated bus enters the frame from the bottom and begins to turn left into the intersection. Halfway through the turn, it slows down to a near stop before completing the maneuver.
- ruled out: A dark SUV turning left at 40.53s also slows down during its turn, but the articulated bus is a much larger and more prominent example of this behavior. Other vehicles, such as the white car turning right at 20.03s, complete their turns at a steady speed without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **absent**
  - why not: No individuals are observed getting into or out of any vehicles throughout the video.
- ruled out: Several vehicles are seen parking along the curb, such as a black SUV at 64.03s and a white SUV at 128.03s. However, at no point does a driver or passenger open a door to enter or exit any of the parked or stopped vehicles.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 1)

- **match** `exact` / conf `high` at 121.5-124.5s (clearest 122.5s)
  - subject: a white car
  - A white car driving downwards encounters a stopped white USPS truck in its lane. The car swerves left to go around the truck, with its left wheels and part of its body clearly crossing over the painted double yellow center line.
- ruled out: A white van driving downwards at 114.53s passes double-parked vehicles but remains within its lane without crossing the double yellow line. A dark SUV at 118.53s also crosses the double yellow line to pass the same USPS truck.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 1)

- **match** `exact` / conf `high` at 32.0-38.0s (clearest 35.0s)
  - subject: a pedestrian
  - A pedestrian steps off the wooden walkway on the right side of the vertical street, far below the intersection, and walks across the active roadway to the left sidewalk.
- ruled out: Many pedestrians are seen crossing the intersection at the top of the frame, but they are using the designated crosswalk areas (despite the construction modifying the exact path).

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: the intersection
  - The primary intersection is an active construction zone for the entirety of the video, featuring orange traffic cones, orange mesh barriers, and several workers wearing high-visibility safety vests standing in the carriageway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.5s)
  - subject: an NYPD police car
  - A marked police car with its roof lights visibly flashing passes through the intersection from right to left.
- ruled out: A white vehicle with a flashing light bar crosses the intersection at 8.03s, but the NYPD vehicle is a more definitive example of an emergency responder.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: Traffic flows without any accidents; no two vehicles make contact.
- ruled out: Vehicles frequently navigate close to one another while maneuvering through the construction zone and passing parked cars, but no collisions or physical contact occurs between any vehicles.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: There are no animals or horse-drawn carriages present in the video.
- ruled out: The scene features cars, trucks, vans, buses, and bicycles.

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 2)

- **match** `exact` / conf `high` at 14.5-17.5s (clearest 16.0s)
  - subject: a grey SUV
  - A grey SUV turning left into the intersection from the right side slows down almost to a stop mid-turn before continuing on its way.
- ruled out: Several vehicles are seen making turns smoothly without slowing down significantly, such as the dark SUV at 34.03s.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **absent**
  - why not: No person is seen entering or exiting any parked or stopped vehicle in the frames.
- ruled out: Pedestrians are visible walking past the cars parked along the street on the lower left, but none approach the doors or attempt to get in or out.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 2)

- **match** `exact` / conf `high` at 131.0-134.5s (clearest 132.5s)
  - subject: a white van
  - A white van driving up the street from the bottom left drives with its left side clearly crossing over the solid double yellow centre line before correcting its path.
- ruled out: Other vehicles change lanes or cross dotted white lines, but they generally stay on the correct side of the double yellow lines dividing opposing traffic.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 2)

- **match** `exact` / conf `high` at 46.5-54.5s (clearest 50.0s)
  - subject: a pedestrian
  - A pedestrian walks horizontally across the traffic lanes of the bottom-left street, crossing between parked cars well away from the marked crosswalk at the intersection.
- ruled out: Many pedestrians are seen crossing the streets, but almost all use the painted crosswalks at the intersection.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: the roadway
  - The upper section of the intersection is under construction throughout the entire clip, clearly marked by orange cones, barriers, and workers in high-visibility vests standing in the carriageway.
- ruled out: The scene is continuous and the construction features remain present in every frame.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 32.0-34.0s (clearest 33.0s)
  - subject: a police SUV
  - A police SUV drives straight across the intersection from left to right with its emergency roof lights actively flashing.
- ruled out: Another police vehicle passes at 9.53s, but the flashing emergency lights on the SUV at 33.03s are much clearer.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: No vehicles are seen colliding or making physical contact with each other.
- ruled out: Vehicles navigate the intersection simultaneously and pass relatively close to each other, but they maintain proper clearance without colliding.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: There is no horse-drawn carriage anywhere in the video clip.
- ruled out: Motor vehicles including cars, SUVs, vans, buses, and construction equipment move through the intersection, but no animal-drawn vehicles are present.

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 3)

- **match** `exact` / conf `high` at 91.0-100.5s (clearest 95.5s)
  - subject: an articulated bus
  - An articulated bus slows down and comes to a complete stop midway through its right turn in order to yield to crossing pedestrians, then eventually proceeds.
- ruled out: Other vehicles turning, such as the dark SUV at 46.53 or the white car at 155.03, were checked but they completed their turns without stopping or significantly slowing down.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **absent**
  - why not: No doors are seen opening, and no person is observed getting into or out of any vehicle during the entire video.
- ruled out: Checked all vehicles parked on the left side of the street and any vehicles that temporarily stopped at the intersection.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 3)

- **match** `exact` / conf `high` at 110.0-113.0s (clearest 111.5s)
  - subject: a white van
  - A white van driving down the main street steers around a parked white van, and in doing so, its left wheels cross completely over the double yellow centre lines into the oncoming lane.
- ruled out: Checked other passing vehicles; some drive close to the line, but the white van at 111.53 is the most unambiguous instance of a vehicle crossing over it.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 3)

- **match** `exact` / conf `high` at 11.0-15.0s (clearest 13.0s)
  - subject: a pedestrian
  - A pedestrian steps off the right sidewalk far below the intersection and crosses the entire roadway diagonally, ending up between the parked cars on the left.
- ruled out: Pedestrians crossing at the intersection were evaluated, but most stay within or very close to the marked crosswalks.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 0.0s)
  - subject: the intersection
  - There is a construction zone occupying part of the intersection and crosswalk areas, featuring orange barriers, traffic cones, and workers in high-visibility vests who remain in the area throughout the video.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **match** `exact` / conf `high` at 31.0-35.0s (clearest 33.0s)
  - subject: a police car
  - A police vehicle with its roof-mounted emergency lights flashing enters from the right on the cross street, travels straight through the intersection, and exits to the left.
- ruled out: Monitored all traffic to ensure other vehicles passing through were standard, non-emergency traffic.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: No vehicles ever make physical contact with one another; traffic proceeds without incident.
- ruled out: Watched the flow of traffic throughout the clip for any sudden stops, swerves, or collisions.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: There are no horse-drawn carriages visible in the scene; all traffic is motorised.
- ruled out: Scanned all the moving traffic and the vehicles using the intersection.

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 4)

- **match** `exact` / conf `high` at 90.0-104.0s (clearest 95.0s)
  - subject: an articulated bus
  - The bus enters the intersection to make a left turn and comes to a near stop mid-turn to wait for a pedestrian in the crosswalk before continuing.
- ruled out: A few other vehicles make turns (e.g., a black SUV around 10s, a blue bus around 133s) but they complete their turns without noticeably slowing down or stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **absent**
  - why not: No person is observed boarding or alighting from any vehicle.
- ruled out: Parked cars are visible on the streets, particularly on the left, but no individuals are seen opening doors or getting into or out of any vehicles throughout the video.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 4)

- **match** `exact` / conf `high` at 111.0-115.5s (clearest 113.5s)
  - subject: a white van
  - The white van, approaching the intersection from the top left, shifts over the painted double yellow center line as it nears the crosswalk.
- ruled out: Most vehicles stay within their lanes; the white van at 113s clearly encroaches on the oncoming lane, crossing the double yellow line.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 4)

- **match** `exact` / conf `high` at 160.0-165.0s (clearest 162.5s)
  - subject: a pedestrian
  - A pedestrian enters the roadway from the left sidewalk between parked cars and crosses the street diagonally, far from the marked crosswalk.
- ruled out: Many pedestrians cross the street, but they almost exclusively use the marked crosswalks at the intersection.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: the roadway on the top left
  - Construction activity is present on the road branching to the top left, visible as orange cones, barriers, and workers in high-visibility vests.
- ruled out: The construction is a static feature present for the entire duration of the clip.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **match** `exact` / conf `high` at 31.5-36.0s (clearest 33.0s)
  - subject: an NYPD police car
  - A police car with its emergency lights flashing enters the intersection from the right and proceeds straight across, exiting to the left.
- ruled out: A white van with blue markings appears around 29s but has no emergency lights flashing.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: No vehicles are seen making contact with one another.
- ruled out: Traffic flows through the intersection without incident. No near misses or collisions are observed.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: There are no horses or carriages present in any of the frames.
- ruled out: All vehicles moving through the intersection are motorized.

### [turn-slow] a vehicle slowing down or coming to a stop while it is making a turn (sample 5)

- **match** `exact` / conf `high` at 176.5-179.5s (clearest 178.0s)
  - subject: yellow taxi
  - A yellow taxi turning right into the upper arm of the intersection stops to wait for pedestrians before completing its turn.
- ruled out: The articulated bus turning left makes a slow, wide turn, but moves continuously rather than coming to a discernible stop.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **absent**
  - why not: No one is observed entering or exiting any parked or stopped vehicles during the video.
- ruled out: A white van double-parked on the left side of the bottom street has activity near it, but no one is seen opening a door to get in or out.

### [over-yellow] a vehicle with part of its body over the painted double yellow centre line (sample 5)

- **match** `exact` / conf `high` at 96.0-102.0s (clearest 99.0s)
  - subject: blue articulated bus
  - As the long articulated bus completes its left turn into the bottom street, its rear section cuts the corner and crosses over the double yellow centre line.
- ruled out: Various smaller vehicles momentarily touch the centre line to pass obstacles, but the bus provides the most prolonged and clear example of a vehicle body traversing the line.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 5)

- **match** `exact` / conf `high` at 111.0-120.0s (clearest 115.5s)
  - subject: pedestrian in dark clothing
  - A pedestrian steps off the right-side scaffolding structure and walks diagonally across the bottom street, well outside of any marked crosswalks, reaching the other side behind a parked white van.
- ruled out: Most pedestrians use the marked crosswalks at the intersection, but this individual crosses mid-block.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: the roadway
  - The upper arm of the intersection is an active construction zone throughout the video, featuring orange barriers, traffic cones, and construction workers standing in the road.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **match** `exact` / conf `high` at 9.5-15.0s (clearest 11.5s)
  - subject: police SUV
  - A white police SUV with its roof lights flashing enters from the right street and drives straight through the intersection, exiting to the top-left.
- ruled out: A second police SUV with flashing lights passes through the intersection later at 32.03s.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: All vehicles in the footage maintain clear separation and no contact is observed.
- ruled out: Several vehicles navigate the intersection simultaneously and pass close to one another, but no collisions or physical contact occurs.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: No horse-drawn carriages are present in the video.
- ruled out: The intersection has various types of traffic including cars, buses, and trucks, but no animal-drawn vehicles.

---

5 call(s) ok, 0 failed, 2003950 in / 26847 out tokens