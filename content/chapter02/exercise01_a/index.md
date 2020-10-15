---
title: Übung 2 - Würfelturm
---

## Prozedurale Würfeltürmchen bauen

![turm](img/turm.png)

Türmchen:

- Genau gestapelte Würfel
- nach oben schmaler werden
- Würfel mit random Scale, Z-Rotation und Location-Offset

**Beispielcode Würfeltürmchen**
```python
import bpy
import random
from datetime import datetime

import mathutils

MAX_STACKS = 10
MIN_STACKS = 2
MAX_SCALE = 2.5
MIN_SCALE = 0.5

# clear scene - später entfernen
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


random.seed(datetime.now())

bpy.ops.mesh.primitive_cube_add()
C = bpy.context

src_obj = C.active_object

src_obj.rotation_euler.z = random.random() * 360

rand_scale = random.uniform(MIN_SCALE, MAX_SCALE)
src_obj.scale = mathutils.Vector((rand_scale,rand_scale,rand_scale))
src_obj.location.z = rand_scale

height = rand_scale * 2 # * 2 weil cube 2m groß ist. Später durch dimensions ersetzen.

previous_scale = rand_scale

for i in range (1, random.randint(MIN_STACKS, MAX_STACKS)):
    new_obj = src_obj.copy()
    new_obj.data = src_obj.data
    new_obj.rotation_euler.z = random.random() * 360
    
    rand_scale = random.uniform(MIN_SCALE, MAX_SCALE)  * (1 - i / MAX_STACKS)
    
    new_obj.scale = mathutils.Vector((rand_scale, rand_scale, rand_scale))
    
    height += rand_scale
    new_obj.location.z = height
    height += rand_scale
    
    previous_scale = rand_scale
    
    C.collection.objects.link(new_obj)

```