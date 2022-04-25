# Initial data
images_per_class = 2
filenameSize     = 10
saveDir          = 'E:/Devs/Python/readyolo/dataset/'
hdrisDIr         = 'C:/Users/Roger/Documents/synthetic_dataset_HDRI/HDRIS'
prob_many_objs   = 0.4
prob_add_obj     = 0.6

# transformation
# scale
prob_scale       = 0.9
scale_min        = 1
scale_max        = 2

# rotation (x, y, z) between -360 and 360
prob_roate       = 0.9
minrot           = [-90, 0, -90]
maxrot           = [90, 360, 90]

# HDRI
min_hdri_rotation = [-45, 0 , 0]
max_hdri_rotation = [15,  0,  360]

# Camera
common_resolutions = [(480, 360), (852,480), (1280,720), (1920, 1080)]
high_resolutions   = [(2048, 1080), (2560, 1440), (4096, 2160)]
prob_common_res    = 0.6
prob_high_res      = 0.05
prob_flip_res      = 0.3 