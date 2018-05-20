# Generate direction map depends on instance label with Matlab.
(refering to the work [Pixel-level Encoding and Depth Layering for Instance-level Semantic Labeling](https://arxiv.org/abs/1604.05096)

* <2017-04-06>: support to generate 4-directions and 8-directions.


*<2018-05-19>: A more fancy way to generate direction: [github::watershed instance seg](https://github.com/min2209/dwt/blob/master/matlab/generate_GT_cityscapes_unified.m)
`
       depth_i = bwdist(1-annotation_i);
       depth_map = depth_map + depth_i;
       
       dir_i = zeros(size(dir_map));
       
       [dir_i(:,:,1), dir_i(:,:,2)] = imgradientxy(depth_i);
       
       dir_i = dir_i / 8;
       
       dir_map = dir_map + dir_i;
`
