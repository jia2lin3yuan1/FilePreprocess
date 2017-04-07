import numpy as np
import os
import os.path

import pdb


#----------------------------------------------------------
'''
Input: baseDir, is the common part of directories for all given directories.
       dir_list, is the different part of given directories in the start part.
       postfix_list, is the different part of given directories at the end.
       train_len / val_len, how much file needed to do train / validation

Output:  create list of file name for train / validation, including files existed in all given directories.
'''
def create_image_lists(baseDir, dir_list, postfix_list, train_len=10000, val_len=1000):

    image_dir = os.path.join(baseDir, dir_list[0])
    file_list = os.listdir(image_dir)

    if not file_list:
        print('No files found')
    else:
        fileNum = len(file_list)
	if fileNum < train_len+val_len:
	    print('No enough files for train and validation')
	else:
            poolNum = train_len + val_len
	    pool = np.random.choice(fileNum, poolNum, replace=False)

	    # generate file list
            train_list, val_list = [], []
            for k in range(poolNum):
		f = file_list[pool[k]]
                filename = os.path.splitext(f.split("/")[-1])[0]

	        exitFile = True # check if file existed?
		for subDir, subPostfix in zip(dir_list, postfix_list):
                    img_dir = os.path.join(baseDir, subDir, filename + subPostfix)
		    if not os.path.exists(img_dir):
			exitFile = False
			break

		if exitFile and k < train_len: # if existed, add to corresponding list
                    train_list.append(filename)
		elif exitFile:
		    val_list.append(filename)
		else:
		    print('%s didn\'t exist in each folder.\n', filename)

            np.savetxt('train.txt', np.array(train_list), fmt = '%s')
	    np.savetxt('val.txt', np.array(val_list), fmt = '%s')

#------------------------------------------------------------------------------------
'''
Input: list_path,    points to a txt file which includes a file list.
       dir_list,     directories that expected to show on output file_list.
       postfix_list, postfix of files in corresponding different directories.
       outPath,      points to the new output file_list file.
Output: a file named 'outPath', with content of file_list separated by space.
'''
def create_image_lists_by_fNameList(dir_list, postfix_list, list_path, outPath):
    save_list = []
    f = open(list_path, 'r')
    fileList = f.read().splitlines()
    for fileName in fileList:

	ele_list, fileExist = [], True
	for subDir, subPostfix in zip(dir_list, postfix_list):
	    saveDir = os.path.join(subDir, fileName+subPostfix)

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
    # generate filelist travel over the directory.
    DIR = './coco/PythonAPI'
    dir_list = ['Images', 'InstanceAnn', 'SemanticAnn']
    postfix_list = ['.jpg', '.png', '.png']
    create_image_lists(DIR, dir_list, 20000, 2000)

    pdb.set_trace()
    # generate complete filelist respect to different directories by filename list
    dir_list = ['./Image', './gt']
    postfix_list = ['.jpg', '_sem.png']
    create_image_lists_by_fNameList(dir_list, postfix_list, './val.txt', 'val_smpl.txt')


