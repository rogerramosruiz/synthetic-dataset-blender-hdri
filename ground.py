import bpy
from camera import projectCam, changeFocalLength
def adjustGround():
    # Adjust the panel for the ground
    ground = bpy.context.scene.objects['Ground']
    coords = projectCam()
    sw = False
    for i in coords:
        if abs(i[0]) >= 100 or abs(i[1]) >= 100 or abs(i[2]) >= 100:
            sw = True
            break
    if len(coords) < 4 or sw:
        changeFocalLength(50)
        coords = projectCam()

    for i in range(len(coords)):
        ground.data.vertices[i].co = coords[i]
