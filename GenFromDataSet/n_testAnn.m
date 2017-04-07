clear all; clc; close all;

DIR = '/home/yuanjial/Documents/Research/coco_2014/annotations/validation/';

fileList  = dir(DIR);
fileNames = {fileList.name};
fileNum   = size(fileNames, 2);

figure,
for k = 3 : fileNum
    fName = strcat(DIR, fileNames{k});
    I = imread(fName);
    imshow(I*40);
end