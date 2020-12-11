# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 10:41:44 2020

@author: repfe
"""

import os
import glob
import random
from shutil import copyfile

n_classes = 8

masks_dirs = ['masks_split', 'masks_gauss', 'masks_sep']
data_dirs = ['data', 'data_gauss', 'data_sep']

val_files = []
for d in range(len(masks_dirs)):

    src_masks_dir = os.path.join(r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data', masks_dirs[d])
    data_dir = os.path.join(r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\maskrcnn', data_dirs[d])
    
    src_images_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\images'
    dst_images_dir = os.path.join(data_dir, 'train', 'images')
    dst_masks_dir = os.path.join(data_dir, 'train', 'masks')
    masks_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks'
    for file in os.listdir(dst_images_dir):
        os.remove(os.path.join(dst_images_dir, file))
    for file in os.listdir(dst_masks_dir):
        os.remove(os.path.join(dst_masks_dir, file))
    
    for mask_file in os.listdir(masks_dir):
        instance = mask_file[:-4]
        src = os.path.join(src_images_dir, instance + '.jpg')
        dst = os.path.join(dst_images_dir, instance + '.jpg')
        copyfile(src, dst)
    
    for file in os.listdir(src_masks_dir):
        src = os.path.join(src_masks_dir, file)
        dst = os.path.join(dst_masks_dir, file)
        copyfile(src, dst)
    
    
    src_images_dir = os.path.join(data_dir, 'train', 'images')
    src_masks_dir = os.path.join(data_dir, 'train', 'masks')
    dst_images_dir = os.path.join(data_dir, 'val', 'images')
    dst_masks_dir = os.path.join(data_dir, 'val', 'masks')
    for file in os.listdir(dst_images_dir):
        os.remove(os.path.join(dst_images_dir, file))
    for file in os.listdir(dst_masks_dir):
        os.remove(os.path.join(dst_masks_dir, file))
    
    all_files = [f[:-4] for f in os.listdir(src_images_dir)]
    n = len(all_files)
    if len(val_files) == 0:
        val_files = random.sample(range(n), k=round(n * 0.2))
    for f in range(n):
        if f in val_files:
            instance = all_files[f]
            src = os.path.join(src_images_dir, instance + '.jpg')
            dst = os.path.join(dst_images_dir, instance + '.jpg')
            os.rename(src, dst)
            mask_files = glob.glob(os.path.join(src_masks_dir, instance + '*'))
            for mask_file in mask_files:
                dst = os.path.join(dst_masks_dir, os.path.basename(mask_file))
                os.rename(mask_file, dst)
