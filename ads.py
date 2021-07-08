import re
import pytesseract
import cv2 
import numpy as np
import shutil
import sys 
from pdf2image import convert_from_path 
import os 
import time
import json
import boto3
import boto3
s3 = boto3.resource('s3')
my_bucket = 'bb-bot-test'
s3_dir=sys.argv[1]
a=sys.argv[2]
pytesseract.pytesseract.tesseract_cmd=r'Tesseract-OCR\tesseract.exe'
DOWNLOAD_FOLDER = 'downloads'
print(a)
start=time.time()
path_file = os.path.join(DOWNLOAD_FOLDER, a)
pages = convert_from_path(path_file,dpi=220,poppler_path=r'poppler-0.68.0\bin')
image_counter = 1
page_lst=[]
for page in pages:
    filename = "page_"+str(image_counter)+".jpg"
    filename = os.path.join(DOWNLOAD_FOLDER, filename)
    page.save(filename, 'JPEG')
    p_img = cv2.imread(filename)
    height, width, channel = p_img.shape
    if height<width:
        img_rot = cv2.rotate(p_img, cv2.cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite(filename, img_rot)
    page_lst.append(filename)
    image_counter = image_counter + 1
filelimit = image_counter-1
print('Total no. of pages: ',filelimit)
file={}
try:
    img = cv2.imread(page_lst[0])
    roi=[[(778, 170), (1150, 212), 'check_text', 'Attorney Docket Number'], [(1165, 171), (1708, 208), 'text', 'docket'], [(788, 226), (1138, 266), 'check_text', 'Attorney Docket Number'], [(1160, 228), (1370, 266), 'text', 'docket'], [(782, 292), (1134, 326), 'check_text', 'Attorney Docket Number'], [(1152, 292), (1598, 322), 'text', 'docket'], [(786, 214), (1140, 256), 'check_text', 'Attorney Docket Number'], [(1156, 214), (1704, 254), 'text', 'docket'], [(778, 260), (1148, 298), 'check_text', 'Attorney Docket Number'], [(1162, 260), (1734, 296), 'text', 'docket'], [(774, 196), (1124, 230), 'check_text', 'Attorney Docket Number'], [(1144, 194), (1702, 226), 'text', 'docket']]
    for x,r in enumerate(roi):
        if r[2]=='check_text':
            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==r[3]:
                roi_r = roi[x+1]
                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value= value.rstrip()
                file[roi_r[3]]=value
                break
    roi=[[(118, 282), (378, 358), 'check_text', 'Title of Invention'], [(392, 280), (1754, 364), 'text', 'title'], [(152, 342), (394, 396), 'check_text', 'Title of Invention'], [(414, 332), (1718, 406), 'text', 'title'], [(156, 400), (394, 448), 'check_text', 'Title of Invention'], [(414, 392), (1714, 454), 'text', 'title'], [(118, 362), (374, 426), 'check_text', 'Title of Invention'], [(392, 362), (1752, 434), 'text', 'title'], [(142, 310), (382, 366), 'check_text', 'Title of Invention'], [(406, 310), (1700, 366), 'text', 'title']]
    for x,r in enumerate(roi):
        if r[2]=='check_text':
            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==r[3]:
                roi_r = roi[x+1]
                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value= value.rstrip()
                value=value.replace('\n',' ')
                file[roi_r[3]]=value
                break
    roi=[[(108, 544), (284, 598), 'check_text', 'Secrecy'], [(134, 638), (174, 680), 'check_box', 'check_box_secrecy'], [(140, 576), (310, 634), 'check_text', 'Secrecy'], [(164, 670), (204, 710), 'check_box', 'check_box_secrecy'], [(142, 618), (310, 670), 'check_text', 'Secrecy'], [(166, 702), (206, 740), 'check_box', 'check_box_secrecy'], [(110, 600), (282, 652), 'check_text', 'Secrecy'], [(132, 686), (176, 726), 'check_box', 'secrecy']]
    for x,r in enumerate(roi):
        if r[2]=='check_text':
            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==r[3]:
                roi_r = roi[x+1]
                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                total_pixels=cv2.countNonZero(value)
                if total_pixels>425:
                    file[roi_r[3]]='yes'
                break
    n=0
    roi=[(118, 802), (290, 836), 'check_text', 'Inventor']    
    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
    value=value.rstrip()
    if value==roi[3]:
        n=0
        print('inventor type1')
        inventor={}
        file['inventor']=inventor
        roi = [(296, 804), (318, 838), 'check_number', '1']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
        value= value.rstrip()
        if value==roi[3]:
            inventor['inventor_1']={}
            roi=[[(242, 960), (616, 998), 'text', 'first_name'], [(738, 958), (972, 998), 'text', 'middle_name'], [(1176, 962), (1596, 996), 'text', 'last_name']]
            for x,r in enumerate(roi):
                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                inventor['inventor_1'][r[3]]=value
            roi=[(124, 1379), (228, 1417), 'check_text', 'Postal']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                roi=[[(502, 1222), (1244, 1262), 'text', 'address_line1'], [(506, 1279), (1253, 1317), 'text', 'address_line2'], [(322, 1331), (633, 1364), 'text', 'city'], [(1311, 1331), (1466, 1371), 'text', 'state'], [(513, 1382), (699, 1417), 'text', 'postal'], [(1164, 1379), (1308, 1417), 'text', 'country']]
                address=''
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    address=address+' '+value
                address=address.lstrip()
                inventor['inventor_1']['address']=address
            else:
                roi=[(124, 1276), (260, 1314), 'check_text', 'Address']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    roi=[[(505, 1274), (1740, 1314), 'text', 'address_line1'], [(505, 1334), (1754, 1368), 'text', 'address_line2'], [(228, 1065), (545, 1100), 'text', 'address_city'], [(1317, 1385), (1728, 1420), 'text', 'address_state'], [(511, 1434), (782, 1474), 'text', 'address_postal'], [(1328, 1065), (1397, 1102), 'text', 'address_country']]
                    address=''
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        address=address+' '+value
                    address=address.lstrip()
                    inventor['inventor_1']['address']=address
                else:
                    roi=[(127, 1224), (259, 1262), 'check_text', 'Address']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        roi=[[(504, 1224), (1219, 1264), 'text', 'line1'], [(509, 1279), (1237, 1317), 'text', 'line2'], [(322, 1329), (714, 1364), 'text', 'city'], [(1312, 1329), (1387, 1367), 'text', 'state'], [(509, 1382), (664, 1414), 'text', 'postal'], [(1164, 1379), (1257, 1417), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            address=address+' '+value
                        address=address.lstrip()
                        inventor['inventor_1']['address']=address                        
                roi= [[(671, 1014), (717, 1042), 'check_box', 'US Residency'], [(951, 1011), (988, 1045), 'check_box', 'Non US Residency']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                    total_pixels=cv2.countNonZero(value)
                    if total_pixels>150:
                        inventor['inventor_1']['residence']=r[3]
                        break
            roi=[(297, 1491), (342, 1534), 'text', '2']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                inventor['inventor_2']={}
                roi=[[(240, 1657), (588, 1694), 'text', 'first_name'], [(745, 1660), (997, 1694), 'text', 'middle_name'], [(1177, 1657), (1482, 1694), 'text', 'last_name']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    inventor['inventor_2'][r[3]]=value
                roi=[[(499, 1971), (1459, 2012), 'text', 'line1'], [(503, 2031), (1609, 2062), 'text', 'line2'], [(321, 2078), (499, 2115), 'text', 'city'], [(1312, 2078), (1578, 2118), 'text', 'state'], [(512, 2128), (731, 2168), 'text', 'postal'], [(1162, 2128), (1356, 2171), 'text', 'country']]
                address=''
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    address=address+' '+value
                address=address.lstrip()
                inventor['inventor_2']['address']=address
                roi= [[(671, 1709), (715, 1740), 'check_box', 'US Residency'], [(946, 1703), (993, 1740), 'check_box', 'Non US Residency'], [(1262, 1709), (1315, 1740), 'check_box', 'Active US Military Service']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                    total_pixels=cv2.countNonZero(value)
                    if total_pixels>150:
                        inventor['inventor_2']['residence']=r[3]
                        break
            else:
                roi=[(122, 1442), (269, 1482), 'check_text', 'Inventor']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    inventor['inventor_2']={}
                    roi=[[(239, 1602), (537, 1639), 'text', 'first_name'], [(737, 1602), (1129, 1642), 'text', 'middle_name'], [(1177, 1604), (1477, 1637), 'test', 'last_name']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        inventor['inventor_2'][r[3]]=value
                    roi=[(126, 1920), (286, 1956), 'check_text', 'Address 1']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        roi=[[(503, 1920), (1703, 1956), 'text', 'line1'], [(506, 1980), (1713, 2010), 'text', 'line2'], [(323, 2026), (946, 2060), 'text', 'city'], [(1313, 2020), (1443, 2063), 'text', 'state'], [(513, 2076), (890, 2113), 'text', 'postal'], [(1166, 2076), (1360, 2113), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            address=address+' '+value
                        inventor['inventor_2']['address']=address
                        roi=[[(353, 1046), (676, 1653), 'check_box', 'US Residency'], [(946, 1653), (993, 1686), 'check_box', 'Non US Residency'], [(1283, 1656), (1323, 1690), 'check_box', 'Active US Military Service']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>150:
                                inventor['inventor_2']['residence']=r[3]
                                break
                        roi=[(296, 2143), (320, 2176), 'check_text', '3']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==roi[3]:
                            inventor['inventor_3']={}
                            roi=[[(243, 2300), (690, 2336), 'text', 'first_name'], [(746, 2300), (1146, 2336), 'text', 'middle_name'], [(1176, 2300), (1606, 2333), 'text', 'last_name']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                inventor['inventor_3'][r[3]]=value
                            img=cv2.imread(page_lst[1])
                            roi=[[(506, 592), (1714, 630), 'text', 'line1'], [(508, 650), (1724, 686), 'text', 'line2'], [(326, 700), (972, 732), 'text', 'city'], [(1314, 698), (1604, 738), 'text', 'state'], [(514, 750), (896, 786), 'text', 'postal'], [(1166, 750), (1438, 786), 'text', 'country']]
                            address=''
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                address=address+' '+value
                            address=address.lstrip()
                            inventor['inventor_3']['address']=address
                            roi=[[(678, 378), (716, 414), 'check_box', 'US Residency'], [(948, 378), (990, 410), 'check_box', 'Non US Residency'], [(1278, 378), (1330, 412), 'check_box', 'Active US Military Service']] 
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>150:
                                    inventor['inventor_3']['residence']=r[3]
                                    break
                    else:
                        roi=[[(503, 1866), (1326, 1903), 'text', 'line1'], [(506, 1926), (1323, 1956), 'text', 'line2'], [(326, 1973), (496, 2010), 'text', 'city'], [(1310, 1973), (1423, 2006), 'text', 'state'], [(513, 2023), (666, 2060), 'text', 'postal'], [(1163, 2023), (1290, 2060), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if r[3]=='line1':
                                value=value.replace('#','4')
                            address=address+' '+value
                        address=address.lstrip()
                        inventor['inventor_2']['address']=address
                        roi=[[(673, 1650), (720, 1690), 'check_box', 'US Residency'], [(933, 1653), (996, 1686), 'check_box', 'Non US Residency'], [(1266, 1656), (1326, 1686), 'check_box', 'Active US Military Service']] 
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>150:
                                inventor['inventor_2']['residence']=r[3]
                                break
            roi=[(293, 2090), (320, 2123), 'check_text', '3']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                inventor['inventor_3']={}
                roi=[[(240, 2246), (540, 2283), 'text', 'first_name'], [(743, 2243), (1063, 2283), 'text', 'middle_name'], [(1176, 2246), (1506, 2283), 'text', 'last_name']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    inventor['inventor_3'][r[3]]=value
                n=1
                img=cv2.imread(page_lst[1])
                roi=[(156, 723), (286, 756), 'check_text', 'Address']
                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    roi=[[(506, 602), (1430, 640), 'text', 'line1'], [(504, 656), (1424, 694), 'text', 'line2'], [(324, 708), (534, 744), 'text', 'city'], [(1316, 706), (1534, 744), 'text', 'state'], [(512, 758), (634, 796), 'text', 'postal'], [(1164, 756), (1302, 796), 'text', 'country']]
                    address=''
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        address=address+' '+value
                    address=address.lstrip()
                    inventor['inventor_3']['address']=address
                else:
                    roi=[(120, 546), (260, 583), 'check_text', 'Address']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        roi=[[(504, 550), (1738, 586), 'text', 'line1'], [(503, 603), (1183, 643), 'text', 'line2'], [(323, 650), (540, 686), 'text', 'city'], [(1313, 653), (1426, 690), 'text', 'state'], [(510, 703), (686, 743), 'text', 'postal'], [(1163, 703), (1260, 743), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            address=address+' '+value
                        address=address.lstrip()
                        inventor['inventor_3']['address']=address
                img=cv2.imread(page_lst[0])
                n=0
                roi=[[(675, 2293), (720, 2331), 'check_box', 'US Residency'], [(944, 2296), (996, 2334), 'check_box', 'Non US Residency'], [(1275, 2296), (1327, 2331), 'check_box', 'Active US Military Service']] 
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                    total_pixels=cv2.countNonZero(value)
                    if total_pixels>300:
                        inventor['inventor_3']['residence']=r[3]
                        break
                img=cv2.imread(page_lst[1])
                roi=[(293, 770), (323, 806), 'check_text', '4']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    img=cv2.imread(page_lst[1])
                    n=1
                    inventor['inventor_4']={}
                    roi=[[(242, 928), (682, 960), 'text', 'first_name'], [(736, 923), (983, 966), 'text', 'middle_name'], [(1176, 920), (1510, 963), 'text', 'last_name']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        inventor['inventor_4'][r[3]]=value
                    roi=[[(503, 1190), (1386, 1230), 'text', 'line1'], [(506, 1243), (1383, 1286), 'text', 'line2'], [(323, 1293), (543, 1333), 'text', 'city'], [(1313, 1296), (1406, 1333), 'text', 'state'], [(510, 1350), (673, 1386), 'text', 'postal'], [(1163, 1346), (1270, 1386), 'text', 'country']]
                    address=''
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        address=address+' '+value
                    address=address.lstrip()
                    inventor['inventor_4']['address']=address
                    roi=[[(673, 973), (716, 1013), 'check_box', 'US Residency'], [(950, 973), (1003, 1013), 'check_box', 'Non US Residency'], [(1273, 976), (1326, 1013), 'check_box', 'Active US Military Service']] 
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                        total_pixels=cv2.countNonZero(value)
                        if total_pixels>450:
                            inventor['inventor_4']['residence']=r[3]
                            break
                    roi=[(293, 1410), (323, 1450), 'check_text', '5']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        inventor['inventor_5']={}
                        roi=[[(240, 1570), (526, 1606), 'text', 'first_name'], [(736, 1566), (970, 1606), 'text', 'middle_name'], [(1176, 1570), (1486, 1606), 'text', 'last_name']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            inventor['inventor_5'][r[3]]=value
                        roi=[[(503, 1830), (1293, 1873), 'text', 'line1'], [(503, 1886), (1306, 1926), 'text', 'line2'], [(323, 1936), (586, 1976), 'text', 'city'], [(1313, 1936), (1420, 1980), 'text', 'state'], [(513, 1986), (656, 2030), 'text', 'postal'], [(1163, 1990), (1256, 2026), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            address=address+' '+value
                        address=address.lstrip()
                        inventor['inventor_5']['address']=address
                        roi=[[(673, 1620), (720, 1656), 'check_box', 'US Residency'], [(953, 1620), (1003, 1653), 'check_box', 'Non US Residency'], [(1283, 1623), (1323, 1656), 'check_box', 'Active US Military Service']] 
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>450:
                                inventor['inventor_5']['residence']=r[3]
                                break
                        roi=[(293, 2053), (323, 2093), 'check_text', '6']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==roi[3]:
                            inventor['inventor_6']={}
                            roi=[[(243, 2210), (490, 2250), 'text', 'first_name'], [(743, 2210), (1043, 2253), 'text', 'middle_name'], [(1176, 2213), (1470, 2250), 'text', 'last_name']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                inventor['inventor_6'][r[3]]=value
                            img=cv2.imread(page_lst[2])
                            roi=[[(506, 483), (1193, 523), 'text', 'line1'], [(503, 540), (1203, 576), 'text', 'line2'], [(323, 590), (546, 626), 'text', 'city'], [(1313, 590), (1443, 630), 'text', 'state'], [(510, 643), (663, 680), 'text', 'postal'], [(1163, 640), (1270, 680), 'text', 'country']]
                            address=''
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                address=address+' '+value
                            address=address.lstrip()
                            inventor['inventor_6']['address']=address
                            img=cv2.imread(page_lst[1])
                            roi=[[(673, 2263), (716, 2300), 'check_box', 'US Residency'], [(960, 2263), (1000, 2300), 'check_box', 'Non US Residency'], [(1283, 2266), (1326, 2296), 'check_box', 'Active US Military Service']] 
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>400:
                                    inventor['inventor_6']['residence']=r[3]
                                    break
                            n=2
                            img=cv2.imread(page_lst[2])
                            roi=[(293, 703), (320, 743), 'check_text', '7']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==roi[3]:
                                inventor['inventor_7']={}
                                roi=[[(243, 863), (496, 903), 'text', 'first_name'], [(736, 863), (953, 903), 'text', 'middle_name'], [(1176, 863), (1413, 903), 'text', 'last_name']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    inventor['inventor_7'][r[3]]=value
                                roi=[[(506, 1126), (1530, 1170), 'text', 'line1'], [(506, 1183), (1450, 1220), 'text', 'line2'], [(323, 1233), (593, 1273), 'text', 'city'], [(1313, 1233), (1416, 1273), 'text', 'state'], [(510, 1283), (656, 1323), 'text', 'postal'], [(1163, 1283), (1293, 1320), 'text', 'country']]
                                address=''
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    address=address+' '+value
                                address=address.lstrip()
                                inventor['inventor_7']['address']=address
                                roi=[[(676, 910), (720, 953), 'check_box', 'US Residency'], [(953, 913), (1000, 950), 'check_box', 'Non US Residency'], [(1283, 916), (1326, 950), 'check_box', 'Active US Military Service']] 
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>400:
                                        inventor['inventor_7']['residence']=r[3]
                                        break
                                roi=[(296, 1352), (318, 1384), 'check_text', '8']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                if value==roi[3]:
                                    inventor['inventor_8']={}
                                    roi=[[(240, 1506), (493, 1543), 'text', 'first_name'], [(740, 1503), (1006, 1546), 'text', 'middle_name'], [(1176, 1503), (1490, 1543), 'text', 'last_name']]
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        inventor['inventor_8'][r[3]]=value
                                    roi=[[(503, 1766), (1300, 1810), 'text', 'line1'], [(503, 1826), (1290, 1863), 'text', 'line2'], [(323, 1876), (563, 1913), 'text', 'city'], [(1310, 1876), (1480, 1916), 'text', 'state'], [(513, 1926), (706, 1966), 'text', 'postal'], [(1163, 1926), (1286, 1963), 'text', 'country']]
                                    address=''
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        address=address+' '+value
                                    address=address.lstrip()
                                    inventor['inventor_8']['address']=address
                                    roi=[[(673, 1550), (720, 1593), 'check_box', 'US Residency'], [(950, 1556), (1000, 1590), 'check_box', 'Non US Residency'], [(1276, 1560), (1330, 1590), 'check_box', 'Active US Military Service']] 
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                        total_pixels=cv2.countNonZero(value)
                                        if total_pixels>400:
                                            inventor['inventor_8']['residence']=r[3]
                                            break
                                    roi=[(293, 1993), (320, 2030), 'check_text', '9']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    if value==roi[3]:
                                        inventor['inventor_9']={}
                                        roi=[[(240, 2150), (533, 2186), 'text', 'first_name'], [(740, 2146), (1063, 2186), 'text', 'middle_name'], [(1176, 2150), (1486, 2186), 'text', 'last_name']]
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            inventor['inventor_9'][r[3]]=value
                                        img=cv2.imread(page_lst[3])
                                        n=3
                                        roi=[[(503, 430), (1256, 473), 'text', 'line1'], [(510, 490), (1280, 523), 'text', 'line2'], [(323, 536), (550, 576), 'text', 'city'], [(1313, 536), (1446, 576), 'text', 'state'], [(510, 590), (680, 626), 'text', 'postal'], [(1163, 590), (1293, 626), 'text', 'country']]
                                        address=''
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            address=address+' '+value
                                        address=address.lstrip()
                                        inventor['inventor_9']['address']=address
                                        img=cv2.imread(page_lst[2])
                                        n=2
                                        roi=[[(673, 2196), (720, 2236), 'check_box', 'US Residency'], [(953, 2200), (1003, 2233), 'check_box', 'Non US Residency'], [(1280, 2203), (1326, 2233), 'check_box', 'Active US Military Service']] 
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                            total_pixels=cv2.countNonZero(value)
                                            if total_pixels>400:
                                                inventor['inventor_9']['residence']=r[3]
                                                break
                                        img=cv2.imread(page_lst[3])
                                        n=3
                                        roi=[(298, 658), (338, 692), 'check_text', '10']
                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        if value==roi[3]:
                                            inventor['inventor_10']={}
                                            roi=[[(244, 814), (560, 850), 'text', 'first_name'], [(742, 810), (1044, 852), 'text', 'middle_name'], [(1180, 814), (1472, 852), 'text', 'last_name']]
                                            for x,r in enumerate(roi):
                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                inventor['inventor_10'][r[3]]=value
                                            roi=[[(506, 1074), (1416, 1116), 'text', 'line1'], [(506, 1132), (1426, 1172), 'text', 'line2'], [(324, 1182), (660, 1218), 'text', 'city'], [(1314, 1182), (1440, 1222), 'text', 'state'], [(512, 1234), (690, 1268), 'text', 'postal'], [(1164, 1234), (1308, 1270), 'text', 'country']]
                                            address=''
                                            for x,r in enumerate(roi):
                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                address=address+' '+value
                                            address=address.lstrip()
                                            inventor['inventor_10']['address']=address
                                            roi=[[(678, 864), (720, 900), 'check_box', 'US Residency'], [(958, 864), (1006, 894), 'check_box', 'Non US Residency'], [(1284, 866), (1332, 898), 'check_box', 'Active US Militiray Service']] 
                                            for x,r in enumerate(roi):
                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                total_pixels=cv2.countNonZero(value)
                                                if total_pixels>400:
                                                    inventor['inventor_10']['residence']=r[3]
                                                    break
        else:
            roi=[(298, 794), (318, 826), 'check_text', '1']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value= value.rstrip()
            if value==roi[3]:
                inventor['inventor_1']={}
                roi=[[(240, 950), (692, 982), 'text', 'first_name'], [(738, 948), (1140, 988), 'text', 'middle_name'], [(1176, 950), (1630, 986), 'text', 'last_name']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    inventor['inventor_1'][r[3]]=value
                roi=[[(502, 1211), (1739, 1253), 'text', 'line1'], [(506, 1268), (1737, 1302), 'text', 'line2'], [(322, 1315), (964, 1353), 'text', 'city'], [(1313, 1317), (1735, 1353), 'text', 'state'], [(513, 1371), (839, 1404), 'text', 'postal'], [(1164, 1368), (1375, 1404), 'text', 'country']]
                address=''
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    address=address+' '+value
                address=address.lstrip()
                inventor['inventor_1']['address']=address
                roi= [[(677, 1002), (715, 1033), 'check_box', 'US Residency'], [(962, 999), (1004, 1031), 'check_box', 'Non US Residency'], [(1284, 1002), (1328, 1035), 'check_box', 'Active US Military Service']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                    total_pixels=cv2.countNonZero(value)
                    if total_pixels>150:
                        inventor['inventor_1']['residence']=r[3]
                        break
                roi=[(296, 1433), (320, 1470), 'check_text', '2']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value= value.rstrip()
                if value==roi[3]:
                    inventor['inventor_2']={}
                    roi=[[(240, 1593), (700, 1626), 'text', 'first_name'], [(736, 1590), (1143, 1626), 'text', 'middle_name'], [(1176, 1590), (1636, 1626), 'text', 'last_name']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        inventor['inventor_2'][r[3]]=value
                    roi=[[(503, 1853), (1726, 1893), 'text', 'line1'], [(510, 1913), (1726, 1946), 'text', 'line2'], [(320, 1960), (860, 1996), 'text', 'city'], [(1313, 1960), (1566, 1996), 'text', 'state'], [(513, 2013), (743, 2046), 'text', 'postal'], [(1163, 2010), (1393, 2046), 'text', 'country']]
                    address=''
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        address=address+' '+value
                    address=address.lstrip()
                    inventor['inventor_2']['address']=address
                    roi= [[(673, 1640), (720, 1680), 'check_box', 'US Residency'], [(963, 1643), (1003, 1676), 'check_box', 'Non US Residency'], [(1296, 1643), (1330, 1676), 'check_box', 'Active US Military Service']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                        total_pixels=cv2.countNonZero(value)
                        if total_pixels>150:
                            inventor['inventor_2']['residence']=r[3]
                            break
                    roi=[(293, 2080), (320, 2113), 'check_text', '3']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value= value.rstrip()
                    if value==roi[3]:
                        inventor['inventor_3']={}
                        roi=[[(238, 2233), (513, 2270), 'text', 'first_name'], [(736, 2233), (1130, 2273), 'text', 'middle_name'], [(1168, 2236), (1513, 2270), 'text', 'last_name']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            inventor['inventor_3'][r[3]]=value
                        roi= [[(673, 2283), (720, 2316), 'check_box', 'US Residency'], [(963, 2286), (1006, 2316), 'check_box', 'Non US Residency'], [(1283, 2286), (1330, 2316), 'check_box', 'Active US Military Service']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>150:
                                inventor['inventor_3']['residence']=r[3]
                                break
                        img=cv2.imread(page_lst[1])
                        n=1
                        roi=[[(504, 546), (1610, 586), 'text', 'line1'], [(508, 604), (1648, 642), 'text', 'line2'], [(322, 656), (950, 688), 'text', 'city'], [(1312, 654), (1662, 694), 'text', 'state'], [(512, 706), (850, 742), 'text', 'postal'], [(1164, 704), (1370, 742), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            address=address+' '+value
                        address=address.lstrip()
                        inventor['inventor_3']['address']=address
                        roi=[(296, 768), (320, 806), 'check_text', '4']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value= value.rstrip()
                        if value==roi[3]:
                            inventor['inventor_4']={}
                            roi=[[(240, 928), (688, 964), 'text', 'first_name'], [(738, 926), (1128, 966), 'text', 'middle_name'], [(1176, 928), (1590, 964), 'text', 'last_name']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                inventor['inventor_4'][r[3]]=value
                            roi=[[(502, 1190), (1712, 1232), 'text', 'line1'], [(508, 1248), (1720, 1284), 'text', 'line2'], [(322, 1296), (968, 1332), 'text', 'city'], [(1312, 1296), (1558, 1336), 'text', 'state'], [(512, 1350), (842, 1384), 'text', 'postal'], [(1164, 1346), (1416, 1384), 'text', 'country']]
                            address=''
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                address=address+' '+value
                            address=address.lstrip()
                            inventor['inventor_4']['address']=address
                            roi= [[(674, 978), (720, 1014), 'check_box', 'US Residency'], [(934, 978), (996, 1010), 'check_box', 'Non US Residency'], [(1278, 980), (1330, 1014), 'check_box', 'Active US Military Service']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>150:
                                    inventor['inventor_4']['residence']=r[3]
                                    break
                            roi=[(294, 1412), (319, 1447), 'check_text', '5']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            if value==roi[3]:
                                inventor['inventor_5']={}
                                roi=[[(239, 1569), (682, 1604), 'text', 'first_name'], [(737, 1569), (1089, 1607), 'text', 'middle_name'], [(1174, 1569), (1524, 1607), 'text', 'last_name']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    inventor['inventor_5'][r[3]]=value
                                roi=[[(500, 1830), (1656, 1870), 'text', 'line1'], [(506, 1893), (1683, 1926), 'text', 'line2'], [(320, 1940), (943, 1973), 'text', 'city'], [(1310, 1936), (1623, 1980), 'text', 'state'], [(513, 1990), (853, 2026), 'text', 'postal'], [(1163, 1990), (1320, 2023), 'text', 'country']]
                                address=''
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    address=address+' '+value
                                address=address.lstrip()
                                inventor['inventor_5']['address']=address
                                roi= [[(673, 1620), (716, 1656), 'check_box', 'US Residency'], [(946, 1620), (1003, 1653), 'check_box', 'Non US Residency'], [(1280, 1623), (1326, 1653), 'check_box', 'Active US Military Service']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>150:
                                        inventor['inventor_5']['residence']=r[3]
                                        break
                                roi=[(296, 2056), (320, 2090), 'check_text', '6']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value= value.rstrip()
                                if value==roi[3]:
                                    inventor['inventor_6']={}
                                    roi=[[(240, 2213), (680, 2246), 'text', 'first_name'], [(736, 2213), (1106, 2250), 'text', 'middle_name'], [(1176, 2213), (1630, 2246), 'text', 'last_name']]
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        inventor['inventor_6'][r[3]]=value
                                    roi= [[(673, 2263), (716, 2300), 'check_box', 'US Residency'], [(936, 2263), (996, 2296), 'check_box', 'Non US Residency'], [(1270, 2266), (1326, 2300), 'check_box', 'Active US Military Service']]
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                        total_pixels=cv2.countNonZero(value)
                                        if total_pixels>150:
                                            inventor['inventor_6']['residence']=r[3]
                                            break
                                    n=2
                                    img=cv2.imread(page_lst[2])
                                    roi=[[(504, 482), (1724, 524), 'text', 'line1'], [(504, 542), (1712, 580), 'text', 'line2'], [(322, 590), (968, 626), 'text', 'city'], [(1314, 590), (1650, 626), 'text', 'state'], [(512, 642), (876, 678), 'text', 'postal'], [(1164, 640), (1384, 678), 'text', 'country']]
                                    address=''
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        address=address+' '+value
                                    address=address.lstrip()
                                    inventor['inventor_6']['address']=address
                                    roi=[(296, 708), (318, 742), 'check_text', '7']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value= value.rstrip()
                                    if value==roi[3]:
                                        inventor['inventor_7']={}
                                        roi=[[(242, 864), (688, 902), 'text', 'first_name'], [(738, 864), (1084, 904), 'text', 'middle_name'], [(1176, 864), (1612, 900), 'text', 'last_name']]
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            inventor['inventor_7'][r[3]]=value
                                        roi=[[(506, 1128), (1734, 1168), 'text', 'line1'], [(506, 1184), (1730, 1218), 'text', 'line2'], [(234, 962), (640, 1000), 'text', 'city'], [(1312, 1232), (1652, 1270), 'text', 'state'], [(512, 1286), (894, 1320), 'text', 'postal'], [(1164, 1284), (1404, 1322), 'text', 'country']]
                                        address=''
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            address=address+' '+value
                                        address=address.lstrip()
                                        inventor['inventor_7']['address']=address
                                        roi= [[(678, 914), (716, 950), 'check_box', 'US Residency'], [(948, 916), (994, 946), 'check_box', 'Non US Residency'], [(1282, 918), (1326, 948), 'check_box', 'Active US Military Service']]
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                            total_pixels=cv2.countNonZero(value)
                                            if total_pixels>150:
                                                inventor['inventor_7']['residence']=r[3]
                                                break
            else:
                inventor={}
                file['inventor']=inventor
                roi=[(126, 806), (320, 838), 'check_text', 'Inventor 1']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    print('inventor type7')
                    inventor['inventor_1']={}
                    roi=[[(238, 962), (688, 1000), 'text', 'first_name'], [(722, 960), (1126, 1000), 'text', 'middle_name'], [(1162, 960), (1544, 998), 'text', 'last_name']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        inventor['inventor_1'][r[3]]=value
                    roi=[[(497, 1222), (1712, 1264), 'text', 'line1'], [(494, 1279), (1712, 1317), 'text', 'line2'], [(319, 1329), (492, 1364), 'text', 'city'], [(1297, 1329), (1424, 1367), 'text', 'state'], [(507, 1382), (624, 1417), 'text', 'postal'], [(1159, 1382), (1314, 1419), 'text', 'country']]
                    address=''
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        address=address+' '+value
                    address=address.lstrip()
                    inventor['inventor_1']['address']=address
                    roi= [[(674, 1009), (717, 1047), 'check_box', 'US Residency'], [(949, 1009), (989, 1047), 'check_box', 'Non US Residency'], [(1277, 1009), (1319, 1047), 'check_box', 'Active US Military Service']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                        total_pixels=cv2.countNonZero(value)
                        if total_pixels>350:
                            inventor['inventor_1']['residence']=r[3]
                            break
                    roi=[(127, 1447), (322, 1479), 'check_text', 'Inventor 2']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        inventor['inventor_2']={}
                        roi=[[(237, 1602), (697, 1639), 'text', 'first_name'], [(722, 1602), (1144, 1639), 'text', 'middle_name'], [(1162, 1602), (1624, 1639), 'text', 'last_name']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            inventor['inventor_2'][r[3]]=value
                        roi=[[(490, 1866), (1710, 1903), 'text', 'line1'], [(490, 1923), (1706, 1960), 'text', 'line2'], [(306, 1970), (546, 2010), 'text', 'city'], [(1296, 1973), (1436, 2013), 'text', 'state'], [(496, 2023), (610, 2060), 'text', 'postal'], [(1150, 2023), (1303, 2056), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            address=address+' '+value
                        address=address.lstrip()
                        inventor['inventor_2']['address']=address
                        roi= [[(680, 1653), (716, 1690), 'check_box', 'US Residency'], [(950, 1650), (990, 1686), 'check_box', 'Non US Residency'], [(1276, 1653), (1323, 1690), 'check_box', 'Active US Military Service']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>350:
                                inventor['inventor_2']['residence']=r[3]
                                break
                        roi=[(123, 2086), (326, 2123), 'check_text', 'Inventor 3']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==roi[3]:
                            inventor['inventor_3']={}
                            roi=[[(233, 2246), (586, 2280), 'text', 'first_name'], [(723, 2246), (1103, 2283), 'text', 'middle_name'], [(1163, 2246), (1566, 2283), 'text', 'last_name']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                inventor['inventor_3'][r[3]]=value
                            roi= [[(680, 1653), (716, 1690), 'check_box', 'US Residency'], [(950, 1650), (990, 1686), 'check_box', 'Non US Residency'], [(1276, 1653), (1323, 1690), 'check_box', 'Active US Military Service']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>350:
                                    inventor['inventor_3']['residence']=r[3]
                                    break
                            img=cv2.imread(page_lst[1])
                            roi=[[(492, 546), (1728, 592), 'text', 'line1'], [(492, 602), (1728, 642), 'text', 'line2'], [(306, 654), (574, 692), 'text', 'city'], [(1304, 654), (1528, 692), 'text', 'state'], [(498, 704), (692, 742), 'text', 'postal'], [(1150, 706), (1278, 744), 'text', 'country']]
                            address=''
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                address=address+' '+value
                            address=address.lstrip()
                            inventor['inventor_3']['address']=address
                            roi=[(124, 772), (332, 804), 'text', 'Inventor 4']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==roi[3]:
                                inventor['inventor_4']={}
                                roi=[[(232, 926), (684, 966), 'text', 'first_name'], [(724, 926), (1140, 968), 'text', 'middle_name'], [(1162, 928), (1626, 966), 'text', 'last_name']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    inventor['inventor_4'][r[3]]=value
                                roi=[[(496, 1188), (1740, 1232), 'text', 'line1'], [(488, 1248), (1738, 1286), 'text', 'line2'], [(310, 1298), (952, 1334), 'text', 'city'], [(1302, 1298), (1706, 1336), 'text', 'state'], [(502, 1348), (864, 1384), 'text', 'postal'], [(1152, 1348), (1396, 1386), 'text', 'country']]
                                address=''
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    address=address+' '+value
                                address=address.lstrip()
                                inventor['inventor_4']['address']=address
                                roi= [[(678, 978), (716, 1014), 'check_box', 'US Residency'], [(950, 978), (990, 1014), 'check_box', 'Non US Residency'], [(1280, 978), (1322, 1014), 'check_box', 'Active US Military Service']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>350:
                                        inventor['inventor_4']['residence']=r[3]
                                        break
    else:
        img=cv2.imread(page_lst[0])
        n=0
        roi=[(154, 832), (292, 866), 'check_text', 'Inventor']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
        value=value.rstrip()
        if value==roi[3]:
            print('inventor type2')
            inventor={}
            file['inventor']=inventor
            roi=[(314, 832), (344, 866), 'check_text', '1']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value= value.rstrip()
            if value==roi[3]:
                inventor['inventor_1']={}
                roi=[[(250, 980), (532, 1020), 'text', 'first_name'], [(732, 982), (968, 1018), 'text', 'middle_name'], [(1156, 982), (1498, 1022), 'text', 'last_name']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    inventor['inventor_1'][r[3]]=value
                roi=[[(505, 1288), (1282, 1328), 'text', 'line1'], [(505, 1342), (1294, 1380), 'text', 'line2'], [(331, 1391), (497, 1428), 'text', 'city'], [(1288, 1394), (1548, 1431), 'text', 'state'], [(517, 1442), (691, 1477), 'text', 'postal'], [(1142, 1442), (1280, 1480), 'text', 'country']]
                address=''
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    address=address+' '+value
                address=address.lstrip()
                inventor['inventor_1']['address']=address
                roi= [[(684, 1028), (731, 1068), 'Check_box', 'US Residency'], [(946, 1028), (993, 1068), 'check_box', 'Non US Residency'], [(1268, 1028), (1312, 1068), 'check_box', 'Active US Military Service']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                    total_pixels=cv2.countNonZero(value)
                    if total_pixels>350:
                        inventor['inventor_1']['residence']=r[3]
                        break
            roi=[(314, 1505), (345, 1540), 'check_text', '2']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                inventor['inventor_2']={}
                roi=[[(254, 1654), (517, 1697), 'text', 'first_name'], [(734, 1654), (1008, 1694), 'text', 'middle_name'], [(1154, 1654), (1377, 1694), 'text', 'last_name']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    inventor['inventor_2'][r[3]]=value
                roi=[[(503, 1956), (1074, 2003), 'text', 'line1'], [(503, 2012), (1087, 2049), 'text', 'line2'], [(334, 2059), (584, 2099), 'text', 'city'], [(1284, 2062), (1537, 2099), 'text', 'state'], [(512, 2109), (734, 2149), 'text', 'postal'], [(1143, 2109), (1343, 2149), 'text', 'country']]
                address=''
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    address=address+' '+value
                address=address.lstrip()
                inventor['inventor_2']['address']=address
                roi= [[(687, 1703), (731, 1740), 'check_box', 'US Residency'], [(949, 1703), (993, 1740), 'check_box', 'Non US Residency'], [(1268, 1703), (1312, 1740), 'check_box', 'Active US Military Service']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                    total_pixels=cv2.countNonZero(value)
                    if total_pixels>350:
                        inventor['inventor_2']['residence']=r[3]
                        break
                roi=[(316, 2176), (343, 2206), 'check_text', '3']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    inventor['inventor_3']={}
                    if len(page_lst)>1:
                        img = cv2.imread(page_lst[1])
                        n=1
                        roi=[[(255, 468), (501, 505), 'text', 'first_name'], [(726, 466), (981, 506), 'text', 'middle_name'], [(1151, 468), (1438, 506), 'text', 'last_name']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            inventor['inventor_3'][r[3]]=value
                        roi=[[(505, 720), (1408, 761), 'text', 'line1'], [(505, 775), (1421, 811), 'text', 'line2'], [(333, 823), (606, 860), 'text', 'city'], [(1280, 823), (1450, 861), 'text', 'state'], [(513, 873), (678, 910), 'text', 'postal'], [(1135, 870), (1218, 908), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            address=address+' '+value
                        address=address.lstrip()
                        inventor['inventor_3']['address']=address
                        roi=[[(683, 515), (723, 551), 'check_box', 'US Residency'], [(945, 515), (988, 551), 'check_box', 'Non US Residency'], [(1263, 515), (1303, 551), 'Check_box', 'Active US Military Service']] 
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>350:
                                inventor['inventor_3']['residence']=r[3]
                                break
                    roi=[(313, 936), (345, 968), 'check_text', '4']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        inventor['inventor_4']={}
                        if len(page_lst)>1:
                            img = cv2.imread(page_lst[1])
                            n=1
                            roi=[[(256, 1086), (510, 1122), 'text', 'first_name'], [(726, 1084), (1044, 1122), 'text', 'middle_name'], [(1150, 1084), (1426, 1124), 'text', 'last_name']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                inventor['inventor_4'][r[3]]=value
                            roi=[[(506, 1390), (1093, 1428), 'text', 'line1'], [(506, 1443), (1149, 1478), 'text', 'line2'], [(334, 1490), (684, 1524), 'text', 'city'], [(1281, 1493), (1540, 1528), 'text', 'state'], [(515, 1540), (721, 1578), 'text', 'postal'], [(1137, 1540), (1315, 1578), 'text', 'country']]
                            address=''
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                address=address+' '+value
                            address=address.lstrip()
                            inventor['inventor_4']['address']=address
                            roi=[[(681, 1131), (724, 1168), 'Check_box', 'US Residency'], [(943, 1131), (987, 1168), 'check_box', 'Non US Residency'], [(1259, 1131), (1303, 1171), 'check_box', 'Active US Military Service']] 
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>350:
                                    inventor['inventor_4']['residence']=r[3]
                                    break
                        roi=[(318, 1606), (343, 1637), 'check_text', '5']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==roi[3]:
                            inventor['inventor_5']={}
                            if len(page_lst)>1:
                                img = cv2.imread(page_lst[1])
                                n=1
                                roi=[[(256, 1756), (506, 1790), 'text', 'first_name'], [(728, 1756), (1006, 1790), 'text', 'middle_name'], [(1149, 1753), (1465, 1790), 'text', 'last_name']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    inventor['inventor_5'][r[3]]=value
                                roi=[[(510, 2056), (1156, 2096), 'text', 'line1'], [(510, 2113), (1170, 2146), 'text', 'line2'], [(336, 2156), (556, 2196), 'text', 'city'], [(1283, 2160), (1650, 2193), 'text', 'state'], [(516, 2206), (636, 2246), 'text', 'postal'], [(1136, 2206), (1253, 2243), 'text', 'country']]
                                address=''
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    address=address+' '+value
                                address=address.lstrip()
                                inventor['inventor_5']['address']=address
                                roi=[[(683, 1800), (726, 1840), 'check_box', 'US Residency'], [(943, 1800), (990, 1840), 'check_box', 'Non US Residency'], [(1260, 1800), (1306, 1840), 'check_box', 'Active US Military Service']] 
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>350:
                                        inventor['inventor_5']['residence']=r[3]
                                        break
        else:
            img=cv2.imread(page_lst[0])
            n=0
            roi=[(139, 779), (312, 822), 'check_text', 'Inventor']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                print('inventor type3')
                inventor={}
                file['inventor']=inventor
                roi=[(154, 846), (362, 878), 'check_text', 'Inventor 1']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value= value.rstrip()
                if value==roi[3]:
                    inventor['inventor_1']={}
                    roi=[[(256, 984), (646, 1020), 'text', 'first_name'], [(730, 984), (1128, 1020), 'text', 'middle_name'], [(1152, 984), (1604, 1020), 'text', 'last_name']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        inventor['inventor_1'][r[3]]=value
                    roi=[[(506, 1214), (1706, 1254), 'text', 'line1'], [(506, 1266), (1710, 1298), 'text', 'line2'], [(332, 1310), (578, 1342), 'text', 'city'], [(1282, 1310), (1506, 1342), 'text', 'state'], [(514, 1354), (680, 1388), 'text', 'postal'], [(1138, 1354), (1344, 1386), 'text', 'country']]
                    address=''
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        address=address+' '+value
                    address=address.lstrip()
                    inventor['inventor_1']['address']=address
                    roi= [[(684, 1028), (726, 1060), 'check_box', 'US Residency'], [(946, 1028), (986, 1062), 'check_box', 'Non US Residency'], [(1262, 1028), (1306, 1060), 'check_box', 'Active US Military Service']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                        total_pixels=cv2.countNonZero(value)
                        if total_pixels>350:
                            inventor['inventor_1']['residence']=r[3]
                            break
                    roi=[(159, 1412), (384, 1442), 'check_text', 'Inventor 2']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value= value.rstrip()
                    if value==roi[3]:
                        inventor['inventor_2']={}
                        roi=[[(259, 1549), (582, 1582), 'text', 'first_name'], [(729, 1549), (1074, 1584), 'text', 'middle_name'], [(1152, 1552), (1484, 1582), 'text', 'last_name']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            inventor['inventor_2'][r[3]]=value
                        roi=[[(508, 1782), (1517, 1817), 'text', 'line1'], [(508, 1831), (1528, 1862), 'text', 'line2'], [(334, 1877), (597, 1908), 'text', 'city'], [(1282, 1877), (1517, 1908), 'text', 'state'], [(517, 1920), (711, 1951), 'text', 'postal'], [(1140, 1920), (1251, 1954), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            address=address+' '+value
                        address=address.lstrip()
                        inventor['inventor_2']['address']=address
                        roi= [[(682, 1594), (725, 1628), 'check_box', 'US Residency'], [(945, 1591), (988, 1628), 'check_box', 'Non US Residency'], [(1260, 1594), (1308, 1628), 'check_box', 'Active US Military Service']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>350:
                                inventor['inventor_2']['residence']=r[3]
                                break
                        roi=[(160, 1976), (383, 2010), 'check_text', 'Inventor 3']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value= value.rstrip()
                        if value==roi[3]:
                            inventor['inventor_3']={}
                            roi=[[(260, 2116), (626, 2150), 'text', 'first_name'], [(733, 2113), (1123, 2150), 'text', 'middle_name'], [(1153, 2113), (1570, 2146), 'text', 'last_name']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                inventor['inventor_3'][r[3]]=value
                            roi= [[(686, 2160), (726, 2193), 'check_box', 'US Residency'], [(950, 2156), (993, 2193), 'check_box', 'Non US Residency'], [(1266, 2156), (1310, 2193), 'check_box', 'Active US Military Service']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>350:
                                    inventor['inventor_3']['residence']=r[3]
                                    break
                            img = cv2.imread(page_lst[1])
                            roi=[[(502, 666), (1582, 704), 'text', 'line1'], [(502, 718), (1590, 748), 'text', 'line2'], [(330, 762), (720, 796), 'text', 'city'], [(1278, 762), (1624, 792), 'text', 'state'], [(512, 806), (760, 840), 'text', 'postal'], [(1136, 806), (1408, 838), 'text', 'country']]
                            address=''
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                address=address+' '+value
                            address=address.lstrip()
                            inventor['inventor_3']['address']=address
                            roi=[(156, 860), (370, 894), 'check_text', 'Inventor 4']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            if value==roi[3]:
                                img = cv2.imread(page_lst[1])
                                n=1
                                inventor['inventor_4']={}
                                roi=[[(256, 1002), (704, 1038), 'text', 'first_name'], [(730, 1002), (1118, 1034), 'text', 'middle_name'], [(1148, 1002), (1574, 1034), 'text', 'last_name']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    inventor['inventor_4'][r[3]]=value
                                img = cv2.imread(page_lst[1])
                                roi=[[(506, 1233), (1659, 1266), 'text', 'line1'], [(506, 1282), (1657, 1317), 'text', 'line2'], [(333, 1326), (906, 1359), 'text', 'city'], [(1279, 1328), (1606, 1359), 'text', 'state'], [(513, 1373), (857, 1404), 'text', 'postal'], [(1135, 1373), (1302, 1402), 'text', 'country']]
                                address=''
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    address=address+' '+value
                                address=address.lstrip()
                                inventor['inventor_4']['address']=address
                                roi= [[(682, 1046), (722, 1077), 'check_box', 'US Residency'], [(944, 1046), (984, 1077), 'check_box', 'Non US Residency'], [(1262, 1046), (1304, 1077), 'check_box', 'Active US Military Service']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>350:
                                        inventor['inventor_4']['residence']=r[3]
                                        break
            else:
                img=cv2.imread(page_lst[0])
                n=0
                roi=[(156, 822), (282, 852), 'check_text', 'Inventor']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    print('inventor type4')
                    inventor={}
                    file['inventor']=inventor
                    roi=[(318, 824), (334, 852), 'check_text', '1']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value= value.rstrip()
                    if value==roi[3]:
                        inventor['inventor_1']={}
                        roi=[[(252, 970), (680, 1008), 'text', 'first_name'], [(728, 972), (1092, 1010), 'text', 'middle_name'], [(1154, 970), (1538, 1010), 'text', 'last_name']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            inventor['inventor_1'][r[3]]=value
                        roi=[[(502, 1224), (1591, 1268), 'text', 'line1'], [(499, 1279), (1624, 1317), 'text', 'line2'], [(328, 1328), (719, 1364), 'text', 'city'], [(1279, 1331), (1508, 1368), 'text', 'state'], [(508, 1377), (726, 1413), 'text', 'postal'], [(1137, 1379), (1344, 1417), 'text', 'country']]
                        address=''
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            address=address+' '+value
                        address=address.lstrip()
                        inventor['inventor_1']['address']=address
                        roi= [[(682, 1017), (722, 1055), 'check_box', 'US Residency'], [(946, 1019), (988, 1055), 'check_box', 'Non US Residency'], [(1262, 1019), (1304, 1055), 'check_box', 'Active US Military Service']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>350:
                                inventor['inventor_1']['residence']=r[3]
                                break
                        roi=[(146, 1439), (406, 1475), 'check_box', 'Inventor 2']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value= value.rstrip()
                        if value==roi[3]:
                            inventor['inventor_2']={}
                            roi=[[(252, 1592), (654, 1632), 'text', 'first_name'], [(727, 1592), (1077, 1629), 'text', 'middle_name'], [(1149, 1594), (1507, 1629), 'text', 'last_name']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                inventor['inventor_2'][r[3]]=value
                            roi=[[(503, 1846), (1620, 1893), 'text', 'line1'], [(500, 1903), (1630, 1940), 'text', 'line2'], [(326, 1950), (766, 1986), 'text', 'city'], [(1276, 1953), (1630, 1986), 'text', 'state'], [(506, 2000), (823, 2036), 'text', 'postal'], [(1133, 2000), (1316, 2036), 'text', 'country']]
                            address=''
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                address=address+' '+value
                            address=address.lstrip()
                            inventor['inventor_2']['address']=address
                            roi= [[(680, 1643), (720, 1676), 'check_box', 'US Residency'], [(940, 1643), (986, 1676), 'check_box', 'Non US Residency'], [(1260, 1643), (1303, 1680), 'check_box', 'Active US Military Service']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>350:
                                    inventor['inventor_2']['residence']=r[3]
                                    break
                            roi=[(143, 2063), (350, 2096), 'check_box', 'Inventor 3']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            if value==roi[3]:
                                inventor['inventor_3']={}
                                roi=[[(246, 2213), (663, 2253), 'text', 'first_name'], [(726, 2213), (973, 2253), 'text', 'middle_name'], [(1146, 2213), (1536, 2250), 'text', 'last_name']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    inventor['inventor_3'][r[3]]=value
                                roi= [[(676, 2260), (720, 2300), 'check_box', 'US Residency'], [(940, 2263), (980, 2296), 'check_box', 'Non US Residency'], [(1256, 2260), (1300, 2300), 'check_box', 'Active US Military Service']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>350:
                                        inventor['inventor_3']['residence']=r[3]
                                        break
                                img = cv2.imread(page_lst[1])
                                roi=[[(512, 570), (1614, 618), 'text', 'line1'], [(512, 626), (1630, 668), 'text', 'line2'], [(338, 674), (786, 710), 'text', 'city'], [(1290, 678), (1530, 714), 'text', 'state'], [(522, 724), (786, 760), 'text', 'postal'], [(1148, 726), (1378, 762), 'text', 'country']]
                                address=''
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    address=address+' '+value
                                address=address.lstrip()
                                inventor['inventor_3']['address']=address
                else:
                    img=cv2.imread(page_lst[0])
                    n=0
                    roi=[(124, 838), (264, 870), 'check_text', 'Inventor']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        print('inventor type5')
                        inventor={}
                        file['inventor']=inventor
                        roi=[(118, 838), (360, 868), 'check_text', 'Inventor 1']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value= value.rstrip()
                        if value=='Inventor 1':
                            inventor['inventor_1']={}
                            roi=[[(230, 980), (666, 1014), 'text', 'first_name'], [(724, 980), (1124, 1018), 'text', 'middle_name'], [(1164, 980), (1586, 1014), 'text', 'last_name']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                inventor['inventor_1'][r[3]]=value
                            roi=[[(487, 1222), (1692, 1262), 'text', 'line1'], [(487, 1274), (1689, 1304), 'text', 'line2'], [(304, 1319), (687, 1352), 'text', 'city'], [(1297, 1319), (1534, 1352), 'text', 'state'], [(497, 1367), (732, 1399), 'text', 'postal'], [(1149, 1367), (1382, 1399), 'text', 'country']]
                            address=''
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                address=address+' '+value
                            address=address.lstrip()
                            inventor['inventor_1']['address']=address
                            roi= [[(677, 1027), (717, 1059), 'check_box', 'US Residency'], [(947, 1027), (989, 1059), 'check_box', 'Non US Residency'], [(1279, 1027), (1322, 1059), 'check_box', 'Active US Military Service']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>350:
                                    inventor['inventor_1']['residence']=r[3]
                                    break
                            roi=[(122, 1427), (347, 1457), 'check_box', 'Inventor 2']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            if value==roi[3]:
                                inventor['inventor_2']={}
                                roi=[[(229, 1569), (664, 1602), 'text', 'first_name'], [(722, 1569), (1092, 1602), 'text', 'middle_name'], [(1162, 1569), (1594, 1604), 'text', 'last_name']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    inventor['inventor_2'][r[3]]=value
                                roi=[[(490, 1813), (1663, 1846), 'text', 'line1'], [(490, 1863), (1686, 1893), 'text', 'line2'], [(310, 1906), (676, 1940), 'text', 'city'], [(1296, 1906), (1523, 1940), 'text', 'state'], [(500, 1953), (750, 1990), 'text', 'postal'], [(1146, 1953), (1350, 1986), 'text', 'country']]
                                address=''
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    address=address+' '+value
                                address=address.lstrip()
                                inventor['inventor_2']['address']=address
                                roi= [[(677, 1614), (717, 1647), 'check_box', 'US Residency'], [(949, 1614), (989, 1649), 'check_box', 'Non US Residency'], [(1277, 1614), (1319, 1649), 'check_box', 'Active US Military Service']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>350:
                                        inventor['inventor_2']['residence']=r[3]
                                        break
                                roi=[(123, 2013), (346, 2046), 'check_text', 'Inventor 3']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value= value.rstrip()
                                if value==roi[3]:
                                    inventor['inventor_3']={}
                                    roi=[[(230, 2156), (543, 2193), 'text', 'first_name'], [(723, 2156), (1030, 2186), 'text', 'middle_name'], [(1160, 2160), (1523, 2190), 'text', 'last_name']]
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        inventor['inventor_3'][r[3]]=value
                                    roi= [[(676, 2200), (720, 2240), 'check_box', 'US Residency'], [(946, 2203), (990, 2240), 'check_box', 'Non US Residency'], [(1276, 2200), (1323, 2236), 'check_box', 'Active US Military Service']]
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                        total_pixels=cv2.countNonZero(value)
                                        if total_pixels>350:
                                            inventor['inventor_3']['residence']=r[3]
                                            break
                                    img = cv2.imread(page_lst[1])
                                    roi=[[(488, 602), (1656, 642), 'text', 'line1'], [(488, 654), (1632, 688), 'text', 'line2'], [(306, 702), (658, 736), 'text', 'city'], [(1296, 702), (1476, 738), 'text', 'state'], [(502, 750), (688, 782), 'text', 'postal'], [(1148, 748), (1294, 782), 'text', 'country']]
                                    address=''
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        address=address+' '+value
                                    address=address.lstrip()
                                    inventor['inventor_3']['address']=address
                                    roi=[(122, 808), (352, 840), 'check_text', 'Inventor 4']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value= value.rstrip()
                                    if value==roi[3]:
                                        img = cv2.imread(page_lst[1])
                                        n=1
                                        inventor['inventor_4']={}
                                        roi=[[(226, 950), (648, 986), 'text', 'first_name'], [(724, 952), (1142, 986), 'text', 'middle_name'], [(1162, 952), (1600, 988), 'text', 'last_name']]
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            inventor['inventor_4'][r[3]]=value
                                        roi=[[(490, 1194), (1692, 1230), 'text', 'line1'], [(490, 1244), (1688, 1276), 'text', 'line2'], [(308, 1290), (822, 1324), 'text', 'city'], [(1298, 1290), (1658, 1324), 'text', 'state'], [(500, 1336), (846, 1370), 'text', 'postal'], [(1150, 1336), (1376, 1368), 'text', 'country']]
                                        address=''
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            address=address+' '+value
                                        address=address.lstrip()
                                        inventor['inventor_4']['address']=address
                                        roi= [[(676, 998), (716, 1032), 'check_box', 'US Residency'], [(950, 996), (994, 1032), 'check_box', 'Non US Residency'], [(1278, 998), (1322, 1032), 'check_box', 'Active US Military Service']]
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                            total_pixels=cv2.countNonZero(value)
                                            if total_pixels>350:
                                                inventor['inventor_4']['residence']=r[3]
                                                break
                                        roi=[(119, 1397), (339, 1427), 'check_text', 'Inventor 5']
                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value= value.rstrip()
                                        if value==roi[3]:
                                            inventor['inventor_5']={}
                                            roi=[[(227, 1539), (637, 1572), 'text', 'first_name'], [(724, 1539), (1127, 1574), 'text', 'middle_name'], [(1162, 1539), (1582, 1572), 'text', 'last_name']]
                                            for x,r in enumerate(roi):
                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                inventor['inventor_5'][r[3]]=value
                                            roi=[[(486, 1780), (1590, 1816), 'text', 'line1'], [(490, 1830), (1603, 1863), 'text', 'line2'], [(310, 1876), (663, 1913), 'text', 'city'], [(1303, 1876), (1520, 1913), 'text', 'state'], [(496, 1923), (703, 1956), 'text', 'postal'], [(1150, 1923), (1376, 1956), 'text', 'country']]
                                            address=''
                                            for x,r in enumerate(roi):
                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                address=address+' '+value
                                            address=address.lstrip()
                                            inventor['inventor_5']['address']=address
                                            roi= [[(673, 1586), (723, 1620), 'check_box', 'US Residency'], [(946, 1586), (993, 1620), 'check_box', 'Non US Residency'], [(1276, 1586), (1320, 1620), 'check_box', 'Active US Military Service']]
                                            for x,r in enumerate(roi):
                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                total_pixels=cv2.countNonZero(value)
                                                if total_pixels>350:
                                                    inventor['inventor_5']['residence']=r[3]
                                                    break
                                            roi=[(123, 1983), (340, 2016), 'check_text', 'Inventor 6']
                                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value= value.rstrip()
                                            if value==roi[3]:
                                                inventor['inventor_6']={}
                                                roi=[[(230, 2126), (623, 2163), 'text', 'first_name'], [(723, 2130), (1116, 2163), 'text', 'middle_name'], [(1160, 2126), (1546, 2160), 'text', 'last_name']]
                                                for x,r in enumerate(roi):
                                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                    value=value.rstrip()
                                                    inventor['inventor_6'][r[3]]=value
                                                roi= [[(676, 2176), (720, 2210), 'check_box', 'US Residency'], [(946, 2176), (990, 2210), 'check_box', 'Non US Residency'], [(1276, 2173), (1320, 2210), 'check_box', 'Active US Military Service']]
                                                for x,r in enumerate(roi):
                                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                    total_pixels=cv2.countNonZero(value)
                                                    if total_pixels>350:
                                                        inventor['inventor_6']['residence']=r[3]
                                                        break
                                                img = cv2.imread(page_lst[2])
                                                n=2
                                                roi=[[(490, 544), (1648, 586), 'text', 'line1'], [(488, 598), (1644, 630), 'text', 'line2'], [(306, 644), (810, 678), 'text', 'city'], [(1296, 644), (1520, 676), 'text', 'state'], [(498, 690), (792, 726), 'text', 'postal'], [(1148, 690), (1354, 724), 'text', 'country']]
                                                address=''
                                                for x,r in enumerate(roi):
                                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                    value=value.rstrip()
                                                    address=address+' '+value
                                                address=address.lstrip()
                                                inventor['inventor_6']['address']=address
                                                roi=[(120, 748), (358, 780), 'check_text', 'Inventor 7']
                                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value= value.rstrip()
                                                if value==roi[3]:
                                                    inventor['inventor_7']={}
                                                    roi=[[(226, 894), (646, 930), 'text', 'first_name'], [(722, 894), (1114, 930), 'text', 'middle_name'], [(1164, 894), (1590, 930), 'text', 'last_name']]
                                                    for x,r in enumerate(roi):
                                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                        value=value.rstrip()
                                                        inventor['inventor_7'][r[3]]=value
                                                    roi=[[(488, 1134), (1582, 1174), 'text', 'line1'], [(488, 1184), (1580, 1220), 'text', 'line2'], [(306, 1232), (718, 1264), 'textt', 'city'], [(1296, 1232), (1566, 1266), 'text', 'state'], [(498, 1278), (784, 1314), 'text', 'postal'], [(1150, 1278), (1394, 1312), 'text', 'country']]
                                                    address=''
                                                    for x,r in enumerate(roi):
                                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                        value=value.rstrip()
                                                        address=address+' '+value
                                                    address=address.lstrip()
                                                    inventor['inventor_7']['address']=address
                                                    roi= [[(674, 940), (720, 974), 'check_box', 'US Residency'], [(948, 940), (992, 974), 'check_box', 'Non US Residency'], [(1280, 940), (1320, 972), 'check_box', 'Active US Military Service']]
                                                    for x,r in enumerate(roi):
                                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                        total_pixels=cv2.countNonZero(value)
                                                        if total_pixels>350:
                                                            inventor['inventor_7']['residence']=r[3]
                                                            break
                                                    roi=[(122, 1338), (338, 1370), 'check_text', 'Inventor 8']
                                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                    value= value.rstrip()
                                                    if value==roi[3]:
                                                        inventor['inventor_8']={}
                                                        roi=[[(227, 1479), (619, 1514), 'text', 'first_name'], [(722, 1482), (1094, 1514), 'text', 'middle_name'], [(1164, 1482), (1499, 1517), 'text', 'last_name']]
                                                        for x,r in enumerate(roi):
                                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                            value=value.rstrip()
                                                            inventor['inventor_8'][r[3]]=value
                                                        roi=[[(490, 1720), (1420, 1763), 'text', 'line1'], [(490, 1776), (1436, 1806), 'text', 'line2'], [(310, 1820), (740, 1856), 'text', 'city'], [(1296, 1820), (1526, 1856), 'text', 'state'], [(500, 1866), (746, 1903), 'text', 'postal'], [(1150, 1866), (1360, 1900), 'text', 'country']]
                                                        address=''
                                                        for x,r in enumerate(roi):
                                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                            value=value.rstrip()
                                                            address=address+' '+value
                                                        address=address.lstrip()
                                                        inventor['inventor_8']['address']=address
                                                        roi= [[(673, 1530), (720, 1560), 'check_box', 'US Residency'], [(946, 1530), (993, 1563), 'check_box', 'Non US Residency'], [(1276, 1530), (1323, 1560), 'check_box', 'Active US Military Service']]
                                                        for x,r in enumerate(roi):
                                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                            total_pixels=cv2.countNonZero(value)
                                                            if total_pixels>350:
                                                                inventor['inventor_8']['residence']=r[3]
                                                                break
                                                        roi=[(116, 1926), (376, 1956), 'check_text', 'Inventor 9']
                                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                        value= value.rstrip()
                                                        if value==roi[3]:
                                                            inventor['inventor_9']={}
                                                            roi=[[(230, 2070), (656, 2103), 'text', 'first_name'], [(720, 2066), (1116, 2103), 'text', 'middle_name'], [(1160, 2070), (1606, 2106), 'text', 'last_name']]
                                                            for x,r in enumerate(roi):
                                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                value=value.rstrip()
                                                                inventor['inventor_9'][r[3]]=value
                                                            roi= [[(673, 2116), (720, 2150), 'check_box', 'US Residency'], [(946, 2113), (993, 2146), 'check_box', 'Non US Residency'], [(1273, 2113), (1323, 2150), 'check_box', 'Active US Military Service']]
                                                            for x,r in enumerate(roi):
                                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                                total_pixels=cv2.countNonZero(value)
                                                                if total_pixels>350:
                                                                    inventor['inventor_9']['residence']=r[3]
                                                                    break
                                                            img = cv2.imread(page_lst[3])
                                                            roi=[[(490, 498), (1420, 538), 'text', 'line1'], [(488, 550), (1446, 584), 'text', 'line2'], [(308, 594), (942, 632), 'text', 'city'], [(1298, 596), (1528, 630), 'text', 'state'], [(500, 644), (830, 678), 'text', 'postal'], [(1148, 644), (1358, 678), 'text', 'country']]
                                                            address=''
                                                            for x,r in enumerate(roi):
                                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                value=value.rstrip()
                                                                address=address+' '+value
                                                            address=address.lstrip()
                                                            inventor['inventor_9']['address']=address
                        else:
                            roi=[(122, 836), (340, 876), 'check_text', 'Inventor 1']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            if value==roi[3]:
                                inventor['inventor_1']={}
                                roi=[[(228, 990), (700, 1030), 'text', 'first_name'], [(722, 990), (1150, 1030), 'text', 'middle_name'], [(1160, 990), (1642, 1030), 'text', 'last_name']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    inventor['inventor_1'][r[3]]=value
                                roi=[[(488, 1306), (1742, 1344), 'text', 'line1'], [(493, 1364), (1746, 1402), 'text', 'line2'], [(306, 1413), (679, 1451), 'text', 'city'], [(1297, 1415), (1722, 1448), 'text', 'state'], [(497, 1464), (902, 1497), 'text', 'postal'], [(1151, 1464), (1448, 1502), 'text', 'country']]
                                address=''
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    address=address+' '+value
                                address=address.lstrip()
                                inventor['inventor_1']['address']=address
                                roi= [[(673, 1039), (717, 1077), 'check_box', 'US Residency'], [(948, 1039), (991, 1077), 'check_box', 'Non US Residency'], [(1275, 1039), (1319, 1077), 'check_box', 'Active US Military Service']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>350:
                                        inventor['inventor_1']['residence']=r[3]
                                        break
                                roi=[(120, 1546), (330, 1590), 'check_text', 'Inventor 2']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value= value.rstrip()
                                if value==roi[3]:
                                    inventor['inventor_2']={}
                                    roi=[[(236, 1703), (703, 1740), 'text', 'first_name'], [(723, 1703), (1143, 1740), 'text', 'middle_name'], [(1163, 1703), (1640, 1740), 'text', 'last_name']]
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        inventor['inventor_2'][r[3]]=value
                                    roi=[[(493, 1966), (1733, 2006), 'text', 'line1'], [(490, 2023), (1730, 2053), 'text', 'line2'], [(310, 2073), (586, 2110), 'text', 'city'], [(1300, 2073), (1726, 2110), 'text', 'state'], [(500, 2126), (646, 2160), 'text', 'postal'], [(1150, 2126), (1320, 2160), 'text', 'country']]
                                    address=''
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        address=address+' '+value
                                    address=address.lstrip()
                                    inventor['inventor_2']['address']=address
                                    roi= [[(676, 1753), (716, 1790), 'check_box', 'US Residency'], [(946, 1750), (990, 1790), 'check_box', 'Non US Residency'], [(1276, 1750), (1320, 1790), 'check_box', 'Active US Military Service']]
                                    for x,r in enumerate(roi):
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                        total_pixels=cv2.countNonZero(value)
                                        if total_pixels>350:
                                            inventor['inventor_2']['residence']=r[3]
                                            break
                                    roi=[(120, 2203), (343, 2246), 'check_box', 'Inventor 3']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value= value.rstrip()
                                    if value==roi[3]:
                                        n=1
                                        img=cv2.imread(page_lst[1])
                                        inventor['inventor_3']={}
                                        roi=[[(226, 432), (692, 472), 'text', 'first_name'], [(720, 434), (1144, 472), 'text', 'middle_name'], [(1160, 432), (1624, 472), 'text', 'last_name']]
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            inventor['inventor_3'][r[3]]=value
                                        roi=[[(490, 696), (1726, 738), 'text', 'line1'], [(488, 754), (1730, 792), 'text', 'line2'], [(308, 804), (650, 842), 'text', 'city'], [(1296, 804), (1564, 842), 'text', 'state'], [(498, 854), (698, 890), 'text', 'postal'], [(1150, 854), (1406, 892), 'text', 'country']]
                                        address=''
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            address=address+' '+value
                                        address=address.lstrip()
                                        inventor['inventor_3']['address']=address
                                        roi= [[(678, 482), (718, 520), 'check_box', 'US Residency'], [(948, 484), (990, 520), 'check_box', 'Non US Residency'], [(1278, 484), (1322, 520), 'check_box', 'Active US Military Service']]
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                            total_pixels=cv2.countNonZero(value)
                                            if total_pixels>350:
                                                inventor['inventor_3']['residence']=r[3]
                                                break
                    else:
                        img=cv2.imread(page_lst[0])
                        n=0
                        roi=[(124, 724), (300, 774), 'check_text', 'inventor']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==roi[3]:
                            print('inventor type6')
                            inventor={}
                            file['inventor']=inventor
                            roi=[(142, 800), (336, 836), 'check_text', 'inventor 1']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            if value==roi[3]:
                                inventor['inventor_1']={}
                                roi=[[(246, 952), (696, 988), 'text', 'first_name'], [(722, 952), (1124, 986), 'text', 'middle_name'], [(1146, 950), (1600, 982), 'text', 'last_name']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    inventor['inventor_1'][r[3]]=value
                                roi=[[(497, 1204), (1707, 1239), 'text', 'line1'], [(499, 1259), (1707, 1287), 'text', 'line2'], [(322, 1307), (967, 1342), 'text', 'city'], [(1274, 1304), (1704, 1337), 'text', 'state'], [(507, 1357), (897, 1389), 'text', 'postal'], [(1132, 1354), (1327, 1387), 'text', 'country']]
                                address=''
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    address=address+' '+value
                                address=address.lstrip()
                                inventor['inventor_1']['address']=address
                                roi= [[(677, 997), (714, 1034), 'check_box', 'US Residency'], [(937, 999), (982, 1032), 'check_box', 'Non US Residency'], [(1254, 997), (1297, 1034), 'check_box', 'Active US Military Service']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>350:
                                        inventor['inventor_1']['residence']=r[3]
                                        break
    if len(page_lst)>1:
        print(n+1)
        img = cv2.imread(page_lst[n+1])
        roi=[(124, 538), (464, 578), 'text', 'Customer Number']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
        value=value.rstrip()
        if value==roi[3]:
            roi=[(516, 542), (654, 578), 'text', 'customer_no']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            value=value.replace('P','2')
            value=value.replace('D','2')
            file['customer_no']=value
            roi=[[(1006, 806), (1200, 850), 'check_text', 'Small Entity'], [(1454, 808), (1496, 850), 'check_box', 'small_entity_status_claimed'], [(190, 1636), (686, 1686), 'check_text', 'Request Not to Publish.'], [(122, 1700), (168, 1742), 'check_box', 'request_not_to_publish']]
            for x,r in enumerate(roi):
                if r[2]=='check_text':
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==r[3]:
                        roi_r=roi[x+1]
                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                        total_pixels=cv2.countNonZero(value)
                        if total_pixels>425:
                            file[roi_r[3]]='yes'
        else:
            roi=[(151, 739), (451, 777), 'check_text', 'Customer Number']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                roi=[(519, 739), (639, 775), 'text', 'customer_no']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                value=value.replace('P','2')
                value=value.replace('D','2')
                file['customer_no']=value
                roi=[[(1006, 1002), (1419, 1042), 'check_text', 'Small Entity Status Claimed'], [(1433, 1002), (1473, 1042), 'check_box', 'small_entity_status_claimed'], [(220, 1810), (700, 1853), 'check_text', 'Request Not to Publish.'], [(153, 1866), (200, 1913), 'check_box', 'request_not_to_publish']]
                for x,r in enumerate(roi):
                    if r[2]=='check_text':
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==r[3]:
                            roi_r=roi[x+1]
                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>425:
                                file[roi_r[3]]='yes'
            else:
                roi=[(152, 740), (450, 774), 'check_text', 'Customer Number']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    roi=[(514, 740), (628, 776), 'text', 'customer_no']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    value=value.replace('P','2')
                    value=value.replace('P','2')
                    file['customer_no']=value
                    roi=[[(1002, 1002), (1422, 1040), 'check_text', 'Small Entity Status Claimed'], [(1434, 1002), (1474, 1042), 'check_box', 'small_entity_status_claimed'], [(220, 1811), (702, 1857), 'check_text', 'Request Not to Publish.'], [(157, 1868), (200, 1908), 'check_box', 'request_not_to_publish']]
                    for x,r in enumerate(roi):
                        if r[2]=='check_text':
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==r[3]:
                                roi_r=roi[x+1]
                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>425:
                                    file[roi_r[3]]='yes'
                else:
                    roi=[(534, 1589), (799, 1627), 'check_text', 'Customer Number']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        roi=[(488, 1591), (525, 1625), 'check_box', 'customer_no']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                        total_pixels=cv2.countNonZero(value)
                        if total_pixels>150:
                            roi=[[(540, 1588), (791, 1628), 'check_text', 'Customer Number'], [(484, 1642), (612, 1682), 'text', 'customer_no'], [(540, 2156), (793, 2196), 'check_text', 'Customer Number'], [(483, 2210), (613, 2250), 'text', 'customer_no']]
                            for x,r in enumerate(roi):
                                if r[2]=='check_text':
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    if value==r[3]:
                                        roi_r=roi[x+1]
                                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        value=value.replace('D','2')
                                        value=value.replace('P','9')
                                        file[roi_r[3]]=value
                        roi=[[(185, 980), (685, 1028), 'check_text', 'Request Not to Publish.'], [(125, 1045), (168, 1085), 'check_box', 'request_not_to_publish']]
                        for x,r in enumerate(roi):
                            if r[2]=='check_text':
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                if value==r[3]:
                                    roi_r=roi[x+1]
                                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>425:
                                        file[roi_r[3]]='yes'
                    else:
                        roi=[(123, 446), (440, 486), 'check_text', 'Customer Number']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==roi[3]:
                            roi=[(516, 446), (676, 483), 'text', 'customer_no']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.replace('P','2')
                            value=value.replace('D','2')
                            value=value.rstrip()
                            file[roi[3]]=value
                            roi=[[(1450, 716), (1496, 763), 'check_box', 'small_entity_status_claimed'], [(123, 1610), (170, 1656), 'check_box', 'request_not_to_publish']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>425:
                                    file[r[3]]='yes'
                        else:
                            roi=[(122, 1088), (418, 1128), 'check_text', 'Customer Number']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==roi[3]:
                                roi=[(512, 1088), (620, 1124), 'check_text', 'customer_no']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.replace('P','2')
                                value=value.replace('D','2')
                                value=value.rstrip()
                                file[roi[3]]=value
                                roi=[[(1453, 1356), (1496, 1396), 'check_box', 'small_entity_status'], [(126, 2250), (166, 2290), 'check_box', 'request_not_to_publish']]
                                for x,r in enumerate(roi):
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>425:
                                        file[r[3]]='yes'
                            else:
                                roi=[(152, 1584), (472, 1619), 'check_text', 'Customer Number']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                if value==roi[3]:
                                    roi=[(492, 1584), (712, 1619), 'text', 'customer_no']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.replace('P','2')
                                    value=value.replace('D','2')
                                    value=value.rstrip()
                                    file[roi[3]]=value
                                    roi=[(157, 1057), (199, 1097), 'check_box', 'request_not_to_publish']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>425:
                                        file[r[3]]='yes'
                                    img=cv2.imread(page_lst[n])
                                    roi=[(1433, 1946), (1470, 1983), 'check_box', 'small_entity_status_claimed']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>425:
                                        file[r[3]]='yes'
                                else:
                                    roi=[(154, 1090), (454, 1136), 'check_text', 'Customer Number']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    if value==roi[3]:
                                        roi=[(522, 1094), (772, 1132), 'text', 'customer_no']
                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        file[roi[3]]=value
                                        roi=[[(1433, 1360), (1473, 1400), 'check_box', 'small_entity_statue_claimed'], [(146, 2210), (190, 2256), 'check_box', 'request_not_to_publish']]
                                        for x,r in enumerate(roi):
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                            total_pixels=cv2.countNonZero(value)
                                            if total_pixels>425:
                                                file[r[3]]='yes'
                                    else:
                                        roi=[(124, 992), (426, 1030), 'check_text', 'Customer Number']
                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        if value==roi[3]:
                                            roi=[(498, 992), (872, 1030), 'text', 'customer_no']
                                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            file[roi[3]]=value
                                            roi=[[(1453, 1240), (1496, 1276), 'check_box', 'small_entity_status_claimed'], [(126, 2056), (166, 2093), 'check_box', 'request_not_to_publish']]
                                            for x,r in enumerate(roi):
                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                total_pixels=cv2.countNonZero(value)
                                                if total_pixels>425:
                                                    file[r[3]]='yes'
                                        else:
                                            roi=[(159, 1612), (422, 1642), 'check_text', 'Customer Number']
                                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            if value==roi[3]:
                                                roi=[(499, 1604), (614, 1642), 'text', 'customer_no']
                                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                file[roi[3]]=value
                                                roi=[(164, 1032), (209, 1074), 'check_box', 'request_not_to_publish']
                                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                total_pixels=cv2.countNonZero(value)
                                                if total_pixels>425:
                                                    file[r[3]]='yes'
                                            else:
                                                roi=[(118, 1158), (450, 1196), 'check_text', 'Customer Number']
                                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                if value==roi[3]:
                                                    roi=[(474, 1160), (672, 1200), 'text', 'customer_no']
                                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                    value=value.rstrip()
                                                    file[roi[3]]=value
                                                    roi=[(124, 558), (168, 602), 'check_box', 'request_not_to_publish']
                                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                    total_pixels=cv2.countNonZero(value)
                                                    if total_pixels>425:
                                                        file[r[3]]='yes'
                                                else:
                                                    roi=[(117, 1572), (397, 1612), 'check_text', 'Customer Number']
                                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                    value=value.rstrip()
                                                    if value==roi[3]:
                                                        roi=[(487, 1572), (612, 1609), 'text', 'customer_no']
                                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                        value=value.rstrip()
                                                        value=value.replace('D','2')
                                                        file[roi[3]]=value
                                                        roi=[(122, 972), (167, 1014), 'check_box', 'request_not_to_publish']
                                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                        total_pixels=cv2.countNonZero(value)
                                                        if total_pixels>425:
                                                            file[r[3]]='yes'
                                                    else:
                                                        if len(page_lst)>2:
                                                            img=cv2.imread(page_lst[n+2])
                                                            roi=[(150, 741), (443, 778), 'check_text', 'Customer Number']
                                                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                            value=value.rstrip()
                                                            if value==roi[3]:
                                                                roi=[(513, 740), (651, 775), 'text', 'customer']
                                                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                value=value.rstrip()
                                                                value=value.replace('P','2')
                                                                value=value.replace('D','2')
                                                                file['customer_no']=value
                                                                roi=[[(1010, 1003), (1190, 1043), 'check_text', 'Small Entity'], [(1430, 1000), (1476, 1043), 'check_box', 'small_entity_status_claimed'], [(223, 1813), (700, 1853), 'check_text', 'Request Not to Publish.'], [(153, 1866), (200, 1913), 'check_box', 'request_not_to_publish']]
                                                                for x,r in enumerate(roi):
                                                                    if r[2]=='check_text':
                                                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                        value=value.rstrip()
                                                                        if value==r[3]:
                                                                            roi_r=roi[x+1]
                                                                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                                                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                                                            total_pixels=cv2.countNonZero(value)
                                                                            if total_pixels>425:
                                                                                file[roi_r[3]]='yes'
        if len(page_lst)>2:
            img = cv2.imread(page_lst[n+2])
            roi=[(132, 682), (490, 720), 'check_text', 'Prior Application Status']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                print(1859)
                roi=[(518, 684), (662, 720), 'text', 'prior']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                file['prior_application_status']=value
                roi=[[(590, 756), (894, 804), 'check_text', 'Continuity Type'], [(518, 844), (826, 876), 'text', 'continuity'], [(953, 750), (1316, 810), 'check_text', 'Prior Application Number'], [(943, 840), (1306, 876), 'text', 'prior_application_no'], [(1386, 732), (1722, 768), 'check_text', 'Filing or 371(c) Date'], [(1342, 840), (1522, 878), 'text', 'filing_date']]
                for x,r in enumerate(roi):
                    if r[2]=='check_text':
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==r[3]:
                            roi_r=roi[x+1]
                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            file[roi_r[3]]=value
                roi=[(129, 1509), (477, 1567), 'check_text', 'Application Number']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    foreign_priority={}
                    file['foreign_priority']=foreign_priority
                    foreign_priority['foreign_priority_1']={}
                    roi=[[(129, 1509), (477, 1567), 'check_text', 'Application Number'], [(129, 1587), (292, 1619), 'text', 'app_number'], [(642, 1532), (754, 1572), 'check_text', 'Country'], [(514, 1587), (607, 1622), 'text', 'country'], [(897, 1529), (1299, 1569), 'check_text', 'Filing Date (YYYY-MM-DD)'], [(899, 1587), (1077, 1619), 'text', 'filing_date']]
                    for x,r in enumerate(roi):
                        if r[2]=='check_text':
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==r[3]:
                                roi_r = roi[x+1]
                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value= value.rstrip()
                                value=value.replace('D','2')
                                value=value.replace('P','2')
                                foreign_priority['foreign_priority_1'][roi_r[3]]=value
                    roi=[(173, 1683), (470, 1723), 'check_text', 'Application Number']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        foreign_priority['foreign_priority_2']={}
                        roi=[[(173, 1683), (470, 1723), 'check_text', 'Application Number'], [(130, 1740), (303, 1776), 'text', 'app_number'], [(633, 1680), (756, 1730), 'check_text', 'Country'], [(516, 1740), (636, 1776), 'text', 'country'], [(896, 1683), (1300, 1726), 'check_text', 'Filing Date (YYYY-MM-DD)'], [(900, 1743), (1090, 1780), 'text', 'filing_date']]
                        for x,r in enumerate(roi):
                            if r[2]=='check_text':
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                if value==r[3]:
                                    roi_r = roi[x+1]
                                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value= value.rstrip()
                                    value=value.replace('D','2')
                                    value=value.replace('P','2')
                                    foreign_priority['foreign_priority_2'][roi_r[3]]=value
            else:
                roi=[(191, 880), (511, 917), 'check_text', 'Prior Application Status']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    print(1924)
                    roi=[(528, 880), (737, 920), 'text', 'prior']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    value=value.replace('é','e')
                    file['prior_application_status']=value
                    roi=[[(611, 948), (885, 1002), 'check_text', 'Continuity Type'], [(528, 1031), (900, 1071), 'text', 'continuity'], [(957, 948), (1302, 1000), 'check_text', 'Prior Application Number'], [(948, 1034), (1117, 1074), 'text', 'prior_application_no'], [(1374, 931), (1680, 965), 'check_text', 'Filing or 371(c) Date'], [(1314, 1034), (1565, 1074), 'text', 'filing_date']]
                    for x,r in enumerate(roi):
                        if r[2]=='check_text':
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==r[3]:
                                roi_r=roi[x+1]
                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                file[roi_r[3]]=value
                else:
                    roi=[(153, 633), (490, 670), 'check_text', 'Prior Application Status']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        print(1950)
                        roi=[(526, 634), (894, 670), 'text', 'prior_application_status']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        file['prior_application_status']=value
                        roi=[[(550, 700), (873, 760), 'check_text', 'Continuity Type'], [(513, 793), (886, 830), 'text', 'continuity'], [(953, 703), (1316, 760), 'check_text', 'Prior Application Number'], [(944, 790), (1310, 834), 'text', 'prior_application_no'], [(1386, 683), (1693, 720), 'check_text', 'Filing or 371(c) Date'], [(1340, 790), (1530, 833), 'text', 'filing_date']]
                        for x,r in enumerate(roi):
                            if r[2]=='check_text':
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                if value==r[3]:
                                    roi_r=roi[x+1]
                                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    file[roi_r[3]]=value
                    else:
                        roi=[(175, 1228), (506, 1268), 'check_text', 'Prior Application Status']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==roi[3]:
                            print(1974)
                            roi=[(519, 1231), (926, 1271), 'text', 'prior_application_status']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            file['prior_application_status']=value
                            roi=[[(586, 1295), (904, 1355), 'check_text', 'Continuity Type'], [(517, 1382), (917, 1426), 'text', 'continuity'], [(959, 1295), (1302, 1355), 'check_text', 'Prior Application Number'], [(944, 1386), (1284, 1431), 'text', 'prior_application_no'], [(1379, 1284), (1664, 1317), 'Filing or 371(c) Date', 'Filing or 371(c) Date'], [(1313, 1384), (1557, 1431), 'text', 'filing_date']]
                            for x,r in enumerate(roi):
                                if r[2]=='check_text':
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    if value==r[3]:
                                        roi_r=roi[x+1]
                                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        file[roi_r[3]]=value
                        else:
                            roi=[(156, 1162), (490, 1200), 'check_text', 'Prior Application Status']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==roi[3]:
                                roi=[(502, 1160), (922, 1198), 'text', 'prior_application_status']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                file['prior_application_status']=value
                                roi=[[(568, 1224), (914, 1278), 'check_text', 'Continuity Type'], [(502, 1304), (926, 1346), 'text', 'continuity'], [(950, 1214), (1314, 1276), 'check_text', 'Prior Application Number'], [(944, 1304), (1304, 1344), 'text', 'prior_application_no'], [(1392, 1208), (1692, 1240), 'check_text', 'Filing or 371(c) Date'], [(1328, 1304), (1556, 1342), 'text', 'filing_date']]
                                for x,r in enumerate(roi):
                                    if r[2]=='check_text':
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        if value==r[3]:
                                            roi_r=roi[x+1]
                                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            file[roi_r[3]]=value
                            else:
                                roi=[(157, 1228), (486, 1268), 'check_text', 'Prior Application Status']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                if value==roi[3]:
                                    roi=[(517, 1231), (891, 1266), 'text', 'prior_application_status']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    file[roi[3]]=value
                                    roi=[[(602, 1302), (871, 1353), 'check_text', 'Continuity Type'], [(517, 1388), (899, 1428), 'text', 'continuity'], [(962, 1299), (1313, 1351), 'check_text', 'Prior Application Number'], [(951, 1388), (1304, 1431), 'text', 'prior_application_no'], [(1397, 1282), (1477, 1317), 'check_text', 'Filing'], [(1344, 1386), (1535, 1433), 'text', 'filing_date']]
                                    for x,r in enumerate(roi):
                                        if r[2]=='check_text':
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            if value==r[3]:
                                                roi_r=roi[x+1]
                                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                file[roi_r[3]]=value
                                else:
                                    if len(page_lst)>3:
                                        img = cv2.imread(page_lst[n+3])
                                        roi=[(192, 878), (510, 920), 'check_text', 'Prior Application Status']
                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        if value==roi[3]:
                                            roi=[(530, 880), (736, 920), 'text', 'prior_application_status']
                                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            file[roi[3]]=value
                                            roi=[[(612, 952), (880, 1002), 'check_text', 'Continuity Type'], [(526, 1030), (916, 1074), 'text', 'continuity_type'], [(958, 946), (1302, 996), 'check_text', 'Prior Application Number'], [(946, 1032), (1160, 1076), 'text', 'prior_application_no'], [(1376, 932), (1694, 968), 'check_text', 'Filing or 371(c) Date'], [(1318, 1034), (1492, 1074), 'text', 'filing_date']]
                                            for x,r in enumerate(roi):
                                                if r[2]=='check_text':
                                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                    value=value.rstrip()
                                                    if value==r[3]:
                                                        roi_r=roi[x+1]
                                                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                        value=value.rstrip()
                                                        file[roi_r[3]]=value
                                        else:
                                            img = cv2.imread(page_lst[n+1])
                                            roi=[(156, 2016), (490, 2056), 'check_text', 'Prior Application Status']
                                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            if value==roi[3]:
                                                roi=[(513, 2016), (736, 2053), 'text', 'prior_application_status']
                                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                file[roi[3]]=value
                                                roi=[[(586, 2080), (890, 2146), 'check_text', 'Continuity Type'], [(520, 2176), (760, 2216), 'text', 'continuity'], [(960, 2090), (1316, 2140), 'check_text', 'Prior Application Number'], [(946, 2173), (1300, 2216), 'text', 'prior_application_no'], [(1386, 2066), (1716, 2103), 'check_text', 'Filing or 371(c) Date'], [(1336, 2173), (1536, 2216), 'text', 'filing_date']]
                                                for x,r in enumerate(roi):
                                                    if r[2]=='check_text':
                                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                        value=value.rstrip()
                                                        if value==r[3]:
                                                            roi_r=roi[x+1]
                                                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                            value=value.rstrip()
                                                            file[roi_r[3]]=value
                                            else:
                                                img = cv2.imread(page_lst[n+1])
                                                roi=[(180, 1910), (506, 1950), 'check_text', 'Prior Application Status']
                                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                if value==roi[3]:
                                                    roi=[(520, 1913), (750, 1946), 'text', 'prior_application_status']
                                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                    value=value.rstrip()
                                                    file[roi[3]]=value
                                                    roi=[[(576, 1966), (903, 2026), 'check_text', 'Continuity Type'], [(520, 2050), (916, 2090), 'text', 'continuity'], [(950, 1966), (1300, 2026), 'check_text', 'Prior Application Number'], [(943, 2050), (1193, 2086), 'text', 'prior_application_no'], [(1376, 1956), (1673, 1986), 'check_text', 'Filing or 371(c) Date'], [(1313, 2053), (1586, 2086), 'text', 'filing_date']]
                                                    for x,r in enumerate(roi):
                                                        if r[2]=='check_text':
                                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                            value=value.rstrip()
                                                            if value==r[3]:
                                                                roi_r=roi[x+1]
                                                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                value=value.rstrip()
                                                                file[roi_r[3]]=value
                                                else:
                                                    img = cv2.imread(page_lst[n+1])
                                                    roi=[(193, 1930), (516, 1970), 'check_text', 'Prior Application Status']
                                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                    value=value.rstrip()
                                                    if value==roi[3]:
                                                        roi=[(533, 1926), (926, 1956), 'text', 'prior_application_status']
                                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                        value=value.rstrip()
                                                        file[roi[3]]=value
                                                        roi=[[(606, 1986), (886, 2046), 'check_text', 'Continuity Type'], [(536, 2076), (896, 2116), 'text', 'continuity'], [(966, 1983), (1313, 2036), 'check_text', 'Prior Application Number'], [(963, 2070), (1306, 2106), 'text', 'prior_application_no'], [(1386, 1960), (1673, 1993), 'check_text', 'Filing or 371(c) Date'], [(1333, 2066), (1523, 2103), 'text', 'filing_date']]
                                                        for x,r in enumerate(roi):
                                                            if r[2]=='check_text':
                                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                value=value.rstrip()
                                                                if value==r[3]:
                                                                    roi_r=roi[x+1]
                                                                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                    value=value.rstrip()
                                                                    file[roi_r[3]]=value
                                                    else:
                                                        img = cv2.imread(page_lst[n+1])
                                                        roi=[(610, 2000), (856, 2040), 'check_text', 'Continuity Type']
                                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                        value=value.rstrip()
                                                        if value==roi[3]:
                                                            roi=[[(153, 1946), (486, 1986), 'check_text', 'Prior Application Status'], [(520, 1946), (866, 1986), 'text', 'prior_application_status'], [(603, 2000), (866, 2040), 'check_text', 'Continuity Type'], [(516, 2056), (876, 2093), 'text', 'continuity'], [(960, 2000), (1313, 2040), 'check_text', 'Prior Application Number'], [(950, 2056), (1310, 2096), 'text', 'prior_application_no'], [(1360, 2000), (1516, 2040), 'check_text', 'Filing Date'], [(1343, 2056), (1516, 2096), 'text', 'filing_date']]
                                                            for x,r in enumerate(roi):
                                                                if r[2]=='check_text':
                                                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                    value=value.rstrip()
                                                                    if value==r[3]:
                                                                        roi_r=roi[x+1]
                                                                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                        value=value.rstrip()
                                                                        file[roi_r[3]]=value
                                                        else:
                                                            img = cv2.imread(page_lst[n+1])
                                                            roi=[(170, 1946), (483, 1983), 'check_text', 'Prior Application Status']
                                                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                            value=value.rstrip()
                                                            if value==roi[3]:
                                                                roi=[(513, 1946), (930, 1983), 'text', 'prior_application_status']
                                                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                value=value.rstrip()
                                                                file[roi[3]]=value
                                                                roi=[[(593, 2010), (863, 2070), 'check_text', 'Continuity Type'], [(506, 2103), (920, 2140), 'text', 'continuity'], [(960, 2016), (1333, 2070), 'check_text', 'Prior Application Number'], [(943, 2103), (1303, 2140), 'text', 'prior_application_no'], [(1403, 1996), (1683, 2030), 'check_text', 'Filing or 371(c) Date'], [(1340, 2103), (1536, 2143), 'text', 'filing_date']]
                                                                for x,r in enumerate(roi):
                                                                    if r[2]=='check_text':
                                                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                        value=value.rstrip()
                                                                        if value==r[3]:
                                                                            roi_r=roi[x+1]
                                                                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                                            value=value.rstrip()
                                                                            file[roi_r[3]]=value
    img = cv2.imread(page_lst[-3])
    roi=[(123, 1970), (286, 2016), 'check_text', 'Signature']
    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
    value=value.rstrip()
    if value==roi[3]:
        signature={}
        file['signature']=signature
        roi=[[(123, 1970), (286, 2016), 'check_text', 'Signature'], [(313, 1970), (586, 2016), 'text', 'signature'], [(1173, 1966), (1486, 2020), 'check_text', 'Date (YYYY-MM-DD)'], [(1506, 1970), (1700, 2020), 'text', 'date'], [(123, 2060), (296, 2100), 'check_text', 'First Name'], [(326, 2060), (510, 2100), 'text', 'first_name'], [(596, 2060), (773, 2100), 'check_text', 'Last Name'], [(806, 2060), (1106, 2100), 'text', 'last_name'], [(1170, 2060), (1476, 2100), 'check_text', 'Registration Number'], [(1510, 2060), (1636, 2100), 'text', 'registration_no']]
        for x,r in enumerate(roi):
            if r[2]=='check_text':
                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==r[3]:
                    roi_r = roi[x+1]
                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value= value.rstrip()
                    signature[roi_r[3]]=value
    else:
        roi=[(136, 1490), (333, 1540), 'check_text', 'Signature']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
        value=value.rstrip()
        if value==roi[3]:
            signature={}
            file['signature']=signature
            roi=[[(156, 1953), (313, 2003), 'check_text', 'Signature'], [(360, 1936), (606, 2013), 'text', 'signature'], [(1166, 1953), (1250, 1996), 'check_text', 'Date'], [(1486, 1953), (1650, 1993), 'text', 'date'], [(153, 2040), (320, 2080), 'check_text', 'First Name'], [(340, 2040), (573, 2080), 'text', 'first_name'], [(613, 2040), (783, 2080), 'check_text', 'Last Name'], [(803, 2040), (1106, 2076), 'text', 'last_name'], [(1163, 2040), (1460, 2076), 'check_text', 'Registration Number'], [(1483, 2040), (1620, 2076), 'text', 'registration_no']]
            for x,r in enumerate(roi):
                if r[2]=='check_text':
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==r[3]:
                        roi_r = roi[x+1]
                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value= value.rstrip()
                        signature[roi_r[3]]=value
        else:
            roi=[(106, 1430), (343, 1480), 'check_text', 'Signature:']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                signature={}
                file['signature']=signature
                roi=[[(123, 1906), (283, 1956), 'check_text', 'Signature'], [(306, 1910), (920, 1966), 'text', 'signature'], [(126, 2000), (296, 2043), 'check_text', 'First Name'], [(326, 2000), (540, 2040), 'text', 'first_name'], [(596, 2000), (773, 2043), 'check_text', 'Last Name'], [(806, 2000), (1090, 2043), 'text', 'last_name'], [(1173, 1906), (1253, 1953), 'check_text', 'Date'], [(1506, 1910), (1693, 1963), 'text', 'date'], [(1170, 2000), (1470, 2043), 'check_text', 'Registration Number'], [(1510, 2000), (1653, 2036), 'text', 'registration_no']]
                for x,r in enumerate(roi):
                    if r[2]=='check_text':
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==r[3]:
                            roi_r = roi[x+1]
                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            signature[roi_r[3]]=value
            else:
                roi=[(133, 1450), (346, 1500), 'check_text', 'Signature:']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    signature={}
                    file['signature']=signature
                    roi=[[(150, 1916), (310, 1963), 'check_text', 'Signature'], [(333, 1913), (1123, 1970), 'text', 'signature'], [(1163, 1910), (1243, 1953), 'check_text', 'Date'], [(1473, 1906), (1650, 1956), 'text', 'date'], [(150, 2003), (316, 2046), 'check_text', 'First Name'], [(336, 2003), (593, 2040), 'text', 'first_name'], [(610, 2000), (783, 2040), 'check_text', 'Last Name'], [(800, 2000), (1136, 2036), 'text', 'last_name'], [(1160, 1996), (1456, 2036), 'check_text', 'Registration Number'], [(1476, 1993), (1656, 2033), 'text', 'registration_no']]
                    for x,r in enumerate(roi):
                        if r[2]=='check_text':
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==r[3]:
                                roi_r = roi[x+1]
                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value= value.rstrip()
                                signature[roi_r[3]]=value
                else:
                    roi=[(110, 1860), (326, 1910), 'check_text', 'Signature:']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        signature={}
                        file['signature']=signature
                        roi=[[(130, 2016), (280, 2063), 'check_text', 'Signature'], [(316, 2013), (1136, 2063), 'text', 'signature'], [(1170, 2013), (1253, 2066), 'check_text', 'Date'], [(1506, 2016), (1660, 2063), 'text', 'Date'], [(126, 2083), (290, 2126), 'check_text', 'First Name'], [(330, 2083), (573, 2123), 'tex', 'first_name'], [(593, 2083), (770, 2123), 'check_text', 'Last Name'], [(806, 2083), (1120, 2123), 'text', 'last_name'], [(1170, 2083), (1463, 2123), 'check_text', 'Registration Number'], [(1506, 2083), (1606, 2123), 'text', 'registration_no']]
                        for x,r in enumerate(roi):
                            if r[2]=='check_text':
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                if value==r[3]:
                                    roi_r = roi[x+1]
                                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value= value.rstrip()
                                    signature[roi_r[3]]=value
                    else:
                        img=cv2.imread(page_lst[-1])
                        roi=[(176, 1360), (376, 1406), 'check_text', 'Signature:']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        if value==roi[3]:
                            signature={}
                            file['signature']=signature
                            roi=[[(193, 1756), (343, 1806), 'check_text', 'Signature'], [(363, 1743), (1046, 1823), 'text', 'signature'], [(1133, 1760), (1210, 1806), 'check_text', 'Date'], [(1430, 1760), (1606, 1810), 'text', 'date'], [(190, 1836), (343, 1873), 'check_text', 'First Name'], [(363, 1836), (576, 1870), 'text', 'first_name'], [(613, 1836), (780, 1873), 'check_text', 'Last Name'], [(793, 1836), (1096, 1873), 'text', 'last_name'], [(1130, 1836), (1413, 1870), 'check_text', 'Registration Number'], [(1430, 1840), (1603, 1873), 'text', 'registration_no']]
                            for x,r in enumerate(roi):
                                if r[2]=='check_text':
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    if value==r[3]:
                                        roi_r = roi[x+1]
                                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value= value.rstrip()
                                        signature[roi_r[3]]=value
                        else:
                            img=cv2.imread(page_lst[-1])
                            roi=[(103, 393), (316, 443), 'check_text', 'Signature:']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==roi[3]:
                                signature={}
                                file['signature']=signature
                                roi=[[(120, 926), (280, 980), 'check_text', 'Signature'], [(313, 930), (770, 993), 'text', 'signature'], [(1176, 933), (1246, 976), 'check_text', 'Date'], [(1496, 920), (1746, 996), 'text', 'date'], [(116, 1023), (286, 1063), 'check_text', 'First Name'], [(313, 1023), (560, 1060), 'text', 'first_name'], [(596, 1023), (773, 1063), 'check_box', 'Last Name'], [(793, 1023), (1153, 1063), 'text', 'last_name'], [(1170, 1023), (1463, 1063), 'check_text', 'Registration Number'], [(1500, 1023), (1720, 1063), 'text', 'registration_no']]
                                for x,r in enumerate(roi):
                                    if r[2]=='check_text':
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value=value.rstrip()
                                        if value==r[3]:
                                            roi_r = roi[x+1]
                                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value= value.rstrip()
                                            signature[roi_r[3]]=value
                            else:
                                img=cv2.imread(page_lst[-2])
                                roi=[(136, 1480), (350, 1533), 'check_text', 'Signature:']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                if value==roi[3]:
                                    signature={}
                                    file['signature']=signature
                                    roi=[[(146, 1946), (306, 2000), 'check_text', 'Signature'], [(340, 1926), (1086, 2013), 'text', 'signature'], [(1160, 1940), (1243, 1996), 'check_text', 'Date'], [(1476, 1936), (1713, 2010), 'text', 'date'], [(146, 2030), (316, 2073), 'check_text', 'First Name'], [(336, 2033), (480, 2073), 'text', 'first_name'], [(610, 2030), (770, 2076), 'check_text', 'Last Name'], [(800, 2033), (1096, 2073), 'text', 'last_name'], [(1160, 2030), (1460, 2070), 'check_text', 'Registration Number'], [(1483, 2033), (1576, 2066), 'text', 'registration_no']]
                                    for x,r in enumerate(roi):
                                        if r[2]=='check_text':
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value=value.rstrip()
                                            if value==r[3]:
                                                roi_r = roi[x+1]
                                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value= value.rstrip()
                                                signature[roi_r[3]]=value
                                else:
                                    img=cv2.imread(page_lst[-2])
                                    roi=[(100, 1463), (343, 1513), 'check_text', 'Signature:']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    if value==roi[3]:
                                        signature={}
                                        file['signature']=signature
                                        roi=[[(120, 1896), (283, 1950), 'check_text', 'Signature'], [(310, 1896), (1150, 1970), 'text', 'signature'], [(1170, 1893), (1253, 1953), 'check_text', 'Date'], [(1496, 1900), (1676, 1950), 'text', 'date'], [(120, 1986), (300, 2023), 'check_text', 'First Name'], [(313, 1990), (570, 2023), 'text', 'first_name'], [(593, 1986), (780, 2026), 'check_text', 'Last Name'], [(793, 1986), (1126, 2026), 'text', 'last_name'], [(1170, 1990), (1473, 2026), 'check_text', 'Registration Number'], [(1496, 1986), (1710, 2026), 'text', 'registration_no']]
                                        for x,r in enumerate(roi):
                                            if r[2]=='check_text':
                                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value=value.rstrip()
                                                if value==r[3]:
                                                    roi_r = roi[x+1]
                                                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                    value= value.rstrip()
                                                    signature[roi_r[3]]=value
    print(file)
    filen=a.replace('pdf','json')
    with open(os.path.join(DOWNLOAD_FOLDER) + "\\" + filen, 'w') as outfile:
        json.dump(file, outfile)
    s3.meta.client.upload_file( os.path.join(DOWNLOAD_FOLDER) + "\\" + filen, my_bucket, s3_dir+'/'+filen)
    end=time.time()
    tot=end-start
    print('Time taken: {} seconds'.format(tot))
except Exception as e:
    print('File found an error: ',e)