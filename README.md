# Cardiac-MR-Left-Ventricle-Segmentation


data prepration for Cardiac MR Left Ventricle detection and Segmentation

1) download the data set from : https://www.cardiacatlas.org/sunnybrook-cardiac-data/  (some sample data is in data.rar file, please unrar this file)

2) convert dicom images to jpeg images

3) run extract_bondingbox_labels.py to extract bonding boxes , sml labels and also create image masks from manual contours

4) run xml_to_csv.py to create .csv file for object detection

5) run tarin_object.py for object detection

6) run visualize for croping 128x128 boxes for left ventricular

7) run segmentation.py for segmentation
