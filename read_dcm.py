import pydicom as dicom
import matplotlib.pylab as plt
import cv2

# specify your image path
image_path_dcm = 'D:/gifani/data_seg/data/data/hf-i-05/d-40.dcm'
image_path_jpg = 'D:/gifani/data_seg/data/data/hf-i-05/d-40.jpg'
ds = dicom.dcmread(image_path_dcm)
im = cv2.imread(image_path_jpg)
print(type(im))
#plt.imshow(ds.pixel_array, cmap=plt.cm.bone) 
plt.imshow(im) 
plt.show()

