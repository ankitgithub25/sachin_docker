import re
import pytesseract
import cv2 
import numpy as np
import sys 
from pdf2image import convert_from_path 
import os 
import time
import json
import boto3
s3 = boto3.resource('s3')
my_bucket = 'bb-bot-test'
s3_dir=sys.argv[1]
a=sys.argv[2]
pytesseract.pytesseract.tesseract_cmd=r'Tesseract-OCR\tesseract.exe'
DOWNLOAD_FOLDER = 'downloads'
print(a)
path_file = os.path.join(DOWNLOAD_FOLDER, a)
file={}
roi=[]
roi2=[]
start=time.time()
page = convert_from_path(path_file,dpi=220,first_page=2,last_page=2,poppler_path=r'poppler-0.68.0\bin')
filename = "page_1.jpg"
filename = os.path.join(DOWNLOAD_FOLDER, filename)
page[0].save(filename, 'JPEG')
b=1
try:
    while not file:
        img=cv2.imread(filename)
        roi=[(252, 656), (436, 694), 'check_text', 'A declaration']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
        value=value.rstrip()
        roi2=[(234, 976), (358, 1016), 'check_text', 'Claim(s)']
        imgcrop = img[roi2[0][1]:roi2[1][1],roi2[0][0]:roi2[1][0]]
        value2=pytesseract.image_to_string(imgcrop, config='--psm 6')
        value2=value2.rstrip()
        if value==roi[3] and value2==roi2[3]:
            roi=[(234, 976), (358, 1016), 'check_text', 'Claim(s)']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            print('type1')
            roi=[(880, 104), (1292, 144), 'text', 'app_number']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            value=value.replace(' ','')
            file['app_number']=value
            check_box={}
            file['check_box']=check_box
            roi=[[(184, 612), (220, 648), 'check_box', '1'], [(226, 612), (1784, 652), 'text', '1'], [(210, 652), (250, 692), 'check_box', '1.1'], [(250, 654), (1300, 694), 'text', '1.1'], [(186, 704), (222, 740), 'check_box', '2.a'], [(228, 704), (698, 740), 'text', '2.a'], [(764, 704), (800, 740), 'check_box', '2.b'], [(804, 706), (1306, 740), 'text', '2.b'], [(184, 746), (220, 782), 'check_box', '3'], [(232, 744), (1758, 826), 'text', '3'], [(184, 832), (220, 868), 'check_box', '4'], [(226, 830), (1760, 910), 'text', '4'], [(184, 974), (220, 1012), 'check_box', '5'], [(226, 976), (1180, 1014), 'text', '5'], [(184, 1060), (220, 1098), 'check_box', '6'], [(226, 1058), (686, 1100), 'text', '6'], [(184, 1104), (220, 1140), 'check_box', '7'], [(232, 1102), (696, 1142), 'text', '7'], [(184, 1146), (220, 1182), 'check_box', '8'], [(232, 1142), (708, 1182), 'text', '8'], [(184, 1190), (220, 1226), 'check_box', '9'], [(230, 1188), (1774, 1226), 'text', '9'], [(186, 1416), (223, 1456), 'check_box', '10'], [(226, 1416), (960, 1456), 'text', '10'], [(186, 1460), (223, 1500), 'check_box', '11'], [(226, 1462), (802, 1502), 'text', '11'], [(837, 1459), (875, 1499), 'check_box', '11.a'], [(879, 1462), (1013, 1504), 'text', '11.a'], [(1077, 1459), (1115, 1497), 'check_box', '11.b'], [(1117, 1459), (1535, 1499), 'text', '11.b'], [(186, 1646), (223, 1686), 'check_box', '12'], [(226, 1646), (1540, 1690), 'text', '12'], [(233, 1733), (270, 1770), 'check_box', '12.a'], [(273, 1730), (323, 1770), 'text', '12.a'], [(380, 1733), (416, 1770), 'check_box', '12.b'], [(420, 1733), (533, 1770), 'text', '12.b'], [(566, 1733), (603, 1770), 'check_box', '12.c'], [(606, 1730), (866, 1773), 'text', '12.c'], [(263, 1776), (303, 1813), 'check_box', '12.1'], [(323, 1773), (1513, 1810), 'text', '12.1'], [(263, 1816), (303, 1856), 'check_box', '12.2'], [(320, 1820), (1550, 1856), 'text', '12.2'], [(263, 1860), (303, 1900), 'check_box', '12.3'], [(320, 1860), (1686, 1946), 'text', '12.3'], [(130, 2156), (170, 2193), 'check_box', 'attach.1'], [(173, 2160), (966, 2203), 'text', 'attach.1'], [(130, 2216), (170, 2253), 'check_box', 'attach.2'], [(173, 2216), (976, 2283), 'text', 'attach.2'], [(1053, 2160), (1090, 2200), 'check_box', 'attach.3'], [(1093, 2160), (1503, 2240), 'text', 'attach.3'], [(1053, 2233), (1090, 2270), 'check_box', 'attach.4'], [(1093, 2236), (1513, 2283), 'text', 'attach.4']]
            for x,r in enumerate(roi):
                if r[2]=='check_box':
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                    total_pixels=cv2.countNonZero(value)
                    if total_pixels>450:
                        roi_r = roi[x+1]
                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value= value.rstrip()
                        value=value.replace('\n',' ')
                        check_box[roi_r[3]]=value
            roi=[(1031, 1464), (1053, 1497), 'check_text', 'b']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                roi=[[(822, 1462), (859, 1499), 'check_box', '11.a'], [(859, 1459), (993, 1504), 'text', '11.a'], [(1059, 1459), (1099, 1499), 'check_box', '11.b'], [(1099, 1459), (1526, 1502), 'text', '11.b']]
                for x,r in enumerate(roi):
                    if r[2]=='check_box':
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                        total_pixels=cv2.countNonZero(value)
                        if total_pixels>450:
                            roi_r = roi[x+1]
                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            check_box[roi_r[3]]=value
        else:
            roi=[(276, 974), (396, 1010), 'check_text', 'Claim(s)']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            if value==roi[3]:
                print('type2')
                roi=[(880, 104), (1042, 138), 'text', 'app_number']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                value=value.replace(' ','')
                file['app_number']=value
                check_box={}
                file['check_box']=check_box
                roi=[[(188, 624), (220, 656), 'check_box', '1'], [(230, 620), (1078, 658), 'text', '1'], [(216, 664), (248, 696), 'check_box', '1.1'], [(252, 664), (1326, 706), 'text', '1.1'], [(188, 712), (220, 742), 'check_box', '2.a'], [(228, 706), (584, 746), 'text', '2.a'], [(844, 708), (876, 740), 'check_box', '2.b'], [(880, 708), (1326, 744), 'text', '2.b'], [(188, 754), (220, 786), 'check_box', '3'], [(228, 750), (1758, 824), 'textt', '3'], [(188, 832), (220, 864), 'check_box', '4'], [(234, 828), (1766, 900), 'text', '4'], [(222, 976), (256, 1008), 'check_box', '5'], [(266, 972), (1498, 1014), 'text', '5'], [(222, 1070), (256, 1102), 'check_box', '6'], [(270, 1064), (1004, 1106), 'text', '6'], [(224, 1118), (256, 1150), 'check_box', '7'], [(262, 1110), (724, 1150), 'text', '7'], [(224, 1164), (254, 1198), 'check_box', '8'], [(266, 1158), (796, 1196), 'text', '8'], [(224, 1212), (256, 1244), 'check_box', '9'], [(268, 1206), (1234, 1248), 'text', '9'], [(186, 1436), (220, 1466), 'check_box', '10'], [(226, 1430), (956, 1473), 'text', '10'], [(190, 1480), (220, 1513), 'check_box', '11'], [(226, 1476), (753, 1516), 'text', '11'], [(793, 1483), (830, 1516), 'check_box', '11.a'], [(840, 1480), (1020, 1516), 'text', '11.a'], [(1060, 1480), (1093, 1516), 'check_box', '11.b'], [(1096, 1473), (1546, 1520), 'text', '11.b'], [(186, 1663), (216, 1696), 'check_box', '12'], [(226, 1660), (1490, 1703), 'text', '12'], [(266, 1743), (300, 1776), 'check_box', '12.a'], [(306, 1740), (383, 1776), 'text', '12.a'], [(453, 1746), (486, 1776), 'check_box', '12.b'], [(490, 1740), (626, 1780), 'text', '12.b'], [(686, 1743), (720, 1776), 'check_box', '12.c'], [(726, 1740), (946, 1776), 'text', '12.c'], [(300, 1790), (333, 1826), 'check_box', '12.1'], [(360, 1786), (1263, 1826), 'text', '12.1'], [(303, 1836), (333, 1870), 'check_box', '12.2'], [(360, 1830), (1600, 1876), 'text', '12.2'], [(300, 1883), (333, 1916), 'check_box', '12.3'], [(360, 1876), (1720, 1960), 'text', '12.3'], [(133, 2126), (166, 2160), 'check_box', 'attach.1'], [(170, 2123), (636, 2160), 'text', 'attach.1'], [(133, 2186), (166, 2223), 'check_box', 'attach.2'], [(170, 2186), (963, 2250), 'text', 'attach.2'], [(1063, 2126), (1100, 2163), 'check_box', 'attach.3'], [(1100, 2126), (1516, 2206), 'text', 'attach.3'], [(1063, 2203), (1096, 2240), 'check_box', 'attach.4'], [(1100, 2203), (1466, 2246), 'text', 'attach.4']]
                for x,r in enumerate(roi):
                    if r[2]=='check_box':
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                        total_pixels=cv2.countNonZero(value)
                        if total_pixels>450:
                            roi_r = roi[x+1]
                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            value=value.replace('\n',' ')
                            check_box[roi_r[3]]=value
                if not check_box:
                    roi=[[(188, 624), (220, 656), 'check_box', '1'], [(230, 620), (1078, 658), 'text', '1'], [(216, 664), (248, 696), 'check_box', '1.1'], [(252, 664), (1326, 706), 'text', '1.1'], [(188, 712), (220, 742), 'check_box', '2.a'], [(228, 706), (584, 746), 'text', '2.a'], [(844, 708), (876, 740), 'check_box', '2.b'], [(880, 708), (1326, 744), 'text', '2.b'], [(188, 754), (220, 786), 'check_box', '3'], [(228, 750), (1758, 824), 'textt', '3'], [(188, 832), (220, 864), 'check_box', '4'], [(234, 828), (1766, 900), 'text', '4'], [(222, 976), (256, 1008), 'check_box', '5'], [(266, 972), (1498, 1014), 'text', '5'], [(222, 1070), (256, 1102), 'check_box', '6'], [(270, 1064), (1004, 1106), 'text', '6'], [(224, 1118), (256, 1150), 'check_box', '7'], [(262, 1110), (724, 1150), 'text', '7'], [(224, 1164), (254, 1198), 'check_box', '8'], [(266, 1158), (796, 1196), 'text', '8'], [(224, 1212), (256, 1244), 'check_box', '9'], [(268, 1206), (1234, 1248), 'text', '9'], [(186, 1436), (220, 1466), 'check_box', '10'], [(226, 1430), (956, 1473), 'text', '10'], [(190, 1480), (220, 1513), 'check_box', '11'], [(226, 1476), (753, 1516), 'text', '11'], [(793, 1483), (830, 1516), 'check_box', '11.a'], [(840, 1480), (1020, 1516), 'text', '11.a'], [(1060, 1480), (1093, 1516), 'check_box', '11.b'], [(1096, 1473), (1546, 1520), 'text', '11.b'], [(186, 1663), (216, 1696), 'check_box', '12'], [(226, 1660), (1490, 1703), 'text', '12'], [(266, 1743), (300, 1776), 'check_box', '12.a'], [(306, 1740), (383, 1776), 'text', '12.a'], [(453, 1746), (486, 1776), 'check_box', '12.b'], [(490, 1740), (626, 1780), 'text', '12.b'], [(686, 1743), (720, 1776), 'check_box', '12.c'], [(726, 1740), (946, 1776), 'text', '12.c'], [(300, 1790), (333, 1826), 'check_box', '12.1'], [(360, 1786), (1263, 1826), 'text', '12.1'], [(303, 1836), (333, 1870), 'check_box', '12.2'], [(360, 1830), (1600, 1876), 'text', '12.2'], [(300, 1883), (333, 1916), 'check_box', '12.3'], [(360, 1876), (1720, 1960), 'text', '12.3'], [(133, 2126), (166, 2160), 'check_box', 'attach.1'], [(170, 2123), (636, 2160), 'text', 'attach.1'], [(133, 2186), (166, 2223), 'check_box', 'attach.2'], [(170, 2186), (963, 2250), 'text', 'attach.2'], [(1063, 2126), (1100, 2163), 'check_box', 'attach.3'], [(1100, 2126), (1516, 2206), 'text', 'attach.3'], [(1063, 2203), (1096, 2240), 'check_box', 'attach.4'], [(1100, 2203), (1466, 2246), 'text', 'attach.4']]
                    for x,r in enumerate(roi):
                        if r[2]=='check_box':
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>290:
                                roi_r = roi[x+1]
                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value= value.rstrip()
                                value=value.replace('\n',' ')
                                check_box[roi_r[3]]=value
            else:
                roi=[(896, 92), (1120, 126), 'check_text', 'Application No.']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                if value==roi[3]:
                    roi=[(114, 892), (434, 924), 'check_text', 'Disposition of Claims']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    if value==roi[3]:
                        print('type3')
                        roi=[(904, 150), (1316, 200), 'text', 'app_number']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        value=value.replace(' ','')
                        file['app_number']=value
                        check_box={}
                        file['check_box']=check_box
                        roi=[[(198, 682), (234, 718), 'check_box', '1'], [(246, 680), (1034, 722), 'text', '1'], [(200, 726), (236, 764), 'check_box', '2.a'], [(244, 726), (604, 762), 'text', '2.a'], [(778, 728), (814, 764), 'check_box', '2.b'], [(818, 726), (1198, 764), 'text', '2.b'], [(198, 774), (234, 808), 'check_box', '3'], [(248, 774), (1738, 864), 'text', '3'], [(198, 948), (234, 986), 'check_box', '4'], [(244, 948), (1210, 988), 'text', '4'], [(198, 1040), (234, 1076), 'check_box', '5'], [(244, 1038), (844, 1078), 'text', '5'], [(198, 1086), (234, 1122), 'check_box', '6'], [(242, 1084), (844, 1118), 'text', '6'], [(198, 1132), (234, 1168), 'check_box', '7'], [(242, 1130), (854, 1168), 'text', '7'], [(198, 1178), (234, 1214), 'check_box', '8'], [(244, 1174), (1236, 1218), 'text', '8'], [(200, 1316), (236, 1352), 'check_box', '9'], [(240, 1316), (966, 1352), 'text', '9'], [(200, 1360), (236, 1400), 'check_box', '10'], [(240, 1360), (746, 1403), 'text', '10'], [(783, 1360), (820, 1400), 'text', '10.a'], [(1023, 1360), (1060, 1400), 'check_box', '10.b'], [(1063, 1356), (1500, 1400), 'text', '10.b'], [(200, 1496), (236, 1536), 'check_box', '11'], [(240, 1496), (1740, 1536), 'text', '11'], [(200, 1626), (236, 1666), 'check_box', '12'], [(240, 1623), (1513, 1670), 'text', '12'], [(236, 1673), (276, 1710), 'check_box', '12.a'], [(276, 1670), (326, 1710), 'text', '12.a'], [(376, 1673), (413, 1710), 'check_box', '12.b'], [(416, 1673), (503, 1713), 'text', '12.b'], [(553, 1673), (590, 1710), 'check_box', '12.c'], [(593, 1670), (756, 1713), 'text', '12.c'], [(276, 1720), (316, 1756), 'check_box', '12.1'], [(330, 1716), (1226, 1760), 'text', '12.1'], [(276, 1763), (316, 1803), 'check_box', '12.2'], [(330, 1763), (1570, 1806), 'text', '12.2'], [(276, 1810), (316, 1850), 'check_box', '12.3'], [(326, 1810), (1710, 1900), 'text', '12.3'], [(146, 2116), (183, 2156), 'check_box', 'attach.1'], [(186, 2116), (666, 2153), 'text', 'attach.1'], [(146, 2153), (183, 2190), 'check_box', 'attach.2'], [(186, 2156), (863, 2193), 'text', 'attach.2'], [(146, 2190), (183, 2226), 'check_box', 'attach.3'], [(186, 2190), (873, 2260), 'text', 'attach.3'], [(1066, 2116), (1106, 2156), 'check_box', 'attach.4'], [(1106, 2116), (1523, 2183), 'text', 'attach.4'], [(1066, 2180), (1106, 2220), 'check_box', 'attach.5'], [(1106, 2186), (1536, 2220), 'text', 'attach.5'], [(1066, 2216), (1106, 2253), 'check_box', 'attach.6'], [(1106, 2220), (1290, 2256), 'text', 'attach.6']]
                        for x,r in enumerate(roi):
                            if r[2]=='check_box':
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>450:
                                    roi_r = roi[x+1]
                                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value= value.rstrip()
                                    value=value.replace('\n',' ')
                                    check_box[roi_r[3]]=value
                    else:
                        roi=[(185, 506), (305, 533), 'check_text', 'if the period']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value= value.rstrip()
                        if value==roi[3]:
                            print('type4')
                            roi=[(896, 151), (1211, 190), 'text', 'app_number']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            value=value.replace(' ','')
                            file['app_number']=value
                            check_box={}
                            file['check_box']=check_box
                            roi=[[(190, 710), (224, 744), 'check_box', '1'], [(230, 706), (1116, 744), 'text', '1'], [(190, 756), (226, 792), 'check_box', '2.a'], [(238, 754), (694, 792), 'text', '2.a'], [(770, 754), (806, 792), 'check_box', '2.b'], [(810, 756), (1228, 792), 'text', '2.b'], [(188, 802), (224, 838), 'check_box', '3'], [(234, 800), (1744, 884), 'text', '3'], [(188, 978), (226, 1016), 'check_box', '4'], [(232, 974), (1258, 1016), 'text', '4'], [(188, 1070), (226, 1106), 'check_box', '5'], [(232, 1070), (1234, 1104), 'text', '5'], [(188, 1116), (226, 1152), 'check_box', '6'], [(232, 1114), (1242, 1146), 'text', '6'], [(188, 1162), (224, 1198), 'check_box', '7'], [(236, 1162), (1242, 1200), 'text', '7'], [(188, 1208), (226, 1246), 'check_box', '8'], [(232, 1206), (1250, 1246), 'text', '8'], [(190, 1346), (226, 1382), 'check_box', '9'], [(228, 1346), (1270, 1388), 'text', '9'], [(190, 1390), (226, 1430), 'check_text', '10'], [(230, 1390), (1740, 1526), 'text', '10'], [(190, 1526), (226, 1566), 'check_box', '11'], [(230, 1526), (1713, 1570), 'text', '11'], [(190, 1660), (226, 1696), 'check_box', '12'], [(230, 1660), (1490, 1700), 'text', '12'], [(226, 1703), (260, 1743), 'check_box', '12.a'], [(266, 1703), (326, 1743), 'text', '12.a'], [(363, 1703), (400, 1743), 'check_box', '12.b'], [(403, 1703), (493, 1746), 'text', '12.b'], [(540, 1703), (576, 1743), 'check_box', '12.c'], [(580, 1703), (760, 1743), 'text', '12.c'], [(266, 1750), (303, 1790), 'check_box', '12.1'], [(316, 1746), (1313, 1786), 'text', '12.1'], [(266, 1796), (303, 1833), 'check_box', '12.2'], [(313, 1796), (1586, 1836), 'text', '12.2'], [(266, 1843), (303, 1880), 'check_box', '12.3'], [(313, 1840), (1706, 1930), 'text', '12.3'], [(133, 2126), (170, 2163), 'check_box', 'attach.1'], [(173, 2126), (856, 2156), 'text', 'attach.1'], [(133, 2163), (170, 2196), 'check_box', 'attach.2'], [(173, 2166), (870, 2196), 'text', 'attach.2'], [(133, 2196), (170, 2233), 'check_box', 'attach.3'], [(173, 2200), (913, 2266), 'text', 'attach.3'], [(1053, 2126), (1090, 2163), 'check_box', 'attach.4'], [(1093, 2126), (1623, 2190), 'text', 'attach.4'], [(1053, 2190), (1086, 2226), 'check_box', 'attach.5'], [(1093, 2196), (1680, 2226), 'text', 'attach.5'], [(1053, 2223), (1090, 2263), 'check_box', 'attach.6'], [(1093, 2230), (1690, 2276), 'text', 'attach.6']]
                            for x,r in enumerate(roi):
                                if r[2]=='check_box':
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>450:
                                        roi_r = roi[x+1]
                                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value= value.rstrip()
                                        value=value.replace('\n',' ')
                                        check_box[roi_r[3]]=value
                        else:
                            roi=[(184, 508), (302, 534), 'check_text', 'If the period']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==roi[3]:
                                print('type5')
                                roi=[(886, 150), (1282, 196), 'text', 'app_number']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                value=value.replace(' ','')
                                file['app_number']=value
                                check_box={}
                                file['check_box']=check_box
                                roi=[[(186, 710), (222, 746), 'check_box', '1'], [(232, 706), (1106, 746), 'text', '1'], [(188, 756), (224, 792), 'check_box', '2.a'], [(232, 752), (706, 796), 'text', '2.a'], [(766, 754), (804, 790), 'check_box', '2.b'], [(806, 752), (1244, 794), 'text', '2.b'], [(186, 802), (222, 838), 'check_box', '3'], [(228, 800), (1768, 880), 'text', '3'], [(186, 978), (222, 1014), 'check_box', '4'], [(232, 972), (1184, 1014), 'text', '4'], [(186, 1070), (222, 1108), 'check_box', '5'], [(230, 1068), (714, 1112), 'text', '5'], [(186, 1116), (222, 1152), 'check_box', '6'], [(232, 1114), (754, 1154), 'text', '6'], [(186, 1162), (222, 1198), 'check_box', '7'], [(230, 1160), (798, 1204), 'text', '7'], [(186, 1208), (222, 1244), 'check_box', '8'], [(230, 1206), (1262, 1246), 'text', '8'], [(188, 1346), (224, 1382), 'check_box', '9'], [(228, 1342), (1278, 1386), 'text', '9'], [(186, 1390), (226, 1430), 'check_box', '10'], [(230, 1390), (1770, 1523), 'text', '10'], [(190, 1530), (226, 1566), 'check_box', '11'], [(230, 1526), (1773, 1570), 'text', '11'], [(190, 1660), (223, 1696), 'check_box', '12'], [(226, 1656), (1523, 1696), 'text', '12'], [(226, 1706), (263, 1743), 'check_box', '12.a'], [(263, 1703), (323, 1746), 'text', '12.a'], [(360, 1703), (400, 1743), 'check_box', '12.b'], [(400, 1703), (490, 1746), 'text', '12.b'], [(540, 1703), (576, 1743), 'check_box', '12.c'], [(580, 1703), (736, 1746), 'text', '12.c'], [(263, 1750), (300, 1790), 'check_box', '12.1'], [(310, 1750), (1320, 1786), 'text', '12.1'], [(263, 1796), (300, 1836), 'check_box', '12.2'], [(310, 1793), (1626, 1836), 'text', '12.2'], [(266, 1843), (300, 1880), 'check_box', '12.3'], [(310, 1840), (1716, 1930), 'text', '12.3'], [(133, 2126), (170, 2163), 'check_box', 'attach.1'], [(173, 2126), (620, 2166), 'text', 'attach.1'], [(133, 2163), (170, 2193), 'check_box', 'attach.2'], [(170, 2166), (866, 2193), 'text', 'attach.2'], [(130, 2200), (170, 2233), 'check_box', 'attach.3'], [(173, 2203), (923, 2266), 'text', 'attach.3'], [(1053, 2123), (1090, 2163), 'check_box', 'attach.4'], [(1093, 2126), (1616, 2186), 'text', 'attach.4'], [(1053, 2190), (1090, 2226), 'check_box', 'attach.5'], [(1093, 2193), (1660, 2230), 'text', 'attach.5'], [(1053, 2226), (1090, 2260), 'check_box', 'attach.6'], [(1090, 2230), (1280, 2270), 'text', 'attach.6']]
                                for x,r in enumerate(roi):
                                    if r[2]=='check_box':
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                        total_pixels=cv2.countNonZero(value)
                                        if total_pixels>450:
                                            roi_r = roi[x+1]
                                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value= value.rstrip()
                                            value=value.replace('\n',' ')
                                            check_box[roi_r[3]]=value
                            else:
                                print('type6')
                                roi=[(904, 150), (1316, 200), 'text', 'app_number']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                value=value.replace(' ','')
                                file['app_number']=value
                                check_box={}
                                file['check_box']=check_box
                                roi=[[(198, 682), (234, 718), 'check_box', '1'], [(246, 678), (1208, 716), 'text', '1'], [(200, 726), (236, 764), 'check_box', '2.a'], [(244, 726), (684, 764), 'text', '2.a'], [(778, 726), (814, 762), 'check_box', '2.b'], [(818, 728), (1288, 762), 'text', '2.b'], [(198, 774), (234, 810), 'check_box', '3'], [(242, 772), (1780, 858), 'text', '3'], [(198, 866), (234, 900), 'check_box', '4'], [(244, 862), (1794, 942), 'text', '4'], [(198, 1024), (234, 1062), 'check_box', '5'], [(240, 1024), (1206, 1062), 'text', '5'], [(198, 1116), (234, 1154), 'check_box', '6'], [(244, 1114), (780, 1152), 'text', '6'], [(198, 1162), (234, 1198), 'check_box', '7'], [(244, 1162), (792, 1198), 'text', '7'], [(198, 1208), (234, 1246), 'check_box', '8'], [(242, 1206), (822, 1242), 'text', '8'], [(198, 1254), (234, 1290), 'check_box', '9'], [(242, 1252), (1286, 1294), 'text', '9'], [(200, 1390), (236, 1430), 'check_box', '10'], [(243, 1390), (1090, 1423), 'text', '10'], [(200, 1436), (236, 1473), 'check_box', '11'], [(240, 1436), (1773, 1566), 'text', '11'], [(200, 1573), (236, 1613), 'check_box', '12'], [(240, 1570), (1786, 1616), 'text', '12'], [(200, 1690), (236, 1726), 'check_box', '13'], [(240, 1686), (1520, 1726), 'text', '13'], [(236, 1733), (276, 1773), 'check_box', '13.a'], [(276, 1733), (336, 1776), 'text', '13.a'], [(376, 1733), (413, 1773), 'check_box', '13.b'], [(413, 1733), (506, 1776), 'text', '13.b'], [(553, 1733), (590, 1773), 'check_box', '13.c'], [(593, 1736), (753, 1773), 'text', '13.c'], [(276, 1780), (316, 1816), 'check_box', '13.1'], [(326, 1776), (1303, 1813), 'text', '13.1'], [(276, 1826), (316, 1863), 'check_box', '13.2'], [(326, 1823), (1606, 1866), 'text', '13.2'], [(276, 1873), (316, 1910), 'check_box', '13.3'], [(330, 1870), (1726, 1963), 'text', '13.3'], [(146, 2116), (183, 2153), 'check_box', 'attach.1'], [(186, 2120), (876, 2150), 'text', 'attach.1'], [(146, 2153), (183, 2190), 'check_box', 'attach.2'], [(186, 2156), (886, 2193), 'text', 'attach.2'], [(146, 2186), (183, 2226), 'check_box', 'attach.3'], [(186, 2193), (896, 2260), 'text', 'attach.3'], [(1066, 2116), (1106, 2153), 'check_box', 'attach.4'], [(1110, 2120), (1566, 2183), 'text', 'attach.4'], [(1066, 2180), (1106, 2216), 'check_box', 'attach.5'], [(1106, 2183), (1576, 2226), 'text', 'attach.5'], [(1066, 2216), (1106, 2253), 'check_box', 'attach.6'], [(1103, 2216), (1586, 2270), 'text', 'attach.6']]
                                for x,r in enumerate(roi):
                                    if r[2]=='check_box':
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                        total_pixels=cv2.countNonZero(value)
                                        if total_pixels>450:
                                            roi_r = roi[x+1]
                                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value= value.rstrip()
                                            value=value.replace('\n',' ')
                                            check_box[roi_r[3]]=value
                else:
                    roi=[(114, 84), (778, 208), 'check_text', 'Advisory Action Before the Filing of an Appeal Brief']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    value=value.replace('\n',' ')
                    if value==roi[3]:
                        print('type7')
                        roi=[(798, 92), (1192, 130), 'text', 'app_number']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        value=value.replace(' ','')
                        file['app_number']=value
                        check_box={}
                        file['check_box']=check_box
                        roi=[[(136, 336), (168, 368), 'check_box', '1'], [(176, 338), (1756, 476), 'text', '1'], [(170, 480), (204, 514), 'check_box', '1.a'], [(210, 484), (1762, 512), 'text', '1.a'], [(172, 518), (204, 550), 'check_box', '1.b'], [(210, 518), (1766, 574), 'text', '1.b'], [(174, 578), (206, 610), 'check_box', '1.c'], [(212, 582), (1738, 666), 'text', '1.c'], [(136, 938), (168, 970), 'check_box', '2'], [(170, 940), (1758, 994), 'text', '2'], [(138, 1058), (168, 1088), 'check_box', '3'], [(172, 1060), (1474, 1092), 'text', '3'], [(204, 1092), (240, 1126), 'check_box', '3.a'], [(242, 1096), (1362, 1128), 'text', '3.a'], [(206, 1128), (238, 1160), 'check_box', '3.b'], [(242, 1130), (862, 1166), 'text', '3.b'], [(206, 1162), (238, 1196), 'check_box', '3.c'], [(242, 1164), (1564, 1226), 'text', '3.c'], [(206, 1224), (240, 1256), 'check_box', '3.d'], [(242, 1230), (1566, 1286), 'text', '3.d'], [(134, 1288), (168, 1320), 'check_box', '4'], [(172, 1292), (1566, 1322), 'text', '4'], [(136, 1324), (170, 1356), 'check_box', '5'], [(172, 1328), (906, 1362), 'text', '5'], [(136, 1360), (170, 1390), 'check_box', '6'], [(170, 1362), (1754, 1390), 'text', '6'], [(134, 1419), (167, 1452), 'check_box', '7'], [(172, 1425), (746, 1455), 'text', '7'], [(782, 1421), (817, 1453), 'check_box', '7.a'], [(817, 1423), (1025, 1455), 'text', '7.a'], [(1089, 1421), (1121, 1453), 'check_box', '7.b'], [(1123, 1423), (1653, 1453), 'text', '7.b'], [(134, 1514), (169, 1547), 'check_box', '8'], [(172, 1517), (1059, 1549), 'text', '8'], [(134, 1549), (169, 1582), 'check_box', '9'], [(169, 1552), (1754, 1642), 'text', '9'], [(149, 1639), (182, 1672), 'check_box', '10'], [(184, 1644), (1759, 1732), 'text', '10'], [(149, 1728), (184, 1763), 'check_box', '11'], [(184, 1734), (1478, 1763), 'text', '11'], [(149, 1794), (181, 1826), 'check_box', '12'], [(184, 1797), (1626, 1826), 'text', '12'], [(149, 1858), (182, 1888), 'check_box', '13'], [(185, 1861), (1232, 1894), 'text', '13'], [(147, 1891), (182, 1923), 'check_box', '14'], [(182, 1894), (370, 1926), 'text', '14']]
                        for x,r in enumerate(roi):
                            if r[2]=='check_box':
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>289:
                                    roi_r = roi[x+1]
                                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value= value.rstrip()
                                    value=value.replace('\n',' ')
                                    check_box[roi_r[3]]=value
                    else:
                        roi=[(280, 1030), (406, 1068), 'check_text', 'Claim(s)']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value=value.rstrip()
                        value=value.replace('\n',' ')
                        if value==roi[3]:
                            print('type8')
                            roi=[(880, 108), (1304, 148), 'text', 'app_number']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            value=value.replace(' ','')
                            file['app_number']=value
                            check_box={}
                            file['check_box']=check_box
                            roi=[[(188, 668), (220, 702), 'check_box', '1'], [(234, 664), (1062, 704), 'text', '1'], [(214, 706), (250, 742), 'check_box', '1.1'], [(254, 708), (1408, 746), 'text', '1.1'], [(188, 758), (222, 790), 'check_box', '2.a'], [(228, 754), (626, 790), 'text', '2.a'], [(864, 756), (898, 790), 'check_box', '2.b'], [(900, 752), (1414, 792), 'text', '2.b'], [(188, 804), (220, 836), 'check_box', '3'], [(228, 796), (1774, 870), 'text', '3'], [(188, 884), (222, 918), 'check_box', '4'], [(230, 880), (1782, 954), 'text', '4'], [(224, 1032), (260, 1066), 'check_box', '5'], [(274, 1026), (1076, 1066), 'text', '5'], [(224, 1128), (258, 1164), 'check_box', '6'], [(272, 1124), (804, 1166), 'text', '6'], [(224, 1178), (258, 1212), 'check_box', '7'], [(268, 1170), (814, 1214), 'text', '7'], [(224, 1226), (258, 1262), 'check_box', '8'], [(266, 1222), (858, 1262), 'text', '8'], [(224, 1276), (258, 1310), 'check_box', '9'], [(272, 1272), (1306, 1308), 'text', '9'], [(186, 1499), (222, 1535), 'check_box', '10'], [(224, 1493), (1775, 1539), 'text', '10'], [(187, 1549), (219, 1584), 'check_box', '11'], [(227, 1542), (759, 1584), 'text', '11'], [(797, 1549), (829, 1582), 'check_box', '11.a'], [(842, 1547), (1032, 1587), 'text', '11.a'], [(1069, 1549), (1104, 1584), 'check_box', '11.b'], [(1107, 1539), (1654, 1587), 'text', '11.b'], [(190, 1733), (223, 1766), 'check_box', '12'], [(230, 1726), (1570, 1773), 'text', '12'], [(266, 1813), (303, 1850), 'check_box', '12.a'], [(306, 1810), (370, 1853), 'text', '12.a'], [(453, 1813), (486, 1850), 'check_box', '12.b'], [(493, 1810), (640, 1853), 'text', '12.b'], [(696, 1813), (730, 1850), 'check_box', '12.c'], [(733, 1810), (976, 1853), 'text', '12.c'], [(300, 1863), (333, 1900), 'check_box', '12.1'], [(353, 1853), (1326, 1900), 'text', '12.1'], [(300, 1913), (333, 1950), 'check_box', '12.2'], [(346, 1906), (1706, 1953), 'text', '12.2'], [(300, 1963), (333, 1996), 'check_box', '12.3'], [(350, 1953), (1756, 2043), 'text', '12.3'], [(133, 2166), (166, 2203), 'check_box', 'attach.1'], [(170, 2163), (640, 2206), 'text', 'attach.1'], [(133, 2226), (166, 2263), 'check_box', 'attach.2'], [(170, 2226), (956, 2293), 'text', 'attach.2'], [(1063, 2166), (1100, 2203), 'check_box', 'attach.3'], [(1100, 2160), (1520, 2246), 'text', 'attach.3'], [(1063, 2243), (1100, 2280), 'check_box', 'attach.4'], [(1100, 2243), (1513, 2283), 'text', 'attach.4']]
                            for x,r in enumerate(roi):
                                if r[2]=='check_box':
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>289:
                                        roi_r = roi[x+1]
                                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value= value.rstrip()
                                        value=value.replace('\n',' ')
                                        check_box[roi_r[3]]=value
                        else:
                            roi=[(278, 992), (404, 1032), 'check_text', 'Claim(s)']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value=value.rstrip()
                            if value==roi[3]:
                                print('type9')
                                roi=[(882, 106), (1304, 142), 'text', 'app_number']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                value=value.replace(' ','')
                                file['app_number']=value
                                check_box={}
                                file['check_box']=check_box
                                roi=[[(188, 632), (220, 664), 'check_box', '1'], [(226, 624), (1092, 666), 'text', '1'], [(214, 670), (248, 704), 'check_box', '1.1'], [(252, 670), (1390, 710), 'text', '1.1'], [(188, 720), (222, 754), 'check_box', '2.a'], [(224, 716), (626, 752), 'text', '2.a'], [(864, 718), (898, 752), 'check_box', '2.b'], [(902, 716), (1276, 752), 'text', '2.b'], [(188, 766), (220, 798), 'check_box', '3'], [(230, 762), (1780, 834), 'text', '3'], [(188, 846), (220, 880), 'check_box', '4'], [(230, 844), (1780, 920), 'text', '4'], [(226, 996), (258, 1026), 'check_box', '5'], [(274, 990), (1026, 1030), 'text', '5'], [(226, 1092), (258, 1126), 'check_box', '6'], [(272, 1088), (740, 1124), 'text', '6'], [(224, 1140), (260, 1176), 'check_box', '7'], [(272, 1136), (752, 1176), 'text', '7'], [(224, 1190), (258, 1224), 'check_box', '8'], [(272, 1184), (780, 1226), 'text', '8'], [(224, 1240), (258, 1272), 'check_box', '9'], [(270, 1234), (1324, 1274), 'text', '9'], [(187, 1462), (219, 1494), 'check_box', '10'], [(224, 1459), (974, 1499), 'text', '10'], [(187, 1512), (219, 1544), 'check_box', '11'], [(224, 1507), (757, 1552), 'text', '11'], [(797, 1512), (829, 1544), 'check_box', '11.a'], [(839, 1509), (1032, 1552), 'text', '11.a'], [(1069, 1512), (1102, 1544), 'check_box', '11.b'], [(1109, 1507), (1574, 1549), 'text', '11.b'], [(187, 1697), (219, 1729), 'check_box', '12'], [(227, 1692), (1567, 1732), 'text', '12'], [(268, 1777), (300, 1811), 'check_box', '12.a'], [(305, 1774), (385, 1814), 'text', '12.a'], [(454, 1777), (488, 1811), 'check_box', '12.b'], [(491, 1774), (637, 1814), 'text', '12.b'], [(697, 1777), (731, 1811), 'check_box', '12.c'], [(734, 1774), (957, 1817), 'text', '12.c'], [(300, 1828), (334, 1862), 'check_box', '12.1'], [(354, 1820), (1311, 1865), 'text', '12.1'], [(300, 1877), (334, 1911), 'check_box', '12.2'], [(351, 1871), (1682, 1914), 'text', '12.2'], [(300, 1925), (334, 1960), 'check_box', '12.3'], [(353, 1920), (1763, 2013), 'text', '12.3'], [(133, 2130), (166, 2166), 'check_box', 'attach.1'], [(170, 2126), (623, 2170), 'text', 'attach.1'], [(130, 2190), (166, 2226), 'check_box', 'attach.2'], [(170, 2186), (956, 2256), 'text', 'attach.2'], [(1063, 2130), (1100, 2166), 'check_box', 'attach.3'], [(1100, 2126), (1486, 2206), 'text', 'attach.3'], [(1063, 2206), (1100, 2243), 'check_box', 'attach.4'], [(1100, 2206), (1320, 2243), 'text', 'attach.4']]
                                for x,r in enumerate(roi):
                                    if r[2]=='check_box':
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                        total_pixels=cv2.countNonZero(value)
                                        if total_pixels>300:
                                            roi_r = roi[x+1]
                                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value= value.rstrip()
                                            value=value.replace('\n',' ')
                                            check_box[roi_r[3]]=value
                            else:
                                roi=[(248, 992), (376, 1030), 'check_text', 'Claim(s)']
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value=value.rstrip()
                                if value==roi[3]:
                                    print('type10')
                                    roi=[(882, 106), (1302, 144), 'text', 'app_number']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value=value.rstrip()
                                    value=value.replace(' ','')
                                    file['app_number']=value
                                    check_box={}
                                    file['check_box']=check_box
                                    roi=[[(188, 632), (222, 664), 'check_box', '1'], [(228, 624), (990, 666), 'text', '1'], [(216, 672), (248, 704), 'check_box', '1.1'], [(252, 668), (1380, 710), 'text', '1.1'], [(188, 722), (220, 754), 'check_box', '2.a'], [(228, 716), (596, 752), 'text', '2.a'], [(862, 718), (898, 752), 'check_box', '2.b'], [(900, 716), (1326, 750), 'text', '2.b'], [(188, 766), (222, 800), 'check_box', '3'], [(230, 760), (1778, 838), 'text', '3'], [(188, 848), (220, 882), 'check_box', '4'], [(228, 842), (1784, 918), 'text', '4'], [(202, 994), (236, 1028), 'check_box', '5'], [(242, 990), (1786, 1066), 'text', '5'], [(224, 1128), (258, 1162), 'check_box', '6'], [(268, 1124), (770, 1162), 'text', '6'], [(224, 1178), (260, 1214), 'check_box', '7'], [(268, 1174), (786, 1216), 'text', '7'], [(224, 1228), (258, 1262), 'check_box', '8'], [(270, 1222), (814, 1264), 'text', '8'], [(200, 1276), (234, 1312), 'check_box', '9'], [(238, 1272), (1770, 1348), 'text', '9'], [(187, 1537), (222, 1572), 'check_box', '10'], [(229, 1534), (1014, 1569), 'text', '10'], [(187, 1587), (219, 1619), 'check_box', '11'], [(224, 1579), (759, 1624), 'text', '11'], [(797, 1587), (829, 1619), 'check_box', '11.a'], [(839, 1584), (1032, 1627), 'text', '11.a'], [(1069, 1587), (1102, 1619), 'check_box', '11.b'], [(1107, 1579), (1577, 1624), 'text', '11.b'], [(186, 1770), (223, 1806), 'check_box', '12'], [(230, 1766), (1546, 1813), 'text', '12'], [(266, 1850), (303, 1886), 'check_box', '12.a'], [(306, 1846), (400, 1890), 'text', '12.a'], [(453, 1850), (486, 1886), 'check_box', '12.b'], [(493, 1846), (650, 1890), 'text', '12.b'], [(696, 1850), (730, 1886), 'check_box', '12.c'], [(736, 1850), (970, 1893), 'text', '12.c'], [(300, 1900), (333, 1936), 'check_box', '12.1'], [(353, 1893), (1490, 1936), 'text', '12.1'], [(300, 1950), (333, 1986), 'check_box', '12.2'], [(350, 1946), (1686, 1990), 'text', '12.2'], [(300, 2000), (330, 2033), 'check_box', '12.3'], [(350, 1996), (1763, 2076), 'text', '12.3'], [(133, 2160), (166, 2193), 'check_box', 'attach.1'], [(170, 2156), (746, 2196), 'text', 'attach.1'], [(133, 2220), (166, 2256), 'check_box', 'attach.2'], [(170, 2213), (980, 2286), 'text', 'attach.2'], [(1063, 2160), (1096, 2196), 'check_box', 'attach.3'], [(1100, 2156), (1470, 2240), 'text', 'attach.3'], [(1063, 2236), (1100, 2273), 'check_box', 'attach.4'], [(1100, 2236), (1480, 2283), 'text', 'attach.4']]
                                    for x,r in enumerate(roi):
                                        if r[2]=='check_box':
                                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                            total_pixels=cv2.countNonZero(value)
                                            if total_pixels>300:
                                                roi_r = roi[x+1]
                                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                                value= value.rstrip()
                                                value=value.replace('\n',' ')
                                                check_box[roi_r[3]]=value
        if file or b==3:
            break
        else:
            if b==1:
                path_file = rootPath+'\\'+a
                page = convert_from_path(path_file,dpi=220,poppler_path=r'C:\poppler-0.68.0\bin')
                filename = "page_1.jpg"
                filename = os.path.join(DOWNLOAD_FOLDER, filename)
                page[-1].save(filename, 'JPEG')
                filename2 = "page_2.jpg"
                filename2 = os.path.join(DOWNLOAD_FOLDER, filename2)
                page[-2].save(filename2, 'JPEG')
            else:
                filename=filename2
            b=b+1
    print(file)
    filen=a.replace('pdf','json')
    with open(os.path.join(DOWNLOAD_FOLDER) + "\\" + filen, 'w') as outfile:
        json.dump(file, outfile)
    s3.meta.client.upload_file( os.path.join(DOWNLOAD_FOLDER) + "\\" + filen, my_bucket, s3_dir+'/'+filen)
    end=time.time()
    tot=end-start
    print('total time taken: {} seconds'.format(tot))
except Exception as e:
    print('File found an error: ',e)