run    fps2
truth  ground-truth-2026-08-25-17_00_01.txt
model  gemini-3.1-pro-preview   fps 2.0   5 samples/query   scene no

category         truth samples presence  localised   mean IoU   best   FP   FN
------------------------------------------------------------------------------
turn-halt        yes   YYYYn   4/5             1/4       0.32   0.50    2   23
pickup-car       yes   YYnYn   3/5             0/4 no overlap   0.00    4    5
bus-dwell        yes   nnnnn   0/5       no answer          —      —    —    5
ped-midblock     yes   YYYYY   5/5            0/14       0.32   0.45    8   34
skateboard       yes   YYnnn   2/5             0/2 no overlap   0.00    2    5
roadworks        yes   YYYYY   5/5             5/5       1.00   1.00    0    0
emergency        no    YnYYY   1/5               —          —      —    —    —
emergency-dark   yes   nYnnY   2/5             1/3       0.55   0.55    2    4
negative         no    nnnnn   5/5               —          —      —    —    —
negative         no    nnnnn   5/5               —          —      —    —    —

presence   32/50 (64%)   -- was the yes/no right, per sample
localised  7/32 (22%)   -- of the intervals returned, how many land on a real one at IoU >= 0.5

These come apart, and the gap is the point: a category can score full marks on presence
while every interval it returned points at the wrong moment.

How far IoU can be read here is capped from both ends -- the sheet's boundaries were
judged by eye to about a second, and the model can only place an edge on a sampled
frame. On a 6 s event that puts a correct answer near 0.8, not 1.0. Unmatched
predictions are not necessarily wrong either: the sheet lists the spans a person
found, not every span that exists.
