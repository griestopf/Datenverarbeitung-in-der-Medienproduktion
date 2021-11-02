---
title: Python Skripte aus der Vorlesung
---

# WiSe21/22

## VL4 - Mesh Generierung

**Code-Zwischenstand aus der Vorlesung vom 26.10.21**
```python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "MyTestAddon",
    "author" : "Simon",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy
import bmesh
import random
import mathutils
import math

def map_range(v, from_min, from_max, to_min, to_max):
    """Bringt einen Wert v von einer Skala (from_min, from_max) auf eine neue Skala (to_min, to_max)"""
    return to_min + (v - from_min) * (to_max - to_min) / (from_max - from_min)

class OT_Mesh_Grassshrub(bpy.types.Operator):
    bl_idname = "mesh.grass_generator"
    bl_label = "Generate Grass"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER", "UNDO"}

    HEIGHT_MIN: bpy.props.IntProperty(name="Min height", min=1, max=30, default=10)
    HEIGHT_MAX: bpy.props.IntProperty(name="Max height", min=1, max=30, default=10)

    TIP_WIDTH_MIN: bpy.props.FloatProperty(name="Tip Min Width", min=0.01, max=0.2, default=0.1)
    TIP_WIDTH_MAX: bpy.props.FloatProperty(name="Tip Max Width", min=0.01, max=0.2, default=0.1)

    BASE_WIDTH_MIN: bpy.props.FloatProperty(name="Base Min Width", min=0.01, max=1, default=0.5)
    BASE_WIDTH_MAX: bpy.props.FloatProperty(name="Base Max Width", min=0.01, max=1, default=0.5)

    BASE_ROT_MIN: bpy.props.IntProperty(name="Base Rot Min", min=1, max=90, default=5)
    BASE_ROT_MAX: bpy.props.IntProperty(name="Base Rot Max", min=1, max=90, default=20)

    TIP_ROT_MIN: bpy.props.IntProperty(name="Tip Rot Min", min=1, max=90, default=40)
    TIP_ROT_MAX: bpy.props.IntProperty(name="Tip Rot Max", min=1, max=90, default=60)

    ROT_FALLOFF: bpy.props.FloatProperty(name="Rotation Falloff", min=0.2, max=10, default=1)

    @classmethod
    def poll(cls, context):
        return True

    

    def execute(self, context):
        grass_mesh = bpy.data.meshes.new("grass mesh")
        grass_object = bpy.data.objects.new("grass object", grass_mesh)
        bpy.context.collection.objects.link(grass_object)

        bm = bmesh.new()
        bm.from_mesh(grass_mesh)

        height = random.randint(self.HEIGHT_MIN, self.HEIGHT_MAX)
        tip_width = random.uniform(self.TIP_WIDTH_MIN, self.TIP_WIDTH_MAX)
        base_width = random.uniform(self.BASE_WIDTH_MIN, self.BASE_WIDTH_MAX)

        last_vert_1 = None
        last_vert_2 = None

        rot_base = random.randint(self.BASE_ROT_MIN, self.BASE_ROT_MAX)
        rot_tip = random.randint(self.TIP_ROT_MIN, self.TIP_ROT_MAX)

        for i in range(height):
            progress = i / height
            pos_x = map_range(i, 0, height, base_width, tip_width)
            vert_1 = bm.verts.new((-pos_x, 0, i))
            vert_2 = bm.verts.new((pos_x, 0, i))

            rot_angle = map_range(math.pow(progress, self.ROT_FALLOFF), 0, 1, rot_base, rot_tip)

            rot_matrix = mathutils.Matrix.Rotation(math.radians(rot_angle), 4, "X")
            bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_matrix, verts=[vert_1, vert_2])

            if i != 0:
                bm.faces.new((last_vert_1, last_vert_2, vert_2, vert_1))
            
            last_vert_1 = vert_1
            last_vert_2 = vert_2
        
        bm.to_mesh(grass_mesh)
        bm.free()

        return {"FINISHED"}

register, unregister = bpy.utils.register_classes_factory({OT_Mesh_Grassshrub})

```

# SoSe21

## VL5 Animation - Springende Kugel

**Code-Zwischenstand aus der Vorlesung vom 20.04.21**

```python
import bpy
import math

points = bpy.data.collections["points"].objects
sphere: bpy.types.Object = bpy.data.objects["Sphere"]

JUMP_HEIGHT = 5
FRAMES_PER_UNIT = 1.5


def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


def set_handle_types():
    for c_curve in sphere.animation_data.action.fcurves:
        for i, c_keyframe in enumerate(c_curve.keyframe_points):
            if i % 2 == 0:
                c_keyframe.handle_left_type = "VECTOR"
                c_keyframe.handle_right_type = "VECTOR"
        c_curve.update()


sphere.location = points[0].location
sphere.keyframe_insert(data_path="location", frame=0)

at_keyframe = 0
for i in range(1, len(points)):

    distance_to_last_point = get_distance(points[i-1].location, points[i].location)
    keyframe_loc = at_keyframe + distance_to_last_point * FRAMES_PER_UNIT
    intermediate_keyframe_location = at_keyframe + (distance_to_last_point * FRAMES_PER_UNIT) / 2

    at_keyframe = keyframe_loc

    sphere.location = points[i].location
    sphere.keyframe_insert(data_path="location", frame=keyframe_loc)

    intermediate_point = points[i-1].location + points[i].location / 2
    intermediate_point.z += JUMP_HEIGHT

    sphere.location = intermediate_point
    sphere.keyframe_insert(data_path="location", frame=intermediate_keyframe_location)

    set_handle_types()

```


## VL4 Meshgenerierung - Graßbüschel

**Code-Zwischenstand aus der Vorlesung vom 14.04.21**

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
