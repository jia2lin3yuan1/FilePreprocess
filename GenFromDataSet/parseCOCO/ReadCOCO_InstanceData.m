close all; clc;
clear all; 

%% initialize COCO api (please specify dataType/annType below)
annTypes = { 'instances', 'captions', 'person_keypoints' };
dataType='train2014'; annType=annTypes{1}; % specify dataType/annType
annFile=sprintf('~/Documents/DataSet/coco/Data/annotations/%s_%s.json',annType,dataType);
coco=CocoApi(annFile);

DIR = '~/Documents/Research/coco_2014/';
IMG_DIR = strcat(DIR, 'images/training/');
LBL_DIR = strcat(DIR, 'annotations/training/');
INL_DIR = strcat(DIR, 'instanceL/training/');
SEL_DIR = strcat(DIR, 'semanticL/training/');
imgNum = numel(coco.data.images);
maxL    = 0;
for k = 1:imgNum
    img_obj = coco.data.images(k);
    imgId = img_obj.id;
    
    imgHt = img_obj.height;
    imgWd = img_obj.width;
    size = [imgHt, imgWd];
%     I = uint8(zeros(imgHt, imgWd, 3));
%     figure, imshow(I);    
    annIds = coco.getAnnIds('imgIds',imgId,'iscrowd',[]);
    anns = coco.loadAnns(annIds);
    [instanceI, semanticI, dirI] = coco.saveInstanceAnn(anns, size);
    maxL = max(maxL, max(max(semanticI)));
%     if(numel(anns) > 0)
%         %I = imread(img_obj.flickr_url);
%         %imwrite(I,strcat(IMG_DIR, img_obj.file_name));  
% 
%         [pathstr,fName,ext] = fileparts(img_obj.file_name);
%         imwrite(uint8(dirI),strcat(LBL_DIR, fName, '.png'));
%         imwrite(uint8(instanceI),strcat(INL_DIR, fName, '.png'));
%         imwrite(uint8(semanticI),strcat(SEL_DIR, fName, '.png'));
%     end
end
