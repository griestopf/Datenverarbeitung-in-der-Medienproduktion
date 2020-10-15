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

**Monkey Grid**
```python
import bpy

GRID_SCALE = 5
GRID_SIZE = 5

for i in range(0, 5):
    for j in range(0, GRID_SIZE):
        bpy.ops.mesh.primitive_monkey_add(location=(GRID_SCALE * j ,GRID_SCALE * i, 0))

        bpy.ops.transform.rotate(value=0.575267, orient_axis='Z', orient_type='VIEW', orient_matrix=((4.93038e-32, 1, 2.22045e-16), (2.22045e-16, 4.93038e-32, 1), (1, 2.22045e-16, 4.93038e-32)), orient_matrix_type='VIEW')

        bpy.ops.transform.translate(value=(0, 0, 0.608087), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')

        # bpy.ops.object.modifier_add(type='SUBSURF')
        # bpy.context.object.modifiers["Subdivision"].levels = 1
        bpy.ops.object.shade_smooth()

```