import sys
import bpy
from mathutils import Euler
from math import radians
import bpy_extras
import random

scene = bpy.context.scene
nodes = scene.world.node_tree.nodes
node_environment_name = "Environment Texture"


sys.path.append(r'C:/Users/Roger/Documents/synthetic_dataset_HDRI')
from transformations import transform, putOverGround
from camera import projectCam, boundingBox, camBox
from objOps import delete, copy
from utils import init



def changeHDRI(path):
    node_environment = nodes[node_environment_name]
    node_environment.image = bpy.data.images.load(path)
    # node_environment.name  = node_environment_name

def rotateHDRI():
    node_map = nodes['Mapping']
    node_map.inputs[2].default_value = [radians(0), radians(0), radians(25)]


# file = 'konigsallee_8k.exr'
# hdri = f"C:\\Users\\Roger\\Documents\\syntetic_dataset_HDRI\\HDRIS\\{file}"
# changeHDRI(hdri)




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
    ground = bpy.context.scene.objects['Ground']
    coords = projectCam(cam)
    
    for i in range(len(coords)):
        ground.data.vertices[i].co = coords[i]
    
    renObjs, colls = chooseObjs(collection)
    objects = []
    
    global imgIndex
    # img = changeBackground(imgs[imgIndex])
    # imgIndex = (imgIndex + 1) % len(imgs)
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
    # bpy.data.images.remove(img)

def save(objs, colls = [0]):
    # filename = randomFilename()
    filename = 'E:/Devs/Python/readyolo/monkeyhdir'
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
groundName = 'Ground'
cam =  bpy.data.objects['Camera']
img_index = 0


saveDir = '.'
collections    = bpy.data.collections['Objects'].children
names          = init(collections, saveDir)

useCollection(collections[0])
