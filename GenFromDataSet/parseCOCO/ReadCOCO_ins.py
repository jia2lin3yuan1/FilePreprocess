# matplotlib inline
from pycocotools.coco import COCO
import pycocotools._mask as mask
import numpy as np
import skimage.io as io

import mahotas.polygon
from scipy import misc

import PIL.Image     as Image
import PIL.ImageDraw as ImageDraw
import matplotlib.pyplot as plt

import pdb

def createInstanceImage(annotations, img):

	# an image we want to create
	instanceImg  = Image.new("I", (img['height'], img['width']), 0)
	semanticImg  = Image.new("I", (img['height'], img['width']), 0)
	directionImg = Image.new("I", (img['height'], img['width']), 0)

	# a drawer to draw into the image
	drawer_ins = ImageDraw.Draw(instanceImg)
	drawer_sem = ImageDraw.Draw(semanticImg)
	drawer_dir = ImageDraw.Draw(directionImg)

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
				poly = [tuple([elem[1],elem[0]]) for elem in poly]

				# pdb.set_trace()
				drawer_ins.polygon(poly, fill=instanceId, outline = None) # outline = None
				drawer_sem.polygon(poly, fill=ann['category_id'], outline = None)
		else: # (type(ann['segmentation'])== dict):
			# mask
			if type(ann['segmentation']['counts']) == list:
				rle = mask.frPyObjects([ann['segmentation']], img['height'], img['width'])
			else:
				rle = [ann['segmentation']]
			m = mask.decode(rle)

			idx = m.nonzero()
			points = [tuple([elem[0], elem[1]]) for elem in zip(idx[0], idx[1])]
			drawer_ins.point(points, fill=instanceId)
			drawer_sem.point(points, fill=ann['category_id'])

	return instanceImg, semanticImg
		


def createInstanceImage_old(annotations, img):
	# create and draw annotation mask.
	semImg = np.zeros((img['height'], img['width']), dtype = np.uint8)
	for ann in annotations:
		pdb.set_trace()
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

def json2instanceImg(inJson, saveDir):
	coco = COCO(inJson)
	imgIds = coco.getImgIds()
	cnt = 0

	
	# pdb.set_trace()
	for k in range(32103, len(imgIds), 1):
		imgId = imgIds[k]
		# for imgId in imgIds:
		img = coco.loadImgs(imgId)[0]
		annIds = coco.getAnnIds(imgIds=img['id'], iscrowd=None)
		anns = coco.loadAnns(annIds)


		I = io.imread('http://mscoco.org/images/%d'%(img['id']))
		instanceImg, semanticImg = createInstanceImage(anns, img);

		imgFileName = img['file_name'].split('.')
		imgFileName = imgFileName[0].encode('utf8')
		#misc.imsave((imgFileName+'_im.png'), I)
		#semanticImg.save(imgFileName+'_sem.png')
		#instanceImg.save(imgFileName+'_ins.png')

		#pdb.set_trace()

		misc.imsave((saveDir[0]+imgFileName+'.png'), I)
		semanticImg.save(saveDir[1]+imgFileName+'.png')
		instanceImg.save(saveDir[2]+imgFileName+'.png')

		print('dealed index is {}'.format(k))
		
		'''
		plt.figure(); plt.axis('off')
		plt.imshow(I)

		coco.showAnns(anns)
		plt.show()
		'''
		
		'''
		#pdb.set_trace()
		instanceImg = createInstanceImage_old(anns, img)

		imgFileName = img['file_name'].split('.')
		imgFileName = imgFileName[0].encode('utf8')
		misc.imsave((saveDir[1]+imgFileName+'.png'), instanceImg)

		I = io.imread('http://mscoco.org/images/%d'%(img['id']))
		misc.imsave((saveDir[0]+imgFileName+'.jpg'), I)
		cnt = cnt + 1
		if (cnt == 50):
			break
		'''


def main():
	dataDir  ='../Data'
	dataType ='train2014'
	annFile  ='%s/annotations/instances_%s.json'%(dataDir,dataType)

	outDir   = ['./Images/','./SemanticAnn/', './InstanceAnn/']
	json2instanceImg(annFile, outDir)
		

# call the main method
if __name__ == "__main__":
    main()
