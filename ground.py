import bpy
from camera import project_cam, change_focal_length

def adjust_ground():
    """
    Adjust the panel for the ground, acoording cameras view
    """
    # Get ground 
    ground = bpy.context.scene.objects['Ground']
    # Camera projection on the ground coordenates
    coords = project_cam()
    sw = False
    for i in coords:
        # Check the projection isn't too large  
        if abs(i[0]) >= 100 or abs(i[1]) >= 100 or abs(i[2]) >= 100:
            sw = True
            break
    # if the prjection is too large or the prjection dosen't have 4 coordenates 
    # chagne camera focal length
    if len(coords) < 4 or sw:
        change_focal_length(50)
        coords = project_cam()

    # Adjust the ground
    for i in range(len(coords)):
        ground.data.vertices[i].co = coords[i]
