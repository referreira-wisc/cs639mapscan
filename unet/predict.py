# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 19:20:04 2020

@author: repfe
"""
from model import *
from data import *
import os

weights_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\unet-master\weights'
results_dir = r'D:\UW\Courses\Fall 2020\COMP SCI 639\Project\unet-master\results'

for weights_file in os.listdir(weights_dir):
    batch = int(weights_file.split('_')[-3])
    steps = int(weights_file.split('_')[-2])
    epochs = int(weights_file.split('_')[-1][:-5])
    suffix = str(batch) + '_' + str(steps) + '_' + str(epochs)

    model = unet(input_size=(224,224,3), num_class=8)
    model.load_weights(os.path.join(weights_dir, weights_file))
    
    test_path = "data/mapscan/test/image"
    testGene = testGenerator(test_path,
                             target_size=(224,224),
                             flag_multi_class=True)
    results = model.predict_generator(testGene, len(os.listdir(test_path)), verbose=1)
    
    results_folder = os.path.join(results_dir, suffix)
    png_folder = os.path.join(results_folder, 'png')
    txt_folder = os.path.join(results_folder, 'txt')
    if not os.path.exists(results_folder):
        os.mkdir(results_folder)
        os.mkdir(png_folder)
        os.mkdir(txt_folder)
    saveResult(png_folder, results, os.listdir(test_path), flag_multi_class=True, num_class=results.shape[-1])
    
    
    yhat = img = np.argmax(results, axis=3)
    ygnd = loadLabels("data/mapscan/test/label")
    
    filenames = os.listdir(test_path)
    results_dir = txt_folder
    
    for file in os.listdir(results_dir):
        os.remove(os.path.join(results_dir, file))
    
    for i, filename in enumerate(filenames):
        instance = filename[:-4]
        np.savetxt(os.path.join(results_dir, instance + '_hat.txt'), yhat[i], delimiter='', fmt='%d')
        np.savetxt(os.path.join(results_dir, instance + '_gnd.txt'), ygnd[i], delimiter='', fmt='%d')