# probe run: rep1

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `interleave` (channels: burn, list, interleave, or none)
- fps: 0.5 | whole range, one call
- frames per call: 91 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `/home/yw4636/traffic_video/runs/20260829-214844-scene/no-scene/rep1`

## by axis

| axis | answered present | note |
|---|---|---|
| bike-sidewalk | 0/1 |  |
| bike-wrongway | 1/1 |  |
| emergency | 1/1 |  |
| negative | 0/2 | ground truth known: all absent |
| ped-conflict | 1/1 |  |
| pickup-car | 0/1 |  |
| right-hook | 1/1 |  |
| stop-crosswalk | 0/1 |  |
| turn-fty | 1/1 |  |

## per query

### [turn-fty] a turning vehicle continuing through a crosswalk while a pedestrian is in it

- **match** `exact` / conf `high` at 102.0-108.0s (clearest 104.0s)
  - subject: dark SUV turning left
  - A dark SUV completes a left turn, driving through the upper crosswalk and passing behind a pedestrian who is currently walking across it.
- ruled out: I examined the black SUV turning left at 2.00s, but the pedestrian waiting at the corner does not step into the crosswalk until after the vehicle passes. I also looked at the articulated bus turning right at 88.03s, but there were no pedestrians in the crosswalk it traversed.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight

- **match** `exact` / conf `high` at 152.0-158.0s (clearest 156.0s)
  - subject: a dark SUV and two cyclists
  - A dark SUV turns right, cutting directly across the path of two cyclists who are proceeding straight across the intersection from left to right.
- ruled out: I also observed cyclists navigating the intersection at other times (such as around 114.03s and 172.03s), but in those instances, no vehicles turned across their paths.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to

- **absent**
  - why not: Throughout the video, vehicles that arrive at red lights stop properly behind the stop lines. No vehicle is seen encroaching or stopping on the crosswalk markings while pedestrians are using or waiting to use the crosswalk.
- ruled out: The dark car waiting at the red light on the right approach between t=42s and t=58s, the dark car waiting there between t=114s and t=128s, and the yellow taxi waiting there from t=176s onwards. In all these cases, pedestrians are crossing or waiting to cross, but the vehicles stop correctly behind the stop line and are not on the crosswalk markings.

### [pickup-car] a person getting into or out of a stopped car, van or taxi

- **absent**
  - why not: While multiple vehicles stop and remain parked in the camera's view throughout the video, the specific action of a person opening a door and getting into or out of a vehicle does not occur or is not visible.
- ruled out: Several vehicles are seen stopping and parking during the sequence. A white car parks on the right side of the lower road from t=10.03s to t=30.03s. A white van and a white car park on the upper right side of the cross street between t=30.03s and t=40.03s. A food truck parks on the left side of the lower road around t=84.03s, and another silver van parks behind it around t=140.03s. However, in all of these instances, no person is ever visible getting into or out of the vehicles.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk

- **match** `exact` / conf `high` at 10.0-14.0s (clearest 12.0s)
  - subject: pedestrian and white car
  - A pedestrian is walking in the left crosswalk while a white car turns left and drives through the same crosswalk right behind them.
- **match** `exact` / conf `high` at 62.0-66.0s (clearest 64.0s)
  - subject: pedestrian and dark SUV
  - A pedestrian is walking in the left crosswalk while a dark SUV turns left and drives through the same crosswalk right behind them.
- ruled out: At 18.03s-22.03s, a pedestrian crosses the bottom crosswalk, but the white car has already cleared the crosswalk before the pedestrian is in its path. At 56.03s-60.03s, a pedestrian crosses the left crosswalk, but the turning white car passes through after the pedestrian has mostly cleared the path. At 174.03s-178.03s, pedestrians are in the crosswalk, but a car correctly waits for them to pass rather than driving through.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians

- **absent**
  - why not: The video contains no instances of a cyclist or e-bike rider riding along the sidewalk; all observed cyclists remain on the roadway or within crosswalks.
- ruled out: Several cyclists and e-bike riders are seen crossing the intersection within or near the marked crosswalks (for example, around 34-38s, 112-124s, 150-156s, and 158-164s). However, none of them are riding along the sidewalks or weaving among pedestrians on the sidewalk.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic

- **match** `exact` / conf `high` at 152.0-176.0s (clearest 154.0s)
  - subject: three cyclists
  - Two cyclists ride downwards on the left side of the avenue, moving opposite to the flow of vehicle traffic. Shortly after they pass, a third cyclist follows them, also riding against the direction of traffic.
- ruled out: Cyclists visible at 112.03s, 114.03s, and 150.03s are riding in the correct direction alongside traffic (upwards). Cyclists seen at 32.03s and 138.03s are crossing the avenue via the crosswalk rather than riding against traffic flow.

### [emergency] an emergency vehicle with lights flashing passing through the intersection

- **match** `exact` / conf `high` at 32.0-36.0s (clearest 34.0s)
  - subject: police SUV
  - A police SUV with flashing lights enters the intersection from the upper right and drives straight through, exiting towards the lower left.
- ruled out: A white van at 30.03s enters the intersection from the same direction shortly before the police vehicle, but it is not an emergency vehicle and lacks flashing lights.

### [negative] two vehicles making contact with each other

- **absent**
  - why not: At no point in the provided video segment do any two vehicles make physical contact with each other.
- ruled out: Multiple vehicles navigate the intersection throughout the video, including an articulated bus making a wide left turn between 88.03s and 96.03s, and various cars and trucks passing nearby. However, all vehicles maintain a safe distance and pass each other without any collisions.

### [negative] a horse-drawn carriage

- **absent**
  - why not: The requested situation (a horse-drawn carriage) does not occur in this video window. The traffic consists entirely of motorized vehicles, bicycles, and pedestrians.
- ruled out: A variety of vehicles pass through the intersection, including cars, SUVs, white vans, an articulated blue bus, a USPS mail truck, and a yellow taxi, but no horse-drawn carriages were present.

---

10 call(s) ok, 0 failed, 1013274 in / 19652 out tokens