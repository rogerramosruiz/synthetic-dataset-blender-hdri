import bpy
from camera import project_cam, change_focal_length

def adjust_ground():
    # Adjust the panel for the ground
    ground = bpy.context.scene.objects['Ground']
    coords = project_cam()
    sw = False
    for i in coords:
        if abs(i[0]) >= 100 or abs(i[1]) >= 100 or abs(i[2]) >= 100:
            sw = True
            break
    if len(coords) < 4 or sw:
        change_focal_length(50)
        coords = project_cam()

    for i in range(len(coords)):
        ground.data.vertices[i].co = coords[i]
