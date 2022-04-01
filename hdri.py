import bpy
from math import radians
import random
from data import min_hdri_rotation, max_hdri_rotation

nodes = bpy.context.scene.world.node_tree.nodes
node_environment_name = "Environment Texture"

def changeHDRI(path):
    img  = bpy.data.images.load(path)
    node_environment = nodes[node_environment_name]
    node_environment.image = img
    rotateHDRI()
    node_environment.name  = node_environment_name
    return img

def rotateHDRI():    
    randx = random.randint(min_hdri_rotation[0], max_hdri_rotation[0])
    randy = random.randint(min_hdri_rotation[1], max_hdri_rotation[1])
    randz = random.randint(min_hdri_rotation[2], max_hdri_rotation[2])
    node_map = nodes['Mapping']
    node_map.inputs[2].default_value = [radians(randx), radians(randy), radians(randz)]