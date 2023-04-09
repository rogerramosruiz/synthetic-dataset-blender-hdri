import bpy
import random
import bpy_extras
from mathutils.geometry import intersect_line_plane as ilp

from utils import convert_yolo
from data import common_resolutions, high_resolutions, prob_common_res, prob_high_res, prob_flip_res
cam =  bpy.data.objects['Camera']

def bounding_box(obj, yolo_format = False, cropped = True):
    """
    obj: Blender mesh object
    yolo_format: If its needed in yolo format or en coordentaes
    cropped: If the mesh exceed the view of the camera, then crop the bounding box to the limits of the view

    Bouding box of a blender mesh object depeding on the camera view
    """
    scene = bpy.context.scene
    render_scale = scene.render.resolution_percentage / 100
    # Widht and hight of the image resultion to be render
    width  = int(scene.render.resolution_x * render_scale)
    height = int(scene.render.resolution_y * render_scale)
    mat   = obj.matrix_world
    # Initial value for the the objects edges form the camera perspecitve
    x, y, _ = bpy_extras.object_utils.world_to_camera_view(scene, cam, obj.data.vertices[0].co)
    left = right = x
    top = bottom = y

    # Get the edges of the blender object from the camera perspective
    for i in obj.data.vertices:
        glob = mat @ i.co
        x, y, _  = bpy_extras.object_utils.world_to_camera_view(scene, cam, glob)
        left = min(left, x)
        right = max(right, x)
        top = max(top, y)
        bottom = min(bottom, y)
    # Blednder mesh object bounding box coordenates 
    p1 = (int(left * width), height - int(top *  height))
    p2 = (int(right * width), height - int(bottom * height))  
    
    # if coordenates exceed the frame then corop the bounding box
    if cropped:
        p1 = (max(p1[0], 0), max(p1[1], 0))
        p2 = (min(p2[0], width), min(p2[1], height))
        
    if yolo_format:
        return convert_yolo(p1[0], p1[1], p2[0], p2[1], (height, width))
    return p1, p2

    
def project_cam():
    """
    Make a projection of the view of the camera on the floor
    """
    plane_coordinates = []
    scene = bpy.context.scene
    mat = cam.matrix_world
    translation = mat.translation
    pers = [mat @ i for i in cam.data.view_frame(scene=scene)]
    x = pers[0] - pers[3]
    y = pers[0] - pers[1]
    # 2D coordenates of a squared floor
    two_d_coordenates = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for i in two_d_coordenates:
        v = (pers[2] + (i[0] * x + i[1] * y)) - translation
        pt = ilp(translation, translation +  v, (0, 0, 0), (0, 0, 1), True)    
        if pt and (pt - translation).dot(v) > 0:
            plane_coordinates.append(pt)
 
    return plane_coordinates

def is_inside_frame(obj):
    """
    obj: Blender mesh

    Check if a mesh is inside the view of the camera 
    """
    scene = bpy.context.scene
    # get the bounding box in coordenates and no cropping
    p1, p2 = bounding_box(obj, False, False)
    render_scale = scene.render.resolution_percentage / 100
    # widht and height of the final image
    width  = int(scene.render.resolution_x * render_scale)
    height = int(scene.render.resolution_y * render_scale)
    # Check the bounding box is inside the camera view
    return p1[0] >= 0 and p1[1] >= 0 and p2[0] <= width and p2[1] <= height

def change_focal_length(val= None):
    """
    Randomly change the camera focal lenght, 
    basicaly sets a random zoom for the camera
    """
    if val:
        cam.data.lens = val
    else:
        cam.data.lens = random.randint(25,65)

def change_resolution():
    """
    Randomly change the cameras resolution
    """
    scene = bpy.context.scene
    # Probabily of changing the resolution 
    if random.random() < prob_common_res:
        # Select a resolutoin from array common_resolutions
        x, y = random.choice(common_resolutions)
        # Probabily of choosing a high resolution
        if random.random() < prob_high_res:
            # Choose a high resoltion from array high_resolutions
            x, y = random.choice(high_resolutions)
        if random.random() < prob_flip_res:
            # Flip the resolution, e.g (1920, 1080)  -> (1080, 1920)
            a = x
            x = y 
            y = a
    # Random resultion
    else:
        while True:
            x = random.randint(852, 1920)
            y = random.randint(480, 1080)
            # mantain an aspect ratio that is visible, not too narrow
            r = x / y 
            if r > 0.8 and r < 2:
                break
    scene.render.resolution_x = x
    scene.render.resolution_y = y