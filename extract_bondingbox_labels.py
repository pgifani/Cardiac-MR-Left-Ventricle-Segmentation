
import os
import glob 
#import pydicom as dicom
import numpy as np
import cv2 
import shutil
from pascal_voc_writer import Writer
cwd = os.getcwd()
manual_contour_root = cwd + "/manual_contour/"
data_root = cwd + "/data/"
final_data_root = cwd + "/final_data/"

os.makedirs(cwd + "/final_data/" + "annotations", exist_ok=True)
os.makedirs(cwd + "/final_data/" + "images", exist_ok=True)
os.makedirs(cwd + "/final_data/" + "masks_out", exist_ok=True)

annotations_root = cwd + "/final_data/" + "annotations"
images_root = cwd + "/final_data/" + "images"
mask_root = cwd + "/final_data/" + "masks_out"

list_contors = os.listdir(manual_contour_root)

list_data = os.listdir(data_root)

for ld in list_data:
    print(ld)
    number_id = ld.split("-")[-1]
    for im in glob.glob(os.path.join(data_root + ld , "*.jpg")):
        print(im)
        
        shutil.copy(im, data_root + '/' + ld + '/' + ld + '-' + os.path.basename(im)[:-4] + '.bmp')
        
        im_jpg = cv2.imread(data_root + '/' + ld + '/' + ld + '-' + os.path.basename(im)[:-4] + '.bmp')
        
        width , height ,dim = im_jpg.shape
        #ds_array = ds.pixel_array
        mask_out = np.zeros(im_jpg.shape[:2])
        d , dname = os.path.basename(im)[:-4].split("-")
        if len(dname) == 2:
            dname = "00" + dname
        if len(dname) == 3:
            dname = "0" + dname
        contours = os.listdir(manual_contour_root + '/' + "SC-" + ld + '/contours-manual/IRCCI-expert/')
        for c in contours:
            if c == "IM-0001-" + dname + "-ocontour-manual.txt":   # change to -icontour-manual for inner contour
                out_countor = c
                label_file_o= manual_contour_root + '/' + "SC-" + ld + '/contours-manual/IRCCI-expert/' + out_countor
                with open(label_file_o, 'r') as lbl:
                    lst1_o= lbl.readlines()
                    x_all = []
                    y_all = []
                    for i in lst1_o:
                        x , y = i.split(' ')
                        x_all.append(round(float(x)))
                        y_all.append(round(float(y)))
                        mask_out[round(float(x)),round(float(y))] = 255
                                        
                    min_x = min(x_all)
                    max_x = max(x_all)

                    min_y = min(y_all)
                    max_y = max(y_all)
                    H = max_x - min_x
                    W = max_y - min_y
                    cx = int(round(H/2))
                    cy = int(round(W/2))
                    im_floodfill = np.uint8(mask_out.copy())
                    h, w = mask_out.shape[:2]
                    mask = np.zeros((h+2, w+2), np.uint8)
                    cv2.floodFill(im_floodfill, mask, (min_y + cy,min_x + cx), 255)
                    #cv2.imshow("im",im_floodfill)
                    #cv2.waitKey()
                    #cv2.rectangle(mask_out, (min_y, min_x), (max_y, max_x), (0, 255, 0), 2)
                    im_crop = im_jpg[min_y-5:max_y+5 , min_x -5: max_x +5 ]
        writer = Writer(data_root + '/' + ld + '/' + ld + '-' + os.path.basename(im)[:-4] + '.bmp', width, height)
        writer.addObject('LV' , min_y-5, min_x-5, max_y+5, max_x+5)
        writer.save(annotations_root+ '/' + ld + '-' + os.path.basename(im)[:-4] + '.xml')
        cv2.imwrite(images_root + '/'+   ld + '-' + os.path.basename(im)[:-4] + '.bmp' , im_jpg )
        cv2.imwrite(mask_root +'/' + ld + '-' + os.path.basename(im)[:-4] + '.bmp' , im_floodfill )            

        print(dname)
        print('ok')
    