# SpringUndRenn
Dies ist der Beitrag des FRS Informatik zum Schüler Workshop.

# Installation
## 1. Klonen
 * Clone das Repository in ein Verzeichnis (zbs. <SuR>)
 * Erstelle im Verzeichnis in dem das Repo liegt eine vituelle Umgebung 
## 2. Laufzeitumgebung
	* Installiere Python 3
	* Führe in <SuR> den folgenden Befehl aus:
		+ python3 -m venv /path/to/new/virtual/environment
	* Aktiviere die virtuelle Umgebung:
		+ Windows(CMD): C:\> <venv>\Scripts\activate.bat
		+ Windows(PowerShell):  PS C:\> <venv>\Scripts\Activate.ps1
		+ POSIX (bsh/zh): $ source <venv>/bin/activate
	* Installiere pygame in virtuelle Umgebung: 
		+ pip install pygame
## 3. Das Spiel starten
	* Starte die virtuelle Umgebung
	* Wechsel in den Ordern SpringUndRenn/src/
	* Starte das Spiel:
		+ python game.py

# Erweitern
## 1. Spielobjekte
	* Erstelle eine neue Klasse in gameObject.py
		+ Sie muss mindestens von GameObject erben
	* Füge in der Klasse die ID und den Constructor (oder andere Funktion die das Object erstellt) in das Dictonary 
	* Eventuell noch die Funktion on_loop in game.py anpassen