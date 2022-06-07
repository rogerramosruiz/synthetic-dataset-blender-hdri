import subprocess
import time

images_per_classs = 1000
max_imgs = 100
blenderfile = "syntethic_hdri_1.blend"
start = 'bag'
end = 'straw'


n = images_per_classs // max_imgs
rest = images_per_classs % max_imgs

file = 'data.py'
def render():
    subprocess.run(["C:/Program Files/Blender Foundation/Blender 3.1/blender",blenderfile, "--background", "--python", "main.py"])

def edit(n, i):
    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            if 'collection_start' in line:
                f.write(f"collection_start = '{start}'\n")
            elif 'collection_end' in line:
                f.write(f"collection_end = '{end}'\n")
            elif 'images_per_class' in line:
                img_class = max_imgs if i != n else rest
                f.write(f"images_per_class = {img_class}\n")
            else:
                f.write(line)

if __name__ == '__main__':
    total = 0
    starttime = time.time()
    for i in range(n+1):
        edit(n,i)
        render()
        total += max_imgs if i != n else rest
        with open(f'progress {start} - {end}.txt', 'a') as f:
            f.write(f'----------------------- TOTAL: {total * 7} -----------------------\n')
    totaltime = time.time() - starttime
    print(f"Executer time", totaltime)