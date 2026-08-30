# probe run: events-key_0825-1700_fps2_n5_batch_0830-0813

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 2 | whole range, one call
- frames per call: 361 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/events-key_0825-1700_fps2_n5_batch_0830-0813`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| bike-sidewalk | 0/1 | 1/1 | 0/1 |  |
| bike-wrongway | 0/1 | 0/1 | 1/1 |  |
| emergency | 0/1 | 0/1 | 1/1 |  |
| negative | 0/2 | 2/2 | 0/2 | ground truth known: all absent |
| ped-conflict | 1/1 | 0/1 | 0/1 |  |
| pickup-car | 0/1 | 0/1 | 1/1 |  |
| right-hook | 0/1 | 1/1 | 0/1 |  |
| stop-crosswalk | 0/1 | 0/1 | 1/1 |  |
| turn-fty | 0/1 | 0/1 | 1/1 |  |

### queries whose samples disagreed

- turn-fty — a turning vehicle continuing through a crosswalk while a ped
- stop-crosswalk — a vehicle stopped with part of its body on the crosswalk mar
- pickup-car — a person getting into or out of a stopped car, van or taxi
- bike-wrongway — a cyclist or e-bike rider riding against the direction of tr
- emergency — an emergency vehicle with lights flashing passing through th

## per query

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 1)

- **absent**
  - why not: No turning vehicle entered a crosswalk while a pedestrian was occupying it.
- ruled out: I observed several turning vehicles throughout the video, such as right turns at 8.53s and 16.53s, left turns at 33.53s and 67.53s, and a wide left turn by an articulated bus at 87.53s. In all instances, there were no pedestrians in the crosswalks the vehicles were entering.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 1)

- **absent**
  - why not: There are no instances of a vehicle turning across the path of a cyclist who is continuing straight.
- ruled out: I tracked the cyclists moving straight through the intersection (e.g., in the left bike lane at 15.03s, 32.03s, 120.03s, and 131.03s). No vehicles made a turn across their path while they were proceeding.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 1)

- **absent**
  - why not: No vehicles stopped with any part of their body on the crosswalk markings.
- ruled out: I checked vehicles coming to a halt at red lights (e.g., traffic on the vertical street stopping around 55s, and on the horizontal street around 110s). All vehicles successfully stopped behind the marked stop lines, leaving the crosswalks completely clear.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **absent**
  - why not: No person is seen getting into or out of any stopped vehicle.
- ruled out: I monitored the vehicles parked along the curbs and the vehicles stopped at red lights in the active lanes. No car doors were opened, and no individuals approached the vehicles.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 1)

- **match** `exact` / conf `high` at 23.0-27.5s (clearest 25.0s)
  - subject: a pedestrian and multiple vehicles
  - A pedestrian is crossing the bottom crosswalk from right to left. While the pedestrian is in the crosswalk, multiple vehicles traveling straight downwards pass through the same crosswalk on the left side of the pedestrian.
- **match** `exact` / conf `high` at 128.5-136.0s (clearest 132.5s)
  - subject: pedestrians and multiple vehicles
  - Pedestrians are walking in the bottom crosswalk. While they are occupying the right half of the crosswalk, several vehicles driving straight downwards pass through the left half of the same crosswalk.
- ruled out: I also observed pedestrians in the crosswalks when the traffic light favored them, but during those times, no vehicles drove through.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 1)

- **absent**
  - why not: No cyclist or e-bike rider was observed riding on the sidewalk.
- ruled out: I looked for cyclists throughout the scene. Cyclists were observed riding in the designated bike lane on the far left (e.g., at 32.03s, 131.03s) and in the main traffic lanes on the horizontal street (e.g., 34.53s, 107.53s). None were on the sidewalks.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 1)

- **absent**
  - why not: No cyclist or e-bike rider is seen riding against the direction of traffic in a vehicle lane.
- ruled out: I monitored the direction of cyclists. The cyclists traveling upwards on the left side of the vertical street are using a designated contraflow protected bike lane. Cyclists on the horizontal street traveled in the correct direction for their respective lanes.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 1)

- **absent**
  - why not: No emergency vehicle with flashing lights is present in the video.
- ruled out: An NYPD police cruiser passes through the intersection at 30.53s and turns left, but its rooftop emergency lights are not activated or flashing.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: No collisions or physical contact between vehicles occurred.
- ruled out: Traffic flowed smoothly through the intersection without conflict. Even tight maneuvers, such as the articulated bus turning at 87.53s, were completed without striking other vehicles.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: There is no horse-drawn carriage visible in the footage.
- ruled out: I scanned the intersection and surrounding streets for animals or carriages.

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 2)

- **match** `exact` / conf `high` at 58.0-63.5s (clearest 61.5s)
  - subject: white sedan and pedestrian
  - A white sedan turns left from the cross street onto the avenue, passing straight through the crosswalk while a pedestrian is actively crossing in it.
- ruled out: Examined the black car turning right at 51.53s and the yellow taxi turning left at 138.53s, but the white sedan provides the clearest and most direct example of passing closely to a pedestrian in the crosswalk.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 2)

- **absent**
  - why not: Several cyclists pass through the intersection, but in every case, there are no vehicles turning across their path to create a conflict.
- ruled out: Monitored the cyclists passing at 133s, 145s, and 154s. For instance, a cyclist goes straight at 133s, and a white car turns left shortly after at 136s, but the cyclist had already safely cleared the intersection.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 2)

- **absent**
  - why not: While traffic stops at the intersection multiple times, vehicles stop behind the crosswalk lines and do not block the path of crossing pedestrians.
- ruled out: Checked vehicles stopped for red lights, such as the white car at 19s and the white van at 94s. They both stop correctly behind the crosswalk lines, and there are no pedestrians attempting to cross in front of them at those times.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **absent**
  - why not: Throughout the entire video, no individuals are seen opening vehicle doors or entering or exiting any of the parked or stopped vehicles.
- ruled out: Kept an eye on the parked cars lining both sides of the avenue, including the white van parked at the bottom left and vehicles near the construction zone, but no one ever interacts with the doors.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 2)

- **match** `exact` / conf `high` at 58.0-63.5s (clearest 61.5s)
  - subject: pedestrian and white sedan
  - A pedestrian is walking in the crosswalk across the avenue when a white sedan, completing a left turn, drives through the very same crosswalk directly behind them.
- ruled out: Also noted a pedestrian in the crosswalk around 139.53s as a yellow taxi drives through, but the sequence at 61.53s is more central and clearly shows the simultaneous occupation of the crosswalk.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 2)

- **absent**
  - why not: Cyclists are present in the video, but they all ride on the roadway. None are observed riding on the sidewalk or weaving through pedestrians.
- ruled out: Observed all three instances of cyclists passing through the scene (133s, 145s, 154s), but all of them were correctly riding in the street lanes.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 2)

- **match** `exact` / conf `high` at 141.0-149.0s (clearest 145.0s)
  - subject: cyclist in white shirt
  - A cyclist rides up the left side of the avenue, moving from the bottom-left of the frame towards the top-right, clearly traveling against the flow of traffic in that specific lane.
- ruled out: Checked the cyclist at 133s, but they were riding in the correct direction with the flow of traffic.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 2)

- **match** `exact` / conf `high` at 31.0-36.0s (clearest 33.5s)
  - subject: police SUV
  - An NYPD police SUV with its roof lights flashing actively enters the intersection from the cross street and makes a left turn onto the avenue.
- ruled out: No other emergency vehicles appear in the footage.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: Traffic navigates the intersection without any collisions, fender benders, or contact between any vehicles.
- ruled out: Monitored busy turning moments, such as when the large articulated bus turns at 102s, but all vehicles maintain appropriate clearance.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: There are no horse-drawn carriages or animals pulling vehicles anywhere in the provided frames.
- ruled out: Scanned the traffic for any unusual vehicle types, but the scene only contains standard cars, trucks, buses, and bicycles.

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 3)

- **absent**
  - why not: There are no instances of a turning vehicle driving through a crosswalk while a pedestrian is actively crossing.
- ruled out: A dark SUV drives through a crosswalk while a pedestrian is in it around t=117s, but the SUV is going straight, not turning. Several vehicles turn at the intersection throughout the video, but none cross a crosswalk while a pedestrian is present.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 3)

- **absent**
  - why not: No vehicle turns across the path of a cyclist in a way that puts it in front of them or causes a conflict.
- ruled out: Vehicles turning right at t=36.03s, t=156.03s, and t=164.53s turn right onto the avenue behind cyclists who are continuing straight on the cross street. Since the cyclists are already fully past the turning vehicles and their paths are not cut off or conflicted, this is merely a superficial match.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 3)

- **absent**
  - why not: No vehicle is seen stopped blocking the crosswalk markings while pedestrians are crossing or waiting.
- ruled out: Vehicles frequently stop for the traffic light on the cross street (e.g., at t=20s, t=70s, t=120s), but they stop correctly behind the white stop line, keeping the crosswalk clear.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **absent**
  - why not: No one is observed getting into or out of any vehicle in the video.
- ruled out: There are parked cars visible on the streets on the left side of the frame, but no activity involving people opening doors or entering/exiting them occurs during the sequence.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 3)

- **match** `exact` / conf `high` at 116.5-118.5s (clearest 117.0s)
  - subject: a dark SUV and a dark car
  - A pedestrian is actively walking in the crosswalk on the avenue when a dark SUV and then a dark car drive straight through the same crosswalk, passing close behind the pedestrian.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 3)

- **absent**
  - why not: No cyclists or e-bike riders are seen riding on the sidewalk.
- ruled out: Several cyclists and e-bike riders are seen riding through the intersection throughout the video, but all of them are riding on the road.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 3)

- **absent**
  - why not: No cyclist is seen riding against the direction of traffic.
- ruled out: Cyclists are seen on the cross street (which is one-way) and the avenue (which is two-way with a double yellow line). All observed riders travel in the correct direction matching the flow of traffic for their respective lanes.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 3)

- **absent**
  - why not: No emergency vehicle with active, flashing lights passes through the intersection.
- ruled out: An NYPD police SUV passes straight through the intersection down the avenue from t=32s to t=34s. However, its emergency light bar is not flashing.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: No vehicles collide or make contact in the video.
- ruled out: Vehicles navigate the intersection smoothly throughout the video without any crashes or close calls.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: There are no horse-drawn carriages in the scene.
- ruled out: The intersection handles motorized traffic, bicycles, and pedestrians, but no animals.

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 4)

- **absent**
  - why not: No vehicle made a turn through a crosswalk while a pedestrian was occupying it.
- ruled out: I looked for vehicles making left or right turns at the intersection and checked if there were any pedestrians in the crosswalks they were passing through. For instance, a dark car turns right around 26.53s and a yellow taxi turns left around 174.53s, but in all cases of turning vehicles, the crosswalks they passed through were clear of pedestrians.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 4)

- **absent**
  - why not: No vehicles turn across the path of a cyclist proceeding straight.
- ruled out: I checked every cyclist that crossed the intersection, such as the ones at 34.53s, 131.03s, and 171.03s. While they proceed straight through the intersection, no vehicles attempt to make a turn across their path at those times.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 4)

- **match** `exact` / conf `high` at 35.5-42.0s (clearest 37.0s)
  - subject: dark car
  - A dark car coming from the top left stops for traffic directly over the crosswalk markings. While it is stopped there, a pedestrian crosses the street by walking right in front of its bumper.
- ruled out: I also observed a similar event around 140.03s where another dark car stops on the same crosswalk while a pedestrian crosses, which would also be a valid match.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **match** `exact` / conf `high` at 11.5-15.0s (clearest 13.0s)
  - subject: person
  - A person walks up to the driver's side of a dark car parked on the left side of the screen, opens the door, and gets in. The door is closed by 15.03s, and the car pulls out a few seconds later.
- ruled out: I monitored the vehicles that pull over on the bottom left (like the white van at 69.53s and 124.03s), but no occupants are seen getting in or out of them.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 4)

- **match** `exact` / conf `high` at 161.5-164.0s (clearest 162.5s)
  - subject: pedestrian
  - A pedestrian is actively walking through the top-right crosswalk when a black car traveling straight across the intersection drives directly through the same crosswalk.
- ruled out: Another instance occurs around 135.53s where a white box truck passes through the top-right crosswalk while a pedestrian is in it, which would also be a match.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 4)

- **absent**
  - why not: No cyclists or e-bike riders are seen riding on the sidewalks.
- ruled out: I monitored the visible sidewalks on the left and the top of the frame for any bicycle or e-bike traffic. All observed cyclists rode in the street.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 4)

- **absent**
  - why not: No cyclists are observed riding against the designated direction of traffic.
- ruled out: I monitored the direction of travel for all cyclists (e.g., at 34.53s, 131.03s, 171.03s). They all traveled in the correct direction along with the flow of vehicular traffic for their respective lanes.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 4)

- **match** `exact` / conf `high` at 32.0-35.5s (clearest 33.5s)
  - subject: police SUV
  - A white police SUV with its red and blue emergency lights flashing enters from the top left and proceeds straight through the intersection to the top right.
- ruled out: There were no other emergency vehicles in the sequence.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: No vehicles made contact with each other; there were no collisions or fender benders.
- ruled out: I observed all interactions between vehicles, especially when cars were pulling out of parking spots or merging, but all maintained appropriate spacing.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: There are no horses or horse-drawn carriages present in the scene.
- ruled out: I scanned all traffic passing through the intersection and the parked vehicles along the streets.

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 5)

- **match** `exact` / conf `high` at 148.5-154.5s (clearest 151.0s)
  - subject: dark SUV and a pedestrian
  - A dark SUV turns left and proceeds through the crosswalk while a pedestrian is actively walking across it.
- ruled out: I examined other turning vehicles, such as the black SUV turning left between 13.03s and 19.53s. While a pedestrian was in the crosswalk, the vehicle passed well behind them after they had mostly cleared its path.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 5)

- **absent**
  - why not: No vehicle turned across the path of a cyclist who was continuing straight.
- ruled out: I tracked all cyclists passing through the intersection (e.g., at 35s, 54s, 87s, 105s, 121s, 134s). In all instances, turning vehicles either completed their turns well before the cyclists arrived or waited for them to pass. No vehicle turned across a cyclist's path.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 5)

- **absent**
  - why not: No vehicles stopped with any part of their body on the crosswalk markings while pedestrians were crossing or waiting.
- ruled out: I observed vehicles waiting to turn (e.g., the turning SUVs at 15s and 150s), but they stopped before the crosswalk lines, not on them.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **absent**
  - why not: No one was observed getting into or out of a stopped vehicle.
- ruled out: I checked the vehicles parked along the sides of the roads, as well as taxis moving through. No individuals approached these vehicles to enter, and no doors opened for anyone to exit.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 5)

- **match** `exact` / conf `high` at 148.5-154.5s (clearest 151.0s)
  - subject: dark SUV and a pedestrian
  - A pedestrian is walking in the crosswalk when a dark SUV driving through the intersection proceeds through that exact same crosswalk.
- ruled out: I reviewed vehicles traveling straight through the intersection, but none drove through a crosswalk while a pedestrian was currently in it.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 5)

- **absent**
  - why not: No cyclist or e-bike rider was observed riding on the sidewalk.
- ruled out: I tracked every cyclist and e-bike rider that appeared in the footage. They all rode on the road surface or within bike lanes.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 5)

- **absent**
  - why not: No cyclist or e-bike rider rode against the direction of traffic.
- ruled out: I observed the direction of travel for all cyclists. Every cyclist rode in the correct direction relative to the traffic flow or designated lanes on their side of the street.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 5)

- **match** `exact` / conf `high` at 29.0-36.0s (clearest 32.5s)
  - subject: police car
  - A police car with its blue and red roof lights flashing drives straight through the intersection from left to right.
- ruled out: A white police vehicle crossed the intersection earlier at 9.03s to 13.03s, but its emergency lights were not flashing.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: No two vehicles made contact with each other.
- ruled out: I watched the flow of traffic throughout the entire video. Vehicles yielded to one another appropriately, and no collisions or physical contacts occurred.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: No horse-drawn carriage was present in the intersection.
- ruled out: I scanned the entire video for a horse-drawn carriage but none appeared.

---

5 call(s) ok, 0 failed, 2004175 in / 38627 out tokens