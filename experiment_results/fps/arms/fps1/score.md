run    fps1
truth  ground-truth-2026-08-25-17_00_01.txt
model  gemini-3.1-pro-preview   fps 1.0   5 samples/query   scene no

category         truth samples presence  localised   mean IoU   best   FP   FN
------------------------------------------------------------------------------
turn-halt        yes   YYYYY   5/5             0/7       0.23   0.23    6   24
pickup-car       yes   YYYYY   5/5             0/8 no overlap   0.00    8    5
bus-dwell        yes   nnnYn   1/5             0/1 no overlap   0.00    1    5
ped-midblock     yes   YYYYY   5/5            7/29       0.38   0.89   11   22
skateboard       yes   YnYYY   4/5             1/4       0.60   0.60    3    4
roadworks        yes   YYYYY   5/5             5/5       1.00   1.00    0    0
emergency        no    YYYYY   0/5               —          —      —    —    —
emergency-dark   yes   nnnYn   1/5             0/1 no overlap   0.00    1    5
negative         no    nnnnn   5/5               —          —      —    —    —
negative         no    nnnnn   5/5               —          —      —    —    —

presence   36/50 (72%)   -- was the yes/no right, per sample
localised  13/55 (24%)   -- of the intervals returned, how many land on a real one at IoU >= 0.5

These come apart, and the gap is the point: a category can score full marks on presence
while every interval it returned points at the wrong moment.

How far IoU can be read here is capped from both ends -- the sheet's boundaries were
judged by eye to about a second, and the model can only place an edge on a sampled
frame. On a 6 s event that puts a correct answer near 0.8, not 1.0. Unmatched
predictions are not necessarily wrong either: the sheet lists the spans a person
found, not every span that exists.
