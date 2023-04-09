import bpy
from math import radians
import random
from data import min_hdri_rotation, max_hdri_rotation

nodes = bpy.context.scene.world.node_tree.nodes
node_environment_name = "Environment Texture"
node_mapping_name = 'Mapping'
ground_nodes = bpy.data.objects['Ground'].material_slots[0].material.node_tree.nodes

def change_HDRI(path):
    """
    path: HDRI path

    Set a new image HDRI 
    """
    # Load hdri image
    img  = bpy.data.images.load(path)
    # set the image to world environment Texture 
    node_environment = nodes[node_environment_name]
    node_environment.image = img
    # Set the ground to HDRI image
    ground_nodes[node_environment_name].image = img
    # hdri image random rotation 
    rotate_HDRI()
    # Set the name of the node to Environment Texture and not to the name of the image
    node_environment.name  = node_environment_name
    ground_nodes[node_environment_name].name  = node_environment_name
    return img

def rotate_HDRI():
    """
    Randomly rotate HDRI image
    """
    # Random values for x, y, z rotation 
    randx = random.randint(min_hdri_rotation[0], max_hdri_rotation[0])
    randy = random.randint(min_hdri_rotation[1], max_hdri_rotation[1])
    randz = random.randint(min_hdri_rotation[2], max_hdri_rotation[2])
    rotation= (radians(randx), radians(randy), radians(randz))
    # Set the rotation values to Mapping node for hdri image and ground
    node_map = nodes[node_mapping_name]
    node_map.inputs[2].default_value = rotation
    ground_nodes[node_mapping_name].inputs[2].default_value = rotation