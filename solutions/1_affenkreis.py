import bpy
import math

MONKEY_NUMBER = 8
RADIUS = 4

for i in range(MONKEY_NUMBER):
    t =  2 * math.pi * i / MONKEY_NUMBER #2 * pi entspricht radians(360)
    pos_x = RADIUS * math.cos(t)
    pos_y = RADIUS * math.sin(t)
    bpy.ops.mesh.primitive_monkey_add(location=(pos_x, pos_y, 0))
    bpy.ops.object.shade_smooth()

    # Optional - in die Mitte gucken lassen
    rotation = math.radians(360) * (1-(i / MONKEY_NUMBER))  #mit 1-.... Rotationsrichtung umkehren
    rotation += math.radians(90) # nochmal um 90° rotieren, damit die Richtung stimmt
    
    bpy.ops.transform.rotate(value=rotation, orient_axis='Z')
