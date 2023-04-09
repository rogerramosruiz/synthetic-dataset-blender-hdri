import os
import platform
import subprocess


def blender_location():
    """
    Return the location where bleneder is installed
    """
    if platform.system() == 'Windows':
        # find the location of instalation of blender
        # where command doesn't work for the space in the path
        default_path = 'C:\Program Files\Blender Foundation'
        # use latests version
        latest = os.listdir(default_path)[-1]
        return os.path.join(default_path, latest, 'blender')

    return subprocess.check_output(['which', 'blender']).decode('utf-8').strip()

def edit(img_class):
    """
    img_class: Imager per class
    Edit data.py for updates in images_per_class 
    """
    file = 'data.py'
    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            if 'images_per_class' in line:
                f.write(f"images_per_class = {img_class}\n")
            else:
                f.write(line)

def get_blender_file():
    """
    Find blender file in the current directory
    """
    for i in os.listdir('.'):
        if i.endswith('.blend'):
            return i
