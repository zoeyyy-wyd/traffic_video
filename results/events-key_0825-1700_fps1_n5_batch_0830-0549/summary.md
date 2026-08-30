# probe run: events-key_0825-1700_fps1_n5_batch_0830-0549

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 1 | whole range, one call
- frames per call: 181 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/events-key_0825-1700_fps1_n5_batch_0830-0549`

## by axis

5 samples per query. **split** = the samples disagreed with each other, so that query has no stable answer on these frames and must not be counted either way.

| axis | all samples present | all absent | split | note |
|---|---|---|---|---|
| bike-sidewalk | 0/1 | 0/1 | 1/1 |  |
| bike-wrongway | 0/1 | 0/1 | 1/1 |  |
| emergency | 0/1 | 0/1 | 1/1 |  |
| negative | 0/2 | 2/2 | 0/2 | ground truth known: all absent |
| ped-conflict | 1/1 | 0/1 | 0/1 |  |
| pickup-car | 0/1 | 0/1 | 1/1 |  |
| right-hook | 0/1 | 0/1 | 1/1 |  |
| stop-crosswalk | 0/1 | 0/1 | 1/1 |  |
| turn-fty | 0/1 | 0/1 | 1/1 |  |

### queries whose samples disagreed

- turn-fty — a turning vehicle continuing through a crosswalk while a ped
- right-hook — a vehicle turning across the path of a cyclist who is contin
- stop-crosswalk — a vehicle stopped with part of its body on the crosswalk mar
- pickup-car — a person getting into or out of a stopped car, van or taxi
- bike-sidewalk — a cyclist or e-bike rider riding along the sidewalk in the d
- bike-wrongway — a cyclist or e-bike rider riding against the direction of tr
- emergency — an emergency vehicle with lights flashing passing through th

## per query

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 1)

- **absent**
  - why not: No turning vehicle was seen passing through a crosswalk while a pedestrian was in it.
- ruled out: I observed all turning vehicles, such as the black SUV turning left at 15s, the white delivery truck turning right at 112s, and the grey car turning left at 140s. In all instances, the crosswalks they passed through were empty.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 1)

- **absent**
  - why not: There was no instance of a vehicle turning across the path of a cyclist continuing straight.
- ruled out: I tracked all cyclists passing through the intersection, such as the ones at 35s and 125s. The turning vehicles in the scene, like the black car turning left at 125s, completed their turns without interacting with or crossing the path of the cyclists.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 1)

- **absent**
  - why not: Traffic flowed through the intersection smoothly, and no vehicles were observed stopping with their bodies over the crosswalk markings.
- ruled out: I monitored the crosswalks for any stopped vehicles. While a large blue bus slowly navigates a turn from 88s to 101s, it moves continuously and does not stop on the crosswalk markings.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 1)

- **absent**
  - why not: No one was seen getting into or out of any parked or stopped vehicle.
- ruled out: I watched the vehicles parked along the left curb and the construction area throughout the entire video segment. No individuals were seen approaching these vehicles or opening their doors.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 1)

- **match** `exact` / conf `high` at 153.0-157.0s (clearest 155.0s)
  - subject: a white van and two pedestrians
  - A white van drives straight through the left crosswalk, passing closely behind two pedestrians who are in the middle of crossing.
- ruled out: I also checked instances like the white sedan passing through at 10s and the black SUV at 15s, but those vehicles did not cross the specific crosswalks where people were standing or walking.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 1)

- **match** `exact` / conf `high` at 161.0-164.0s (clearest 163.0s)
  - subject: a cyclist and a pedestrian
  - A cyclist rides across the top crosswalk and continues onto the right-side sidewalk, passing a pedestrian who is walking towards the intersection on that sidewalk.
- ruled out: Other cyclists, such as those at 35s and 125s, were correctly riding in the street rather than on the sidewalk.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 1)

- **absent**
  - why not: No cyclist or e-bike rider was seen riding against the direction of traffic.
- ruled out: I observed every cyclist passing through the intersection (e.g., at 35s, 125s, and 134s). All of them were traveling in the same direction as the traffic flow for the lanes they were using.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 1)

- **match** `exact` / conf `high` at 31.0-34.0s (clearest 32.0s)
  - subject: a police SUV
  - A white police SUV with its emergency lights flashing enters from the left and drives straight across the intersection, exiting on the right.

### [negative] two vehicles making contact with each other (sample 1)

- **absent**
  - why not: There were no instances of vehicles colliding or making contact with one another.
- ruled out: I closely watched the intersection for any collisions, especially during the turns made by the large bus at 88s and the various cars cutting through, but all vehicles maintained safe distances from each other.

### [negative] a horse-drawn carriage (sample 1)

- **absent**
  - why not: No horse-drawn carriage appeared in the footage.
- ruled out: I scanned the street and traffic for the entirety of the video sequence looking for any horse-drawn vehicles.

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 2)

- **match** `exact` / conf `high` at 43.0-49.0s (clearest 46.0s)
  - subject: black car and pedestrian
  - A black car turns left from the left street to head up the top street, passing through the top crosswalk while a pedestrian is actively walking in it.
- ruled out: A dark SUV turning right at 154s passes through a crosswalk, but no pedestrians are in its path. An articulated bus turns left at 89s but clears the crosswalk without interfering with pedestrians.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 2)

- **absent**
  - why not: No vehicles are seen turning across the path of a cyclist who is traveling straight.
- ruled out: A cyclist moves straight through the intersection at 35.03s with a vehicle turning left behind them, but the vehicle does not cross their path. Another cyclist travels straight at 125.03s with turning vehicles nearby, but none cross their trajectory.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 2)

- **match** `exact` / conf `high` at 111.0-119.0s (clearest 114.0s)
  - subject: white USPS truck and pedestrians
  - A white USPS truck stops with its front end resting on the right crosswalk markings. Pedestrians cross the street by walking closely around the front of the truck.
- ruled out: Other vehicles stop properly behind the crosswalk lines or pass through without stopping while pedestrians are present.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 2)

- **absent**
  - why not: No doors are seen opening, and no individuals are observed getting into or out of any parked or stopped vehicles.
- ruled out: Parked cars on the bottom left are visible throughout the video, but no one approaches them. The USPS truck stops at 112s, but the driver remains inside.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 2)

- **match** `exact` / conf `high` at 136.0-140.0s (clearest 138.0s)
  - subject: dark SUV and pedestrian
  - A dark SUV drives straight through the intersection from the top street, passing through the top crosswalk while a pedestrian is actively walking in it.
- ruled out: Vehicles passing through crosswalks that are entirely empty or where pedestrians have already completely cleared the path.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 2)

- **absent**
  - why not: No cyclists or e-bike riders are seen riding on any of the sidewalks.
- ruled out: Several cyclists are observed in the footage (e.g., at 35s, 108s, 125s, and 154s), but all are riding correctly in the street.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 2)

- **absent**
  - why not: No cyclists are seen riding against the flow of traffic.
- ruled out: Cyclists are visible at 35s, 108s, 125s, and 154s. All are observed traveling in the correct direction of traffic for their respective lanes.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 2)

- **absent**
  - why not: No emergency vehicles with active, flashing lights are seen passing through the intersection.
- ruled out: A police SUV passes through the intersection between 31.03s and 34.03s. However, its emergency lights are not flashing.

### [negative] two vehicles making contact with each other (sample 2)

- **absent**
  - why not: No collisions or physical contact between vehicles occurred.
- ruled out: Normal traffic interactions and turning maneuvers are observed, but no vehicles come close enough to suggest a collision.

### [negative] a horse-drawn carriage (sample 2)

- **absent**
  - why not: No horse-drawn carriages are present in the footage.
- ruled out: All vehicles observed in the intersection are motor vehicles (cars, SUVs, vans, buses) or bicycles.

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 3)

- **match** `exact` / conf `high` at 156.0-159.0s (clearest 158.0s)
  - subject: dark SUV
  - A dark SUV turns right from the avenue onto the cross street, continuing through the crosswalk while a pedestrian is actively crossing it.
- ruled out: A dark SUV turning left at 52.03s also passes through the crosswalk while a pedestrian is crossing, but the pedestrian is further away. The event at 158.03s is a clearer example.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 3)

- **match** `exact` / conf `high` at 119.0-123.0s (clearest 121.0s)
  - subject: white van and cyclist
  - A white van on the avenue makes a left turn onto the cross street, crossing directly over the bike lane. A cyclist approaching in that bike lane continues straight through the intersection shortly after the van clears their path.
- ruled out: Several other vehicles turn left or right during the video, but they either do not cross the active bike lane or there is no cyclist nearby at the time.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 3)

- **absent**
  - why not: While some vehicles stop slightly past the stop line, there are no observed instances of a vehicle blocking a crosswalk while pedestrians are attempting to use it.
- ruled out: At 113.03s, a USPS truck stops at a red light with its front end resting over the crosswalk markings on the cross street. However, there are no pedestrians crossing or waiting to cross at that location during the time it is stopped.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 3)

- **absent**
  - why not: No individuals are seen entering or exiting any parked, stopped, or waiting vehicles during the footage.
- ruled out: The parked cars lined up on the left side of the avenue were checked throughout the video, but no activity occurs around their doors.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 3)

- **match** `exact` / conf `high` at 156.0-159.0s (clearest 158.0s)
  - subject: pedestrian and turning SUV
  - A pedestrian is crossing the cross street within the marked crosswalk when a dark SUV turns right and drives directly through the same crosswalk.
- ruled out: Other pedestrians cross safely while traffic is completely stopped for the red light.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 3)

- **absent**
  - why not: No cyclists or e-bike riders are seen using the pedestrian sidewalks.
- ruled out: Cyclists are observed throughout the video (e.g., at 34.03s, 123.03s, 134.03s, and 160.03s), but they are consistently riding on the road or within the designated bike lane.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 3)

- **absent**
  - why not: There are no instances of a cyclist or e-bike riding against the designated traffic flow.
- ruled out: Multiple cyclists travel along both the avenue and the cross street, but all observed riders are flowing in the correct direction of the one-way traffic.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 3)

- **match** `superficial` / conf `high` at 31.0-34.0s (clearest 33.0s)
  - subject: police car
  - An emergency vehicle (a police car) drives straight through the intersection along the cross street, but its roof lights are not flashing.
- ruled out: No other emergency vehicles (fire trucks, ambulances) appear in the footage.

### [negative] two vehicles making contact with each other (sample 3)

- **absent**
  - why not: There are no collisions, bumps, or instances of physical contact between any vehicles in the scene.
- ruled out: Turning vehicles occasionally navigate tight spaces (e.g., the articulated bus turning at 92.03s), but they maintain safe clearance from other road users.

### [negative] a horse-drawn carriage (sample 3)

- **absent**
  - why not: A horse-drawn carriage never enters the frame.
- ruled out: The traffic consists entirely of motorized vehicles, bicycles, and pedestrians.

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 4)

- **match** `exact` / conf `high` at 72.0-75.0s (clearest 74.0s)
  - subject: the black SUV and the pedestrian in the left crosswalk
  - A black SUV turns left into the cross street, driving straight through the left crosswalk while a pedestrian is actively crossing in it.
- **match** `exact` / conf `high` at 55.0-58.0s (clearest 57.0s)
  - subject: the black SUV and the pedestrian in the left crosswalk
  - A black SUV makes a left turn, passing through the left crosswalk right behind a pedestrian who is crossing.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 4)

- **match** `exact` / conf `high` at 89.0-94.0s (clearest 91.0s)
  - subject: the blue and white articulated bus and the cyclist
  - A cyclist is riding straight up the main street in the left lane when a bus traveling in the same direction makes a left turn across the cyclist's path, forcing the cyclist to maneuver and pass behind the bus.
- ruled out: A dark car turns left in frame 136, but there is no cyclist moving straight alongside it at the time.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 4)

- **absent**
  - why not: No vehicles are observed stopping with their bodies on any crosswalk markings while pedestrians are crossing or waiting to cross.
- ruled out: A white truck pulls over in frames 80-84 and a white box truck stops in frames 108-111. Both vehicles stop near crosswalks, but they do not stop on the crosswalk markings themselves, and no pedestrians are crossing or waiting at those moments.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 4)

- **match** `exact` / conf `high` at 138.0-142.0s (clearest 140.0s)
  - subject: the person and the black car parked on the bottom left
  - A person approaches the driver's side of a parked black car, opens the door, and gets inside.
- ruled out: A person opens the rear cargo doors of a stopped white van in frames 107-112 to retrieve items, but does not get into or out of the vehicle's seating area. A person squeezes between two parked cars in frames 68-70 to reach the sidewalk, but does not enter either car.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 4)

- **match** `exact` / conf `high` at 133.0-135.0s (clearest 134.0s)
  - subject: the two pedestrians and the silver SUV in the top crosswalk
  - Two pedestrians are crossing the top crosswalk and pause as a silver SUV drives straight through the crosswalk directly in front of them.
- **match** `exact` / conf `high` at 135.0-138.0s (clearest 136.0s)
  - subject: the two pedestrians and the white car in the top crosswalk
  - The same two pedestrians are still waiting to finish crossing the top crosswalk when a white car moving straight up the main street drives through the crosswalk beside them.
- **match** `exact` / conf `high` at 72.0-75.0s (clearest 74.0s)
  - subject: the pedestrian and the black SUV in the left crosswalk
  - A pedestrian is in the left crosswalk as a black SUV drives through the crosswalk while completing a left turn.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 4)

- **absent**
  - why not: Several cyclists and scooter riders are observed in the footage, but all of them ride in the street or crosswalks; none are observed riding along the sidewalks among pedestrians.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 4)

- **match** `exact` / conf `high` at 120.0-126.0s (clearest 123.0s)
  - subject: the cyclist in the dark shirt
  - A cyclist enters the intersection from the top crosswalk and rides straight down the main street, which is a one-way street with traffic and parked cars facing the opposite direction.
- ruled out: A person on a scooter crosses the bottom crosswalk from left to right in frames 60-63, but this is crossing the street rather than riding against the flow of traffic.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 4)

- **absent**
  - why not: An emergency vehicle is present in the scene, but its emergency lights are not activated or flashing.
- ruled out: A white NYPD police SUV drives through the intersection from right to left between 31s and 34s. However, its light bar remains completely dark, so it is not flashing.

### [negative] two vehicles making contact with each other (sample 4)

- **absent**
  - why not: Traffic flows smoothly and no vehicles are seen making contact or colliding with each other.
- ruled out: A yellow taxi turning left and a white van approaching from the right in frame 158 come somewhat close to each other, but the van yields and no contact is made.

### [negative] a horse-drawn carriage (sample 4)

- **absent**
  - why not: There are no horses or horse-drawn carriages visible anywhere in the scene.

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it (sample 5)

- **match** `exact` / conf `high` at 111.0-116.0s (clearest 114.0s)
  - subject: white box truck and pedestrian
  - A white box truck turns left through the intersection. As it exits the intersection, it drives through the crosswalk on the right side while a pedestrian is walking in it.
- ruled out: The blue articulated bus turning right at 87s was considered, but it stops and waits for the pedestrian to clear its path before driving through the crosswalk.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight (sample 5)

- **absent**
  - why not: No vehicles turn across the path of a cyclist continuing straight.
- ruled out: A cyclist goes straight through the intersection at 86s while a blue bus turns right, but the bus was far ahead and completed its turn before the cyclist reached the intersection, so paths did not cross.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to (sample 5)

- **match** `exact` / conf `high` at 88.0-94.0s (clearest 91.0s)
  - subject: blue articulated bus and pedestrian
  - An articulated bus turning right stops with its front section on the crosswalk markings. While it is stopped, a pedestrian crosses the crosswalk directly in front of the bus.
- ruled out: The white box truck turning left at 111s was considered, but it drives through the crosswalk without stopping.

### [pickup-car] a person getting into or out of a stopped car, van or taxi (sample 5)

- **absent**
  - why not: No person opens a vehicle door or gets in or out of any vehicle during the sequence.
- ruled out: Vehicles parked on the left side of the road and vehicles waiting at the red lights were observed for activity.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk (sample 5)

- **match** `exact` / conf `high` at 111.0-116.0s (clearest 114.0s)
  - subject: white box truck and pedestrian
  - A pedestrian is walking in the crosswalk on the right side of the intersection while a white box truck turning left drives continuously through that same crosswalk.
- ruled out: The blue bus at 91s was considered, but it was stopped on the crosswalk rather than driving through it while the pedestrian was crossing in front of it.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians (sample 5)

- **absent**
  - why not: All observed cyclists are riding on the roadway; none are seen riding on the sidewalks.
- ruled out: The sidewalks on the top, bottom, and right sides of the scene were checked for bicycle traffic.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic (sample 5)

- **match** `exact` / conf `high` at 33.0-38.0s (clearest 35.0s)
  - subject: cyclist on horizontal road
  - A cyclist rides from right to left through the intersection and continues onto the left street, traveling opposite to the flow of traffic on the one-way horizontal street.
- ruled out: Other cyclists riding with the flow of traffic, such as the one crossing downwards at 62s, were observed but rule out.

### [emergency] an emergency vehicle with lights flashing passing through the intersection (sample 5)

- **match** `exact` / conf `high` at 29.0-36.0s (clearest 32.0s)
  - subject: police SUV
  - A police SUV with its emergency light bar flashing enters the intersection from the top road and completes a left turn.
- ruled out: A yellow taxi turning left at 178s was checked, but it is not an emergency vehicle and has no flashing lights.

### [negative] two vehicles making contact with each other (sample 5)

- **absent**
  - why not: Traffic flows safely and no vehicles make contact with one another.
- ruled out: Vehicles waiting at the traffic lights and interacting through turns were monitored for collisions.

### [negative] a horse-drawn carriage (sample 5)

- **absent**
  - why not: There are no horse-drawn carriages present in the video; only motor vehicles, bicycles, and pedestrians.
- ruled out: The entire intersection was scanned for any non-motorized vehicles.

---

5 call(s) ok, 0 failed, 1006625 in / 46145 out tokens