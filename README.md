# FilePreprocess
* 2017-04-06, adding of descripte dataset with text file. There are mainly two methods to do it:
  + a file list includes all example names in the dataset.
  `
  2007_0012340
  2007_0012540
  ...
  `
  + for each example, there are multiple directories point to different kind of files.
  `
  /Images/2007_0012340.jpg /Labels/2007_0012340_gt.png
  /Images/2007_0012540.jpg /Labels/2007_0012540_gt.png
  ...
  `
  
  The example to do it in both two ways are shown in the file.
