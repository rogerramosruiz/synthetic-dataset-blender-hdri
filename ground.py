import bpy
from camera import projectCam
def adjustGround():
    ground = bpy.context.scene.objects['Ground']
    coords = projectCam()
    # Adjust the palen
    for i in range(len(coords)):
        ground.data.vertices[i].co = coords[i]
