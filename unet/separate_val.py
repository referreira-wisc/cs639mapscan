# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 15:34:14 2020

@author: repfe
"""

import os
import random
from shutil import copyfile

src_txt_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks_gauss_argmax'
src_masks_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks_gauss_argmax_png'
data_dir = r'C:\Users\repfe\Desktop\CS639Project\unet-master\data\mapscan'
src_images_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\images'

dst_images_dir = os.path.join(data_dir, 'train', 'image')
dst_masks_dir = os.path.join(data_dir, 'train', 'label')
dst_txt_dir = os.path.join(data_dir, 'train', 'mask')

for file in os.listdir(dst_images_dir):
    os.remove(os.path.join(dst_images_dir, file))
for file in os.listdir(dst_masks_dir):
    os.remove(os.path.join(dst_masks_dir, file))
for file in os.listdir(dst_txt_dir):
    os.remove(os.path.join(dst_txt_dir, file))

for file in os.listdir(src_masks_dir):
    src = os.path.join(src_masks_dir, file)
    dst = os.path.join(dst_masks_dir, file)
    copyfile(src, dst)
    instance = file[:-4]
    src = os.path.join(src_images_dir, instance + '.jpg')
    dst = os.path.join(dst_images_dir, instance + '.jpg')
    copyfile(src, dst)
    src = os.path.join(src_txt_dir, instance + '.txt')
    dst = os.path.join(dst_txt_dir, instance + '.txt')
    copyfile(src, dst)
    
src_images_dir = os.path.join(data_dir, 'train', 'image')
src_masks_dir = os.path.join(data_dir, 'train', 'label')
src_txt_dir = os.path.join(data_dir, 'train', 'mask')
dst_images_dir = os.path.join(data_dir, 'test', 'image')
dst_masks_dir = os.path.join(data_dir, 'test', 'label')
dst_txt_dir = os.path.join(data_dir, 'test', 'mask')

for file in os.listdir(dst_images_dir):
    os.remove(os.path.join(dst_images_dir, file))
for file in os.listdir(dst_masks_dir):
    os.remove(os.path.join(dst_masks_dir, file))
for file in os.listdir(dst_txt_dir):
    os.remove(os.path.join(dst_txt_dir, file))

all_files = [f[:-4] for f in os.listdir(src_images_dir)]
n = len(all_files)
val_files = random.sample(range(n), k=round(n * 0.2))
for f in range(n):
    if f in val_files:
        instance = all_files[f]
        src = os.path.join(src_images_dir, instance + '.jpg')
        dst = os.path.join(dst_images_dir, instance + '.jpg')
        os.rename(src, dst)
        src = os.path.join(src_masks_dir, instance + '.png')
        dst = os.path.join(dst_masks_dir, instance + '.png')
        os.rename(src, dst)
        src = os.path.join(src_txt_dir, instance + '.txt')
        dst = os.path.join(dst_txt_dir, instance + '.txt')
        os.rename(src, dst)