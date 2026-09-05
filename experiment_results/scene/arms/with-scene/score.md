run    with-scene
truth  ground-truth-2026-08-25-17_00_01.txt
model  gemini-3.1-pro-preview   fps 1.0   5 samples/query   scene yes

category         truth samples presence  localised   mean IoU   best   FP   FN
------------------------------------------------------------------------------
turn-halt        yes   YYYYY   5/5            0/14       0.14   0.24   10   21
pickup-car       yes   nYYYn   3/5             0/4       0.14   0.14    3    4
bus-dwell        yes   nnnnY   1/5             0/1 no overlap   0.00    1    5
ped-midblock     yes   YYYYY   5/5            5/36       0.42   0.73   20   24
skateboard       yes   YYYYn   4/5             1/5       0.44   0.67    2    2
roadworks        yes   YYYYY   5/5             5/5       1.00   1.00    0    0
emergency        no    YYYYY   0/5               —          —      —    —    —
emergency-dark   yes   nnYnn   1/5             0/1 no overlap   0.00    1    5
negative         no    nnnnn   5/5               —          —      —    —    —
negative         no    nnnnn   5/5               —          —      —    —    —

presence   34/50 (68%)   -- was the yes/no right, per sample
localised  11/66 (17%)   -- of the intervals returned, how many land on a real one at IoU >= 0.5

These come apart, and the gap is the point: a category can score full marks on presence
while every interval it returned points at the wrong moment.

How far IoU can be read here is capped from both ends -- the sheet's boundaries were
judged by eye to about a second, and the model can only place an edge on a sampled
frame. On a 6 s event that puts a correct answer near 0.8, not 1.0. Unmatched
predictions are not necessarily wrong either: the sheet lists the spans a person
found, not every span that exists.
