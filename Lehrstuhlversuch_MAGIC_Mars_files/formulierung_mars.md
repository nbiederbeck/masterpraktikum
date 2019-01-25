Coach
=====

Gamma/Hadron - Separation
-------------------------
Die Hadronness eines Events wird vom Random Forest geschätzt
auf einen Wertebereich von 0 bis 1.
Dabei haben Gammas eine Hadronness um 0,
der Untergrund hat Werte im gesamten Bereich.
Die Hadronness wird später dazu verwendet,
Gammas und Protonen zu klassifizieren,
indem ein Schnitt in der Hadronness gemacht wird.
In einem optimalen Modell hätten
Gammas eine Hadronness 0 und Hadronen eine Hadronness 1,
sodass sie einfach getrennt werden können.

Random Forest
-------------
Ein Random Forest besteht aus vielen binären Entscheidungsbäumen.
Diese trennen einen hochdimensinalen Hyperraum in mehreren Schritten so,
dass die im letzten Schritt entstehenden Unterräume (genannt Blätter)
ausschließlich aus einer Klasse bestehen (Gamma oder Hadron).
Die Entscheidung für jede Trennung wird mittels Gini-Index bestimmt.
Ein Random Forest mittelt die Entscheidungen aller Entscheidungsbäume.

Energierekonstruktion
---------------------
Die Energie des Gammas ist beinahe proportional
zur Anzahl der Tscherenkowphotonen
und somit der Photoelektronen in der Kamera,
jedoch hängt die Menge an detektiertem Licht von weiteren Parametern,
wie unter anderem Winkel der Kamera und Lage des Schauers im Kamerabild, ab.

In MARS wird die Energie des Primärteilchens auf zwei Arten rekonstruiert.

Look-up Tables
..............
Für eine Look-up Table werden Monte Carlo Gammas
in ausgewählten Parametern gebinnt.
Diesen Bins wird eine mittlere Energie aller
zugehörigen Gammas zugewiesen.
Bei realen Events werden die Parameter mit der Tabelle verglichen
und so eine Energie geschätzt.
Es muss darauf geachtet werden,
dass die Bins möglichst homogen und mit ausreichend Statistik gefüllt sind.

Random Forest
.............
Außerdem wird eine Random Forest Regression (s.o.)
zur Bestimmung der Energie durchgeführt.
