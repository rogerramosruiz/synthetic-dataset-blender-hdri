import bpy
import random
from math import radians
from mathutils import Euler

from objOps import select
from camera import project_cam, is_inside_frame
from utils import min_obj_z
from data import scale_min, scale_max, min_rot, max_rot, prob_roate, prob_scale

def move(obj):
    """
    obj: Blender mesh

    Move a blender mesh to a random place inside the view of the camera
    """
    # bounds of the camera view
    coords = project_cam()
    minx = maxx = coords[0][0]
    miny = maxy = coords[0][1]
    for i in coords:
        minx = min(minx, i[0])
        maxx = max(maxx, i[0])
        miny = min(miny, i[1])
        maxy = max(maxy, i[1])
    data = obj.data.copy()
    c = 0
    maxy = min(6, maxy)
    while True:
        # random values inside the cameara view
        randX = random.uniform(minx, maxx)
        randY = random.uniform(miny, maxy)
        # move mesh
        obj.location = (randX, randY, obj.location[2])
        select(obj)
        bpy.ops.object.transform_apply(location=True)
        # check that the whole mesh is visible by the camera
        if is_inside_frame(obj):
            break
        c += 1
        if c > 20:
            # after 20 tries is the object couldn't be places break and restore to default place
            obj.data = data.copy()
            break
        # When the object mesh couldn't be placed restore the original data
        obj.data = data.copy()

def rotate(obj):
    """
    Random roatation
    """
    # choose to rotate with probability of prob_roate
    if random.random() < prob_roate:
        # random values for rotation
        rx = radians(random.uniform(min_rot[0], max_rot[0]))
        ry = radians(random.uniform(min_rot[1], max_rot[1]))
        rz = radians(random.uniform(min_rot[2], max_rot[2]))
        # Set rotation
        obj.rotation_euler = Euler((rx, ry, rz), 'XYZ')

def scale(obj):
    """
    Randomly scale a blender mesh object
    """
    # choose to scale with probability of prob_roate
    if random.random() < prob_scale:
        # random scale value
        scale = random.uniform(scale_min, scale_max)
        scl = [scale for _ in range(3)]
        obj.scale = scl

def put_over_ground(obj):
    """
    obj: Blender object mesh

    Put a mesh over the plane (Ground)
    """
    # z coordenate of the ground
    groundz = bpy.context.scene.objects['Ground'].location[2]
    # lowest z coordenate value of the mesh 
    z = min_obj_z(obj)
    # Put the mesh just above the ground
    obj.location[2] -= z - groundz - 0.01

def transform(obj):
    """
    obj: Blender mesh

    Transform a blender mesh object randomly by rotating, scaling, puting over ground and moving in that order
    """
    rotate(obj)
    scale(obj)
    select(obj)
    put_over_ground(obj)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    move(obj)
    bpy.ops.object.transform_apply(location=True)