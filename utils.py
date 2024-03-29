import os 

prog = {}
prog_file_name = 'progress.txt'

def convert_yolo(x1,y1,x2,y2, shape):
    x = ((x1 + x2) / 2) / shape[1]
    y = ((y1 + y2) / 2) / shape[0]
    h = abs(y1 - y2) / shape[0]
    w = abs(x2 - x1) / shape[1]
    return x, y, w, h


def init(collections, path):
    """
    Initialization
    Creates a directory to renderthe images and saves 
    the classes.txt with all the collections names
    """
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
    """
    obj: Blender mesh 

    Returns the lowest value in z coordenate of a mesh
    """
    mat   = obj.matrix_world
    minz = (mat @ obj.data.vertices[0].co)[2]
    for i in obj.data.vertices:
        glob = mat @ i.co
        minz = min(minz, glob[2])

    return minz

def save():
    with open(prog_file_name, 'w') as f:
        for i, v in prog.items():
            f.write(f'{i}:{v}\n')

def load():
    if not os.path.exists(prog_file_name):
        return
    with open(prog_file_name, 'r') as f:
        for i in f.read().splitlines():
            vals  = i.split(':')
            prog[vals[0]] = int(vals[1])


def progress(colname):
    """
    Save in a txt file the progress made
    """
    if len(prog) == 0:
        load()
    prog[colname] = prog[colname] + 1 if colname in prog else 1
    save()