# scene

## Configuration

- clip `L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`, 180s
- queries `queries/events-key.txt`, 10 categories
- model `gemini-3.1-pro-preview`, 5 samples per query, all queries in one call
- timestamps `interleave`
- ground truth `2026-08-25-17_00_01.txt`
- **varied across arms: scene_file**

| arm | scene_file | frames | tokens in |
|---|---|---|---|
| `no-scene` | None | 181 | 1,005,990 |
| `with-scene` | scene/12F-Ams.built.md | 181 | 1,007,790 |

## Result

`presence` is whether the yes/no was right, per sample. `localised` is how many returned intervals land on a real one at IoU >= 0.5. They come apart, and only the second one means anything for annotation.

| arm | presence | localised | mean IoU over matched pairs |
|---|---|---|---|
| `no-scene` | 41/50 (82%) | 11/68 (16%) | 0.47 |
| `with-scene` | 34/50 (68%) | 11/66 (17%) | 0.47 |

## Every answer

One row per interval the model returned, plus a row where it returned nothing. `IoU` is against the best unclaimed real span, matched one-to-one so a single wide interval cannot claim several. `below` means it overlapped but under the threshold; `no overlap` means it landed nowhere near.

### no-scene

| category | s | interval | subject | IoU | quality |
|---|---|---|---|---|---|
| turn-halt | 1 | 1:25.0-1:27.0 | black car | no overlap | exact |
| turn-halt | 2 | 0:31.0-0:33.0 | white van | no overlap | exact |
| turn-halt | 2 | 0:40.0-0:42.0 | dark SUV | no overlap | exact |
| turn-halt | 2 | 0:43.0-0:46.0 | dark SUV | no overlap | exact |
| turn-halt | 2 | 1:45.0-1:49.0 | dark car | 0.07 below | exact |
| turn-halt | 2 | 2:03.0-2:05.0 | white van | no overlap | exact |
| turn-halt | 2 | 2:21.0-2:23.0 | black car | no overlap | exact |
| turn-halt | 2 | 2:26.0-2:29.0 | dark SUV | no overlap | exact |
| turn-halt | 3 | 1:34.0-1:38.0 | an articulated MTA bus | 0.25 below | exact |
| turn-halt | 3 | 1:47.0-1:50.0 | a white car | no overlap | exact |
| turn-halt | 4 | 1:33.0-1:42.0 | articulated bus | 0.54 | exact |
| turn-halt | 5 | 0:16.0-0:17.0 | a dark car | no overlap | exact |
| turn-halt | 5 | 0:46.0-0:48.0 | a dark SUV | no overlap | exact |
| pickup-car | 1 | 2:05.0-2:08.0 | pedestrian | no overlap | exact |
| pickup-car | 2 | 2:07.0-2:10.0 | pedestrian | no overlap | exact |
| pickup-car | 3 | 1:06.0-1:08.0 | the driver of a white van | no overlap | exact |
| pickup-car | 3 | 2:23.0-2:25.0 | the driver of a white van | no overlap | exact |
| pickup-car | 3 | 2:53.0-2:55.0 | the driver of a silver car | no overlap | exact |
| pickup-car | 4 | 2:05.0-2:09.0 | person | no overlap | exact |
| pickup-car | 5 | — | absent | MISS |  |
| bus-dwell | 1 | 1:30.0-1:46.0 | articulated bus | no overlap | exact |
| bus-dwell | 2 | — | absent | MISS |  |
| bus-dwell | 3 | — | absent | MISS |  |
| bus-dwell | 4 | — | absent | MISS |  |
| bus-dwell | 5 | — | absent | MISS |  |
| ped-midblock | 1 | 2:04.0-2:11.0 | pedestrian | 0.28 below | exact |
| ped-midblock | 2 | 0:09.0-0:13.0 | construction worker | no overlap | exact |
| ped-midblock | 2 | 0:17.0-0:21.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 0:24.0-0:28.0 | construction worker | no overlap | exact |
| ped-midblock | 2 | 0:44.0-0:47.0 | pedestrian | 0.18 below | exact |
| ped-midblock | 2 | 0:50.0-0:53.0 | two pedestrians | no overlap | exact |
| ped-midblock | 2 | 0:53.0-0:56.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 1:01.0-1:06.0 | pedestrian | 0.50 | exact |
| ped-midblock | 2 | 1:13.0-1:16.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 1:18.0-1:21.0 | pedestrian | 0.43 below | exact |
| ped-midblock | 2 | 1:26.0-1:29.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 1:40.0-1:44.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 1:49.0-1:51.0 | pedestrian | 0.20 below | exact |
| ped-midblock | 2 | 1:54.0-1:56.0 | pedestrian | 0.11 below | exact |
| ped-midblock | 2 | 2:03.0-2:07.0 | pedestrian | 0.44 below | exact |
| ped-midblock | 2 | 2:13.0-2:16.0 | pedestrian | 0.12 below | exact |
| ped-midblock | 2 | 2:18.0-2:21.0 | pedestrian | 0.23 below | exact |
| ped-midblock | 2 | 2:31.0-2:34.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 2:37.0-2:40.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 2:41.0-2:48.0 | pedestrian | no overlap | exact |
| ped-midblock | 3 | 1:58.0-2:04.0 | a pedestrian in a white t-shirt an | 0.67 | exact |
| ped-midblock | 4 | 0:18.0-0:22.0 | pedestrian | no overlap | exact |
| ped-midblock | 4 | 0:33.0-0:36.0 | pedestrian | no overlap | exact |
| ped-midblock | 4 | 1:02.0-1:05.0 | pedestrian | 0.30 below | exact |
| ped-midblock | 4 | 1:10.0-1:14.0 | pedestrian | no overlap | exact |
| ped-midblock | 4 | 1:24.0-1:27.0 | pedestrian | no overlap | exact |
| ped-midblock | 4 | 1:52.0-1:56.0 | pedestrian | 0.09 below | exact |
| ped-midblock | 4 | 2:03.0-2:06.0 | pedestrian | 0.33 below | exact |
| ped-midblock | 4 | 2:08.0-2:12.0 | pedestrian | 0.16 below | exact |
| ped-midblock | 4 | 2:18.0-2:22.0 | pedestrian | 0.34 below | exact |
| ped-midblock | 5 | 0:11.0-0:17.0 | a pedestrian | no overlap | exact |
| ped-midblock | 5 | 2:01.0-2:07.0 | a pedestrian | 0.66 | exact |
| skateboard | 1 | 2:49.0-2:55.0 | person | no overlap | exact |
| skateboard | 2 | 0:45.0-0:48.0 | skateboarder | no overlap | exact |
| skateboard | 2 | 2:33.0-2:36.0 | skateboarder | no overlap | exact |
| skateboard | 3 | 2:10.0-2:19.0 | a person on a skateboard | no overlap | exact |
| skateboard | 4 | 0:53.0-0:58.0 | person | no overlap | exact |
| skateboard | 5 | 2:41.0-2:49.0 | a person | no overlap | exact |
| roadworks | 1 | 0:00.0-3:00.0 | construction site | 1.00 | exact |
| roadworks | 2 | 0:00.0-3:00.0 | construction zone | 1.00 | exact |
| roadworks | 3 | 0:00.0-3:00.0 | the intersection and roadway | 1.00 | exact |
| roadworks | 4 | 0:00.0-3:00.0 | construction zone | 1.00 | exact |
| roadworks | 5 | 0:00.0-3:00.0 | the roadway | 1.00 | exact |
| emergency | 1 | 0:31.0-0:34.0 | police SUV | FABRICATED | exact |
| emergency | 2 | 0:30.0-0:35.0 | police car | FABRICATED | exact |
| emergency | 3 | — | absent | correct |  |
| emergency | 4 | 0:31.0-0:35.0 | police SUV | FABRICATED | exact |
| emergency | 5 | — | absent | correct |  |
| emergency-dark | 1 | 0:09.0-0:15.0 | police car | no overlap | exact |
| emergency-dark | 2 | — | absent | MISS |  |
| emergency-dark | 3 | 0:31.0-0:34.0 | a police car | 0.51 | exact |
| emergency-dark | 4 | 0:25.0-0:29.0 | police car | no overlap | exact |
| emergency-dark | 5 | 0:32.0-0:36.0 | a police car | 0.74 | exact |
| emergency-dark | 5 | 1:18.0-1:25.0 | an ambulance | no overlap | exact |
| negative | 1 | — | absent | correct |  |
| negative | 2 | — | absent | correct |  |
| negative | 3 | — | absent | correct |  |
| negative | 4 | — | absent | correct |  |
| negative | 5 | — | absent | correct |  |
| negative | 1 | — | absent | correct |  |
| negative | 2 | — | absent | correct |  |
| negative | 3 | — | absent | correct |  |
| negative | 4 | — | absent | correct |  |
| negative | 5 | — | absent | correct |  |

### with-scene

| category | s | interval | subject | IoU | quality |
|---|---|---|---|---|---|
| turn-halt | 1 | 0:58.0-1:01.0 | dark grey SUV | no overlap | exact |
| turn-halt | 1 | 1:26.0-1:28.0 | black SUV | no overlap | exact |
| turn-halt | 2 | 0:55.0-0:56.0 | black SUV | no overlap | exact |
| turn-halt | 2 | 1:14.0-1:15.0 | dark SUV | no overlap | exact |
| turn-halt | 2 | 1:32.0-1:37.0 | articulated bus | 0.15 below | exact |
| turn-halt | 2 | 2:16.0-2:22.0 | black SUV | no overlap | exact |
| turn-halt | 3 | 0:06.0-0:08.0 | red car | 0.24 below | exact |
| turn-halt | 3 | 0:56.0-0:59.0 | grey car | no overlap | exact |
| turn-halt | 4 | 1:31.0-1:34.0 | blue articulated bus | no overlap | exact |
| turn-halt | 5 | 0:35.0-0:36.0 | dark car | no overlap | exact |
| turn-halt | 5 | 0:43.0-0:44.0 | white SUV | no overlap | exact |
| turn-halt | 5 | 1:33.0-1:37.0 | articulated bus | 0.16 below | exact |
| turn-halt | 5 | 1:51.0-1:52.0 | silver car | 0.02 below | exact |
| turn-halt | 5 | 2:19.0-2:20.0 | silver SUV | no overlap | exact |
| pickup-car | 1 | — | absent | MISS |  |
| pickup-car | 2 | 2:52.0-2:56.0 | pedestrian | no overlap | exact |
| pickup-car | 3 | 2:04.0-2:07.0 | driver | no overlap | exact |
| pickup-car | 3 | 2:24.0-2:27.0 | person | no overlap | exact |
| pickup-car | 4 | 0:28.0-0:32.0 | driver of a black SUV | 0.14 below | exact |
| pickup-car | 5 | — | absent | MISS |  |
| bus-dwell | 1 | — | absent | MISS |  |
| bus-dwell | 2 | — | absent | MISS |  |
| bus-dwell | 3 | — | absent | MISS |  |
| bus-dwell | 4 | — | absent | MISS |  |
| bus-dwell | 5 | 0:00.0-0:15.0 | bus | no overlap | exact |
| ped-midblock | 1 | 0:18.0-0:25.0 | pedestrian | no overlap | exact |
| ped-midblock | 1 | 1:49.0-1:56.0 | skateboarder | 0.30 below | exact |
| ped-midblock | 1 | 2:09.0-2:15.0 | skateboarder | 0.24 below | exact |
| ped-midblock | 1 | 2:39.0-2:44.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 0:10.0-0:14.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 0:15.0-0:19.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 0:18.0-0:22.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 0:33.0-0:37.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 1:23.0-1:27.0 | pedestrian | 0.10 below | exact |
| ped-midblock | 2 | 1:30.0-1:34.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 2:02.0-2:06.0 | pedestrian | 0.44 below | exact |
| ped-midblock | 2 | 2:09.0-2:13.0 | pedestrian | 0.16 below | exact |
| ped-midblock | 2 | 2:22.0-2:26.0 | pedestrian | 0.50 | exact |
| ped-midblock | 2 | 2:35.0-2:39.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 2:44.0-2:48.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 2:48.0-2:52.0 | pedestrian | no overlap | exact |
| ped-midblock | 3 | 0:21.0-0:27.0 | pedestrian | no overlap | exact |
| ped-midblock | 3 | 1:46.0-1:51.0 | pedestrian | 0.50 | exact |
| ped-midblock | 3 | 1:54.0-2:00.0 | pedestrian | 0.56 | exact |
| ped-midblock | 3 | 2:03.0-2:08.0 | pedestrian | 0.40 below | exact |
| ped-midblock | 3 | 2:31.0-2:37.0 | two pedestrians | no overlap | exact |
| ped-midblock | 3 | 2:44.0-2:48.0 | pedestrian | no overlap | exact |
| ped-midblock | 4 | 0:11.0-0:22.0 | pedestrian in light clothing | no overlap | exact |
| ped-midblock | 4 | 1:56.0-2:06.0 | pedestrian in dark clothing | 0.73 | exact |
| ped-midblock | 4 | 2:15.0-2:24.0 | pedestrian in a light top | 0.42 below | exact |
| ped-midblock | 4 | 2:42.0-2:52.0 | pedestrian in dark clothing | no overlap | exact |
| ped-midblock | 5 | 0:05.0-0:12.0 | pedestrian | no overlap | exact |
| ped-midblock | 5 | 0:15.0-0:25.0 | pedestrian in blue shirt | no overlap | exact |
| ped-midblock | 5 | 0:35.0-0:42.0 | pedestrian | no overlap | exact |
| ped-midblock | 5 | 0:48.0-0:56.0 | pedestrian in white | 0.47 below | exact |
| ped-midblock | 5 | 0:58.0-1:05.0 | pedestrian | 0.42 below | exact |
| ped-midblock | 5 | 1:48.0-1:56.0 | pedestrian | 0.38 below | exact |
| ped-midblock | 5 | 2:00.0-2:08.0 | pedestrian | 0.69 | exact |
| ped-midblock | 5 | 2:11.0-2:19.0 | pedestrian | 0.32 below | exact |
| ped-midblock | 5 | 2:42.0-2:51.0 | pedestrian | no overlap | exact |
| ped-midblock | 5 | 2:52.0-3:00.0 | pedestrian carrying a bag | no overlap | exact |
| skateboard | 1 | 1:49.0-1:56.0 | skateboarder | 0.37 below | exact |
| skateboard | 1 | 2:09.0-2:15.0 | skateboarder | no overlap | exact |
| skateboard | 2 | 1:51.0-1:58.0 | skateboarder | 0.67 | exact |
| skateboard | 3 | 1:39.0-1:58.0 | person on a skateboard | 0.29 below | exact |
| skateboard | 4 | 2:12.0-2:21.0 | person on a skateboard | no overlap | exact |
| skateboard | 5 | — | absent | MISS |  |
| roadworks | 1 | 0:00.0-3:00.0 | road construction | 1.00 | exact |
| roadworks | 2 | 0:00.0-3:00.0 | intersection construction | 1.00 | exact |
| roadworks | 3 | 0:00.0-3:00.0 | intersection construction zone | 1.00 | exact |
| roadworks | 4 | 0:00.0-3:00.0 | intersection construction zone | 1.00 | exact |
| roadworks | 5 | 0:00.0-3:00.0 | roadway intersection | 1.00 | exact |
| emergency | 1 | 0:32.0-0:35.0 | police car | FABRICATED | exact |
| emergency | 2 | 0:31.0-0:35.0 | police SUV | FABRICATED | exact |
| emergency | 3 | 0:30.0-0:34.0 | police SUV | FABRICATED | exact |
| emergency | 4 | 0:29.0-0:35.0 | NYPD police SUV | FABRICATED | exact |
| emergency | 5 | 0:30.0-0:34.0 | police car | FABRICATED | exact |
| emergency-dark | 1 | — | absent | MISS |  |
| emergency-dark | 2 | — | absent | MISS |  |
| emergency-dark | 3 | 2:18.0-2:22.0 | ambulance | no overlap | exact |
| emergency-dark | 4 | — | absent | MISS |  |
| emergency-dark | 5 | — | absent | MISS |  |
| negative | 1 | — | absent | correct |  |
| negative | 2 | — | absent | correct |  |
| negative | 3 | — | absent | correct |  |
| negative | 4 | — | absent | correct |  |
| negative | 5 | — | absent | correct |  |
| negative | 1 | — | absent | correct |  |
| negative | 2 | — | absent | correct |  |
| negative | 3 | — | absent | correct |  |
| negative | 4 | — | absent | correct |  |
| negative | 5 | — | absent | correct |  |

## Reading it

n=5 per arm over 10 categories. A difference of a few decisions between arms is inside the run-to-run variance this probe has already been shown to have, so the per-answer rows are more informative than the totals.

IoU is capped from both ends: the sheet's boundaries were judged by eye to about a second, and the model can only place an edge on a sampled frame. On a 6 s event that puts a correct answer near 0.8, not 1.0.

## Reproduce

```bash
./experiment_scene.sh
```
