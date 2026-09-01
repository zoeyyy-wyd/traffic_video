# probe run: events-key_0825-1700_fps2_n5_batch_0901-0624

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 2 | whole range, one call
- frames per call: 361 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/events-key_0825-1700_fps2_n5_batch_0901-0624`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| bus-dwell | 0/1 | 1/1 | 0/1 |  |
| emergency | 1/1 | 0/1 | 0/1 |  |
| emergency-dark | 0/1 | 0/1 | 1/1 |  |
| negative | 0/2 | 2/2 | 0/2 | ground truth known: all absent |
| ped-midblock | 1/1 | 0/1 | 0/1 |  |
| pickup-car | 0/1 | 0/1 | 1/1 |  |
| roadworks | 1/1 | 0/1 | 0/1 |  |
| skateboard | 0/1 | 0/1 | 1/1 |  |
| turn-halt | 1/1 | 0/1 | 0/1 |  |

### queries whose samples disagreed

- pickup-car — a person getting into or out of a stopped car, van or taxi
- skateboard — a person riding a skateboard
- emergency-dark — an emergency vehicle passing through the intersection with i

## per query

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 1)

- **match** `exact` / conf `high` at 86.0-106.5s (clearest 95.0s)
  - subject: articulated bus
  - An articulated bus attempts to turn left, but due to its length and the flow of traffic, it must stop or crawl at a near standstill midway through the intersection for several seconds before it can complete the turn.
- ruled out: A grey SUV turning left around 71.03s also pauses mid-turn to wait for pedestrians, but the articulated bus's extended halt is the most prominent example.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **match** `exact` / conf `high` at 82.0-85.0s (clearest 83.5s)
  - subject: driver of the white van
  - The driver's side door of a white van stopped in the road opens, and a person steps out, walking toward the rear of the van.
- ruled out: Many pedestrians walk on the sidewalks or cross the streets, but only the person exiting the white van involves getting out of a vehicle in the frame.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 1)

- **absent**
  - why not: No bus ever pulls over to the kerb or stops to pick up or drop off passengers.
- ruled out: A bus shelter is visible on the sidewalk in the top left, but no buses stop there to load or unload passengers during the video. The articulated bus that appears is actively navigating the intersection, not servicing a stop.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 1)

- **match** `exact` / conf `high` at 123.0-129.0s (clearest 126.0s)
  - subject: pedestrian
  - A pedestrian who initially entered the bottom crosswalk diverges from it, walking diagonally across the open intersection roadway well away from any painted crosswalk markings.
- ruled out: Most pedestrians stick closely to the marked crosswalks. Another pedestrian briefly steps slightly outside the crosswalk lines at 11.03s, but the one at 123.03s clearly traverses the middle of the intersection.

### [skateboard] a person riding a skateboard (sample 1)

- **absent**
  - why not: No one on a skateboard is visible at any point in the footage.
- ruled out: Several people are seen riding bicycles through the intersection (e.g., at 35.03s, 68.03s, and 135.03s), but none are riding a skateboard.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 1)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 50.0s)
  - subject: construction zone
  - A section of the roadway in the top left is cordoned off with orange barriers and traffic cones. Workers wearing high-visibility yellow vests are standing and actively working in the carriageway.
- ruled out: There are no near misses here; the construction zone is clearly established and occupied for the entirety of the video.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 31.0-36.0s (clearest 33.0s)
  - subject: police car
  - A police car enters the intersection from the left and turns leftwards (upwards on screen). The red, white, and blue emergency lightbar on its roof is actively flashing.
- ruled out: The ambulance seen later at 140.03s is an emergency vehicle but does not have flashing lights active.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 1)

- **match** `exact` / conf `high` at 140.0-143.0s (clearest 141.5s)
  - subject: ambulance
  - An FDNY ambulance travels straight across the intersection from left to right. Its emergency lights are turned off and not flashing.
- ruled out: The police car at 31.03s is an emergency vehicle, but its lights are actively flashing. Various white delivery vans pass through, but they are not emergency vehicles.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: All vehicles navigate the intersection without colliding or bumping into one another.
- ruled out: When the articulated bus makes its left turn between 86.03s and 106.53s, several cars have to wait and get relatively close to it, but they clear each other without making physical contact.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: There is no horse-drawn carriage or any animal-drawn vehicle present in the scene.
- ruled out: There is a wide variety of traffic, including cars, SUVs, delivery vans, an articulated bus, an ambulance, and a police car, but no horses.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 2)

- **match** `exact` / conf `high` at 137.5-142.5s (clearest 139.5s)
  - subject: white USPS truck
  - The truck enters the intersection from the top-right and begins a right turn, but comes to a complete stop part-way through the turn to yield to a crossing pedestrian before resuming.
- ruled out: A white van turning left from the bottom-left approach at 113.53s stops to yield to oncoming traffic before completing its turn. However, the USPS truck at 139.53s is a clearer example of stopping mid-turn for a pedestrian.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **absent**
  - why not: No one is seen getting into or out of any stopped vehicle in the video.
- ruled out: There are several parked vehicles along the sides of the streets, but none show any passengers or drivers entering or exiting during the clip.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 2)

- **absent**
  - why not: No passengers are observed boarding or alighting from any bus.
- ruled out: A blue articulated bus approaches the bus stop in the top-left area of the frame at 178.03s. However, the video ends just as it comes to a stop, so no passengers are seen getting on or off.
- unreadable: The video ends immediately after a bus pulls into a stop, cutting off any view of passengers getting on or off.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 2)

- **match** `exact` / conf `high` at 147.0-152.0s (clearest 149.5s)
  - subject: pedestrian in dark clothing
  - A pedestrian crosses the top-right approach street mid-block, significantly far away from the marked crosswalk at the intersection.
- ruled out: A pedestrian crosses the top-left street at 114.03s slightly outside the faded crosswalk lines, but the mid-block crossing on the top-right street at 147.03s is a more definitive example.

### [skateboard] a person riding a skateboard (sample 2)

- **absent**
  - why not: No person riding a skateboard appears in the video.
- ruled out: Several bicyclists pass through the intersection (e.g., at 35.03s, 135.03s, 158.03s), but they are riding bicycles, not skateboards.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 2)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: the top-left corner of the intersection
  - A large construction zone is present in the roadway, marked by orange barriers and traffic cones, with workers in high-visibility vests actively working in the area.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 31.0-35.0s (clearest 33.0s)
  - subject: white and blue police SUV
  - A police SUV travels through the intersection from the bottom-right to the top-left with its roof-mounted red and blue emergency lights visibly flashing.
- ruled out: Another police SUV passes through the intersection earlier (8.03s - 12.03s) also with its lights flashing, which is an equally valid match.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 2)

- **absent**
  - why not: No emergency vehicles are observed passing through without their lights flashing.
- ruled out: Two emergency vehicles (police SUVs) are seen passing through the intersection, one at 8.03s and another at 31.03s. Both of them have their emergency lights flashing.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: No vehicles crash or make contact with each other in the video.
- ruled out: Vehicles yield to each other in the intersection (e.g., the white van yielding to oncoming traffic at 114.53s), but they maintain safe distances and no collisions occur.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: No horse-drawn carriages are present in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 3)

- **match** `exact` / conf `high` at 176.5-180.5s (clearest 178.5s)
  - subject: a yellow taxi
  - A yellow taxi turns left into the intersection, then slows to a near-stop to yield to a silver car traveling straight in the opposite direction before completing its turn.
- ruled out: Several other vehicles turn during the video, such as a silver SUV around 84s and an articulated bus around 90s, but they maintain their momentum through the turn.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **absent**
  - why not: No one is seen getting into or out of any stopped vehicle in the frames provided.
- ruled out: Several cars and vans are parked along the curbs on the lower-left and top-left streets throughout the video. Pedestrians walk past them on the sidewalks, but none are observed opening a door to enter or exit a vehicle.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 3)

- **absent**
  - why not: No buses are seen stopping at the kerb, and no passengers board or alight.
- ruled out: An articulated blue bus turns through the intersection around 90s, and a standard blue bus passes straight through around 102s. Both remain in motion the entire time.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 3)

- **match** `exact` / conf `high` at 108.0-114.5s (clearest 111.0s)
  - subject: a pedestrian
  - A pedestrian crosses the street heading toward the bottom-left mid-block, far from the painted crosswalks at the intersection, moving from the left curb to the right curb.
- ruled out: Most pedestrians use the marked crosswalks at the intersection. A few step slightly outside the lines, but the noted pedestrian crosses well down the block.

### [skateboard] a person riding a skateboard (sample 3)

- **match** `exact` / conf `high` at 126.5-132.5s (clearest 129.0s)
  - subject: a person
  - A person on a skateboard glides rapidly from the street on the far right, across the middle of the intersection, and proceeds down the street to the bottom-left.
- ruled out: People on bicycles also cross the intersection at various points, but the stance and smooth gliding motion of this individual identify them as a skateboarder.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 3)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 90.0s)
  - subject: the roadway
  - The top-left street and part of its intersection crosswalk are undergoing construction. Orange barriers, traffic cones, and workers in high-visibility vests are present in the carriageway.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 3)

- **match** `exact` / conf `high` at 31.0-35.5s (clearest 32.5s)
  - subject: a police SUV
  - A police SUV with its roof light bar actively flashing approaches the intersection from the right and turns right into the top-left street.
- ruled out: Another police vehicle passes through the intersection later, but its emergency lights are off.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 3)

- **match** `exact` / conf `high` at 80.0-83.5s (clearest 81.5s)
  - subject: a police SUV
  - A police SUV drives straight through the intersection from the bottom-left street to the top-right street without any emergency lights flashing.
- ruled out: A USPS truck passes through later, but it is not an emergency vehicle.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: No vehicles are observed colliding or making physical contact with each other.
- ruled out: Vehicles interact and yield to each other in the intersection (such as a yellow cab yielding to a silver car around 178s), but they maintain safe distances.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: No horse-drawn carriages appear in the frames.
- ruled out: Various types of motorized vehicles, bicycles, and pedestrians pass through the intersection.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 4)

- **match** `exact` / conf `high` at 91.5-105.0s (clearest 101.5s)
  - subject: an articulated bus
  - The bus makes a right turn from the top left street to the downward street, slowing to a near stop mid-turn as it navigates the tight corner.
- ruled out: I checked other turning vehicles, such as the dark SUVs turning at 35.03s and 73.03s, but they completed their turns smoothly without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **absent**
  - why not: No person is seen entering or exiting any parked or stopped vehicle in the visible area.
- ruled out: I closely observed the white van that parallel parks on the left side of the downward street between 81.53s and 92.53s. Although it parks successfully, no one opens a door or gets out for the remainder of the video.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 4)

- **absent**
  - why not: No bus stops at a kerb to allow passengers to board or alight during the video.
- ruled out: There is a bus shelter on the top left street. A blue articulated bus passes by it at 148.53s, but it continues straight through the intersection without stopping to pick up or drop off passengers.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 4)

- **match** `exact` / conf `high` at 10.5-13.5s (clearest 12.0s)
  - subject: a pedestrian in light-colored clothing
  - A pedestrian crosses the main downward street diagonally from left to right, far below the designated crosswalk markings.
- ruled out: There are multiple instances of this behavior, such as another pedestrian crossing mid-block from left to right between 133.53s and 136.53s, confirming this is a recurring event.

### [skateboard] a person riding a skateboard (sample 4)

- **absent**
  - why not: No person is seen riding a skateboard in the video.
- ruled out: I checked the various small moving figures in the bike lanes and crosswalks, but they are all cyclists or walking pedestrians.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 4)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 0.0s)
  - subject: the top half of the intersection
  - The roadway is under active construction throughout the entire video, with orange barriers, cones, and workers in high-visibility vests occupying a large portion of the intersection.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 4)

- **match** `exact` / conf `high` at 31.5-35.0s (clearest 33.0s)
  - subject: a police car
  - A police car drives through the intersection from right to left with its roof lightbar clearly flashing red and blue.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 4)

- **match** `exact` / conf `high` at 9.5-13.0s (clearest 11.0s)
  - subject: a police car
  - A police car drives through the intersection from right to left, and its roof lightbar is completely dark.
- ruled out: I also observed the police car at 31.53s, but that one had its emergency lights flashing.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: There are no collisions or contacts between any vehicles in the visible frames.
- ruled out: I observed the articulated bus making a very tight turn near waiting traffic between 91.53s and 105.03s, but it clears the corner without contacting any other vehicles.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: No horse-drawn carriages are present in the video.

### [turn-halt] a vehicle that stops, or almost stops, part-way through a turn (sample 5)

- **match** `exact` / conf `high` at 177.0-180.0s (clearest 178.5s)
  - subject: yellow taxi
  - A yellow taxi begins a left turn into the main roadway but stops completely before the crosswalk to yield to crossing pedestrians, then resumes its turn.
- ruled out: Several other vehicles make turns throughout the video (e.g., a white SUV at 55.53s, an articulated bus at 90.53s), but they complete their maneuvers without coming to a stop mid-turn.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **absent**
  - why not: No one gets into or out of a stopped vehicle in the visible area.
- ruled out: Parked cars are visible on the left and right sides of the main roadway, and a white van is parked near the top right, but no individuals are seen opening doors or getting in or out of any vehicles during the clip.

### [bus-dwell] a bus stopped at the kerb with people getting on or off it (sample 5)

- **absent**
  - why not: No bus stops to pick up or drop off passengers in the frame.
- ruled out: Several MTA transit buses travel through the intersection (e.g., at 85.03s, 90.03s, 97.03s, and 100.03s), but they all continue moving and pass through the intersection without pulling over to a curb to board or alight passengers.

### [ped-midblock] a pedestrian crossing the roadway away from the crosswalk markings (sample 5)

- **match** `exact` / conf `high` at 129.0-135.5s (clearest 132.5s)
  - subject: pedestrian
  - A pedestrian walks across the main vertical roadway from left to right, entirely outside of any painted crosswalks, navigating far south of the intersection.
- ruled out: Many pedestrians cross within the designated crosswalk lines at the intersection, which does not match the prompt's requirement of crossing away from the markings.

### [skateboard] a person riding a skateboard (sample 5)

- **match** `exact` / conf `high` at 152.0-158.5s (clearest 155.5s)
  - subject: person on skateboard
  - A person riding a skateboard travels downwards through the intersection, utilizing the green-painted bike lane on the left side of the roadway.
- ruled out: Many cyclists use the bike lane throughout the clip (e.g., at 20.03s, 42.03s, 111.03s), but they are riding bicycles, not skateboards.

### [roadworks] the roadway is under construction: cones, barriers, an excavation, or workers standing in the carriageway (sample 5)

- **match** `exact` / conf `high` at 0.0-180.0s (clearest 10.0s)
  - subject: construction zone
  - A major construction zone occupies the upper portion of the intersection, complete with orange barriers, cones, excavation plates, and workers standing and moving within the carriageway.
- ruled out: The sequence is persistent for the entirety of the video.

### [emergency] an emergency vehicle with its lights flashing passing through the intersection (sample 5)

- **match** `exact` / conf `high` at 31.5-34.0s (clearest 33.0s)
  - subject: NYPD police vehicle
  - An NYPD police SUV drives straight through the intersection from left to right with its roof emergency lights visibly flashing.
- ruled out: Another NYPD vehicle crosses at 9.53s, but its emergency lights are off.

### [emergency-dark] an emergency vehicle passing through the intersection with its lights NOT flashing (sample 5)

- **match** `exact` / conf `high` at 8.5-11.0s (clearest 9.5s)
  - subject: NYPD police vehicle
  - An NYPD police SUV drives straight through the intersection from right to left with its roof emergency lights turned off.
- ruled out: The NYPD vehicle crossing at 33.03s has its lights actively flashing, which is the opposite of this query.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: No collisions or vehicles bumping into each other occur in the footage.
- ruled out: While traffic is steady and there are numerous turning maneuvers and instances of vehicles yielding to pedestrians, all vehicles navigate the intersection without colliding.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: No horse-drawn carriages are present in the video.
- ruled out: Various types of vehicles traverse the intersection, including cars, SUVs, delivery trucks, city buses, and emergency vehicles, but no animal-drawn vehicles appear.

---

5 call(s) ok, 0 failed, 2004080 in / 32931 out tokens