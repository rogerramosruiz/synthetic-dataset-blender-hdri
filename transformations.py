import bpy
import random
from math import radians
from mathutils import Euler

from objOps import select
from camera import project_cam, is_inside_frame
from utils import min_obj_z
from data import scale_min, scale_max, min_rot, max_rot, prob_roate, prob_scale

def move(obj):
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
        randX = random.uniform(minx, maxx)
        randY = random.uniform(miny, maxy)
        obj.location = (randX, randY, obj.location[2])
        select(obj)
        bpy.ops.object.transform_apply(location=True)
        if is_inside_frame(obj):
            break
        c += 1
        if c > 20:
            obj.data = data.copy()
            break
        obj.data = data.copy()

def rotate(obj): 
    if random.random() < prob_roate:
        rx = radians(random.uniform(min_rot[0], max_rot[0]))
        ry = radians(random.uniform(min_rot[1], max_rot[1]))
        rz = radians(random.uniform(min_rot[2], max_rot[2]))
        obj.rotation_euler = Euler((rx, ry, rz), 'XYZ')

def scale(obj):
    if random.random() < prob_scale:
        scale = random.uniform(scale_min, scale_max)
        scl = [scale for _ in range(3)]
        obj.scale = scl

def put_over_ground(obj):
    groundz = bpy.context.scene.objects['Ground'].location[2]
    z = min_obj_z(obj)
    obj.location[2] -= z - groundz - 0.01

def transform(obj):
    rotate(obj)
    scale(obj)
    select(obj)
    put_over_ground(obj)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    move(obj)
    bpy.ops.object.transform_apply(location=True)