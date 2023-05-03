import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET



def xml_to_csv(im_path,xml_path):
    xml_list = []
    for xml_file in glob.glob(xml_path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):

            value = (im_path + root.find('filename').text,
                     
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text),
                     member[0].text,
                     )
            xml_list.append(value)

    column_name = ['filename',   'xmin', 'ymin', 'xmax', 'ymax' ,'class']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    
    return xml_df


def main():
    cwd = os.getcwd()
    im_path=cwd + "/final_data/" + "images/"
    xml_path = cwd + "/final_data/" + "annotations/"
    xml_df = xml_to_csv(im_path,xml_path)
    xml_df.to_csv(cwd + '/final_data/train.csv', index=None)
    



    with open(cwd + '/final_data/train.csv') as rf, open(cwd + "/final_data/train.csv.temp", "w") as wf:
        for i, line in enumerate(rf):
            if i != 0:  # Everything but the second line
                wf.write(line)

    os.replace(cwd + "/final_data/train.csv.temp", cwd + '/final_data/train.csv')

    print('Successfully converted xml to csv.')

main()