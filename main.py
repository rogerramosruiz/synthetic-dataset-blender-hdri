import sys
import bpy
import random
import os
import string

sys.path.append('.')

from transformations import transform
from camera import changeResolution, boundingBox, changeFocalLength
from objOps import delete, copy
from utils import init
from hdri import changeHDRI
from data import images_per_class, saveDir, hdrisDIr, filenameSize, prob_many_objs, prob_add_obj
from ground import adjustGround
from color import shiftColor

def randomFilename():
    letters = string.ascii_lowercase + string.ascii_uppercase
    name = ''.join(random.choice(letters) for _ in range(filenameSize))
    return f'{saveDir}/{name}'

def intersersct(obj1,obj2):
    # Boundingbox the objects
    o1p1, o1p2 = boundingBox(obj1)
    o2p1, o2p2  = boundingBox(obj2)
    return o1p1[0] < o2p2[0] and o1p2[0] > o2p1[0] and o1p1[1] < o2p2[1] and o1p2[1] > o2p1[1] 

def chooseObjs(collection):
    collectionsNames = [collection.name]
    renderObjs = [random.choice(collection.all_objects).name]
    if random.random() < prob_many_objs:
        for i in collections:
            if random.random() < prob_add_obj:
                renderObjs.append(random.choice(i.all_objects).name)
                collectionsNames.append(i.name)
    return renderObjs, collectionsNames

def useCollection(collection):
    changeResolution()
    changeFocalLength()
    adjustGround()
    renObjs, colls = chooseObjs(collection)
    objects = []
    materials = []
    global imgIndex
    img = changeHDRI(hdris[imgIndex])
    imgIndex = (imgIndex + 1) % len(hdris)
    for i in renObjs:
        objc = copy(i)
        objc.hide_render = False
        transform(objc)
        materials += shiftColor(objc, bpy.context.scene.objects[i].users_collection[0].name) 
        b = True
        attemps = 10
        for j in range(attemps):
            for o in objects:
                b = b and not intersersct(o, objc)
            if b:
                objects.append(objc)
                break
            elif j != (attemps -1):
                objc.data = bpy.context.scene.objects[i].data.copy()
                transform(objc)
                b = True
        if not b:
            delete(objc)
    save(objects, colls)
    for obj in objects:
        obj.hide_render = True
        delete(obj)
    bpy.data.images.remove(img)
    for material in materials:
        bpy.data.materials.remove(material)
def save(objs, colls = [0]):
    filename = randomFilename()
    bpy.context.scene.render.filepath = f'{filename}'
    with open (f'{filename}.txt', 'w') as f:
        ln = len(objs)
        for i in range(len(objs)):
            x, y, w, h = boundingBox(objs[i], True)
            f.write(f'{names[colls[i]]} {x} {y} {w} {h}')
            if i != ln - 1 :
                f.write('\n')  
    bpy.ops.render.render(write_still = True)


def main(n):
    for i in collections:
        for _ in range(n):
            useCollection(i)


if __name__ == '__main__':
    imgIndex    = 0
    hdris       = [os.path.join(hdrisDIr, i) for i in os.listdir(hdrisDIr)]
    collections = bpy.data.collections['Objects'].children
    names       = init(collections, saveDir)
    main(images_per_class)