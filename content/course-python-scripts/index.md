---
title: Python Skripte aus der Vorlesung
---

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