clear all; clc;

% DIR = '/home/yuanjial/Code/TensorFlow/FCN2/logs/';
% DIR = '/home/yuanjial/Documents/DataSet/coco/PythonAPI/'; 
DIR = '/home/yuanjial/Documents/Research/coco_2014/';

fileList  = dir(strcat(DIR, 'instanceL/validation/'));
% fileList  = dir(strcat(DIR, 'result/'));
fileNames = {fileList.name};
fileNum   = numel(fileNames);

for i =  3 : fileNum % 5:24 %
    fileNames{i} = 'COCO_train2014_000000522653.png';
    [pathstr,name,ext] = fileparts(fileNames{i});
    
    I  = imread(char(strcat(DIR, 'images/training_total/', name, '.jpg')));
    %Ig = imread(char(strcat(DIR, 'annotations/training/', fileNames{i})));
    Ii = imread(char(strcat(DIR, 'instanceL/training/', fileNames{i})));
    Is = imread(char(strcat(DIR, 'semanticL/training_total/', fileNames{i})));
    close all;figure,
    subplot(2,2,1), imshow(I), title('image');
    %subplot(2,2,2), imagesc(Ig), title('direction img');
    subplot(2,2,3), imagesc(Ii), title('instance semantic segmentation');
    subplot(2,2,4), imagesc(Is),title('semantic segmentation');

%     I  = imread(char(strcat(DIR, 'images/', name, '.jpg')));
%     In = imread(char(strcat(DIR, 'result/', name, '.png')));
%     close all; figure,
%     subplot(1,2,1), imshow(I);
%     In = In(:,:,1);
%     subplot(1,2,2), imagesc(In);
%     continue;
    
%     I  = imread(char(strcat(DIR, 'inp_', string(i), '.png')));
%     Ig = imread(char(strcat(DIR, 'gt_', string(i), '.png')));
%     Ip = imread(char(strcat(DIR, 'pred_', string(i), '.png')));
%     
%     close all;figure,
%     subplot(2,2,1), imshow(I), title('image');
%     subplot(2,2,2), imagesc(Ig), title('grd truth');
%     subplot(2,2,3), imagesc(Ip), title('pred rst');    
    
end