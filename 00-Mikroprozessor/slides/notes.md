Notizen
=======

Motivation
----------
Wetterstation

- Programmieren einer Software-Hardware Interaktion
- Ziel: klarer Nutzen des Projektes im Alltag (auch für andere)
- Reproduzierbarkeit wichtig
- Verstehen des Wetters
    - Beeinflusst Freizeitgestaltung

Mikroprozessor

- Raspberry Pi, da vorhanden und günstig
- Interaktion mit Sensoren
- klein, also besser als Rechner im Garten

Python

- Schon erste Erfahrungen
- Gesamtes Projekt in einer Programmiersprache
- (Pseudo-)Code für andere leicht nachvollziehbar

Aufgabenbereiche
----------------

- Drei Teilbereiche, von denen die ersten beiden auf dem Mikroprozessor laufen
    - da nur für diese Bereiche der Mikroprozessor ein sinnvoller Einsatzbereich ist
    - alle Bereiche könnten wenn gefordert auf dem Mikroprozessor laufen

Datennahme 

- Lokale Datennahme distributiert über zwei Stationen
- Stationenanzahl einfach erweiterbar 
- alle 30 min Datennahme

Transfer

- Domänenspezifische (genau dafür wurde der Mikroprozessor gebaut) Anwendung des Mikroprozessors
- Beschränkung des Mikroprozessor auf elementare Aufgaben
- Datennahme impliziert Datentransfer
- Speicherung auf Rechner, um den Mikroprozessor ressourcenschonend (= günstig) zu betreiben
- Schaffung einer dafür notwendigen Architektur

Analyse

- Durchführung auf Rechner, da höhere Leistung
- Wofür nimmt man Daten auf, wenn man daraus nichts ableitet (wir sind Physiker)?
- Maschinelle Lernverfahren zur Bestimmung der aktuellen und zukünfitgen Wetterlage
    - zwei Bereiche: Wolkenklassifizierung $\subset$ Wettervorhersage
- Erkenntnisse über Sachzusammenhänge (da wir keine Meteorologen sind)
    - Physikalische Gesetze des Wetters (Temperatur [steigt] - Luftfeuchtigkeit [sinkt])


Datennahme
----------

Folie 1

- 2 günstige, kleine Sensoren
- Seriell: Mehrere (verschiedene) Sensoren am selben Datenpin (I2C Schnittstelle)
    - Byteweise Übertragungen
- Adafruit Bibliotheken
- im Programm: Tupel von Floats
- Umgang mit Sensor-Fehlern (neuer Versuch / ignorieren) + Warnung mit Hinweis (siehe Sensor 4)
- Logger übernimmt Datenprotokoll (Konkurrenz zum Praktikumsheft :) )
- SSH-Zugang um ortunabhängige Änderungen vorzunehmen

Folie 2

- am Bild die Verbindungsleitungen veranschaulichen
    - 3.3V (rot), Ground (schwarz), Datenleitung (grün, gelb, blau)
- Fritzing vorstellen
- dritter Sensor PiCamera
    - 15-poliges Flachbandkabel am CSI Port

Wolkenfotos
-----------

PiCamera

- Samsung 8MP Sensor
- Auflösung der Fotos an Datentransfer und Analyse optimiert
- Leider teuer (ab 25 EUR)
- PNG 
    - Größe: 44KB
    - 1GB = 23.000 Fotos
    - bei aktueller Rate: 470 Tage
    - Für Wolkentracking höhere Rate nötig

Motivation

- Klassifizierung der Wolkendecke
    - an sich
    - Parametergeneration für die Wettervorhersage
- Wolkentracking
    - Windrichtung 
    - Windstärke
    - weiterer Parameter

Datenvorbereitung

- Labeln der Fotos für maschinelles Lernen notwendig
- Telegram dafür einfach zu nutzen
    - Paket (beinahe) wiederverwendbar für andere Anwendungen

Live-Demo
---------

Noahs Wetterstation mitbringen!

- Wetter in Brackel zeigen
- Wetter in Sölde (also der aktuelle Raum) zeigen
- Ein Foto labeln
- Info: Twitter

Datentransfer
-------------

Folie 1

- Lokal auf Mikroprozessor aufgenommen werden
- Aussotieren schlechter Daten
- Wie bekommen wir die Daten dorthin wo wir sie weiterverarbeiten können
- In WLAN Reichweite 

Folie 2

- Genutzt werden 2 Kanäle
- SQL Daten für alle die man in Tabellen darstellen kann
- Bilder über ein Socket
- Bisher größte Fehlerquelle des Projekts
- Durch Upstream kein Zugriff auf Wetterstation nötig

Folie 3

- Empfang der Daten
- Speichern 
- Indizieren und sortieren
- Bereitstellung einer Datenbank

Folie 4

- Analyse auf der Datenbank
- Setzt die Bausteine zusammen 
- Labeln der Daten für die Analyse
- ! Wettereinsicht über Telegram !


Datenanalyse
------------

Folie 1

- Zwei Schritte in der Analyse
- Vorverarbeitung
- Neuronales Netz zum Klassifizieren

Folie 2

- Schnitte auf Farbkanälen, um Nicht-Himmel-Farben zu maskieren (schwarz) 
- Entfernt Grün- und Rottöne und somit Nicht-Himmel-Objekte
- Blau, Weiß, Grau bleibt erhalten $\rightarrow$ ausschließlich Himmel

Folie 3

- Klassifizierung in 9 Klassen (Cumulus, Cirrus, Stratus, etc.)
- Ungleiche Klassengrößen

Folie 4

- Training eines Neuronalen Netzes (Convolution - Bilderkennung)
- Training offenbar möglich!
- Bessere Klassifizierung von (visuell für Menschen) "eindeutigen"  Klassen
    - Beispiel: Altocumulus - Schäfchenwolken
- Trainingserfolg abhänging von der Datensatzgröße
    - Trainingsergebnisse werden mit der Zeit immer besser


Wettervorhersage
----------------

- Parameter $m$  erklären
- $y$ erläutern
- $y_i$ in $f$ sind zeitlich sortiert und äquidistant
- $f$ nichtlineare Abbildungen
- $y_{n+2}$ durch Einsetzen von $y_{n+1}$ in $f$

Website
-------

Website

- Zentrale Darstellung aller genannten Ergebnisse und Erkenntnisse für viele einfach einsehbar (= große Reichweite)
- Mikroprozessor füllt die Website mit Inhalt
- Kaufen der Station möglich

Anleitung

- Python Paket Sphinx
- Welche Teile (Einkaufsliste), wie zusammenstecken, Installation des Programms
- momentan auf Mikroprozessor gehostet
