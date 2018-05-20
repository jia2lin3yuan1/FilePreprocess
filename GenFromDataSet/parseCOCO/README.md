# Parse Instance Segmentation and Semantic Segmentation label from COCO DataSet
<2017-04-06, Share how to parsing and save COCO to new comers>

* There includes Python and Matlab API to save from COCO .json dataset
* To be able to use it:
  + download [coco_api](https://github.com/pdollar/coco), and install if needed
  + copy .py and .m to PythonAPI and MatlabAPI separately
  + use Python or Matlab as you like to parse Dataset
  
<2018-05-19, update python script because coco rgb image are not available on given url anymore>
* Download train2014 and corresponding json file, put to path './Data/'
* Download cocoAPI from [coco_api](https://github.com/pdollar/coco), go to PythonAPI, install coco api by running 'make'.
* copy .py to the './PythonAPI'.
* excute the script.
* To read the data in python, you could consider using 'scipy.misc.imread'. 'cv2.imread' has been tested that it would fail to read.
