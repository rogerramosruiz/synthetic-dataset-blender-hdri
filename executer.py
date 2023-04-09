import time
import subprocess

from helper import blender_location, edit, get_blender_file

"""
The executer is used to separate in many chunks the total images to render and thus avoiding error of 
RAM or the GPU memory being saturated:

Error: System is out of GPU and shared host memory 
"""
# Images to render per class
images_per_classs = 1
# images to render per execution
max_imgs = 100

def render():
    subprocess.run([blender_command, blender_file, "--background", "--python", "main.py"])

def main():
    starttime = time.time()
    for i in range(executions + 1):
        img_class = max_imgs if i != executions else rest
        edit(img_class)
        render()
    
    totaltime = time.time() - starttime
    print(f"Executer time", totaltime)

if __name__ == '__main__':
    executions = images_per_classs // max_imgs
    # Remainder images to render 
    rest = images_per_classs % max_imgs
    # blender file to use 
    blender_file = get_blender_file()
    # get blender command depending on the version
    blender_command = blender_location()
    
    main()