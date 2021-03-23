import bpy
import math
import typing

bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

pi2 = math.pi * 2


class tower():
    tower_radius: float = 3
    tower_height: float = 10
    roof_height: float = 5
    roof_overhang: float = 1
    windows_num_circular: int = 5
    windows_num_vertical: int = 4
    windows_size: float = 1
    wall_thickness = 0.5

    def generate_windows(self):
            
            # generate circular window layer and save each object in list
                
            windows = []

            height = self.tower_height / self.windows_num_vertical / 2
            
            for i in range(self.windows_num_circular):    
                bpy.ops.mesh.primitive_cube_add(scale = (self.windows_size,self.windows_size,self.windows_size * 1.5))
                window = bpy.context.object
                
                window.location = (
                    math.cos(i/self.windows_num_circular * pi2) * self.tower_radius,
                    math.sin(i/self.windows_num_circular  * pi2) * self.tower_radius,
                    height)
                
                if i > 0:
                    window.rotation_euler.z = pi2 * i / self.windows_num_circular
                windows.append(window)
                
            for c_window in windows:
                c_window.select_set(True)
            bpy.ops.object.join()
            
            # array mpdofier
            arr = window.modifiers.new('Arraymodifier','ARRAY')
            arr.count = self.windows_num_vertical
            arr.use_relative_offset = False
            arr.use_constant_offset = True
            arr.constant_offset_displace = (0, 0, self.tower_height / self.windows_num_vertical)

            window.display_type = 'WIRE'

            return window

    def create_material_base(self) -> bpy.types.Material:
        mat_tower: bpy.types.Material = bpy.data.materials.new("Tower Base")
        mat_tower.use_nodes = True
        nodes: typing.List[bpy.types.Nodes] = mat_tower.node_tree.nodes
        
        node_princ: bpy.types.Node = nodes["Principled BSDF"]
        node_brick: bpy.types.Node = nodes.new("ShaderNodeTexBrick")
        node_coords: bpy.types.Node = nodes.new("ShaderNodeTexCoord")

        node_brick.inputs[1].default_value = (0, 0, 0, 1)   # Farbe setzen
        node_brick.inputs[4].default_value = 10             # Size setzen

        mat_tower.node_tree.links.new(node_brick.outputs[0], node_princ.inputs[0])
        mat_tower.node_tree.links.new(node_coords.outputs[2], node_brick.inputs[0])

        return mat_tower

    def create_material_roof(self) -> bpy.types.Material:
        mat_roof: bpy.types.Material = bpy.data.materials.new("Tower Roof")
        mat_roof.use_nodes = True
        nodes: typing.List[bpy.types.Nodes] = mat_roof.node_tree.nodes
        
        node_princ: bpy.types.Node = nodes["Principled BSDF"]

        node_princ.inputs[0].default_value = (.01, 0.05, 0.03, 1)   # Farbe setzen

        return mat_roof


    def generate_tower(self):
        
        # Turm erzeugen
        bpy.ops.mesh.primitive_cylinder_add(
            location = (0, 0, self.tower_height/2), 
            depth = self.tower_height, 
            radius = self.tower_radius)

        tower_base = bpy.context.object

        # Shading
        bpy.ops.object.shade_smooth()
        tower_base.data.use_auto_smooth = True

        tower_base.data.materials.append(self.create_material_base())

        windows = self.generate_windows()

        # Wand Dicke geben mit Solidify Modifier
        mod_solid = tower_base.modifiers.new('Wall Thickness','SOLIDIFY')
        mod_solid.thickness = self.wall_thickness

        mod_bool = tower_base.modifiers.new('Windowboolean','BOOLEAN')
        mod_bool.object = windows


        # dach erzeugen
        bpy.ops.mesh.primitive_cone_add(
            depth = self.roof_height,
            location = (0, 0, self.tower_height + self.roof_height/2),
            radius1 = self.tower_radius + self.roof_overhang)

        bpy.context.object.data.materials.append(self.create_material_roof())
        
t = tower()
t.generate_tower()