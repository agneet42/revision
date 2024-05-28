import blenderproc as bproc
import argparse
import numpy as np

from glob import glob
import random
from datetime import datetime
random.seed(datetime.now().timestamp())

import sys
import math


parser = argparse.ArgumentParser()
parser.add_argument('obj1', default="apple", help="Name of object 1")
parser.add_argument('obj2', default="banana", help="Name of object 2")
parser.add_argument('obj3', default="orange", help="Name of object 3")
parser.add_argument('bg_path', default="background/white-background.hdr", help="Path to the background hdr image")
parser.add_argument('output_dir', default="output/debug/", help="Path to where the final files, will be saved")
parser.add_argument('pair_index', default=0, help="Non-Random Pair index")
parser.add_argument('debug', default=0)
args = parser.parse_args()

pair_index = int(args.pair_index)

# obj_list = ["apple", "banana", "bed", "bicycle", "book", "car", "chair", "laptop", "person", "tv"]

obj_list = ["apple", "banana",  "bicycle", "book", "chair", "laptop", "person", "tv"]
big_list = ['bicycle', 'person']
medium_list = ['chair', 'tv']
tiny_list = ['apple', 'banana']
small_list = ['book', 'laptop']
tall_list = ['person']

def get_obj_scale(obj_name): 
    return 1.0

def get_article(noun):
    if noun[0] in ['a', 'e', 'i', 'o', 'u']:
        return 'an '+noun
    else:
        return 'a '+noun

def retrieve3obj(obj1="apple", obj2="banana", obj3="orange", index=-1, asset_path="/scratch/yluo97/data/blender_assets_ver2/"):

    # obj1, obj2 = random.sample(obj_list, 2)
    # assert obj1 in obj_list and obj2 in obj_list
    
    obj1_list = sorted(glob(f'{asset_path}/{obj1}/*.blend'))
    obj2_list = sorted(glob(f'{asset_path}/{obj2}/*.blend'))
    obj3_list = sorted(glob(f'{asset_path}/{obj3}/*.blend'))

    if index == -1:
        obj1_path = random.choice(obj1_list)
        obj2_path = random.choice(obj2_list)
        obj3_path = random.choice(obj3_list)
    else:
        obj1_path = obj1_list[index]
        obj2_path = obj2_list[index]
        obj3_path = obj3_list[index]
    return obj1_path, obj2_path, obj3_path, f'{obj1}+{obj2}+{obj3}'

def retrieve_floor(bgpath):
    if 'white' in bgpath:
        floor_path = "floor/floor_white.blend"
    elif 'autumn' in bgpath:
        floor_path = "floor/floor_grass_brass.blend"
    elif 'studio' in bgpath:
        floor_path = 'floor/floor_wood.blend'
    return floor_path

bproc.init()

# activate normal and depth rendering
# bproc.renderer.enable_normals_output()
# bproc.renderer.enable_depth_output(activate_antialiasing=False)
# set realistic background
# haven_hdri_path = bproc.loader.get_random_world_background_hdr_img_path_from_haven('/home/lawrence/Documents/3dscene/')
haven_hdri_path = args.bg_path

for i in range(1):

    path1, path2, path3, output_name = retrieve3obj(args.obj1, args.obj2, args.obj3, index=pair_index)

    if args.bg_path != "None":
        bproc.world.set_world_background_hdr_img(haven_hdri_path)

    
    print('Generating', output_name)

    r = random.uniform(5.0, 5.75)
    if args.obj2 in tall_list :
        height_offset = -0.5
    else:
        height_offset = 0.0
    #     offset = 1.35  
    # elif args.obj2 in medium_list:
    #     offset = 0.5
    # else:
    #     offset = 0.5

    # Set the scale of the objects
    obj1_scale = get_obj_scale(args.obj1)
    obj2_scale = get_obj_scale(args.obj2)
    obj3_scale = get_obj_scale(args.obj3)

    # if args.obj1 in small_list and args.obj2 in small_list:
    #     obj1_scale = random.uniform(4.0, 5.0)
    #     obj2_scale = obj1_scale
    # elif args.obj1 in small_list:
    #     obj1_scale = random.uniform(4.0, 5.0)
    # elif args.obj2 in small_list:
    #     obj2_scale = random.uniform(4.0, 5.0)
    floor_z = height_offset + random.uniform(-0.5, -0.75)
    floor = bproc.loader.load_blend(retrieve_floor(args.bg_path), obj_types= ['armature','mesh', 'empty', 'hair'] )
    floor = bproc.object.merge_objects(floor)
    floor.set_location([0,0,floor_z+random.uniform(-0.25, -0.05)])

    obj1 = bproc.loader.load_blend(path1, obj_types= ['armature','mesh', 'empty', 'hair'] )
    poi1 = bproc.object.compute_poi(bproc.filter.all_with_type(obj1, bproc.types.MeshObject))
    obj1 = bproc.object.merge_objects(obj1)
    obj1.set_location([random.uniform(-0.05, 0.05), random.uniform(1, 1.05), random.uniform(0.5, 0.75)]) # up 
    # obj1.set_location([0, random.uniform(-1.0, 0.0), 0]) # left
    obj1.set_scale([obj1_scale, obj1_scale, obj1_scale])
    obj1.set_rotation_euler([0, 0, random.uniform(-np.pi/16, np.pi/16)])

    obj2 = bproc.loader.load_blend(path2, obj_types= ['armature', 'mesh', 'empty', 'hair'])
    poi2 = bproc.object.compute_poi(bproc.filter.all_with_type(obj2, bproc.types.MeshObject))
    obj2 = bproc.object.merge_objects(obj2)
    obj2.set_location([random.uniform(-0.05, 0.05), random.uniform(1, 1.05), height_offset + random.uniform(-0.5, -0.75)]) # down
    # obj2.set_location([0, random.uniform(0.0, 1.0), 0]) # right
    obj2.set_scale([obj2_scale, obj2_scale, obj2_scale])
    obj2.set_rotation_euler([0, 0, random.uniform(-np.pi/16, np.pi/16)])
    
    obj3 = bproc.loader.load_blend(path3, obj_types= ['armature', 'mesh', 'empty', 'hair'])
    poi3 = bproc.object.compute_poi(bproc.filter.all_with_type(obj3, bproc.types.MeshObject))
    obj3 = bproc.object.merge_objects(obj3)
    obj3.set_location([random.uniform(-0.05, 0.05), random.uniform(-1.05, -1), height_offset + random.uniform(0.5, 0.75)]) # left up
    # obj2.set_location([0, random.uniform(0.0, 1.0), 0]) # right
    obj3.set_scale([obj3_scale, obj3_scale, obj3_scale])
    obj3.set_rotation_euler([0, 0, random.uniform(-np.pi/16, np.pi/16)])

    poi = (0,0,height_offset+0.5)

    

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

    # Sample five camera poses
    for j in range(1):
        # Sample random camera location around the object
        location = bproc.sampler.part_sphere([cam_x, cam_y, 0.5], radius=1.25, part_sphere_dir_vector=[1, 0, 0], mode="SURFACE")
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

    print('Objects chosen:\n', path1, '\n', path2, '\n', path3)
    print('Background:\n', haven_hdri_path)

import json
with open(args.output_dir + output_name + '/description.json', 'w') as fs:
    above_below_txt = [f"{get_article(args.obj1)} is above {get_article(args.obj2)}.", f"{get_article(args.obj2)} is below {get_article(args.obj1)}."]
    left_right_txt = [f"{get_article(args.obj3)} is to the left of {get_article(args.obj1)}.", f"{get_article(args.obj1)} is to the right of {get_article(args.obj3)}."]
    
    dct = {'above_below': above_below_txt, 'left_right': left_right_txt}
    json.dump(dct,fs)
    
