import numpy as np
import os
import os.path

import pdb

#--------------------------------------------------
def creat_video_image_lists(baseDir, dir_list, postfix_list, video_list_path, out_path):
    outList = []
    with open(video_list_path) as f:
        seq_list = f.read().splitlines()
    for seq_name in seq_list:
        image_dir = os.path.join(baseDir, dir_list[0], seq_name)
        file_list = os.listdir(image_dir)
        file_list = sorted(file_list)
        for img_name in file_list:
            file_name = img_name.split(postfix_list[0])[0]
            ele_list = []
            for k, sdir in enumerate(dir_list):
                ele_list.append(os.path.join(sdir, seq_name, file_name+postfix_list[k]))
            outList.append(ele_list)

    np.savetxt(out_path, np.asarray(outList), delimiter=" ", fmt = '%s')


#----------------------------------------------------------
'''
Input: baseDir, is the common part of directories for all given directories.
       dir_list, is the different part of given directories in the start part.
       postfix_list, is the different part of given directories at the end.
       train_len / train.len, how much file needed to do train / train.dation

Output:  create list of file name for train / train.dation, including files existed in all given directories.
'''
def create_image_lists(baseDir, dir_list, postfix_list, train_len=10000, val_len=1000):

    image_dir = os.path.join(baseDir, dir_list[0])
    file_list = os.listdir(image_dir)

    if not file_list:
        print('No files found')
    else:
        fileNum = len(file_list)
        if fileNum < train_len+val_len:
            print('No enough files for train and train.dation')
        else:
            poolNum = train_len + val_len

            # generate file list
            addFileNum = 0
            train_list, val_list = [], []
            for f in file_list:
                filename = os.path.splitext(f.split("/")[-1])[0]

                exitFile = True # check if file existed?
                for subDir, subPostfix in zip(dir_list, postfix_list):
                    img_dir = os.path.join(baseDir, subDir, filename + subPostfix)
                    if not os.path.exists(img_dir):
                        exitFile = False
                        print('Not Exist: ', img_dir, '\n')

                if exitFile and addFileNum < train_len: # if existed, add to corresponding list
                    train_list.append(filename)
                    addFileNum = addFileNum + 1
                elif exitFile and addFileNum < train_len+val_len:
                    val_list.append(filename)
                    addFileNum = addFileNum + 1
                else:
                    continue

                if addFileNum == poolNum:
                    break

            np.savetxt('train.txt', np.array(train_list), fmt = '%s')
            np.savetxt('val.txt', np.array(val_list), fmt = '%s')

#------------------------------------------------------------------------------------
'''
Input: baseDir, is the common part of directories for all given directories.
       list_path,    points to a txt file which includes a file list.
       dir_list,     directories that expected to show on output file_list.
       postfix_list, postfix of files in corresponding different directories.
       outPath,      points to the new output file_list file.
Output: a file named 'outPath', with content of file_list separated by space.
'''
def create_image_lists_by_fNameList(baseDir, dir_list, postfix_list, list_path, outPath):
    save_list = []
    f = open(list_path, 'r')
    fileList = f.read().splitlines()
    for fileName in fileList:

        ele_list, fileExist = [], True
        for subDir, subPostfix in zip(dir_list, postfix_list):
            saveDir = os.path.join(baseDir, subDir, fileName+subPostfix)

            if(os.path.exists(saveDir)):
                ele_list.append(saveDir)
            else:
                fileExist = False
                break

        if (fileExist == True):
            save_list.append(ele_list)

    np.savetxt(outPath, np.array(save_list), delimiter=" ", fmt = '%s')


#-----------------------------------------------------------------------
if __name__ == '__main__':

    pdb.set_trace()
    if False: # parse images
        DIR = '/media/zhouzh/LargeDisk/yjl_dataset/PASCAL_aug/'
        dir_list = ['JPEGImages', 'SegmentationClass_crf', 'direction_8']
        postfix_list = ['.jpg', '.png', '.png']
        if False:
            # generate filelist travel over the directory.
            create_image_lists(DIR, dir_list, postfix_list, 9000, 2000)
        else:
            # pdb.set_trace()
            # generate complete filelist respect to different directories by filename list
            create_image_lists_by_fNameList(DIR, dir_list, postfix_list, './pascal/train.txt', './pascal/sem_dir/train_pascal.txt')
    else: # parse video
        baseDir      = '/media/zhouzh/LargeDisk/yjl_dataset/cityscape/'
        dir_list     = ['leftImg8bit/val', 'semantic_ann/val', 'direction_8/val']
        postfix_list = ['leftImg8bit.png', 'gtFine_labelIds.png', 'gtFine_.png']
        video_list_path = os.path.join(baseDir,  'val.txt')
        out_path  = os.path.join(baseDir, 'val.sem.file.txt')
        creat_video_image_lists(baseDir, dir_list, postfix_list, video_list_path, out_path)

