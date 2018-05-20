# matplotlib inline
from pycocotools.coco import COCO
import pycocotools._mask as mask
import mahotas.polygon

import os
import cv2
import numpy as np
from scipy import misc
import skimage.io as io
import PIL.Image     as Image
import PIL.ImageDraw as ImageDraw
import matplotlib.pyplot as plt

import pdb

def createInstanceImage(annotations, img):

	# an image we want to create
	instanceImg  = Image.new("I", (img.shape[1], img.shape[0]), 0)
	semanticImg  = Image.new("I", (img.shape[1], img.shape[0]), 0)
	#directionImg = Image.new("I", (img['width'], img['height']), 0)

	# a drawer to draw into the image
	drawer_ins = ImageDraw.Draw(instanceImg)
	drawer_sem = ImageDraw.Draw(semanticImg)
	#drawer_dir = ImageDraw.Draw(directionImg)

	#loop over all objects
	insId_list = []
	instanceId = 0
	for ann in annotations:
		if ann['id'] not in insId_list:
					insId_list.append(ann['id'])
					instanceId = instanceId + 1

		if type(ann['segmentation']) == list:
			# polygon
			for seg in ann['segmentation']:
				poly = np.array(seg).reshape((len(seg)/2),2)
				poly = poly.tolist()
				poly = [tuple([elem[0],elem[1]]) for elem in poly]

				# pdb.set_trace()
				drawer_ins.polygon(poly, fill=instanceId, outline = None) # outline = None
				drawer_sem.polygon(poly, fill=ann['category_id'], outline = None)
		elif False: # (type(ann['segmentation'])== dict): ignore crowd object.
			# mask
			if type(ann['segmentation']['counts']) == list:
				rle = mask.frPyObjects([ann['segmentation']], img.shape[0], img.shape[1])
			else:
				rle = [ann['segmentation']]
			m = mask.decode(rle)

			idx = m.nonzero()
			points = [tuple([elem[1], elem[0]]) for elem in zip(idx[0], idx[1])]
			drawer_ins.point(points, fill=instanceId)
			drawer_sem.point(points, fill=ann['category_id'])

	return instanceImg, semanticImg



def createInstanceImage_old(annotations, img):
	# create and draw annotation mask.
	semImg = np.zeros((img['height'], img['width']), dtype = np.uint8)
	for ann in annotations:
		# pdb.set_trace()
		catgr_id = ann['category_id']
		# c = ([catgr_id, catgr_id,catgr_id]).tolist()[0]
		if type(ann['segmentation']) == list:
			# polygon
			for seg in ann['segmentation']:
				seg = [round(elem, 0) for elem in seg] # rounding
				seg = map(int, seg) # convert to int, floor
				poly = np.array(seg).reshape((len(seg)/2), 2)

				canvas = np.zeros((img['height'],img['width'],1), dtype = int)
				poly = poly.tolist()
				poly = [tuple([elem[1],elem[0]]) for elem in poly]
				mahotas.polygon.fill_polygon(poly, canvas, catgr_id)

				idx = canvas.nonzero()
				annImg[idx[0],idx[1]] = catgr_id

		else: # if type(ann['segmentation']) == dict
			# mask
			if type(ann['segmentation']['counts']) == list:
				rle = mask.frPyObjects([ann['segmentation']], img['height'], img['width'])
			else:
				rle = [ann['segmentation']]
			m = mask.decode(rle)

			idx = m.nonzero()
			annImg[idx[0],idx[1]] = catgr_id

	return annImg

def json2instanceImg(inJson, rgbDir, dataSet,  saveDir):
	coco = COCO(inJson)
	imgIds = coco.getImgIds()


	pdb.set_trace()
	for k in range(len(imgIds)):
		imgId = imgIds[k]
		annIds = coco.getAnnIds(imgId, iscrowd=None)
		anns = coco.loadAnns(annIds)

                imgname = 'COCO_%s_'%(dataSet) + format(imgId, '012d')
                img     = cv2.imread(os.path.join(rgbDir, imgname+'.jpg'))

		instanceImg, semanticImg = createInstanceImage(anns, img);

                if False:
			pdb.set_trace()
			semanticImg.save(imgname+'_sem.png')
			instanceImg.save(imgname+'_ins.png')
		else:
			semanticImg.save(os.path.join(saveDir[0], imgname+'.png'))
			instanceImg.save(os.path.join(saveDir[1], imgname+'.png'))
			print('processed image is {}'.format(imgname))

		'''
		plt.figure(); plt.axis('off')
		plt.imshow(I)

		coco.showAnns(anns)
		plt.show()
		'''

		'''
		#pdb.set_trace()
		instanceImg = createInstanceImage_old(anns, img)
		'''


def main():
	jsonDir  ='../Data/annotations_trainval2014/'
	dataSet  ='train2014'
	annFile  ='%s/instances_%s.json'%(jsonDir,dataSet)

        rgbDir   = '../Data/%s'%(dataSet)
	outDir   = ['%s/instances_%s/semantic/'%(jsonDir, dataSet), '%s/instances_%s/instance/'%(jsonDir, dataSet)]
        if(not os.path.exists(outDir[0])):
            os.makedirs(outDir[0])
        if(not os.path.exists(outDir[1])):
            os.makedirs(outDir[1])

	json2instanceImg(annFile, rgbDir, dataSet,  outDir)


# call the main method
if __name__ == "__main__":
    main()
