# fps

## Configuration

- clip `L12thFloorBotwinik-D-2026-08-25_T-17_00_01.mp4`, 180s
- queries `queries/events-key.txt`, 10 categories
- model `gemini-3.1-pro-preview`, 5 samples per query, all queries in one call
- timestamps `interleave`
- ground truth `2026-08-25-17_00_01.txt`
- **varied across arms: fps**

| arm | fps | frames | tokens in |
|---|---|---|---|
| `fps1` | 1.0 | 181 | 1,005,990 |
| `fps2` | 2.0 | 361 | 2,003,540 |

## Result

`presence` is whether the yes/no was right, per sample. `localised` is how many returned intervals land on a real one at IoU >= 0.5. They come apart, and only the second one means anything for annotation.

| arm | presence | localised | mean IoU over matched pairs |
|---|---|---|---|
| `fps1` | 36/50 (72%) | 13/55 (24%) | 0.51 |
| `fps2` | 32/50 (64%) | 7/32 (22%) | 0.58 |

## Every answer

One row per interval the model returned, plus a row where it returned nothing. `IoU` is against the best unclaimed real span, matched one-to-one so a single wide interval cannot claim several. `below` means it overlapped but under the threshold; `no overlap` means it landed nowhere near.

### fps1

| category | s | interval | subject | IoU | quality |
|---|---|---|---|---|---|
| turn-halt | 1 | 2:58.0-3:00.0 | yellow taxi | no overlap | exact |
| turn-halt | 2 | 1:04.0-1:06.0 | black car | no overlap | exact |
| turn-halt | 3 | 1:33.0-1:38.0 | articulated bus | 0.23 below | exact |
| turn-halt | 3 | 1:46.0-1:48.0 | dark SUV | no overlap | exact |
| turn-halt | 3 | 1:50.0-1:51.0 | silver car | no overlap | exact |
| turn-halt | 4 | 2:14.0-2:17.0 | white box truck | no overlap | exact |
| turn-halt | 5 | 1:46.0-1:49.0 | dark SUV | no overlap | exact |
| pickup-car | 1 | 1:52.0-1:54.0 | driver of white van | no overlap | exact |
| pickup-car | 2 | 1:14.0-1:16.0 | person and white van | no overlap | exact |
| pickup-car | 2 | 2:04.0-2:08.0 | person and white van | no overlap | exact |
| pickup-car | 3 | 1:51.0-1:55.0 | person and white van | no overlap | exact |
| pickup-car | 4 | 1:50.0-1:53.0 | driver of the white SUV | no overlap | exact |
| pickup-car | 4 | 2:18.0-2:21.0 | driver of the black car | no overlap | exact |
| pickup-car | 4 | 2:57.0-2:59.0 | pedestrian | no overlap | exact |
| pickup-car | 5 | 1:07.0-1:11.0 | person | no overlap | exact |
| bus-dwell | 1 | — | absent | MISS |  |
| bus-dwell | 2 | — | absent | MISS |  |
| bus-dwell | 3 | — | absent | MISS |  |
| bus-dwell | 4 | 0:00.0-0:02.0 | white and blue city bus | no overlap | exact |
| bus-dwell | 5 | — | absent | MISS |  |
| ped-midblock | 1 | 0:15.0-0:18.0 | pedestrian | no overlap | exact |
| ped-midblock | 1 | 2:00.0-2:05.0 | pedestrian | 0.56 | exact |
| ped-midblock | 1 | 2:13.0-2:17.0 | pedestrian | 0.16 below | exact |
| ped-midblock | 1 | 2:43.0-2:47.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 0:09.0-0:17.0 | pedestrian | no overlap | exact |
| ped-midblock | 2 | 1:51.0-1:57.0 | pedestrian | 0.17 below | exact |
| ped-midblock | 2 | 2:09.0-2:15.0 | pedestrian | 0.24 below | exact |
| ped-midblock | 2 | 2:40.0-2:46.0 | pedestrian | no overlap | exact |
| ped-midblock | 3 | 0:11.0-0:21.0 | pedestrian in blue shirt | no overlap | exact |
| ped-midblock | 3 | 0:34.0-0:41.0 | pedestrian in grey shirt | no overlap | exact |
| ped-midblock | 3 | 0:52.0-0:59.0 | pedestrian in black shirt | 0.26 below | exact |
| ped-midblock | 3 | 1:02.0-1:07.0 | pedestrian in white shirt | 0.50 | exact |
| ped-midblock | 3 | 1:21.0-1:28.0 | pedestrian in grey shirt | 0.27 below | exact |
| ped-midblock | 3 | 2:00.0-2:05.0 | pedestrian in white shirt | 0.56 | exact |
| ped-midblock | 3 | 2:10.0-2:16.0 | pedestrian in dark shirt | 0.24 below | exact |
| ped-midblock | 3 | 2:18.0-2:24.0 | pedestrian in dark shirt | 0.56 | exact |
| ped-midblock | 3 | 2:33.0-2:39.0 | pedestrian in black shirt | no overlap | exact |
| ped-midblock | 3 | 2:46.0-2:51.0 | pedestrian in white shirt | no overlap | exact |
| ped-midblock | 4 | 2:01.0-2:07.0 | pedestrian | 0.66 | exact |
| ped-midblock | 4 | 2:40.0-2:45.0 | pedestrian | no overlap | exact |
| ped-midblock | 5 | 0:11.0-0:22.0 | pedestrian | no overlap | exact |
| ped-midblock | 5 | 0:34.0-0:45.0 | pedestrian | no overlap | exact |
| ped-midblock | 5 | 0:50.0-0:55.0 | pedestrian | 0.29 below | exact |
| ped-midblock | 5 | 1:01.0-1:07.0 | pedestrian | 0.60 | exact |
| ped-midblock | 5 | 1:13.0-1:19.0 | pedestrian | 0.19 below | exact |
| ped-midblock | 5 | 1:41.0-1:45.0 | pedestrian | 0.17 below | exact |
| ped-midblock | 5 | 1:58.0-2:06.0 | pedestrian | 0.89 | exact |
| ped-midblock | 5 | 2:00.0-2:06.0 | pedestrian | 0.27 below | exact |
| ped-midblock | 5 | 2:11.0-2:18.0 | pedestrian | 0.28 below | exact |
| skateboard | 1 | 2:01.0-2:14.0 | person on a skateboard | no overlap | exact |
| skateboard | 2 | — | absent | MISS |  |
| skateboard | 3 | 2:01.0-2:07.0 | skateboarder | no overlap | exact |
| skateboard | 4 | 1:50.0-1:58.0 | person riding a skateboard | 0.60 | exact |
| skateboard | 5 | 2:13.0-2:18.0 | person | no overlap | exact |
| roadworks | 1 | 0:00.0-3:00.0 | construction zone | 1.00 | exact |
| roadworks | 2 | 0:00.0-3:00.0 | construction zone | 1.00 | exact |
| roadworks | 3 | 0:00.0-3:00.0 | construction zone | 1.00 | exact |
| roadworks | 4 | 0:00.0-3:00.0 | roadway construction zone | 1.00 | exact |
| roadworks | 5 | 0:00.0-3:00.0 | construction area | 1.00 | exact |
| emergency | 1 | 0:30.0-0:35.0 | police car | FABRICATED | exact |
| emergency | 2 | 0:31.0-0:35.0 | police vehicle | FABRICATED | exact |
| emergency | 3 | 0:31.0-0:36.0 | police car | FABRICATED | exact |
| emergency | 4 | 0:31.0-0:34.0 | police car | FABRICATED | exact |
| emergency | 5 | 0:31.0-0:34.0 | police car | FABRICATED | exact |
| emergency-dark | 1 | — | absent | MISS |  |
| emergency-dark | 2 | — | absent | MISS |  |
| emergency-dark | 3 | — | absent | MISS |  |
| emergency-dark | 4 | 0:09.0-0:11.0 | police car | no overlap | exact |
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

### fps2

| category | s | interval | subject | IoU | quality |
|---|---|---|---|---|---|
| turn-halt | 1 | 1:28.0-1:34.0 | blue articulated bus | no overlap | exact |
| turn-halt | 2 | 1:32.0-1:37.0 | an articulated blue bus | 0.15 below | exact |
| turn-halt | 3 | 2:23.0-2:30.5 | dark SUV | no overlap | exact |
| turn-halt | 4 | 1:51.5-1:53.5 | a blue SUV | 0.50 | exact |
| turn-halt | 5 | — | absent | MISS |  |
| pickup-car | 1 | 2:06.0-2:08.0 | pedestrian | no overlap | exact |
| pickup-car | 2 | 0:10.5-0:12.5 | a person exiting a black SUV | no overlap | exact |
| pickup-car | 2 | 2:41.0-2:43.5 | a person entering a white car | no overlap | exact |
| pickup-car | 3 | — | absent | MISS |  |
| pickup-car | 4 | 1:58.0-2:01.5 | a person | no overlap | exact |
| pickup-car | 5 | — | absent | MISS |  |
| bus-dwell | 1 | — | absent | MISS |  |
| bus-dwell | 2 | — | absent | MISS |  |
| bus-dwell | 3 | — | absent | MISS |  |
| bus-dwell | 4 | — | absent | MISS |  |
| bus-dwell | 5 | — | absent | MISS |  |
| ped-midblock | 1 | 1:53.5-1:57.5 | pedestrian | 0.27 below | exact |
| ped-midblock | 2 | 0:11.0-0:16.0 | a pedestrian in a light blue shirt | no overlap | exact |
| ped-midblock | 2 | 0:34.0-0:38.0 | a pedestrian | no overlap | exact |
| ped-midblock | 2 | 0:59.5-1:03.5 | a pedestrian | 0.34 below | exact |
| ped-midblock | 2 | 1:24.0-1:28.0 | a pedestrian | no overlap | exact |
| ped-midblock | 2 | 1:48.5-1:53.0 | a pedestrian in dark clothing | 0.45 below | exact |
| ped-midblock | 2 | 2:10.0-2:15.0 | a pedestrian | 0.20 below | exact |
| ped-midblock | 2 | 2:22.5-2:25.5 | a pedestrian | 0.38 below | exact |
| ped-midblock | 2 | 2:42.5-2:45.5 | a pedestrian | no overlap | exact |
| ped-midblock | 2 | 2:54.5-2:57.5 | a pedestrian | no overlap | exact |
| ped-midblock | 3 | 0:10.5-0:16.0 | pedestrian | no overlap | exact |
| ped-midblock | 4 | 2:47.0-2:53.5 | a pedestrian | no overlap | exact |
| ped-midblock | 5 | 0:11.0-0:16.0 | a pedestrian | no overlap | exact |
| ped-midblock | 5 | 2:03.0-2:11.0 | a pedestrian | 0.32 below | exact |
| skateboard | 1 | 2:53.0-2:57.5 | skateboarder | no overlap | exact |
| skateboard | 2 | 2:48.0-2:54.0 | a person on a skateboard | no overlap | exact |
| skateboard | 3 | — | absent | MISS |  |
| skateboard | 4 | — | absent | MISS |  |
| skateboard | 5 | — | absent | MISS |  |
| roadworks | 1 | 0:00.0-3:00.0 | roadwork zone | 1.00 | exact |
| roadworks | 2 | 0:00.0-3:00.0 | a construction site in the roadway | 1.00 | exact |
| roadworks | 3 | 0:00.0-3:00.0 | construction area | 1.00 | exact |
| roadworks | 4 | 0:00.0-3:00.0 | the roadway | 1.00 | exact |
| roadworks | 5 | 0:00.0-3:00.0 | the intersection | 1.00 | exact |
| emergency | 1 | 0:31.0-0:34.0 | police SUV | FABRICATED | exact |
| emergency | 2 | — | absent | correct |  |
| emergency | 3 | 0:31.0-0:36.0 | police car | FABRICATED | exact |
| emergency | 4 | 0:31.5-0:34.5 | a police car | FABRICATED | exact |
| emergency | 5 | 0:28.5-0:35.0 | a police SUV | FABRICATED | exact |
| emergency-dark | 1 | — | absent | MISS |  |
| emergency-dark | 2 | 0:08.5-0:12.5 | a police car | no overlap | exact |
| emergency-dark | 2 | 0:30.5-0:36.0 | a police car | 0.55 | exact |
| emergency-dark | 3 | — | absent | MISS |  |
| emergency-dark | 4 | — | absent | MISS |  |
| emergency-dark | 5 | 0:10.0-0:14.0 | a police car | no overlap | exact |
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
./experiment_fps.sh
```
