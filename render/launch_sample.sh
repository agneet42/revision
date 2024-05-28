#!/bin/bash

### we assume the blender object assets are located in assets/blender_assets/ and assets/blender_assets_non_coco/

( python ./util/py_gen_above_below.py --partition 0 --num_partition 1 --num_variants 2 --num_background 3 --output_folder output/mscoco_above_below ) &
pid1=$!
( python ./util/py_gen_left_right.py --partition 0 --num_partition 1 --num_variants 2 --num_background 3 --output_folder output/mscoco_left_right ) &
pid2=$!
( python ./util/py_gen_front_behind.py --partition 0 --num_partition 1 --num_variants 2 --num_background 3 --output_folder output/mscoco_front_behind ) &
pid3=$!
( python ./util/py_gen_left_right_near.py --partition 0 --num_partition 1 --num_variants 2 --num_background 3 --output_folder output/mscoco_near ) &
pid4=$!
### wait for the termination of all 3 programs runs
wait $pid1 $pid2 $pid3 $pid4

chmod -R 755 output/mscoco_above_below
chmod -R 755 output/mscoco_left_right
chmod -R 755 output/mscoco_front_behind 
chmod -R 755 output/mscoco_front_near

echo "Complete!"
