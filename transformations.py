import bpy
import random
from math import radians
from mathutils import Euler

from objOps import select, copy
from camera import camBox, projectCam, checkInsideFrame
from utils import minObj
# from data import scale_min, scale_max, minrot, maxrot, prob_roate, prob_scale

# def move(obj):
#     maxY = bpy.context.scene.objects['Plane'].location[1] - obj.dimensions[1]
#     randY = random.uniform(-1, maxY)
#     obj.location[1] = randY 
#     width, height = camBox(obj)
#     owidth, _, oheight = obj.dimensions    
#     owidth /= 2
#     oheight /= 2
#     x = width - owidth
#     z = height - oheight
#     randX = random.uniform(-x, x)
#     randZ = random.uniform(-z , z)
#     obj.location = (randX, randY, randZ)

def move(obj):
    coords = projectCam(bpy.data.objects['Camera'], False)
    minx = maxx = coords[0][0]
    miny = maxy = coords[0][1]
    for i in coords:
        minx = min(minx, i[0])
        maxx = max(maxx, i[0])
        miny = min(miny, i[1])
        maxy = max(maxy, i[1])
    data = obj.data.copy()
    c = 0
    while True:
        randX = random.uniform(minx, maxx)
        randY = random.uniform(miny, maxy)
        obj.location = (randX, randY, obj.location[2])
        select(obj)
        bpy.ops.object.transform_apply(location=True)
        if checkInsideFrame(obj):
            return (randX, randY)
            # break
        c += 1
        if c > 100:
            print('This is happenign')
            obj.data = data.copy()
            return None
        obj.data = data.copy()

def rotate(obj): 
    # if random.random() < prob_roate:
    minrot = [0, 0, 0]
    maxrot = [360, 360, 360]
    rx = radians(random.randint(minrot[0], maxrot[0]))
    ry = radians(random.randint(minrot[1], maxrot[1]))
    rz = radians(random.randint(minrot[2], maxrot[2]))
    obj.rotation_euler = Euler((rx, ry, rz), 'XYZ')

def scale(obj):
    # if random.random() < prob_scale:
    scale_min = 0.5
    scale_max = 1.5
    scale = random.uniform(scale_min, scale_max)
    scl = [scale for _ in range(3)]
    obj.scale = scl

# def putOverGround(obj):
#     groundz = bpy.context.scene.objects['Ground'].location[2]
#     z = minObj(obj)
#     obj.location[2] += groundz - z

def putOverGround(obj):
    groundz = bpy.context.scene.objects['Ground'].location[2]
    z = minObj(obj)
    # print(z)
    obj.location[2] -= z - groundz - 0.01
    # z -= 0.01
    # bpy.context.scene.objects['Ground'].location[2] = z

def transform(obj):
    rotate(obj)
    scale(obj)
    select(obj)
    putOverGround(obj)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    move(obj)
    # ground = copy('Ground')
    # ground.location = (objx, objy, ground.location[2])
    # return ground