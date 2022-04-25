import random
from mathutils import Color
from data import objData

def shiftColor(obj,collectionName):
    if 'custom_function' in objData[collectionName]:
        return objData[collectionName]['custom_function'](obj, collectionName)
    materials = []
    if 'colors' in objData[collectionName]:
        colors = objData[collectionName]['colors']  #if 'colors' in objData[collectionName] else None
        color = colors[random.randint(0,len(colors) - 1)]  #if 'colors' in objData[collectionName] else None
    else:
        color = None
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
    rgba = (random.random(), random.random(), random.random(), 1) if color == None else (color[0], color[1], color[2], 1)
    colorRamp = material.node_tree.nodes['ColorRamp']
    color = Color(rgba[:-1])
    for i in range(len(colorRamp.color_ramp.elements)):
        if i == 0:
            colorRamp.color_ramp.elements[i].color = rgba
        else:
            color.hsv = (color.h, color.s, random.random())
            colorRamp.color_ramp.elements[i].color = (color.r, color.g, color.b, 1)


def colorBottle(obj, collectionName):
    materials = []
    color = (random.random(), random.random(), random.random(), 1)
    for i in range(len(obj.material_slots)):
        material = obj.material_slots[i].material
        newMaterial = material.copy()
        obj.material_slots[i].material = newMaterial
        materials.append(newMaterial)
        prob = objData[collectionName][material.name]
        if random.random() < prob:
            sameColorProb = objData[collectionName]['sameColorProb'] if 'sameColorProb' in objData[collectionName] else 0
            if i > 0 and random.random() > sameColorProb:
                color = None
            colorChange(newMaterial, color)

    return materials
    
    


matereialBSDFS = {
    'spoon'              :  'Diffuse BSDF',
    'Plastic_transparent':  'Glass BSDF',
    'gloves'              :  'ColorRamp'
}
objData['gloves']['custom_function'] =  colorBottle