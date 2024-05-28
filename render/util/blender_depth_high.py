import blenderproc as bproc
import argparse
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from glob import glob
import random
from datetime import datetime
random.seed(datetime.now().timestamp())

import sys
import math

parser = argparse.ArgumentParser()
parser.add_argument('obj1', default="apple", help="Name of object 1, the one in the front")
parser.add_argument('obj2', default="banana", help="Name of object 2, the one behind")
parser.add_argument('bg_path', default="hdris/autumn/autumn_park_2k.hdr", help="Path to the background hdr image")
parser.add_argument('output_dir', default="output/above_below/", help="Path to where the final files, will be saved")
parser.add_argument('pair_index', default=-1, help="Non-Random Pair index")
parser.add_argument('debug', default=0)
args = parser.parse_args()

pair_index = int(args.pair_index)

# obj_list = ["apple", "banana", "bed", "bicycle", "book", "car", "chair", "laptop", "person", "tv"]


coco_objects = ['airplane', 'apple', 'backpack', 'banana', 'baseball_bat', 'baseball_glove', 'bear', 'bed', 'bench', 'bicycle', 'bird', 'boat', 'book', 'bottle', 'bowl', 'broccoli', 'bus', 'cake', 'car', 'carrot', 'cat', 'cell_phone', 'chair', 'clock', 'couch', 'cow', 'cup', 'dining_table', 'dog', 'donut', 'elephant', 'fire_hydrant', 'fork', 'frisbee', 'giraffe', 'hair_drier', 'handbag', 'horse', 'hot_dog', 'keyboard', 'kite', 'knife', 'laptop', 'microwave', 'motorcycle', 'mouse', 'orange', 'oven', 'parking_meter', 'person', 'pizza', 'potted_plant', 'refrigerator', 'remote', 'sandwich', 'scissors', 'sheep', 'sink', 'skateboard', 'skis', 'snowboard', 'spoon', 'sports_ball', 'stop_sign', 'suitcase', 'surfboard', 'teddy_bear', 'tennis_racket', 'tie', 'toaster', 'toilet', 'toothbrush', 'traffic_light', 'train', 'truck', 'tv', 'umbrella', 'vase', 'wine_glass', 'zebra']

big_obj = ['airplane', 'bus', 'car', 'boat', 'train', 'truck']


def retrieve_floor(bgpath):
    if 'white' in bgpath:
        floor_path = "floor/floor_white.blend"
    elif 'autumn' in bgpath:
        floor_path = "floor/floor_grass_brass.blend"
    elif 'studio' in bgpath:
        floor_path = 'floor/floor_wood.blend'
    return floor_path

def get_obj_scale(obj_name, is_front=True): 
    if is_front:
        if obj_name in big_obj:
            return random.uniform(0.5, 0.6)
        else:
            return random.uniform(0.8, 0.9)
    else:
        if obj_name in big_obj:
            return random.uniform(1.4, 1.6)
        else:
            return random.uniform(1.8, 2.0)
    # return 1.0
    
def retrieve2obj(obj1="apple", obj2="banana", index=-1, 
                 asset_path="assets/blender_assets/", 
                 noncoco_asset_path = "assets/blender_assets_non_coco/"):

    if obj1 in coco_objects:
        obj1_list = sorted(glob(f'{asset_path}/{obj1}/*.blend'))
    else:
        obj1_list = sorted(glob(f'{noncoco_asset_path}/{obj1}/*.blend'))
    if obj2 in coco_objects:    
        obj2_list = sorted(glob(f'{asset_path}/{obj2}/*.blend'))
    else:
        obj2_list = sorted(glob(f'{noncoco_asset_path}/{obj2}/*.blend'))

    if index == -1:
        obj1_path = random.choice(obj1_list)
        obj2_path = random.choice(obj2_list)
    else:
        obj1_path = obj1_list[index]
        obj2_path = obj2_list[index]
    return obj1_path, obj2_path, f'{obj1}_{obj2}'

bproc.init()

# activate normal and depth rendering
# bproc.renderer.enable_normals_output()
# bproc.renderer.enable_depth_output(activate_antialiasing=False)
# set realistic background
# haven_hdri_path = bproc.loader.get_random_world_background_hdr_img_path_from_haven('/home/lawrence/Documents/3dscene/')
haven_hdri_path = args.bg_path

for i in range(1):

    path1, path2, output_name = retrieve2obj(args.obj1, args.obj2, index=pair_index)

    if args.bg_path != "None":
        # bproc.world.set_world_background_hdr_img(haven_hdri_path)
        bproc.world.set_world_background_hdr_img(haven_hdri_path, rotation_euler=[0.0, 0.0, random.uniform(-np.pi, np.pi)])

    
    print('Generating', output_name)

    r = random.uniform(4.5, 5.5)

    height_offset = 0.0

    # Set the scale of the objects
    obj1_scale = get_obj_scale(args.obj1)
    obj2_scale = get_obj_scale(args.obj2, False)


    obj1 = bproc.loader.load_blend(path1, obj_types= ['armature','mesh', 'empty', 'hair'] )
    poi1 = bproc.object.compute_poi(bproc.filter.all_with_type(obj1, bproc.types.MeshObject))
    obj1 = bproc.object.merge_objects(obj1)
    obj1_y = random.uniform(-0.6, 0.6)
    obj1.set_location([random.uniform(0.5, 0.75), obj1_y, random.uniform(-0.05, 0.05)]) 

    obj1.set_scale([obj1_scale, obj1_scale, obj1_scale])
    obj1.set_rotation_euler([0, 0, random.uniform(-np.pi/16, np.pi/16)])

    obj2 = bproc.loader.load_blend(path2, obj_types= ['armature', 'mesh', 'empty', 'hair'])
    poi2 = bproc.object.compute_poi(bproc.filter.all_with_type(obj2, bproc.types.MeshObject))
    obj2 = bproc.object.merge_objects(obj2)
    obj2.set_location([random.uniform(-2.5, -2.0), obj1_y*-1, random.uniform(-0.05, 0.05)]) 

    obj2.set_scale([obj2_scale, obj2_scale, obj2_scale])
    obj2.set_rotation_euler([0, 0, random.uniform(-np.pi/16, np.pi/16)])

    poi = (poi1 + poi2) / 2.0
    
    offset_z = random.uniform(0.0, 0.5)
    offset_2 = random.uniform(-0.5, 0.0)
    
    floor = bproc.loader.load_blend(retrieve_floor(args.bg_path), obj_types= ['armature','mesh', 'empty', 'hair'] )
    floor = bproc.object.merge_objects(floor)
    floor.set_location([0,0,min(offset_2, offset_z)])

    

    # define a light and set its location and energy level
    light = bproc.types.Light()
    light.set_type("POINT")
    light.set_location([0, random.uniform(-5.0, 5.0), 5])
    light.set_energy(3000)

    # random camera angle
    alpha = random.uniform(-np.pi / 8, np.pi / 8) 
    # r = 3.0
    cam_x = r * math.cos(alpha)
    cam_y = r * math.sin(alpha)

    if cam_y * obj1_y < 0:
        cam_y = -cam_y

    # Set camera pose
    
    # Set output resolution to 1024x1024
    bproc.camera.set_resolution(1024, 1024)
    # Sample random camera location around the object
    location = bproc.sampler.part_sphere([cam_x, cam_y, 1.25], radius=0.25, part_sphere_dir_vector=[1, 0, 0], mode="SURFACE")
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location)
    # Add homog cam pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
    bproc.camera.add_camera_pose(cam2world_matrix)


    # Render the scene
    bproc.renderer.set_max_amount_of_samples(24)
    data = bproc.renderer.render()

    # Write the rendering into an hdf5 file
    bproc.writer.write_hdf5(args.output_dir + output_name, data, append_to_existing_output=True)
    # bproc.clean_up()

    print('Objects chosen:\n', path1, '\n', path2)
    print('Background:\n', haven_hdri_path)
    
