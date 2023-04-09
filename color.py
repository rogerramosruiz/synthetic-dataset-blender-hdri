import random
from mathutils import Color
from data import obj_data

def shift_color(obj, collection_name):
    if 'custom_function' in obj_data[collection_name]:
        return obj_data[collection_name]['custom_function'](obj, collection_name)
    materials = []
    color = random.choice(obj_data[collection_name]['colors']) if 'colors' in obj_data[collection_name] else None
    for i in range(len(obj.material_slots)):
        material = obj.material_slots[i].material
        newMaterial = material.copy()
        obj.material_slots[i].material = newMaterial
        materials.append(newMaterial)
        prob = obj_data[collection_name][material.name]
        if random.random() < prob:
            color_change(newMaterial, color)
    
    return materials    
    
def color_change(material, color = None):
    name = material.name.split('.')[0]
    node_name = matereial_BSDFS[name] if name in matereial_BSDFS else 'Principled BSDF'
    if node_name == 'ColorRamp':
        color_ramp(material, color)
    else:
        rgba = color if color != None else [random.random(), random.random(), random.random(), 1]
        material.node_tree.nodes[node_name].inputs[0].default_value = rgba

def color_ramp(material, color = None):
    random_color = color == None
    rgba = (random.random(), random.random(), random.random(), 1) if color == None else (color[0], color[1], color[2], 1)
    color_ramp_material = material.node_tree.nodes['ColorRamp']
    color = Color(rgba[:-1])
    for i in range(len(color_ramp_material.color_ramp.elements)):
        if random_color:
            color = Color((random.random(), random.random(), random.random()))
        else:
            if i == 0:
                color_ramp_material.color_ramp.elements[i].color = rgba
            else:
                color.hsv = (color.h, color.s, random.random())
        color_ramp_material.color_ramp.elements[i].color = (color.r, color.g, color.b, 1)



def color_bottle(obj, collection_name):
    materials = []
    for i in range(len(obj.material_slots)):
        no_label_prob =  obj_data[collection_name]['no_label_prob']
        material = obj.material_slots[i].material
        prob = 0.1
        # remove label maeterial
        if random.random() < no_label_prob and 'label' in material.name:
            material = obj.material_slots[0].material
        else:
            prob = obj_data[collection_name][material.name]
        new_material = material.copy()
        obj.material_slots[i].material = new_material
        materials.append(new_material)
        if random.random() < prob:
            color = (random.random(), random.random(), random.random(), 1)
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
    
    


matereial_BSDFS = {
    'spoon'              :  'Diffuse BSDF',
    'Plastic_transparent':  'Glass BSDF',
    'gloves'              :  'ColorRamp'
}
obj_data['bottle']['custom_function'] =  color_bottle