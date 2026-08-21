# probe run: roi-none-bus

- clip: `data/12thFBotwinik/L12thFloorBotwinik-D-2025-11-03_T-17_00_01.mp4`
- range: 130s - 166s (3840x2160, vfr=True)
- roi: `none` | fps: 0.5 | whole range, one call
- frames per call: 18 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/roi-none-bus`

## by axis

| axis | answered present | note |
|---|---|---|
| negative | 0/1 | ground truth known: all absent |
| referential | 1/1 |  |
| temporal | 1/1 |  |

## per query

### [negative] a vehicle driving the wrong way against the flow of traffic

- **absent**
  - why not: No vehicle is seen driving against the flow of traffic on either street during this video segment.
- ruled out: I examined all vehicular traffic (cars, taxis, buses) on both streets. The vertical street is a one-way street with all vehicles correctly traveling downwards in the frame. The horizontal street is two-way, and all observed vehicles are traveling in the correct lanes for their direction of travel.

### [referential] an articulated (bendy) city bus passing through the intersection

- **match** `exact` / conf `high` at 130.0-140.0s (clearest 134.0s)
  - subject: articulated bus going straight
  - An articulated bus (number 5444) travels straight through the intersection, coming from the bottom street and proceeding to the top street.
- **match** `exact` / conf `high` at 142.0-148.0s (clearest 144.0s)
  - subject: articulated bus turning left
  - A second articulated city bus enters the intersection from the top street, makes a left turn, and exits on the left cross street.
- ruled out: No non-articulated buses or similar large vehicles were confused with articulated buses; both instances clearly show the flexible middle section.

### [temporal] the moment a stopped bus begins to move off

- **match** `exact` / conf `high` at 132.0-134.0s (clearest 134.0s)
  - subject: articulated bus
  - The articulated bus, which was previously stationary at the intersection, begins to drive forward.
- ruled out: The blue bus approaching from the left on the cross street around 146.03s slows down, but it is not clear if it comes to a complete stop before proceeding through the intersection.

---

3 call(s) ok, 0 failed, 0 in / 0 out tokens