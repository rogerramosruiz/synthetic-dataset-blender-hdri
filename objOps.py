import bpy

def select(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
 
def delete(obj):
    select(obj)
    bpy.ops.object.delete()

def copy(obj_name):
    objc = bpy.context.scene.objects[obj_name].copy()
    objc.data = bpy.context.scene.objects[obj_name].data.copy()
    bpy.context.scene.collection.objects.link(objc)
    return objc