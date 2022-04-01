import bpy
from camera import projectCam, changeFocalLength
def adjustGround():
    ground = bpy.context.scene.objects['Ground']
    coords = projectCam()
    # Adjust the palen
    if len(coords) < 4:
        changeFocalLength(50)
        coords = projectCam()
    for i in range(len(coords)):
        ground.data.vertices[i].co = coords[i]
