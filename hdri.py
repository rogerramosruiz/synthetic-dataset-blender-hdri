import bpy
from math import radians
import random

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
    randz = random.randint(0,360)
    randx = random.randint(-45,15)
    node_map = nodes['Mapping']
    node_map.inputs[2].default_value = [radians(randx), radians(0), radians(randz)]