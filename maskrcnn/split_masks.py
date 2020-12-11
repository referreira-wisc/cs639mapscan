# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 07:45:33 2020

@author: repfe
"""

import os
import numpy as np

n_classes = 8
src_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks'
dst_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\Data\masks_split'

for mask_file in os.listdir(src_dir):
    rows = []
    with open(os.path.join(src_dir, mask_file), 'r') as file:
        for row in file:
            rows.append(row)
    for class_id in range(n_classes):
        mask = []
        for row in rows:
            mask.append([c == str(class_id) for c in row.strip()])
        mask = np.stack(mask)
        if np.max(mask):
            instance = mask_file[:-4]
            with open(os.path.join(dst_dir, instance + '_' + str(class_id) + '.txt'), "w") as f:
                for row in mask:
                    f.write("".join(row.astype(int).astype(str)) + '\n')
