# probe run: 20260829-090902-key10

- clip: `videos/L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`
- range: 0s - 180s (3840x2160, vfr=True)
- timestamps: `burn,list` (channels: burn, list, interleave, or none)
- fps: 0.5 | whole range, one call
- frames per call: 91 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/20260829-090902-key10`

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

- **match** `exact` / conf `high` at 124.0-128.0s (clearest 126.0s)
  - subject: a black SUV turning left
  - The SUV turns left and proceeds through the crosswalk while a pedestrian is walking across it.
- **match** `exact` / conf `high` at 164.0-168.0s (clearest 166.0s)
  - subject: a dark sedan turning right
  - The sedan turns right and drives through the crosswalk while a pedestrian is in it on the right side.
- ruled out: Considered the USPS truck turning left at 112.03s, but there were no pedestrians in the crosswalk it drove through (the pedestrian was in the crosswalk the truck had already passed). Considered the articulated bus turning left at 94.03s and the white van turning right at 28.03s, but the crosswalks they passed through were empty.

### [right-hook] a vehicle turning across the path of a cyclist who is continuing straight

- **match** `exact` / conf `high` at 90.0-96.0s (clearest 94.0s)
  - subject: cyclist and turning bus
  - An articulated bus turns left across the avenue's left lane, cutting directly across the path of a cyclist who is riding straight up the avenue. The cyclist is forced to brake and wait for the bus to clear the intersection before continuing.
- ruled out: 104.03s-108.03s: A grey SUV turns left from the cross street onto the avenue, joining the lane ahead of a cyclist riding up the avenue. The SUV merges rather than turning across the cyclist's path.
110.03s-116.03s: A white SUV turns right onto the avenue, heading directly toward a cyclist riding the wrong way down the right side of the avenue. They pass each other in the lane; the SUV does not turn across the cyclist's path.
174.03s-180.03s: A cyclist riding up the avenue stops at the crosswalk to allow a yellow cab to pass. The cab is traveling straight on the cross street, not turning.

### [stop-crosswalk] a vehicle stopped with part of its body on the crosswalk markings while pedestrians are crossing there or waiting to

- **match** `exact` / conf `high` at 68.0-72.0s (clearest 70.0s)
  - subject: a grey SUV and a pedestrian
  - A grey SUV approaches the intersection and stops before turning right. It stops with its front wheels past the stop line and resting on the zebra stripes of the crosswalk. A pedestrian arrives at the adjacent corner and stands waiting to use that crosswalk while the vehicle is blocking it, eventually turning away after the vehicle leaves.
- ruled out: Between 46.03s and 52.03s, a white car stops to yield to pedestrians on the left crosswalk. However, it stops properly behind the thick white stop line and does not intrude onto the crosswalk markings themselves. Between 168.03s and 172.03s, a dark car stops with its front end over the line on the right crosswalk, but there are no pedestrians waiting to use that specific crosswalk. At 180.03s, a yellow taxi stops partially on the right crosswalk with pedestrians nearby, but the video ends before the interaction concludes, and it is unclear which direction the pedestrians intend to cross.

### [pickup-car] a person getting into or out of a stopped car, van or taxi

- **match** `exact` / conf `high` at 10.0-16.0s (clearest 12.0s)
  - subject: driver of the red car
  - A red car pulls into a parking spot on the left side of the street and stops. The driver then opens the door, steps out, and walks away towards the sidewalk.
- ruled out: A person walking along the right side of the street near the parked cars (around t=102.03) was checked, but they are simply walking past the vehicles and do not interact with them. Various vehicles stopping for traffic or construction in the intersection were also observed, but no one gets in or out of them.

### [ped-conflict] a pedestrian in the crosswalk while vehicles are driving through that same crosswalk

- **match** `exact` / conf `high` at 20.0-24.0s (clearest 22.0s)
  - subject: a pedestrian and a white car
  - A pedestrian is in the bottom crosswalk while a white car drives vertically up through the same crosswalk.
- **match** `exact` / conf `high` at 48.0-52.0s (clearest 50.0s)
  - subject: pedestrians and a black SUV
  - Pedestrians are walking down in the top crosswalk while a black SUV turns left and drives through that crosswalk.
- **match** `exact` / conf `high` at 76.0-82.0s (clearest 78.0s)
  - subject: a pedestrian and a light SUV
  - A pedestrian is in the right crosswalk while a light SUV turns right and drives directly through it.
- **match** `exact` / conf `high` at 102.0-106.0s (clearest 104.0s)
  - subject: a pedestrian and a grey SUV
  - A pedestrian is in the right crosswalk while a grey SUV drives horizontally right-to-left through the same crosswalk.
- **match** `exact` / conf `high` at 106.0-110.0s (clearest 108.0s)
  - subject: a pedestrian and a light SUV
  - A pedestrian is in the top crosswalk while a light SUV drives vertically up through it.
- **match** `exact` / conf `high` at 122.0-126.0s (clearest 124.0s)
  - subject: a pedestrian and a white car
  - A pedestrian is crossing the bottom crosswalk while a white car drives vertically up through the same crosswalk.
- ruled out: At t=12.03, a pedestrian is in the left crosswalk and a car turns left, but the car does not drive through the left crosswalk. At t=130.03 - 132.03, a pedestrian is crossing the bottom crosswalk, but they step out of the crosswalk just before a white van drives through it. At t=140.03, a white van drives through the right crosswalk while a pedestrian is present, but the pedestrian is in the top crosswalk, not the one the vehicle is passing through.

### [bike-sidewalk] a cyclist or e-bike rider riding along the sidewalk in the direction it runs, passing or weaving among pedestrians

- **absent**
  - why not: All observed cyclists are riding on the road, in a bike lane, or within crosswalks. No cyclist is seen riding along a sidewalk and weaving through pedestrians.
- ruled out: Several cyclists are visible in this video, but they use the roadways, bike lanes, or crosswalks. For example, at 36.03s, a cyclist crosses the top intersection via the crosswalk. From 132.03s to 140.03s, a cyclist rides up the street in the painted bike lane. At 170.03s, multiple cyclists cross the intersection. None of them are riding longitudinally along the sidewalk space itself.

### [bike-wrongway] a cyclist or e-bike rider riding against the direction of traffic

- **match** `exact` / conf `high` at 106.0-120.0s (clearest 112.0s)
  - subject: cyclist
  - A cyclist rides up the main avenue from the bottom left towards the top right, moving directly against the established flow of traffic on that street.
- **match** `exact` / conf `high` at 168.0-178.0s (clearest 172.0s)
  - subject: cyclist
  - Another cyclist rides up the main avenue from the bottom left towards the top right, also moving against the flow of traffic.
- ruled out: A cyclist is visible between 34.03s and 38.03s crossing the intersection, but they are not riding against the flow of traffic on the avenues or streets they traverse.

### [emergency] an emergency vehicle with lights flashing passing through the intersection

- **match** `exact` / conf `high` at 30.0-36.0s (clearest 32.0s)
  - subject: white police car
  - A white police vehicle with flashing roof lights enters the intersection from the bottom road, crosses the intersection, and turns left into the far cross street.
- ruled out: No other emergency vehicles were observed in the provided frames.

### [negative] two vehicles making contact with each other

- **absent**
  - why not: At no point in this video sequence do any two vehicles make contact with each other.
- ruled out: I observed all vehicle movements and interactions throughout the sequence, including the tight left turn made by the long articulated bus between 86.03s and 104.03s, and various right turns by other vehicles (e.g., a USPS truck at 112.03s). None of these resulted in any vehicles touching or colliding.

### [negative] a horse-drawn carriage

- **absent**
  - why not: No horse-drawn carriage appears in any of the provided frames. The scene contains only motorized vehicles, pedestrians, and cyclists.
- ruled out: Looked for a horse-drawn carriage among the various vehicles (cars, trucks, vans, buses) navigating the intersection and surrounding streets.

---

10 call(s) ok, 0 failed, 1012424 in / 42269 out tokens