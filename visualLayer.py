import scipy.misc as misc
from matplotlib import image as mpimg
from matplotlib import pyplot as plt

import numpy as np
import cv2


num_white = 2
def _arrange_data(inData, visize):
    img_ht, img_wd = visize
    num_data = inData.shape[2] # data has shape [ht, wd, ch]
    cell_wd = min(8, int(np.sqrt(num_data)))
    cell_ht = (num_data + cell_wd -1) // cell_wd

    out_wd = cell_wd*img_wd + cell_wd * num_white
    out_ht = cell_ht*img_ht + cell_ht * num_white

    outI = np.zeros([out_ht, out_wd])
    stX, stY = 0, 0
    for k in range(num_data):
        # resize inData to 32x32
        rs_img = cv2.resize(inData[..., k], (img_ht, img_wd))
        outI[stY:(stY+img_ht), stX:(stX+img_wd)] = rs_img

        stX = stX+num_white+img_wd
        if(stX >= out_wd):
            stX = 0
            stY = stY + num_white + img_ht

    return outI

def visual_layer(inData, layer_name, out_dir='./output/', visize=[64, 64]):

    bsize = inData.shape[0] # inData has shape [batchSize, ht, wd, ch]
    for k in range(bsize):
        #normalization to 0~255.
        tmpData = inData[k, ...]
        minV, maxV = np.min(tmpData), np.max(tmpData)
        tmpData = (tmpData - minV)* (255.0 / max(1, maxV-minV))

        vI = _arrange_data(tmpData, visize)
        mpimg.imsave(out_dir+str(k)+'_'+layer_name+'.png', vI)
        #img = misc.toimage(vI, high=np.max(vI), low=np.min(vI), mode='I')
        #img.save('./output/'+layer_name+'_gray_'+str(k)+'.png', vI)

if __name__ == '__main__':
    arr  = np.zeros([64, 64])
    arr[0:16, :] = 1
    arr[:, 0:16] = 2
    arr[16:32, :] = 3
    arr[:, 16:32] = 4
    arr[32:48, :] = 5
    arr[:, 32:48] = 6
    arr[48:64, :] = 7
    arr[:, 48:64] = 8
    arrs = np.asarray([arr]*19)
    arrs = np.transpose(arrs, [2,1,0])

    import pdb
    pdb.set_trace()

    if False:
        img = _arrange_data(arrs)
        plt.imshow(img)
        plt.show()
    else:
        visual_layer(arrs[np.newaxis, ...], 'test')
