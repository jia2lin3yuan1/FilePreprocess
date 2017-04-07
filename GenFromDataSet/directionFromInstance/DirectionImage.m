function [dirImg] = DirectionImage(inI, mode)
 
    gI     = uint8(inI);

    rgn    = regionprops(gI, 'Area', 'Centroid', 'Orientation');
    rgnId  = find([rgn.Area]> 20);
    rNum   = size(rgnId, 2);

    dirImg  = uint8(zeros(size(gI(:,:,1))));
    for rk = 1 : rNum
        if (mode>0) % compute direction Image
            rgn_s = rgn(rgnId(rk));
            cx    = rgn_s.Centroid(1);
            cy    = rgn_s.Centroid(2);
            theta = rgn_s.Orientation*pi/90;
            [rIdx, cIdx] = find(gI == rgnId(rk));
            ptNum        = numel(rIdx);
            for pk = 1 : ptNum
                if(mode == 1)
                    dirId = Direction_8ID(cIdx(pk), rIdx(pk), cx, cy, theta);
                else % mode == 2
                    dirId = Direction_4ID(cIdx(pk), rIdx(pk), cx, cy);
                end
                dirImg(rIdx(pk), cIdx(pk)) = dirId;
            end
        else % compute distance image.
            bwI = (gI == rgnId(rk));
            distImg = DistanceTransform(bwI, 256);
            idx = find(distImg > 0);
            dirImg(idx) = distImg(idx);
        end
    end
end

%% four directions
function dirID = Direction_4ID(px, py, cx, cy)
    if(py <= cy)
        if(px >= cx)
            dirID = 1;
        else
            dirID = 2;
        end
    else
        if(px < cx)
            dirID = 3;
        else
            dirID = 4;
        end
    end
end

%% eight directions
function dirID = Direction_8ID(px, py, cx, cy, theta)
    % divide a region to 8 direction, based on 4 lines
    line_8dir_arg = [[0, 1]; [-1, 1]; [1, 0]; [1,1]]';
    dir_code      = [[1,0,1,1]; [1,1,1,1];[1,1,0,1];[1,1,0,0];[0,1,0,0];[0,0,0,0];[0,0,1,0];[0,0,1,1]];
    
    % orientation template
    theta = 0;
    ori_template = [cos(theta),sin(theta);-sin(theta),cos(theta)];
    pt_axis      = [px-cx, py-cy]*ori_template;
    
    % encode, and decode.
    dirID = 0;
    pt_enCode  = pt_axis * line_8dir_arg > 0;
    for k = 1:8
        if(pt_enCode == dir_code(k,:))
            dirID = k;
            return
        end
    end
end
%% distance transform
function distImg = DistanceTransform(bwI, level)
    dist = bwdist(~bwI);
    maxD = max(max(dist));
    
    distImg = uint8(dist*level/maxD);
end