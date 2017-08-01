from collections import OrderedDict
from scipy import misc
import numpy as np
import os
import os.path

DIR = '/media/zhouzh/LargeDisk/yjl_dataset/PASCAL_aug/direction_8/'
#DIR = '/home/yuanjial/DataSet/COCO/coco2014_train/SemanticAnn/'

import pdb
pdb.set_trace()

if False:
    file_list = os.listdir(DIR)
else:
    f = open('./pascal/train.txt', 'r')
    file_list = f.read().splitlines()
    for k, fname in enumerate(file_list):
        file_list[k] = DIR + fname + '.png'

stat_dict = OrderedDict()
for fPath in file_list:
    img_path = os.path.join(DIR, fPath)
    img = misc.imread(img_path, mode='P')

    label_list = np.unique(img)
    for val in label_list:
        stat_dict[val] = np.sum(img==val) if val not in stat_dict else stat_dict[val]+np.sum(img==val)

print('statistical information: ')
stat_dict_order = OrderedDict(sorted(stat_dict.items()))
for val in stat_dict_order:
    pix_num              = stat_dict[val]
    stat_dict_order[val] = [val, pix_num, (1.0/pix_num)**1.0/3]
    print('label: %03d'%val,  ' -- pix num: %06d'% pix_num, ' -- 1/cubic(pxinum): ', stat_dict_order[val][2])

print('weight on each class:')
partial_dict = OrderedDict()
for val in stat_dict_order:
    partial_dict[val] = stat_dict_order[val][2]/stat_dict_order[0][2]
    print('label: %02d'%val, ' -- weight: ', '%.4f'%partial_dict[val])
