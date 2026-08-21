# probe run: roi-junction-bus

- clip: `data/12thFBotwinik/L12thFloorBotwinik-D-2025-11-03_T-17_00_01.mp4`
- range: 130s - 166s (3840x2160, vfr=True)
- roi: `junction` | fps: 0.5 | whole range, one call
- frames per call: 18 | model: gemini-3.1-pro-preview (resolution=high, thinking=high)
- frames written to `runs/roi-junction-bus`

## by axis

| axis | answered present | note |
|---|---|---|
| negative | 0/1 | ground truth known: all absent |
| referential | 1/1 |  |
| temporal | 0/1 |  |

## per query

### [negative] a vehicle driving the wrong way against the flow of traffic

- **absent**
  - why not: No cars, trucks, or motorcycles are observed driving against the flow of traffic in the video. All vehicles in the main traffic lanes travel in the correct direction as indicated by the pavement arrows (the top three lanes flow left, and the bottom two flow right).
- ruled out: A person on a scooter or bicycle rides rightwards in the left-flowing bike lane on the far side of the main road from t=138.03s to t=146.03s. This was rejected because the prompt asks for a 'vehicle' driving against the flow of traffic, which typically implies a motor vehicle in the main traffic lanes rather than a micromobility user in a bike lane. Additionally, mopeds/motorcycles are seen in the main lanes (e.g., moving right at 138.03s, moving left at 160.03s), but they are all in the correct lanes according to the pavement arrows.

### [referential] an articulated (bendy) city bus passing through the intersection

- **match** `exact` / conf `high` at 134.0-148.0s (clearest 142.0s)
  - subject: articulated city bus
  - A blue and white articulated city bus enters the intersection from the bottom, turns left, and exits the frame to the left.

### [temporal] the moment a stopped bus begins to move off

- **absent**
  - why not: No bus is seen stopped in the footage; all visible buses are already moving and remain in continuous motion.
- ruled out: The articulated bus that enters from the bottom at 134.03s and turns left, as well as the articulated bus that enters from the left at 160.03s moving right. Both are in continuous motion the entire time they are in frame and never stop.

---

3 call(s) ok, 0 failed, 0 in / 0 out tokens