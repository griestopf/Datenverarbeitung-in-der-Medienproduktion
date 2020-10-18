---
title: Übung 1 - Intro
---

## Blender Setup und Scripting-Tools

- Setup Blender für Scripting
- Blender Basics falls nötig
- Blender Tools:
	- Terminal
	- Echtzeit Konsole
	- Infopanel
	- Texteditor
	- Python Tooltips
- bpy
- copypasta stuff aus Echtzeitkonsole
	- Suzanne hinzufügen und platzieren

![turm](img/monkeygrid.png)

**In dieser Übung wollen wir uns mit dem Setup von Blender für Scripting, sowie den Tools, die uns von Blender selbst dafür zur Verfügung gestellt werden beschäftigen.**

## Blender Setup
- Ladet euch zunächst von [Blender.org](https://www.blender.org/download/) die aktuelle Version von Blender herunter. Dieses Script behandelt die Version 2.90. Zukünftige Versionen könnten eventuell Änderungen an der API vornehmen, normalerweise bleibt die API bei Updates jedoch großteils unverändert.

<!--Link zu CG Webseite? Ist ja nicht immer alles Online und vlt auch nicht immer auf Davids Webspace?-->
> Eine Einführung in Blender selbst, sowie Links mit Tutorials etc. gibt es im [**Script zur Veranstalltung Computergrafik**](https://sftp.hs-furtwangen.de/~lochmann/computergrafik2019/script/chapter01/lecture01/) 

- Öffnet Blender und in Blender die ***Preferences***
![Preferences](img/preferences.png)
- Aktiviert hier nun im ***Interface*** Tab *Python Tooltips* und *Development Extras*

> **Python Tooltips** zeigt beim Hovern mit dem Cursor über einen Wert dessen Pfad in der Blender API an.<br>
> ![Python Tooltip](img/python_tooltip.png)
> 
> **Development Extras** Ermöglicht einige Funktionen, die uns das Scripten erleichter, wie z.b. das Anzeigen des Python-Codes von Features (`RMB` → *Edit Source*)<br>
> ![Edit Source](img/edit_source.png)

## Scripting Tools

- Wechselt nun zum Workspace-Tab ***Scripting***

![Scripting Workspace](img/scripting_workspace.png)
- Der **<span style="color: ForestGreen">3D View</span>** stellt die aktuelle Szene in 3D dar.
- Die **<span style="color: DarkGoldenRod">Python Konsole</span>** ermöglicht es live Python-Befehle mit Autovervollständigung (`TAB`)auszuführen
- Das **<span style="color: Blue">Info Fenster</span>** gibt den Code von in Blender ausgeführten Aktionen aus
- Im **<span style="color: Red">Text Editor</span>** wird der Code für unsere Scripte geschrieben
- Die beiden **<span style="color: DarkOrange">Outliner Fenster</span>** zeigen oben die aktuelle Szenen-Hierarchie und unten alle Daten des geöffneten Blender Files
- Der **<span style="color: Magenta">Properties Editor</span>** ermöglicht die Bearbeitung von Werten des aktuellen Objekts, sowie Einstellungen der Szene.

## Live Scripting
Todo

## Affentheater
Todo

```python
import bpy

GRID_SCALE = 5
GRID_SIZE = 5

for i in range(0, GRID_SIZE):
    for j in range(0, GRID_SIZE):
        bpy.ops.mesh.primitive_monkey_add(location=(GRID_SCALE * j ,GRID_SCALE * i, 0))

        bpy.ops.transform.rotate(value=0.575267, orient_axis='Z', orient_type='VIEW', orient_matrix=((4.93038e-32, 1, 2.22045e-16), (2.22045e-16, 4.93038e-32, 1), (1, 2.22045e-16, 4.93038e-32)), orient_matrix_type='VIEW')

        bpy.ops.transform.translate(value=(0, 0, 0.608087), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')

        # bpy.ops.object.modifier_add(type='SUBSURF')
        # bpy.context.object.modifiers["Subdivision"].levels = 1
        bpy.ops.object.shade_smooth()

```

## Aufgabe bis zum nächsten Mal
- Schreibt ein Script, welches eine Horde (5 oder mehr) von Affen in der Szene platziert und im Kreis anordnet
- Optional: Lasst die Affenköpfe alle in die Mitte der Szene gucken.
> **Tipps** 
> - Die Formel für die Position eines Punktes im Einheitskreis ist<br>
> ![img](img/einheitskreis.png)<br>
> - **t** ist dabei der Winkel in Radianten. 360° entspricht 2Pi
> - Zur Nutzung von Sinus & Cosinus muss das math Modul importiert werden 
> ```python
>  import math
> ```