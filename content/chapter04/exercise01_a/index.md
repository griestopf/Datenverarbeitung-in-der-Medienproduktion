---
title: Übung 4 - Meshgenerierung
---

**Basics der Meshgenerierung und -manipulation**

- BMesh
- Vertices bewegen
- Anwendung? Funktion plotten, Terrain / Fraktal generieren?

## Meshmanipulation Codebeispiel

- [BMesh](https://docs.blender.org/api/current/bmesh.html) Einführung

```python
# This example assumes we have a mesh object selected

import bpy
import bmesh

# Get the active mesh
me = bpy.context.object.data

# Get a BMesh representation
bm = bmesh.new()   # create an empty BMesh
bm.from_mesh(me)   # fill it in from a Mesh

# Modify the BMesh, can do anything here...
for v in bm.verts:
    v.co.x += 1.0

# Finish up, write the bmesh back to the mesh
bm.to_mesh(me)
bm.free()  # free and prevent further access

me.update()
```

## Ressourcen & Tutorials
- [How to Make Meshes with Python in Blender!](https://youtu.be/mljWBuj0Gho)
- [create meshes from low-level data | Diego Gangl](http://sinestesia.co/blog/tutorials/python-2d-grid/)
- [Shaping models with BMesh | jeremy Beherandt](https://medium.com/@behreajj/shaping-models-with-bmesh-in-blender-2-9-2f4fcc889bf0)

