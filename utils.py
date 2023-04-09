import os 
from data import collection_start, collection_end

def convert_yolo(x1,y1,x2,y2, shape):
    x = ((x1 + x2) / 2) / shape[1]
    y = ((y1 + y2) / 2) / shape[0]
    h = abs(y1 - y2) / shape[0]
    w = abs(x2 - x1) / shape[1]
    return x, y, w, h


def init(collections, path):
    if not os.path.exists(path):
        os.mkdir(path)
    names = {}
    ln = len(collections)
    with open(os.path.join(path, 'classes.txt'), 'w') as f:
        for i in range(ln):
            collections[i].hide_render = True
            f.write(collections[i].name)
            names[collections[i].name] = i
            if i != ln -1:
                f.write('\n')
    return names

def min_obj_z(obj):
    mat   = obj.matrix_world
    minz = (mat @ obj.data.vertices[0].co)[2]
    for i in obj.data.vertices:
        glob = mat @ i.co
        minz = min(minz, glob[2])

    return minz

def progress(colname, i= None, n=None):
    with open(f'progress {collection_start} - {collection_end}.txt', 'a') as f:
        if i==None and n == None:
            f.write('-------------------------------------------\n')
            f.write(f'\t\t\tdone {colname}\n')
            f.write('-------------------------------------------\n')
            return
        f.write(f'{colname} {i}/{n}\n')