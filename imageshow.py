import numpy as np

import matplotlib.pyplot as plt
from matplotlib import image as mImg
from matplotlib import cm

def showImage():
    '''
    refering to: https://matplotlib.org/devdocs/gallery/pylab_examples/demo_tight_layout.html#sphx-glr-gallery-pylab-examples-demo-tight-layout-py
    '''
    arr  = np.zeros([64, 64])
    arr[0:16, :] = 1
    arr[:, 0:16] = 2
    arr[16:32, :] = 3
    arr[:, 16:32] = 4
    arr[32:48, :] = 5
    arr[:, 32:48] = 6
    arr[48:64, :] = 7
    arr[:, 48:64] = 8

    cond = 2
    if cond == 0:
        plt.imshow(arr)
        plt.show()
    elif cond == 1:
        fig, axes = plt.subplots(3, 2, subplot_kw={'xticks':[], 'yticks':[]})
        axes[0, 0].imshow(arr)
        axes[0, 1].imshow(8-arr)

        import pdb
        pdb.set_trace()
        x = np.arange(0,1,20)
        y = pow(x,2)
        axes[1,0].plot(x,y)
        axes[1,1].scatter(x,y)

        axes[2,0].imshow(arr+8)
        axes[2,1].imshow(arr)

        plt.show()
    elif cond == 2:
        ax1 = plt.subplot(221)
        ax2 = plt.subplot(223)
        ax3 = plt.subplot(122)

        ax1.imshow(arr)
        ax2.imshow(8-arr)
        ax3.imshow(arr+8)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    showImage()


