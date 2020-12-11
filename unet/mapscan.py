# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:29:29 2020

@author: repfe
"""

from model import *
from data import *

data_gen_args = dict(rotation_range=0.2,
                    width_shift_range=0.05,
                    height_shift_range=0.05,
                    shear_range=0.05,
                    zoom_range=0.05,
                    horizontal_flip=True,
                    fill_mode='nearest')
myGene = trainGenerator(2,
                        'data/mapscan/train',
                        'image',
                        'label',
                        data_gen_args,
                        save_to_dir=None,
                        image_color_mode="rgb",
                        mask_color_mode="rgb",
                        flag_multi_class=True,
                        num_class=8,
                        target_size=(224,224))
model = unet(input_size=(224,224,3), num_class=8)
model_checkpoint = ModelCheckpoint('unet_mapscan.hdf5', monitor='loss', verbose=0, save_best_only=True)
model.fit_generator(myGene,steps_per_epoch=2000,epochs=20,callbacks=[model_checkpoint])
