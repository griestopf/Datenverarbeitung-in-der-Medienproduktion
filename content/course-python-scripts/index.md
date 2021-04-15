---
title: Python Skripte aus der Vorlesung
---

## VL4 Meshgenerierung - Graßbüschel

**Code-Zwischenstand aus der Vorlesung am 14.04.21**

```python
import bpy
import bmesh
import math
import mathutils
import random

BLADES = 8

WIDTH_MAX = 0.6
WIDTH_MIN = 0.03

HEIGHT_MIN = 4
HEIGHT_MAX = 12

ROT_BASE_MIN = 3
ROT_BASE_MAX = 25
ROT_TIP_MIN = 30
ROT_TIP_MAX = 90
ROT_FALLOFF = 5

# Szene leeren
bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

# Mesh und Objekt erstellen
grass_mesh = bpy.data.meshes.new("grass_shrub_mesh")
grass_object = bpy.data.objects.new("grass shrub", grass_mesh)

# Mesh in aktuelle Collection der Szene verlinken
bpy.context.collection.objects.link(grass_object)

# 
bm = bmesh.new()
bm.from_mesh(grass_mesh)

def map_range(v, from_min, from_max, to_min, to_max):
    """Bringt einen Wert v von einer Skala (from_min, from_max) auf eine neue Skala (to_min, to_max)"""
    return to_min + (v - from_min) * (to_max - to_min) / (from_max - from_min)

for i in range(BLADES):

    # Zufällige Werte für jedes Blatt generieren
    c_height = random.randrange(HEIGHT_MIN, HEIGHT_MAX)
    c_blade = []

    c_rot_base = random.uniform(ROT_BASE_MIN, ROT_BASE_MAX)
    c_rot_tip = random.uniform(ROT_TIP_MIN, ROT_TIP_MAX)

    last_vert_1 = None
    last_vert_2 = None

    for i in range(c_height):
        progress = i / c_height

        v = math.pow(progress, 0.8)

        pos_x = map_range(v, 0, 1, WIDTH_MAX, WIDTH_MIN)
        
        vert_1 = bm.verts.new((-pos_x,0,i))
        vert_2 = bm.verts.new((pos_x,0,i))

        # Halm immer weiter biegen desto weiter oben wir uns im Mesh/Loop befinden
        rot_angle = map_range(math.pow(progress, ROT_FALLOFF), 0, 1, c_rot_base, c_rot_tip)
        rot_matrix = mathutils.Matrix.Rotation(math.radians(rot_angle), 4, 'X')
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rot_matrix, verts=[vert_1, vert_2])
        
        # Generierung des Polygons in erster Stufe überspringen (weil bisher nur 2 Verices bestehen)
        if i is not 0:
            bm.faces.new((last_vert_1,last_vert_2,vert_2,vert_1))
            
        # Vertices der Vertices-Liste des aktuellen Halms hinzufügen
        c_blade.append(vert_1)
        c_blade.append(vert_2)

        # Letzte Vertices speichern, um sie für die generierung des nächsten Polygons zu verwenden
        last_vert_1 = vert_1
        last_vert_2 = vert_2

    # Jeden Halm zufällig auf Z Achse rotieren
    random_angle = random.randrange(0, 360)
    rot_matrix_blade = mathutils.Matrix.Rotation(math.radians(random_angle), 4, 'Z')

    # Dabei jeden Vertex des aktuellen Halms rotieren
    for v in c_blade:
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rot_matrix_blade, verts=[v])

# BMesh auf Mesh anwenden und abschließen
bm.to_mesh(grass_mesh)
bm.free()
```

## VL2 Turmgenerator

**Code-Zwischenstand aus der Vorlesung am 23.03.21**

```python
import bpy
import typing
import math

class tower():
    tower_radius: float = 3
    tower_height: float = 8
    roof_height: float = 2.5
    roof_overhang: float = 0.5

    windows_num_circular: int = 5
    windows_num_vertical: int = 3
    windows_size: float = 1
    wall_thickness: float = 0.5

    PI2 = math.pi * 2

    def generate_windows(self) -> object:


        windows = []

        for i in range(self.windows_num_circular):
            bpy.ops.mesh.primitive_cube_add(
                scale=(self.windows_size, self.windows_size, self.windows_size * 1.5)
            )
        
            c_window = bpy.context.object

            c_window.location = (
                (math.cos(i / self.windows_num_circular * self.PI2) * self.tower_radius),
                (math.sin(i / self.windows_num_circular * self.PI2) * self.tower_radius),
                1
            )

            if i > 0:
                c_window.rotation_euler.z = self.PI2 * i / self.windows_num_circular

            windows.append(c_window)

        for c_window in windows:
            c_window.select_set(True)

        bpy.ops.object.join()

        window = bpy.context.object
        modifier_array = window.modifiers.new("Window Array", "ARRAY")
        modifier_array.use_relative_offset = False
        modifier_array.use_constant_offset = True
        modifier_array.count = self.windows_num_vertical
        
        modifier_array.constant_offset_displace = (0, 0, 2.5)

        bpy.context.object.display_type = 'WIRE'
        
        return bpy.context.object


    def create_roof_material(self) -> bpy.types.Material:
        mat_roof: bpy.types.Material = bpy.data.materials.new("Roof Material")
        mat_roof.use_nodes = True
        nodes_roof: typing.List[bpy.types.Node] = mat_roof.node_tree.nodes
        nodes_roof["Principled BSDF"].inputs[0].default_value = [0.103312, 0.236954, 0.177671, 1.000000]

        return mat_roof

    def create_tower_material(self) -> bpy.types.Material:
        mat_tower: bpy.types.Material = bpy.data.materials.new("Tower Material")

        mat_tower.use_nodes = True

        nodes_tower: typing.List[bpy.types.Node] = mat_tower.node_tree.nodes
        node_bricks: bpy.types.Node = nodes_tower.new("ShaderNodeTexBrick")
        node_coords: bpy.types.Node = nodes_tower.new("ShaderNodeTexCoord")

        node_bricks.inputs[1].default_value = (0.1,0.1,0.1,0.1)
        node_bricks.inputs[4].default_value = 10
        
        mat_tower.node_tree.links.new(node_bricks.outputs[0], nodes_tower["Principled BSDF"].inputs[0])
        mat_tower.node_tree.links.new(node_coords.outputs[2], node_bricks.inputs[0])
        
        return mat_tower

    def generate_tower(self):
        bpy.ops.mesh.primitive_cylinder_add(
            location=(0, 0, self.tower_height / 2), 
            depth=self.tower_height, 
            radius=self.tower_radius)
        
        tower_base = bpy.context.object
        
        

        bpy.context.object.data.materials.append(self.create_tower_material())

        bpy.ops.mesh.primitive_cone_add(
            depth=self.roof_height,
            location=(0, 0, self.tower_height + self.roof_height / 2),
            radius1=self.tower_radius + self.roof_overhang
            )

        bpy.context.object.data.materials.append(self.create_roof_material())

        windows = self.generate_windows()

        modifier_solidify = tower_base.modifiers.new("Wall Thickness", "SOLIDIFY")
        modifier_solidify.thickness = self.wall_thickness
        
        modifier_bool = tower_base.modifiers.new("Window Bool", "BOOLEAN")
        modifier_bool.object = windows


bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

t = tower()
t.generate_tower()


```