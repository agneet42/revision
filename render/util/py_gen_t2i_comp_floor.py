import subprocess
import os
from tqdm import tqdm
import argparse
from datetime import datetime

rel_list_above = ['on the top of', 'on the bottom of']
rel_list_left = ['on the left of', 'on the right of']
rel_list_near = ['on side of', 'next to', 'near']

swap_table = {
    'bag': 'handbag',
    'sofa': 'couch',
    'television': 'tv',
    'table': 'dining_table',
    'phone': 'cell_phone'
}

with open('util/t2i_prompt_spatial_all.txt', 'r') as f:
    texts = f.read().splitlines()
    # texts = list(set(texts))
# texts = ['a book on the left of a bird', 'a man on the bottom of a sofa','a painting on the right of a pig','a pig on the bottom of a wallet']

def get_obj_t2i(prompt):
    first_obj = prompt.split(' ')[1]
    second_obj = prompt.split(' ')[-1]
    
    if first_obj in swap_table:
        first_obj = swap_table[first_obj]
    if second_obj in swap_table:
        second_obj = swap_table[second_obj]
    return first_obj, second_obj

def get_blender_command(prompt):
    relation = ''
    script = ''
    obj1, obj2 = get_obj_t2i(prompt)
    if 'right' in prompt or 'bottom' in prompt:
        obj1, obj2 = obj2, obj1        
    for rel in rel_list_above:
        if rel in prompt:
            script = './util/blender_above_below_floor.py'
    for rel in rel_list_left:
        if rel in prompt:
            script = './util/blender_left_right_floor.py'
    if len(script) == 0:
        script = './util/blender_left_right_near_floor.py'
        
    return obj1, obj2, prompt, script

def divide_list_into_partitions(lst, num_partitions):
    partition_size = len(lst) // num_partitions
    partitions = [lst[i:i + partition_size] for i in range(0, len(lst), partition_size)]
    return partitions

parser = argparse.ArgumentParser()
parser.add_argument('--partition', default=0, type=int, help="Partition 0 - 7")
parser.add_argument('--num_partition', default=7, type=int, help="Total number of parallel jobs")
parser.add_argument('--num_variants', default=5, type=int, help="Number of variants per 2-object scene")
parser.add_argument('--num_background', default=3, type=int, help="Number of variants of backgrounds")
parser.add_argument('--obj1_asset_folder', default="assets/blender_assets/", help="Object1 Asset Location")
parser.add_argument('--obj2_asset_folder', default="assets/blender_assets/", help="Object2 Asset Location")
parser.add_argument('--output_folder', default="/scratch/yluo97/3dscene_output_ver3_debug/", help="hdf5 files output location")
parser.add_argument('--non_random', action='store_true', help='Description for flag1')
parser.add_argument('--dry_run', action='store_true', help='Perform dry run only')
args = parser.parse_args()

asset_folder = args.obj1_asset_folder
output_folder = args.output_folder
background_info = [("background/white-background.hdr", "bg_white"),
                   ("background/autumn_park_2k.hdr", "bg_real_outdoors"),
                   ("background/photo_studio_loft_hall_2k.hdr", "bg_real_indoors"),
                   ("background/black-background.hdr", "bg_black")]
background_info = background_info[:args.num_background] 
num_variants = args.num_variants 

# object_names = sorted([name for name in os.listdir(args.obj1_asset_folder) if os.path.isdir(os.path.join(args.obj1_asset_folder, name))])
# object2_names = sorted([name for name in os.listdir(args.obj2_asset_folder) if os.path.isdir(os.path.join(args.obj2_asset_folder, name))])
# Command and arguments
# command = ["blenderproc", "run", f'blender_{relation}_small.py']

texts_partition = divide_list_into_partitions(texts, args.num_partition)[args.partition]
# print('Generating partition of ', texts_partition)

for prompt in texts_partition:
    obj1, obj2, text, script = get_blender_command(prompt)
    command = ["blenderproc", "run", script]
    text = '_'.join(text.split())
    for background_path, background_name in background_info:
        success = 0
        if args.non_random:
            arguments = [obj1, obj2, background_path, f'{output_folder}/{background_name}/{text}/', str(success), '0']
        else:
            arguments = [obj1, obj2, background_path, f'{output_folder}/{background_name}/{text}/', '-1', '0']

        while success < args.num_variants :

            # Run the command
            try:
                if args.dry_run:
                    print(command + arguments)
                else:
                    completed_process = subprocess.run(command + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False, check=True)
                success += 1
                if args.non_random:
                    arguments = [obj1, obj2, background_path, f'{output_folder}/{background_name}/{text}/', str(success), '0']
                else:
                    arguments = [obj1, obj2, background_path, f'{output_folder}/{background_name}/{text}/', '-1', '0']

            except subprocess.CalledProcessError as e:
                print("Error:", e)

    print(f'Templates of {text} is complete!', f'{datetime.now():%Y-%m-%d %H:%M:%S%z}')
