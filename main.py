import sys
import bpy
import random
import os
import string
import time

sys.path.append('.')

from transformations import transform
from camera import change_resolution, bounding_box, change_focal_length
from objOps import delete, copy
from utils import init, progress
from hdri import change_HDRI
from data import images_per_class, save_dir, hdris_dir, filename_size, prob_many_objs, prob_add_obj, collection_start, collection_end
from ground import adjust_ground
from color import shift_color

def randomFilename():
    letters = string.ascii_lowercase + string.ascii_uppercase
    name = ''.join(random.choice(letters) for _ in range(filename_size))
    return f'{save_dir}/{name}'

def intersersct(obj1,obj2):
    # Boundingbox the objects
    o1p1, o1p2 = bounding_box(obj1)
    o2p1, o2p2  = bounding_box(obj2)
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
    change_resolution()
    change_focal_length()
    adjust_ground()
    renObjs, colls = chooseObjs(collection)
    objects = []
    materials = []
    img = change_HDRI(random.choice(hdris))
    for i in renObjs:
        objc = copy(i)
        objc.hide_render = False
        transform(objc)
        materials += shift_color(objc, bpy.context.scene.objects[i].users_collection[0].name) 
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
    while os.path.exists(f'{filename}.jpg'):
        filename = randomFilename()
    bpy.context.scene.render.filepath = f'{filename}'
    with open (f'{filename}.txt', 'w') as f:
        ln = len(objs)
        for i in range(len(objs)):
            x, y, w, h = bounding_box(objs[i], True)
            f.write(f'{names[colls[i]]} {x} {y} {w} {h}')
            if i != ln - 1 :
                f.write('\n')  
    bpy.ops.render.render(write_still = True)


def main(n):
    b = False
    for i in collections:
        if i.name == collection_start:
            b = True
        if b:
            for j in range(n):
                tm = time.time()
                useCollection(i)
                endt = time.time() - tm
                with open('algtimes.txt', 'a') as f:
                    f.write(f'{endt}\n')
                progress(i.name, j+1, n)
            progress(i.name)
        if i.name == collection_end:
            break

if __name__ == '__main__':
    startTime = time.time()
    hdris       = [os.path.join(hdris_dir, i) for i in os.listdir(hdris_dir)]
    collections = bpy.data.collections['Objects'].children
    names       = init(collections, save_dir)
    main(images_per_class)
    totalTime =  time.time() - startTime    
    print('Total time:', totalTime)