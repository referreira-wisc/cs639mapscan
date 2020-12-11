# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:13:50 2020

@author: repfe
"""

# Prepare dataset
import os
import random
import skimage.io
import numpy as np
from shutil import copyfile

n_classes = 8
dataset_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\mean_pixels'
main_masks_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks'
main_images_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\images'

for file in os.listdir(os.path.join(dataset_dir, 'train', 'images')):
    os.remove(os.path.join(dataset_dir, 'train', 'images', file))
for file in os.listdir(os.path.join(dataset_dir, 'train', 'masks')):
    os.remove(os.path.join(dataset_dir, 'train', 'masks', file))
for file in os.listdir(os.path.join(dataset_dir, 'val', 'images')):
    os.remove(os.path.join(dataset_dir, 'val', 'images', file))
for file in os.listdir(os.path.join(dataset_dir, 'val', 'masks')):
    os.remove(os.path.join(dataset_dir, 'val', 'masks', file))

mask_files = os.listdir(main_masks_dir)
n = len(mask_files)
val_files = random.sample(range(n), k=round(n * 0.2))
for i in range(n):
    mask_file = mask_files[i]
    image_file = mask_file[:-4] + '.jpg'
    src_mask = os.path.join(main_masks_dir, mask_file)
    src_image = os.path.join(main_images_dir, image_file)
    if i in val_files:
        dst_mask = os.path.join(dataset_dir, 'val', 'masks', mask_file)
        dst_image = os.path.join(dataset_dir, 'val', 'images', image_file)
    else:
        dst_mask = os.path.join(dataset_dir, 'train', 'masks', mask_file)
        dst_image = os.path.join(dataset_dir, 'train', 'images', image_file)
    copyfile(src_mask, dst_mask)
    copyfile(src_image, dst_image)


# Calculate mean pixel for each class
mean_pixels = {}
for image_file in os.listdir(os.path.join(dataset_dir, 'train', 'images')):
    instance = image_file[:-4]
    image = skimage.io.imread(os.path.join(dataset_dir, 'train', 'images', image_file))
    mask_file = os.path.join(dataset_dir, 'train', 'masks', instance + '.txt')
    for class_id in range(n_classes):
        with open(mask_file, 'r') as file:
            mask = []
            for row in file:
                mask.append([c == str(class_id) for c in row.strip()])
        mask = np.stack(mask)
        if class_id in mean_pixels:
            mean_pixels[class_id] = np.concatenate((mean_pixels[class_id], image[mask]))
        else:
            mean_pixels[class_id] = image[mask]

mp = {}
for c in range(n_classes):
    mp[c] = np.mean(mean_pixels[c], axis=0)


# Set class based on pixel value (closest value)
val_images_dir = os.path.join(dataset_dir, 'val', 'images')
pred_dir = os.path.join(dataset_dir, 'results')
for image_file in os.listdir(val_images_dir):
    instance = image_file[:-4]
    image = skimage.io.imread(os.path.join(val_images_dir, image_file))
    diffs = []
    for c in range(n_classes):
        diffs.append(np.sqrt(np.sum((image - mp[c]) ** 2, axis=-1)))
    diffs = np.stack(diffs)
    mask = np.argmin(diffs, axis=0)
    with open("{}/{}.txt".format(pred_dir, instance + '_hat'), "w") as f:
        for row in mask:
            f.write("".join(row.astype(int).astype(str)) + '\n')
    src = os.path.join(dataset_dir, 'val', 'masks', instance + '.txt')
    dst = os.path.join(pred_dir, instance + '_gnd.txt')
    copyfile(src, dst)