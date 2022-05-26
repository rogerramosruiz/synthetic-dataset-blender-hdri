import random
from mathutils import Color
from data import objData

def shiftColor(obj,collectionName):
    if 'custom_function' in objData[collectionName]:
        return objData[collectionName]['custom_function'](obj, collectionName)
    materials = []
    color = random.choice(objData[collectionName]['colors']) if 'colors' in objData[collectionName] else None
    for i in range(len(obj.material_slots)):
        material = obj.material_slots[i].material
        newMaterial = material.copy()
        obj.material_slots[i].material = newMaterial
        materials.append(newMaterial)
        prob = objData[collectionName][material.name]
        if random.random() < prob:
            colorChange(newMaterial, color)
    
    return materials    
    
def colorChange(material, color = None):
    name = material.name.split('.')[0]
    nodename = matereialBSDFS[name] if name in matereialBSDFS else 'Principled BSDF'
    if nodename == 'ColorRamp':
        colorRamp(material, color)
    else:
        rgba = color if color != None else [random.random(), random.random(), random.random(), 1]
        material.node_tree.nodes[nodename].inputs[0].default_value = rgba

def colorRamp(material, color = None):
    randomColor = color == None
    rgba = (random.random(), random.random(), random.random(), 1) if color == None else (color[0], color[1], color[2], 1)
    colorRamp = material.node_tree.nodes['ColorRamp']
    color = Color(rgba[:-1])
    for i in range(len(colorRamp.color_ramp.elements)):
        if randomColor:
            color = Color((random.random(), random.random(), random.random()))
        else:
            if i == 0:
                colorRamp.color_ramp.elements[i].color = rgba
            else:
                color.hsv = (color.h, color.s, random.random())
        colorRamp.color_ramp.elements[i].color = (color.r, color.g, color.b, 1)



def colorBottle(obj, collectionName):
    materials = []
    for i in range(len(obj.material_slots)):
        no_label_prob =  objData[collectionName]['no_label_prob']
        material = obj.material_slots[i].material
        prob = 0
        # remove label maeterial
        if random.random() < no_label_prob and 'label' in material.name:
            material = obj.material_slots[0].material
        else:
            prob = objData[collectionName][material.name]
        newMaterial = material.copy()
        obj.material_slots[i].material = newMaterial
        materials.append(newMaterial)
        if random.random() < prob:
            color = (random.random(), random.random(), random.random(), 1)
            if material.name == 'label':
                noise = newMaterial.node_tree.nodes['Noise Texture.001']
                noise.inputs['Scale'].default_value = random.uniform(2,30)
                noise.inputs['Detail'].default_value = random.uniform(0,2)
                noise.inputs['Roughness'].default_value = random.uniform(0,0.55)
                noise.inputs['Distortion'].default_value = random.uniform(0,2)
                newMaterial.node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = random.random()
                colorRamp(newMaterial)
            else:
                colorChange(newMaterial, color)

    return materials
    
    


matereialBSDFS = {
    'spoon'              :  'Diffuse BSDF',
    'Plastic_transparent':  'Glass BSDF',
    'gloves'              :  'ColorRamp'
}
objData['bottle']['custom_function'] =  colorBottle