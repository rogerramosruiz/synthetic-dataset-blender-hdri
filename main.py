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

def random_filename():
    """
    Genrate a random string 
    """
    letters = string.ascii_lowercase + string.ascii_uppercase
    name = ''.join(random.choice(letters) for _ in range(filename_size))
    return f'{save_dir}/{name}'

def intersersct(obj1,obj2):
    """
    Check if two obejct intersect from the camera view perspective
    """
    # Boundingbox the objects
    o1p1, o1p2 = bounding_box(obj1)
    o2p1, o2p2  = bounding_box(obj2)
    return o1p1[0] < o2p2[0] and o1p2[0] > o2p1[0] and o1p1[1] < o2p2[1] and o1p2[1] > o2p1[1] 

def choose_objs(collection):
    """
    collection: main collection to use

    Choose an object mesh from a collection 
    returns a list of chosed obejcts and a list of collctions names that have been used
    """
    # add the principal collection to be used
    collections_names = [collection.name]

    # Chooose a mesh from collection
    render_objs = [random.choice(collection.all_objects).name]
    # Add others collections with randomly with probabily of prob_many_objs
    if random.random() < prob_many_objs:
        for i in collections:
            # Choose collection with probabliy of prob_add_obj
            if random.random() < prob_add_obj:
                # Choose a random object mesh from the random collection selected
                render_objs.append(random.choice(i.all_objects).name)
                # Add the collection selectd
                collections_names.append(i.name)
    return render_objs, collections_names

def use_collection(collection):
    """
    collection: main collection to be used for the new render image
    """
    # Random resolution
    change_resolution()
    # Random zoom
    change_focal_length()
    # Adjust the ground to cameras view
    adjust_ground()
    # Choose the objects ot be render
    possible_objs, possible_collections = choose_objs(collection)
    objects = []
    materials = []
    collections = []
    # Set a random hdri image
    img = change_HDRI(random.choice(hdris))
    for i, coll in zip(possible_objs, possible_collections):
        # Copy the current object, so won't be altred for next renders
        obj_copy = copy(i)
        # Set the object to be visible
        obj_copy.hide_render = False
        # make random transformations
        transform(obj_copy)
        # Change the color of the materials in the object mesh 
        materials += shift_color(obj_copy, bpy.context.scene.objects[i].users_collection[0].name) 
        b = True
        # Try 10 times to randomly acomodate the object mesh inside the view of the camera with no intersections
        attempts = 10
        for j in range(attempts):
            # check the object dosen't intersect with others from camera's perspective
            for o in objects:
                b = b and not intersersct(o, obj_copy)
            # If there is no intersection append the object
            if b:
                collections.append(coll)
                objects.append(obj_copy)
                break
            # If the object intersects with others make another random trasnfomation
            # Unless its the try 9, then the object can not be fitted
            elif j != (attempts -1):
                # set the copied object mesh the original data like loation, rotation, scale
                obj_copy.data = bpy.context.scene.objects[i].data.copy()
                # ranodm transfomration
                transform(obj_copy)
                b = True
        # If the object was not placed delete it
        if not b:
            delete(obj_copy)
    # Render and save the coordenates
    save(objects, collections)
    # Dispose copied objects 
    for obj in objects:
        obj.hide_render = True
        delete(obj)
    # Remove hdri image
    bpy.data.images.remove(img)
    # Dispose copied materials
    for material in materials:
        bpy.data.materials.remove(material)

def save(objs, colls):
    """ 
    objs: Array with the blender object meshes used
    colls: Array with the collection's names used

    Save a new render image and a txt file with the coordenates (YOLO)
    of the objects contained in the image 
    """
    # Random file name
    filename = random_filename()
    # Ensure the file name dosen't exist already
    while os.path.exists(f'{filename}.jpg'):
        filename = random_filename()
    # Set the path for saving the render image
    bpy.context.scene.render.filepath = f'{filename}'
    # Save the txt file with the coordenates of the image
    with open (f'{filename}.txt', 'w') as f:
        ln = len(objs)
        for i in range(len(objs)):
            # Get the bouding box of the objects in YOLO formtat
            x, y, w, h = bounding_box(objs[i], True)
            f.write(f'{names[colls[i]]} {x} {y} {w} {h}')
            if i != ln - 1 :
                f.write('\n')  
    # Render the image
    bpy.ops.render.render(write_still = True)


def main(n):
    b = False
    for i in collections:
        if i.name == collection_start:
            b = True
        if b:
            for j in range(n):
                tm = time.time()
                use_collection(i)
                endt = time.time() - tm
                with open('algtimes.txt', 'a') as f:
                    f.write(f'{endt}\n')
                progress(i.name)
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