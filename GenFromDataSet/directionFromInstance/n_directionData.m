% generate direction image according to instance label image
% jialin yuan, 2017-02-16
% for simulation of pixel level encoding-decoding semantic segmentation
% -----------------------

%% extract file list from directory
saveDir     = '/home/yuanjial/Documents/DataSet/PASCAL/directions_8dir/';
instanceDir = '/home/yuanjial/Documents/DataSet/PASCAL/SegmentationObjectFilledDenseCRF/';
fileList    = dir(instanceDir);
fileNames   = {fileList.name};
fileNum     = size(fileNames, 2);

%% process over each image
%cmap = copper(5);
for k = 37:fileNum
    img  = imread(strcat(instanceDir,fileNames{k}));
    dirI = DirectionImage(img, 0);
    imagesc(dirI)
    % imwrite(dirI, strcat(saveDir, fileNames{k}));
end
