import os
import numpy as np
import torch
import argparse
from transformers import pipeline
from PIL import Image
from tqdm import tqdm
import itertools 
import json 

device = 'cuda'

parser = argparse.ArgumentParser()
parser.add_argument('--image_path', default="/scratch/achatt39/1.5/0.6/bg_indoor/")
parser.add_argument('--output_path', default="output/depth_scores/1.5_0.6_indoor_depth.json")

args = parser.parse_args()

images = args.image_path
output_object_detect_path = args.output_path

def get_objects(text):
    # Assume the prompt/image file name always comes in terms of 'obj1 in front of obj2_imagenumber' or 'obj1 behind obj2_imagenumber'
    sentence = text.split('_')[0]
    if(' in front of ' in sentence):
        rel = ' in front of '
        objs_pre = sentence.split(rel)
        obj1 = objs_pre[0]
        obj2 = objs_pre[1]
        
    else:
        rel = ' behind '
        objs_pre = sentence.split(rel)
        obj1 = objs_pre[0]
        obj2 = objs_pre[1]
    
    return obj1, obj2, rel, sentence

def process_detection(outs, obj1, obj2, rel, image):

    # verify if the output of depth-anything matches with the prompt {obj1}{rel}{obj2} into object_recall and sra(spatial relationship accuracy)
    
    objects = [obj1, obj2]
    boxes, scores, labels = outs[0]["boxes"], outs[0]["scores"], outs[0]["labels"]

    det_bbox, det_scores, det_labels = [], [], []
    for box, score, label in zip(boxes, scores, labels):
        if score > 0.1:
            det_bbox.append(box.tolist())
            det_scores.append(score.tolist())
            det_labels.append(objects[label.item()])

    det_centroid = [((box[0]+box[2])/2, (box[1]+box[3])/2) for box in det_bbox]
    N = len(det_centroid)

    if obj1 in det_labels and obj2 in det_labels:
        recall = 2
    elif obj1 in det_labels:
        recall = 1
    elif obj2 in det_labels:
        recall = 1
    else:
        recall = 0

    idx1 = np.where(np.array(det_labels)==obj1)[0]
    idx2 = np.where(np.array(det_labels)==obj2)[0]
    sra = 0
    
    if(recall == 2):

        depth = pipe(image)["depth"]
        # pixels = np.array(depth.getdata()).reshape((depth.size[0], depth.size[1]))


        if obj1 in det_labels and obj2 in det_labels:
            idx1 = np.where(np.array(det_labels)==obj1)[0]
            idx2 = np.where(np.array(det_labels)==obj2)[0]
        
        # sra=1 when at least one of the bbox pairs follows the prompt's spatial relationship, otherwise sra=0
        for i1, i2 in itertools.product(idx1.tolist(), idx2.tolist()):
            obj1_depth_bbox = depth.crop(det_bbox[i1])
            obj1_depth = obj1_depth_bbox.getpixel((obj1_depth_bbox.size[0]/2, obj1_depth_bbox.size[1]/2))

            obj2_depth_bbox = depth.crop(det_bbox[i2])
            obj2_depth = obj2_depth_bbox.getpixel((obj2_depth_bbox.size[0]/2, obj2_depth_bbox.size[1]/2))
            
            if rel == " in front of " and obj1_depth < obj2_depth:
                sra = 1
                break
            if rel == " behind " and obj1_depth > obj2_depth:
                sra = 1
                break
    
    return {
        "classes": det_labels, "centroid": det_centroid, "recall": recall, "sra": sra, "rel_type": rel
        }

pipe = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-large-hf")

from transformers import Owlv2Processor, Owlv2ForObjectDetection

processor = Owlv2Processor.from_pretrained("google/owlv2-base-patch16-ensemble")
model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble").to(device)

dict_vals = {}
all_images = os.listdir(images)
all_images = sorted(all_images)

for x in tqdm(all_images):
    image_name = images+x
    image = Image.open(image_name)
    obj1, obj2, rel, key = get_objects(x)
    with torch.no_grad():
        texts = [["a photo of %s"%obj1, "a photo of %s"%obj2]]
        inputs = processor(text=texts, images=image, return_tensors="pt").to(device)
        outputs = model(**inputs)
        target_sizes = torch.Tensor([image.size[::-1]]).to(device)
        outs = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes)
        if key in dict_vals:
            dict_vals[key].append(process_detection(outs, obj1, obj2, rel, image))
        else:
            dict_vals[key] = [process_detection(outs, obj1, obj2, rel, image)]

with open(output_object_detect_path, "w", encoding='utf-8') as f:
    json.dump(dict_vals, f, indent=2, sort_keys=True, ensure_ascii=False)
    