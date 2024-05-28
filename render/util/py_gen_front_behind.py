import subprocess
import os
import sys
from tqdm import tqdm
import argparse
from datetime import datetime

relation = "depth" 

def divide_list_into_partitions(lst, num_partitions):
    partition_size = len(lst) // num_partitions
    partitions = [lst[i:i + partition_size] for i in range(0, len(lst), partition_size)]
    return partitions

parser = argparse.ArgumentParser()
parser.add_argument('--partition', default=0, type=int, help="Partition 0 - 7")
parser.add_argument('--num_partition', default=8, type=int, help="Total number of parallel jobs")
parser.add_argument('--num_variants', default=5, type=int, help="Number of variants per 2-object scene")
parser.add_argument('--num_background', default=3, type=int, help="Number of variants of backgrounds")
parser.add_argument('--obj1_asset_folder', default="assets/blender_assets/", help="Object1 Asset Location")
parser.add_argument('--obj2_asset_folder', default="assets/blender_assets/", help="Object2 Asset Location")
parser.add_argument('--output_folder', default="/scratch/yluo97/3dscene_output_depth_coco/", help="hdf5 files output location")
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

object_names = sorted([name for name in os.listdir(args.obj1_asset_folder) if os.path.isdir(os.path.join(args.obj1_asset_folder, name))])
object2_names = sorted([name for name in os.listdir(args.obj2_asset_folder) if os.path.isdir(os.path.join(args.obj2_asset_folder, name))])
# Command and arguments
command = ["blenderproc", "run", f'./util/blender_depth_high.py']

obj2_partition = divide_list_into_partitions(object2_names, args.num_partition)[args.partition]
print('Generating partition of ', obj2_partition)

if args.dry_run:
    print('List of obj1 is', object_names)
    sys.exit(0)

for obj1 in object_names:
    for obj2 in obj2_partition:
        if obj1 != obj2:
            for background_path, background_name in background_info:
                success = 0
                if args.non_random:
                    arguments = [obj1, obj2, background_path, f'{output_folder}/{relation}_{background_name}/', str(success), '0']
                else:
                    arguments = [obj1, obj2, background_path, f'{output_folder}/{relation}_{background_name}/', '-1', '0']


                
                while success < args.num_variants :

                    # Run the command
                    try:
                        completed_process = subprocess.run(command + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False, check=True)
                        success += 1
                        if args.non_random:
                            arguments = [obj1, obj2, background_path, f'{output_folder}/{relation}_{background_name}/', str(success), '0']
                        else:
                            arguments = [obj1, obj2, background_path, f'{output_folder}/{relation}_{background_name}/', '-1', '0']

                    except subprocess.CalledProcessError as e:
                        print("Error:", e)

            print(f'Templates of {obj1}+{obj2} is complete!', f'{datetime.now():%Y-%m-%d %H:%M:%S%z}')
