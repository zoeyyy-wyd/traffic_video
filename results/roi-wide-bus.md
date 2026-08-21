# probe run: roi-wide-bus

- clip: `data/12thFBotwinik/L12thFloorBotwinik-D-2025-11-03_T-17_00_01.mp4`
- range: 130s - 166s (3840x2160, vfr=True)
- roi: `wide` | fps: 0.5 | whole range, one call
- frames per call: 18 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/roi-wide-bus`

## by axis

| axis | answered present | note |
|---|---|---|
| negative | 1/1 | **every hit here is a fabrication** |
| referential | 1/1 |  |
| temporal | 1/1 |  |

## per query

### [negative] a vehicle driving the wrong way against the flow of traffic

- **match** `exact` / conf `high` at 136.0-140.0s (clearest 138.0s)
  - subject: black SUV with flashing lights
  - A black SUV, functioning as an emergency vehicle, drives northbound up the avenue while traveling in the southbound lanes, completely on the wrong side of the double yellow dividing lines and painted traffic island.
- ruled out: Other vehicles moving north (such as the articulated bus and taxis) and south (such as the white car and other taxis) on the avenue were considered, but they are traveling in their correct respective lanes on either side of the double yellow line.

### [referential] an articulated (bendy) city bus passing through the intersection

- **match** `exact` / conf `high` at 130.0-140.0s (clearest 134.0s)
  - subject: articulated city bus
  - An articulated city bus (with number 5444 on its rear roof) travels northbound, passing straight through the intersection.
- **match** `exact` / conf `high` at 152.0-164.0s (clearest 158.0s)
  - subject: second articulated city bus
  - Another articulated city bus enters from the left and travels eastbound, passing straight across the intersection.
- ruled out: A third articulated bus passes eastbound through the intersection between 142.03s and 150.03s. However, in the frame at 142.03s, the bus suffers from a severe visual glitch (likely a panorama stitching artifact), making its shape highly distorted. Therefore, it was rejected in favor of the two clean, distortion-free passages.

### [temporal] the moment a stopped bus begins to move off

- **match** `exact` / conf `high` at 134.0-138.0s (clearest 136.0s)
  - subject: articulated bus 5444
  - The bus, which had been stopped just before the intersection, begins moving forward to complete its turn.
- ruled out: The second bus that appears on the left cross street around 146.03s comes to a stop but does not begin to move off again within the timeframe of this window.

---

3 call(s) ok, 0 failed, 0 in / 0 out tokens