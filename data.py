# Number of images to generate per class or collection
# E.G if  there are three collections A, B, C and the value is set to  10 
# then there will be at least 10 images with collection A, 10 with B, and 10 with C
# in total there will be 30 images
images_per_class = 2
# name length of the files
filename_size     = 10
# Location to save the dataset, must be full path
save_dir          = 'D:/dataset_shyntethic_hdri'
# Location of the images, must be full path
hdris_dir         = 'D:/generadores/hdri-downloader/downloads'

# Probability of having more than one object per background image
# if the value is 0 then there will just one object per background image
# if the values is 1 then there will more than one obejct per background image

prob_many_objs   = 0.3

# Probabylity of one object image to be added
# When one more than object will be added per background image 
# prob_add_obj is the probabily of adding a type or class of an object
# e.g there are three classes of objects A,B,C and the values is 0.5
# there is a 50% of adding an object A, 50% of adding an object of B
# and 50% of adding an object of C

prob_add_obj     = 0.5

# transformations
# probabily of scaling a mesh
prob_scale       = 0.9
# minimum and maximum value to scale
scale_min        = 1
scale_max        = 2

# probabily of rotating a mesh
prob_roate       = 0.55
# rotation (x, y, z) between -360 and 360
# minimum and maximum rotationn value 
min_rot           = [-80, 0, -80]
max_rot           = [80, 360, 80]

# HDRI
# minimum and maximum rotationn for HDRI images
min_hdri_rotation = [-45, 0 , 0]
max_hdri_rotation = [15,  0,  360]

# Camera
# usual camera resolutions
common_resolutions = [(852,480), (1280,720), (1920, 1080)]
high_resolutions   = [(2048, 1080), (2560, 1440), (4096, 2160)]
# Probabily of choosing a comon resolution
prob_common_res    = 0.6
# Probabily of choosing a high resolution
prob_high_res      = 0.05
# Probability of fliping the resoltion
prob_flip_res      = 0.3 

# Object mesh aditional data
# format
"""
obj_data = {
   collection_name: {
        material_name: probability of changeing color,
        material_name 2: probability of changeing color,
        
        # Optional value 
        # Colors to use for this sepecific collection
        colors: [[R,G,B], [R,G,B], [R,G,B]]
 }
}

"""

obj_data = {
    'bag': {
        'garbagebags': 0.1,
        'transparent bag': 0.7
    },
    'bottle': {
        'Plastic_transparent': 0.3,
        'lid': 1,
        'label': 1,
        'inner label': 0,
        'no_label_prob': 0.1
    },
    'container': {
        'Plastic_transparent': 0.005,
    },
    'cup': {
        'Plastic_transparent': 0.005
    },
    'gloves': {
        'gloves': 0.8,
        'colors' : [[0.238398, 0.341915, 0.904661], [0.208637, 0.558341, 0.930111], [0.027321, 0.114435, 0.327778], [0.871367, 0.83077, 0.708376]]
    },
    'spoon': {
        'spoon': 0.5,
    },
    'straw': {
        'straw': 1,
    }
}
