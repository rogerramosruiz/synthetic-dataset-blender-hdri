import random
from mathutils import Color
from data import obj_data

def shift_color(obj, collection_name):
    """
    obj: Blender mesh
    collection_name: Mesh collection name

    Randomly change an object mesh color
    Return an array of materials, to be disposed later on

    """
    
    # If the collection name has an especfic function to change its color, use that funciton
    if 'custom_function' in obj_data[collection_name]:
        return obj_data[collection_name]['custom_function'](obj, collection_name)
    # Materials to be used
    materials = []
    # Choose a random color, unless there are already colors defined for a particular mesh in obj_data
    color = random.choice(obj_data[collection_name]['colors']) if 'colors' in obj_data[collection_name] else None
    # Go through all materials
    for i in range(len(obj.material_slots)):
        material = obj.material_slots[i].material
        # Copy the material in order to not alter the original one
        newMaterial = material.copy()
        obj.material_slots[i].material = newMaterial
        materials.append(newMaterial)
        # Get probabily of changing the color according to data specified in obj_data
        prob = obj_data[collection_name][material.name]
        if random.random() < prob:
            color_change(newMaterial, color)
    
    return materials    
    
def color_change(material, color = None):
    """
    Randomly change the color for a an object mesh
    """
    # name of the material
    name = material.name.split('.')[0]
    # node name of the material, by defualt is Principled BSDF unless is set something different 
    # in the dictonary matereial_BSDFS
    node_name = matereial_BSDFS[name] if name in matereial_BSDFS else 'Principled BSDF'
    # If its color ramp change in the color in function color_ramp
    if node_name == 'ColorRamp':
        color_ramp(material, color)
    else:
        # Alter the mateiral color randomly
        rgba = color if color != None else [random.random(), random.random(), random.random(), 1]
        material.node_tree.nodes[node_name].inputs[0].default_value = rgba

def color_ramp(material, color = None):
    """
    Random colors in color ramp
    """
    # create a ranodm color if there is no default color
    random_color = color == None
    rgba = (random.random(), random.random(), random.random(), 1) if color == None else (color[0], color[1], color[2], 1)
    color_ramp_material = material.node_tree.nodes['ColorRamp']
    # Color object for altering the hue
    color = Color(rgba[:-1])
    # Go through all colors in color ramp
    for i in range(len(color_ramp_material.color_ramp.elements)):
        if random_color:
            color = Color((random.random(), random.random(), random.random()))
        else:
            # if its the first color set to the random color generated before
            if i == 0:
                color_ramp_material.color_ramp.elements[i].color = rgba
            # For the rest of the colors alter the hue randomly
            else:
                color.hsv = (color.h, color.s, random.random())
        color_ramp_material.color_ramp.elements[i].color = (color.r, color.g, color.b, 1)



def color_bottle(obj, collection_name):
    """
    Custom function color for bottle objects
    """
    materials = []
    for i in range(len(obj.material_slots)):
        # Get the probabily for the bottle to have a label
        no_label_prob =  obj_data[collection_name]['no_label_prob']
        material = obj.material_slots[i].material
        # Probabily of having a colorful noise in label 
        prob = 0.1
        # randomly remove label maeterial based on probabily of no_lavel_prob
        if random.random() < no_label_prob and 'label' in material.name:
            material = obj.material_slots[0].material
        else:
            prob = obj_data[collection_name][material.name]
        
        # Copy the maerial so the original material won't altered for the next meshes
        new_material = material.copy()
        # Set the copied material in the mesh
        obj.material_slots[i].material = new_material
        materials.append(new_material)
        if random.random() < prob:
            # Create a random color
            color = (random.random(), random.random(), random.random(), 1)
            # add random noise to the label, so it will more colorful
            if material.name == 'label':
                noise = new_material.node_tree.nodes['Noise Texture.001']
                noise.inputs['Scale'].default_value = random.uniform(3,30)
                noise.inputs['Detail'].default_value = random.uniform(0,2)
                noise.inputs['Roughness'].default_value = random.uniform(0,0.55)
                noise.inputs['Distortion'].default_value = random.uniform(0,5)
                new_material.node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = random.random()
                color_ramp(new_material)
            else:
                color_change(new_material, color)

    return materials
    
    

# Specific types of shader used for one material
# if a mateiral is not here the default shader will be Principled BSDF

matereial_BSDFS = {
    'spoon'              :  'Diffuse BSDF',
    'Plastic_transparent':  'Glass BSDF',
    'gloves'              :  'ColorRamp'
}

# Set custom fucntion for speficif collections
obj_data['bottle']['custom_function'] =  color_bottle