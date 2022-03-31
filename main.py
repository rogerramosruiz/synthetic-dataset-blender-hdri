import sys
import bpy
from mathutils import Euler
from math import radians
import bpy_extras
import random
import os

scene = bpy.context.scene
nodes = scene.world.node_tree.nodes
node_environment_name = "Environment Texture"


sys.path.append(r'C:/Users/Roger/Documents/synthetic_dataset_HDRI')
from transformations import transform, putOverGround
from camera import projectCam, boundingBox, camBox, changeFocalLength
from objOps import delete, copy
from utils import init
from hdri import changeHDRI


def intersersct(obj1,obj2):
    # Boundingbox the objects
    o1p1, o1p2 = boundingBox(obj1)
    o2p1, o2p2  = boundingBox(obj2)
    return o1p1[0] < o2p2[0] and o1p2[0] > o2p1[0] and o1p1[1] < o2p2[1] and o1p2[1] > o2p1[1] 



def chooseObjs(collection):
    collectionsNames = [collection.name]
    prob_many_objs = 1
    renderObjs = [random.choice(collection.all_objects).name]
    if random.random() > 0:
        for i in collections:
            if random.random() < prob_many_objs:
                renderObjs.append(random.choice(i.all_objects).name)
                collectionsNames.append(i.name)
    return renderObjs, collectionsNames

def useCollection(collection):
    changeFocalLength()
    ground = bpy.context.scene.objects['Ground']
    coords = projectCam(cam)
    
    for i in range(len(coords)):
        ground.data.vertices[i].co = coords[i]
    
    renObjs, colls = chooseObjs(collection)
    objects = []
    global imgIndex
    img = changeHDRI(hdris[imgIndex])
    imgIndex = (imgIndex + 1) % len(hdris)
    for i in renObjs:
        objc = copy(i)
        objc.hide_render = False
        transform(objc)
        b = True
        for _ in range(100):
            for o in objects:
                b = b and not intersersct(o, objc)            
            if b:
                objects.append(objc)
                break
            else:
                objc.data = bpy.context.scene.objects[i].data.copy()
                transform(objc)
                b = True
        if not b:
            delete(obj)
    save(objects, colls)
    for obj in objects:
        delete(obj)
    bpy.data.images.remove(img)

def save(objs, colls = [0]):
    # filename = randomFilename()
    filename = f'{saveDir}/{imgIndex}'
    bpy.context.scene.render.filepath = f'{filename}'
    with open (f'{filename}.txt', 'w') as f:
        ln = len(objs)
        for i in range(len(objs)):
            x, y, w, h = boundingBox(objs[i], True)
            f.write(f'{names[colls[i]]} {x} {y} {w} {h}')
            # f.write(f'0 {x} {y} {w} {h}')
            if i != ln - 1 :
                f.write('\n')  
    bpy.ops.render.render(write_still = True)


obj = bpy.context.scene.objects['Suzanne']
cam =  bpy.data.objects['Camera']
img_index = 0

def main(n):
    for i in collections:
        for _ in range(n):
            useCollection(i)


saveDir = 'E:/Devs/Python/readyolo/dataset'
collections    = bpy.data.collections['Objects'].children
names          = init(collections, saveDir)
imgIndex = 0

hdrisDIr = 'C:/Users/Roger/Documents/synthetic_dataset_HDRI/HDRIS'
hdris = [os.path.join(hdrisDIr, i) for i in os.listdir(hdrisDIr)]
main(1)
