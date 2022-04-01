import bpy
import random
from math import atan, tan
import bpy_extras
from mathutils.geometry import intersect_line_plane as ilp

from utils import convertYolo, distance
from data import common_resolutions, high_resolutions, prob_common_res, prob_high_res, prob_flip_res
cam =  bpy.data.objects['Camera']

def getAngles():
    scene = bpy.context.scene    
    frame = cam.data.view_frame(scene = scene)
    x = abs(frame[0][0])
    y = abs(frame[0][1])
    z = abs(frame[0][2])
    angleX = atan(x/z)
    angleY = atan(y/z)
    return angleX, angleY

def camBox(obj):
    angleX, angleY = getAngles()
    distanceY = distance(obj, cam)
    width  = tan(angleX) * distanceY
    height = tan(angleY) * distanceY
    return width, height

def adjustResolution(img):
    width, height = img.size
    bpy.context.scene.render.resolution_x = width
    bpy.context.scene.render.resolution_y = height
    bpy.context.scene.render.resolution_percentage = random.randint(10, 50) if width > 3000 or height > 3000 else 100

def boundingBox(obj, yoloFormat = False, cropped = True):
    scene = bpy.context.scene
    renderScale = scene.render.resolution_percentage / 100
    width  = int(scene.render.resolution_x * renderScale)
    height = int(scene.render.resolution_y * renderScale)
    mat   = obj.matrix_world
    x, y, _ = bpy_extras.object_utils.world_to_camera_view(scene, cam, obj.data.vertices[0].co)
    left = right = x
    top = bottom = y

    for i in obj.data.vertices:
        glob = mat @ i.co
        x, y, _  = bpy_extras.object_utils.world_to_camera_view(scene, cam, glob)
        left = min(left, x)
        right = max(right, x)
        top = max(top, y)
        bottom = min(bottom, y)

    p1 = (int(left * width), height - int(top *  height))
    p2 = (int(right * width), height - int(bottom * height))  
    
    # if coordenates exceed the frame then corop the boundingBox
    if cropped:
        p1 = (max(p1[0], 0), max(p1[1], 0))
        p2 = (min(p2[0], width), min(p2[1], height))
        
    if yoloFormat:
        return convertYolo(p1[0], p1[1], p2[0], p2[1], (height, width))
    return p1, p2

    
def projectCam():
    planeCoords = []
    scene = bpy.context.scene
    mat = cam.matrix_world
    translation = mat.translation
    pers = [mat @ i for i in cam.data.view_frame(scene=scene)]
    x = pers[0] - pers[3]
    y = pers[0] - pers[1]
    twodcoord = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for i in twodcoord:
        v = (pers[2] + (i[0] * x + i[1] * y)) - translation
        pt = ilp(translation, translation +  v, (0, 0, 0), (0, 0, 1), True)    
        if pt and (pt - translation).dot(v) > 0:
            planeCoords.append(pt)
 
    return planeCoords

def checkInsideFrame(obj):
    scene = bpy.context.scene
    p1, p2 = boundingBox(obj, False, False)
    renderScale = scene.render.resolution_percentage / 100
    width  = int(scene.render.resolution_x * renderScale)
    height = int(scene.render.resolution_y * renderScale)
    return p1[0] >= 0 and p1[1] >= 0 and p2[0] <= width and p2[1] <= height

def changeFocalLength(val= None):
    if val:
        cam.data.lens = val
    else:
        cam.data.lens = random.randint(25,65)

def changeResolution():
    scene = bpy.context.scene
    if random.random() < prob_common_res:
        x, y = random.choice(common_resolutions)
        if random.random() < prob_high_res:
            # High resolution
            x, y = random.choice(high_resolutions)
        if random.random() < prob_flip_res:
            # Flip the resolution
            a = x
            x = y 
            y = a
    else:
        while True:
            x = random.randint(852, 1920)
            y = random.randint(480, 1080)
            r = x / y 
            if r > 0.8 and r < 2:
                break
    scene.render.resolution_x = x
    scene.render.resolution_y = y