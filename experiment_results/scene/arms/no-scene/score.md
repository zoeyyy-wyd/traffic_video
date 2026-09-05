run    no-scene
truth  ground-truth-2026-08-25-17_00_01.txt
model  gemini-3.1-pro-preview   fps 1.0   5 samples/query   scene no

category         truth samples presence  localised   mean IoU   best   FP   FN
------------------------------------------------------------------------------
turn-halt        yes   YYYYY   5/5            1/13       0.29   0.54   10   22
pickup-car       yes   YYYYn   4/5             0/6 no overlap   0.00    6    5
bus-dwell        yes   Ynnnn   1/5             0/1 no overlap   0.00    1    5
ped-midblock     yes   YYYYY   5/5            3/32       0.31   0.67   16   24
skateboard       yes   YYYYY   5/5             0/6 no overlap   0.00    6    5
roadworks        yes   YYYYY   5/5             5/5       1.00   1.00    0    0
emergency        no    YYnYn   2/5               —          —      —    —    —
emergency-dark   yes   YnYYY   4/5             2/5       0.62   0.74    3    3
negative         no    nnnnn   5/5               —          —      —    —    —
negative         no    nnnnn   5/5               —          —      —    —    —

presence   41/50 (82%)   -- was the yes/no right, per sample
localised  11/68 (16%)   -- of the intervals returned, how many land on a real one at IoU >= 0.5

These come apart, and the gap is the point: a category can score full marks on presence
while every interval it returned points at the wrong moment.

How far IoU can be read here is capped from both ends -- the sheet's boundaries were
judged by eye to about a second, and the model can only place an edge on a sampled
frame. On a 6 s event that puts a correct answer near 0.8, not 1.0. Unmatched
predictions are not necessarily wrong either: the sheet lists the spans a person
found, not every span that exists.
