import re
import pytesseract
import cv2 
import numpy as np
import shutil
import sys 
from pdf2image import convert_from_path 
import os 
import time
from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileReader
import json
import boto3
s3 = boto3.resource('s3')
my_bucket = 'bb-bot-test'
s3_dir=sys.argv[1]
a=sys.argv[2]
pytesseract.pytesseract.tesseract_cmd=r'Tesseract-OCR\tesseract.exe'
total_time=0
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
#time.sleep(2)
filelimit = image_counter-1
print('Total no. of pages: ',filelimit)
file={}
section_1_0,section_1_1,section_1_2,section_1_3,section_1_4,section_1_5='','','','','',''
file_set=''
try:
    img = cv2.imread(page_lst[0])
    roi = [(112, 2308), (400, 2360), 'text', 'code_at_bottom']
    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
    code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
    code_at_bottom= code_at_bottom.rstrip()
    if 'PTOL-90A' in code_at_bottom:
        section_1_0=True
        print('section_1_0 ',section_1_0)
    else:
        roi=[(110, 2266), (406, 2310), 'text', 'code_at_bottom']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
        code_at_bottom= code_at_bottom.rstrip()
        if 'PTOL-90A' in code_at_bottom:
            section_1_0=True
            print('section_1_0 ',section_1_0)
    roi = [(476, 330), (1390, 390), 'Text', 'file type']
    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
    file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
    file_type = file_type.rstrip()
    #print(file_type)
    roi = [(48, 2328), (328, 2388), 'text', 'code_at_bottom']
    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
    code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
    code_at_bottom= code_at_bottom.rstrip()
    #print(code_at_bottom)
    if file_type=='NOTICE OF ALLOWANCE AND FEE(S) DUE' and 'PTOL-85' in code_at_bottom:
        section_1_1=True
        #print('sect 1 type 1')
        file['type']='Notice of Allowance'
        print('section_1_1 ',section_1_1)
        roi = [[(124, 806), (318, 840), 'Number', 'app_number'], [(394, 804), (604, 838), 'Date', 'filing_date'],
         [(694, 804), (1236, 840), 'Name', 'first_named_inventor'],
         [(1250, 806), (1520, 858), 'number', 'attorney_docket_no'],
         [(1538, 802), (1794, 846), 'Number', 'confirmation_no'], [(72, 1018), (306, 1058), 'text', 'appln_type'],
         [(314, 1018), (546, 1060), 'text', 'entity_status'], [(564, 1020), (800, 1058), 'amount', 'issue_fee_due'],
         [(812, 1022), (1058, 1062), 'amount', 'publication_fee_due'],
         [(1076, 1018), (1312, 1060), 'amount', 'prev_paid_issue_fee'],
         [(1332, 1020), (1554, 1062), 'amount', 'total_fee_due'], [(1572, 1020), (1798, 1060), 'Date', 'date_due'],
         [(1354, 594), (1414, 624), 'Number', 'art_unit'], [(1406, 486), (1648, 510), 'Name', 'examiner'],
         [(60, 852), (1644, 900), 'text', 'title'],[(48, 2332), (316, 2384), 'text', 'code_at_bottom']]
        for x,r in enumerate(roi):
            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
            value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
            value= value.rstrip()
            file[r[3]]=value
    else:
        roi=[(480, 352), (1432, 428), 'text', 'file_type']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
        file_type = file_type.rstrip()
        #print(file_type)
        roi=[(76, 2280), (810, 2316), 'text', 'code_at_bottom']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
        code_at_bottom= code_at_bottom.rstrip()
        if 'PTOL-85' in code_at_bottom:
            pass
        else:
            roi=[(100, 2230), (700, 2273), 'text', 'code_at_bottom']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
            code_at_bottom= code_at_bottom.rstrip()
        #print(code_at_bottom)
        section_1_1_lst=['NOTICE OF ALLOWANCE AND FEE(S) DUE','NOTICE OF ALLOWANCE AND FEK(S) DUE']
        if file_type in section_1_1_lst and 'PTOL-85' in code_at_bottom:
            #print('sect 1 type 2')
            section_1_1=True
            file['type']='Notice of Allowance'
            print('section_1_1 ',section_1_1)
            roi=[(158, 746), (340, 772), 'text', 'file_type']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
            file_type = file_type.rstrip()
            #print(file_type)
            if file_type=='APPLICATION NO.':
                roi=[[(160, 788), (370, 816), 'number', 'app_number'], [(398, 788), (620, 820), 'number', 'filing_date'], [(710, 792), (1142, 816), 'text', 'first_named_inventor'], [(1228, 790), (1452, 820), 'text', 'docket_no'], [(1494, 790), (1712, 822), 'number', 'confirmation_no'], [(114, 828), (1730, 924), 'text', 'title'], [(158, 990), (364, 1024), 'text', 'appln_type'], [(406, 992), (608, 1018), 'text', 'small_entity'], [(674, 988), (908, 1022), 'number', 'issue_fee'], [(960, 992), (1194, 1024), 'number', 'pub_fee'], [(1238, 990), (1450, 1020), 'number', 'total_fee_due'], [(1494, 990), (1714, 1028), 'number', 'date_due'], [(1248, 588), (1460, 616), 'number', 'art_unit'], [(1256, 488), (1722, 520), 'text', 'examiner']]
                for x,r in enumerate(roi):
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                    value= value.rstrip()
                    file[r[3]]=value
                file['code_at_bottom']=code_at_bottom
            else:
                roi=[(142, 790), (326, 818), 'text', 'file_type']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                file_type = file_type.rstrip()
                if file_type=='APPLICATION NO.':
                    roi=[[(132, 836), (350, 868), 'number', 'app_number'], [(388, 834), (604, 866), 'number', 'filing_date'], [(700, 838), (1198, 874), 'text', 'first_named_inventor'], [(1236, 836), (1470, 874), 'text', 'docket_no'], [(1520, 838), (1726, 876), 'number', 'confirmation_no'], [(100, 864), (1732, 960), 'text', 'title'], [(134, 1042), (356, 1078), 'text', 'appln_type'], [(386, 1042), (618, 1076), 'text', 'small_entity'], [(654, 1040), (914, 1078), 'number', 'issue_fee'], [(954, 1040), (1212, 1078), 'number', 'pub_fee'], [(1248, 1042), (1472, 1076), 'number', 'total_fee_due'], [(1516, 1044), (1724, 1078), 'number', 'date_due'], [(1248, 620), (1476, 644), 'number', 'art_unit'], [(1302, 532), (1710, 558), 'text', 'examiner']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                        value= value.rstrip()
                        file[r[3]]=value
                    file['code_at_bottom']=code_at_bottom
                else:
                    roi=[[(146, 808), (360, 842), 'number', 'app_number'], [(406, 810), (626, 842), 'number', 'filing_date'], [(732, 814), (1200, 848), 'text', 'first_named_inventor'], [(1248, 812), (1480, 844), 'text', 'docket_no'], [(1530, 814), (1734, 844), 'number', 'confirmation_no'], [(150, 1012), (372, 1048), 'text', 'appln_type'], [(420, 1014), (596, 1048), 'text', 'small_entity'], [(704, 1014), (898, 1048), 'number', 'issue_fee'], [(1000, 1014), (1186, 1048), 'number', 'pub_fee'], [(1288, 1018), (1456, 1046), 'number', 'total_fee'], [(1528, 1016), (1730, 1046), 'number', 'date_due'], [(1288, 606), (1472, 636), 'number', 'art_unit'], [(1344, 508), (1688, 538), 'text', 'examiner'], [(110, 848), (1752, 938), 'text', 'title']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                        value= value.rstrip()
                        file[r[3]]=value
                    file['code_at_bottom']=code_at_bottom
        else:
            roi=[(76, 2293), (696, 2336), 'text', 'code_at_bottom']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
            code_at_bottom= code_at_bottom.rstrip()
            if file_type=='NOTICE OF ALLOWANCE AND FEE(S) DUE' and 'PTOL-85' in code_at_bottom:
                #print('sect 1 type 3')
                section_1_1=True
                file['type']='Notice of Allowance'
                print('section_1_1 ',section_1_1)
                roi=[(130, 780), (320, 810), 'text', 'file_type']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                file_type=pytesseract.image_to_string(imgcrop, config='--psm 6')
                file_type= file_type.rstrip()
                if file_type=='APPLICATION NO.':
                    roi=[[(152, 826), (322, 858), 'number', 'app_number'], [(384, 828), (600, 860), 'number', 'filing_date'], [(744, 826), (1182, 860), 'text', 'first_named_inventor'], [(1238, 826), (1480, 858), 'text', 'docket_no'], [(1522, 826), (1730, 856), 'number', 'confirmation_no'], [(1276, 606), (1446, 630), 'number', 'art_unit'], [(1348, 516), (1700, 540), 'text', 'examiner'], [(86, 860), (1754, 948), 'text', 'title'], [(108, 1034), (322, 1070), 'text', 'appln_type'], [(342, 1034), (536, 1066), 'text', 'small_entity'], [(588, 1036), (772, 1064), 'text', 'issue_fee_due'], [(814, 1034), (1028, 1064), 'number', 'pub_fee_due'], [(1066, 1032), (1280, 1068), 'number', 'prev_paid_issue_fee'], [(1312, 1034), (1516, 1062), 'number', 'total_fee_due'], [(1556, 1032), (1752, 1062), 'number', 'date_due']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                        value= value.rstrip()
                        file[r[3]]=value
                else:
                    roi=[[(146, 808), (360, 842), 'number', 'app_number'], [(406, 810), (626, 842), 'number', 'filing_date'], [(732, 814), (1200, 848), 'text', 'first_named_inventor'], [(1248, 812), (1480, 844), 'text', 'docket_no'], [(1530, 814), (1734, 844), 'number', 'confirmation_no'], [(150, 1012), (372, 1048), 'text', 'appln_type'], [(420, 1014), (596, 1048), 'text', 'small_entity'], [(704, 1014), (898, 1048), 'number', 'issue_fee'], [(1000, 1014), (1186, 1048), 'number', 'pub_fee'], [(1288, 1018), (1456, 1046), 'number', 'total_fee'], [(1528, 1016), (1730, 1046), 'number', 'date_due'], [(1288, 606), (1472, 636), 'number', 'art_unit'], [(1344, 508), (1688, 538), 'text', 'examiner'], [(110, 848), (1752, 938), 'text', 'title']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                        value= value.rstrip()
                        file[r[3]]=value
                file['code_at_bottom']=code_at_bottom
            else:
                roi=[(100, 2260), (750, 2313), 'text', 'code_at_bottom']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
                code_at_bottom= code_at_bottom.rstrip()
                #print(code_at_bottom)
                if file_type=='NOTICE OF ALLOWANCE AND FEE(S) DUE' and 'PTOL-85' in code_at_bottom:
                    section_1_1=True
                    file['type']='Notice of Allowance'
                    print('section_1_1 ',section_1_1)
                    roi=[[(146, 808), (360, 842), 'number', 'app_number'], [(406, 810), (626, 842), 'number', 'filing_date'], [(732, 814), (1200, 848), 'text', 'first_named_inventor'], [(1248, 812), (1480, 844), 'text', 'docket_no'], [(1530, 814), (1734, 844), 'number', 'confirmation_no'], [(150, 1012), (372, 1048), 'text', 'appln_type'], [(420, 1014), (596, 1048), 'text', 'small_entity'], [(704, 1014), (898, 1048), 'number', 'issue_fee'], [(1000, 1014), (1186, 1048), 'number', 'pub_fee'], [(1288, 1018), (1456, 1046), 'number', 'total_fee'], [(1528, 1016), (1730, 1046), 'number', 'date_due'], [(1288, 606), (1472, 636), 'number', 'art_unit'], [(1344, 508), (1688, 538), 'text', 'examiner'], [(110, 848), (1752, 938), 'text', 'title']]
                    for x,r in enumerate(roi):
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                        value= value.rstrip()
                        file[r[3]]=value
                    file['code_at_bottom']=code_at_bottom
                else:
                    roi=[(430, 286), (1413, 380), 'text', 'file_type']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    file_type=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    file_type= file_type.rstrip()
                    file_type=file_type.replace('\n',' ')
                    roi=[(24, 2334), (306, 2382), 'text', 'code_at_bottom']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    code_at_bottom= code_at_bottom.rstrip()
                    if file_type=='CORRECTED NOTICE OF ALLOWANCE AND FEE(S) DUE' and 'PTOL-85' in code_at_bottom:
                        section_1_1=True
                        file['type']='Corrected Notice of Allowance'
                        print('section_1_1 ',section_1_1)
                        roi=[[(70, 800), (308, 832), 'number', 'app_number'], [(344, 800), (592, 830), 'number', 'filing_date'], [(646, 798), (1220, 826), 'text', 'first_named_inventor'], [(1254, 794), (1504, 826), 'text', 'docket_no'], [(1542, 796), (1772, 824), 'number', 'confirmation_no'], [(28, 838), (1782, 924), 'text', 'title'], [(62, 1020), (272, 1054), 'text', 'appln_type'], [(300, 1018), (516, 1052), 'text', 'entity'], [(562, 1016), (760, 1050), 'number', 'issue_fee_due'], [(806, 1016), (1022, 1046), 'number', 'pub_fee_due'], [(1090, 1014), (1284, 1044), 'number', 'prev_paid_issue_fee'], [(1334, 1012), (1536, 1044), 'text', 'total_fee_due'], [(1576, 1014), (1774, 1046), 'number', 'date_due'], [(1278, 582), (1464, 608), 'number', 'art_unit'], [(1352, 472), (1700, 502), 'text', 'examiner']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                            value= value.rstrip()
                            file[r[3]]=value
                        file['code_at_bottom']=code_at_bottom
    for i in file.keys():
        if i=='title':
            value=file['title']
            value = value.replace('\n',' ')
            value = value.replace('TITLE OF INVENTION: ','')
            file['title']=value
        if i=='attorney_docket_no':
            value=file['attorney_docket_no']
            value = value.replace('\n',' ')
            file['attorney_docket_no']=value
    if len(page_lst)>1:
        img = cv2.imread(page_lst[1])
        roi = [(668, 40), (1212, 104), 'text', 'file_type']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
        file_type = file_type.rstrip()
        #print(file_type)
        roi = [(36, 2324), (348, 2388), 'text', 'code_at_bottom']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
        code_at_bottom= code_at_bottom.rstrip()
        #print(code_at_bottom)
        if file_type=='PART B - FEE(S) TRANSMITTAL' and 'PTOL-85' in code_at_bottom:
            section_1_2=True
            print('section_1_2 ',section_1_2)
        else:
            roi=[(683, 73), (1180, 120), 'text', 'file_type']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
            file_type = file_type.rstrip()
            #print(file_type)
            roi=[(73, 2296), (696, 2340), 'text', 'code_at_bottom']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
            code_at_bottom= code_at_bottom.rstrip()
            #print(code_at_bottom)
            if 'PTOL-85' in code_at_bottom:
                pass
            else:
                roi=[(100, 2276), (693, 2316), 'text', 'code_at_bottom']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
                code_at_bottom= code_at_bottom.rstrip()
            section_1_2_lst=['PART B- FEE(S) TRANSMITTAL','PART B - FEE(S) TRANSMITTAL']
            if file_type in section_1_2_lst and 'PTOL-85' in code_at_bottom:
                section_1_2=True
                print('section_1_2 ',section_1_2)
            else:
                roi=[(690, 96), (1196, 143), 'text', 'file_type']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                file_type = file_type.rstrip()
                #print(file_type)
                roi=[(100, 2260), (710, 2306), 'text', 'code_at_bottom']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
                code_at_bottom= code_at_bottom.rstrip()
                #print(code_at_bottom)
                if 'PTOL-85' in code_at_bottom:
                    pass
                else:
                    roi=[(83, 2300), (696, 2340), 'text', 'code_at_bottom']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    code_at_bottom= code_at_bottom.rstrip()
                if file_type in section_1_2_lst and 'PTOL-85' in code_at_bottom:
                    section_1_2=True
                    print('section_1_2 ',section_1_2)
                else:
                    roi=[(689, 120), (1175, 162), 'text', 'file_type']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                    file_type = file_type.rstrip()
                    roi=[(86, 2310), (706, 2365), 'text', 'code_at_bottom']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    code_at_bottom= code_at_bottom.rstrip()
                    if file_type in section_1_2_lst and 'PTOL-85' in code_at_bottom:
                        section_1_2=True
                        print('section_1_2 ',section_1_2)
    if len(page_lst)>2:
        img = cv2.imread(page_lst[2])
        roi = [(380, 876), (1496, 936), 'text', 'file_type']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
        file_type = file_type.rstrip()
        #print(file_type)
        roi = [(70, 2296), (716, 2343), 'text', 'code_at_bottom']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
        code_at_bottom= code_at_bottom.rstrip()
        #print(code_at_bottom)
        if 'PTOL-85' in code_at_bottom:
            pass
        else:
            roi=[(96, 2256), (746, 2310), 'text', 'code_at_bottom']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
            code_at_bottom= code_at_bottom.rstrip()
        #print(code_at_bottom)
        if file_type=='Determination of Patent Term Adjustment under 35 U.S.C. 154 (b)' and 'PTOL-85' in code_at_bottom:
            section_1_3=True
            print('section_1_3 ',section_1_3)
        else:
            roi=[(420, 856), (1443, 910), 'text', 'file_type']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
            file_type = file_type.rstrip()
            #print(file_type)
            roi=[(100, 2226), (733, 2273), 'text', 'code_at_bottom']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
            code_at_bottom= code_at_bottom.rstrip()
            #print(code_at_bottom)
            if file_type=='Determination of Patent Term Adjustment under 35 U.S.C. 154 (b)' and 'PTOL-85' in code_at_bottom:
                section_1_3=True
                print('section_1_3 ',section_1_3)
            else:
                roi=[(416, 903), (1443, 953), 'text', 'file_type']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                file_type = file_type.rstrip()
                #print(file_type)
                roi = [(90, 2273), (716, 2316), 'text', 'code_at_bottom']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
                code_at_bottom= code_at_bottom.rstrip()
                if file_type=='Determination of Patent Term Adjustment under 35 U.S.C. 154 (b)' and 'PTOL-85' in code_at_bottom:
                    section_1_3=True
                    print('section_1_3 ',section_1_3)
                else:
                    roi=[(366, 878), (1492, 924), 'text', 'file_type']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                    file_type = file_type.rstrip()
                    #print(file_type)
                    roi = [(24, 2334), (317, 2386), 'text', 'code_at_bottom']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    code_at_bottom= code_at_bottom.rstrip()
                    if file_type=='Determination of Patent Term Adjustment under 35 U.S.C. 154 (b)' and 'PTOL-85' in code_at_bottom:
                        section_1_3=True
                        print('section_1_3 ',section_1_3)
                    if len(page_lst)>3:
                        img = cv2.imread(page_lst[3])
                        roi = [(380, 876), (1496, 936), 'text', 'file_type']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                        file_type = file_type.rstrip()
                        #print(file_type)
                        roi = [(44, 2324), (356, 2388), 'text', 'code_at_bottom']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        code_at_bottom=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        code_at_bottom= code_at_bottom.rstrip()
                        #print(code_at_bottom)
                        if file_type=='Determination of Patent Term Adjustment under 35 U.S.C. 154 (b)' and 'PTOL-85' in code_at_bottom:
                            section_1_3=True
                            print('section_1_3 ',section_1_3)
    img_section_1_4=''
    img = cv2.imread(page_lst[0])        
    roi=[(172, 170), (850, 310), 'text', 'file_type']
    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
    file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
    file_type = file_type.rstrip()
    file_type=file_type.lower()
    file_type=file_type.replace('\n',' ')
    file_type=file_type.replace(' |','')
    lst_section_1_4=['notice of allowability','corrected notice of allowability','supplemental notice of allowability']
    if file_type in lst_section_1_4:
        file['type']='Notice of Allowability'
        section_1_4=True
        img_section_1_4=cv2.imread(page_lst[0])
    else:
        roi=[(255, 268), (820, 362), 'text', 'file_type']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
        file_type = file_type.rstrip()
        file_type=file_type.lower()
        file_type=file_type.replace('\n',' ')
        if file_type in lst_section_1_4:
            file['type']='Notice of Allowability'
            section_1_4=True
            img_section_1_4=cv2.imread(page_lst[0])
        else:
            if len(page_lst)>1:
                img = cv2.imread(page_lst[1])
                roi=[(204, 156), (804, 278), 'text', 'file_type']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                file_type = file_type.rstrip()
                file_type=file_type.lower()
                file_type=file_type.replace('\n',' ')
                file_type=file_type.replace("'","")
                file_type=file_type.replace('  ',' ')
                if file_type in lst_section_1_4:
                    section_1_4=True
                    img_section_1_4=cv2.imread(page_lst[1])
                else:
                    roi=[(200, 144), (712, 240), 'text', 'file_type']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                    file_type = file_type.rstrip()
                    file_type=file_type.lower()
                    file_type=file_type.replace('\n',' ')
                    file_type=file_type.replace("'","")
                    file_type=file_type.replace('  ',' ')
                    file_type=file_type.replace('supplemenial','supplemental')
                    #print(file_type)
                    if file_type in lst_section_1_4:
                        section_1_4=True
                        img_section_1_4=cv2.imread(page_lst[1])
                    else:
                        if len(page_lst)>4:
                            img = cv2.imread(page_lst[4])
                            roi=[(168, 174), (811, 300), 'text', 'file_type']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                            file_type = file_type.rstrip()
                            file_type=file_type.lower()
                            file_type=file_type.replace('\n',' ')
                            if file_type in lst_section_1_4:
                                section_1_4=True
                                img_section_1_4=cv2.imread(page_lst[4])
                            else:
                                if len(page_lst)>5:
                                    img = cv2.imread(page_lst[5])
                                    roi=[(174, 171), (837, 280), 'text', 'file_type']
                                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                    file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                                    file_type = file_type.rstrip()
                                    file_type=file_type.lower()
                                    file_type=file_type.replace('\n',' ')
                                    if file_type in lst_section_1_4:
                                        section_1_4=True
                                        img_section_1_4=cv2.imread(page_lst[5])

    roi=[(176, 160), (766, 284), 'text', 'file type']
    if len(page_lst)>1:
        img = cv2.imread(page_lst[1])
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
        file_type = file_type.rstrip()
        file_type = file_type.replace('\n',' ')
        file_type=file_type.lower()
        if file_type=='supplemental notice of allowability' and 'PTOL-90A' in code_at_bottom:
            file['type']='Supplemental Notice of Allowance'
        if file_type=='supplemental notice of allowability' and 'PTOL-37' in code_at_bottom:
            file['type']='Supplemental Notice of Allowability'
        if file_type=='corrected notice of allowability' and 'PTOL-90A' in code_at_bottom:
            file['type']='Corrected Notice of Allowance'
        if file_type=='corrected notice of allowability' and 'PTOL-37' in code_at_bottom:
            file['type']='Corrected Notice of Allowability'

    lst_section_1_5=['Page 2','Page2']
    roi = [(1465, 41), (1848, 244), 'text', 'file_type']
    img = cv2.imread(page_lst[0])
    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
    Set_3_examiner = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
    Set_3_examiner = Set_3_examiner.rstrip()
    #print(Set_3_examiner)
    img_section_1_5=''
    if Set_3_examiner in lst_section_1_5:
        file_set='Set_3'
        section_1_5=True
        img_section_1_5=cv2.imread(page_lst[0])
        img_n=0
    else:
        if len(page_lst)>1:
            img = cv2.imread(page_lst[1])
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            Set_3_examiner = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
            Set_3_examiner = Set_3_examiner.rstrip()
            #print(Set_3_examiner)
            if Set_3_examiner in lst_section_1_5:
                file_set='Set_3'
                section_1_5=True
                img_section_1_5=cv2.imread(page_lst[1])
                img_n=1
            else:
                roi=[(1470, 190), (1762, 310), 'text', 'file_type']
                img = cv2.imread(page_lst[1])
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                Set_3_examiner = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                Set_3_examiner = Set_3_examiner.rstrip()
                #print(Set_3_examiner)
                if Set_3_examiner in lst_section_1_5:
                    file_set='Set_3'
                    section_1_5=True
                    img_section_1_5=cv2.imread(page_lst[1])
                    img_n=1
                else:
                    if len(page_lst)>2:
                        roi=[(1517, 94), (1714, 162), 'text', 'file_type']
                        img = cv2.imread(page_lst[2])
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        Set_3_examiner = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                        Set_3_examiner = Set_3_examiner.rstrip()
                        if Set_3_examiner in lst_section_1_5:
                            file_set='Set_3'
                            section_1_5=True
                            img_section_1_5=cv2.imread(page_lst[2])
                            img_n=2
                        else:
                            if len(page_lst)>3:
                                roi=[(1525, 97), (1697, 162), 'text', 'file_type']
                                img = cv2.imread(page_lst[3])
                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                Set_3_examiner = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                                Set_3_examiner = Set_3_examiner.rstrip()
                                if Set_3_examiner in lst_section_1_5:
                                    file_set='Set_3'
                                    section_1_5=True
                                    img_section_1_5=cv2.imread(page_lst[3])
                                    img_n=3
                                else:
                                    roi = [(1465, 41), (1848, 244), 'text', 'file_type']
                                    if len(page_lst)>5:
                                        img = cv2.imread(page_lst[5])
                                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                        Set_3_examiner = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                                        Set_3_examiner = Set_3_examiner.rstrip()
                                        #print(Set_3_examiner)
                                        if Set_3_examiner in lst_section_1_5:
                                            file_set='Set_3'
                                            section_1_5=True
                                            img_section_1_5=cv2.imread(page_lst[5])
                                            img_n=5
                                        else:
                                            if len(page_lst)>6:
                                                img = cv2.imread(page_lst[6])
                                                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                                                Set_3_examiner = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                                                Set_3_examiner = Set_3_examiner.rstrip()
                                                #print(Set_3_examiner)
                                                if Set_3_examiner in lst_section_1_5:
                                                    file_set='Set_3'
                                                    section_1_5=True
                                                    img_section_1_5=cv2.imread(page_lst[6])
                                                    img_n=6
except Exception as e:
    print('File found an error: ',e)
if section_1_1 and section_1_2 and section_1_3 and section_1_4 and section_1_5:
    file_set='Set_1'
elif section_1_1 and section_1_2 and section_1_3 and section_1_5:
    file_set='Set_1'
elif section_1_1 and section_1_2 and section_1_4 and section_1_5:
    file_set='Set_1'
elif section_1_1 and section_1_2 and section_1_3 and section_1_4:
    file_set='Set_1'
elif section_1_0 and section_1_4 and section_1_5:
    file_set='Set_2'
file['File_sets']=file_set
if section_1_0 or section_1_1 or section_1_2 or section_1_3 or section_1_4 or section_1_5:
    pass
else:
    file['File_sets']='error'
    error_file_path=r'C:\Users\admin\Abhishek_working\error_files'
    shutil.copy(path_file, error_file_path)
if section_1_0:
    if len(page_lst)>1:
        roi=[(894, 204), (1040, 238), 'text', 'check_number']
        img = cv2.imread(page_lst[1])
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        file_type = pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
        file_type = file_type.rstrip()
        if file_type=='Examiner':
            roi=[[(896, 172), (1108, 198), 'number', 'app_number'], [(892, 238), (1284, 264), 'text', 'examiner'], [(1334, 172), (1688, 198), 'text', 'applicant'], [(1332, 236), (1450, 264), 'text', 'art_unit'], [(1518, 238), (1654, 266), 'text', 'aia_status']]
            for x,r in enumerate(roi):
                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                value= value.rstrip()
                file[r[3]]=value
                if r[3]=='app_number':
                    value = value.replace('.',',')
                    file[r[3]]=value
        else:
            roi=[[(880, 178), (1134, 234), 'Number', 'app_number'],
                 [(880, 274), (1154, 330), 'Name', 'examiner'],
                 [(1322, 174), (1622, 232), 'Name', 'applicant'],
                 [(1320, 274), (1504, 332), 'Number', 'art_unit'],
                 [(100, 2324), (392, 2376), 'text', 'code_at_bottom']]
            for x,r in enumerate(roi):
                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                value= value.rstrip()
                file[r[3]]=value
                if r[3]=='app_number':
                    value = value.replace('.',',')
                    file[r[3]]=value
if section_1_4:
    check_box_dict={}
    print('section_1_4 ',section_1_4)
    if section_1_0 or section_1_1:
        pass
    else:
        img = img_section_1_4
        roi=[[(878, 182), (1118, 230), 'number', 'app_number'], [(1318, 182), (1720, 230), 'text', 'applicant'], [(878, 276), (1226, 328), 'text', 'examiner'], [(1318, 274), (1506, 328), 'number', 'art_unit']]
        for x,r in enumerate(roi):
            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
            value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
            value= value.rstrip()
            file[r[3]]=value
            if r[3]=='app_number':
                value = value.replace('.',',')
                file[r[3]]=value
    img = img_section_1_4
    roi = [(80, 514), (117, 551), 'check_number', '1']
    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
    value= value.rstrip() 
    if value=='1.':
        #print('type 1')
        roi=[[(117, 511), (157, 551), 'check_box', 'check_box_1'], [(157, 511), (1791, 548), 'text', '1'], [(162, 554), (205, 597), 'check_box', 'check_box_1.1'], [(205, 557), (1794, 594), 'text', '1.1'], [(117, 614), (157, 654), 'check_box', 'check_box_2'], [(157, 611), (1797, 691), 'text', '2'], [(117, 702), (157, 745), 'check_box', 'check_box_3'], [(157, 702), (1797, 822), 'text', '3'], [(117, 834), (157, 874), 'check_box', 'check_box_4'], [(157, 834), (1800, 877), 'text', '4'], [(211, 922), (251, 960), 'check_box', 'check_box_4.a'], [(257, 922), (331, 960), 'text', '4.a'], [(371, 922), (411, 960), 'check_box', 'check_box_4.b'], [(411, 922), (511, 960), 'text', '4.b'], [(554, 922), (594, 960), 'check_box', 'check_box_4.c'], [(594, 922), (774, 960), 'text', '4.c'], [(280, 962), (320, 1002), 'check_box', 'check_box_4.1'], [(317, 968), (1794, 994), 'text', '4.1'], [(280, 1005), (320, 1045), 'check_box', 'check_box_4.2'], [(317, 1011), (1797, 1040), 'text', '4.2'], [(280, 1051), (320, 1088), 'check_box', 'check_box_4.2'], [(317, 1054), (1800, 1140), 'text', '4.3'], [(211, 1231), (254, 1274), 'check_box', 'check_box_interim_a'], [(254, 1234), (320, 1274), 'text', 'interim_copies.a'], [(351, 1231), (394, 1274), 'check_box', 'check_box_interim_b'], [(394, 1234), (505, 1271), 'text', 'interim_copies.b'], [(542, 1231), (585, 1274), 'check_box', 'check_box_interim_c'], [(585, 1237), (1800, 1271), 'text', 'interim_copies.c'], [(117, 1400), (157, 1440), 'check_box', 'check_box_5'], [(157, 1400), (1800, 1425), 'text', '5'], [(165, 1451), (205, 1491), 'check_box', 'check_box_5.1'], [(214, 1451), (1800, 1511), 'text', '5.1'], [(117, 1597), (157, 1637), 'check_box', 'check_box_6'], [(137, 1600), (1794, 1662), 'text', '6'], [(117, 1745), (157, 1785), 'check_box', 'check_box_attach_1'], [(157, 1751), (931, 1782), 'text', 'attachments.1'], [(117, 1791), (157, 1831), 'check_box', 'check_box_attach.2'], [(157, 1794), (937, 1854), 'text', 'attachments.2'], [(117, 1854), (157, 1894), 'check_box', 'check_box_attach.3'], [(157, 1857), (922, 1922), 'text', 'attachments.3'], [(117, 1917), (157, 1957), 'check_box', 'check_box_attach.4'], [(157, 1920), (931, 1985), 'text', 'attachments.4'], [(1048, 1748), (1085, 1785), 'check_box', 'check_box_attach.5'], [(1085, 1751), (1748, 1782), 'text', 'attachments.5'], [(1045, 1791), (1085, 1831), 'check_box', 'check_box_attach.6'], [(1085, 1794), (1757, 1837), 'text', 'attachments.6'], [(1045, 1854), (1085, 1894), 'check_box', 'check_box_attach.7'], [(1085, 1857), (1280, 1897), 'text', 'attachments.7']]
        for x,r in enumerate(roi):
            if r[2]=='check_box':
                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                total_pixels=cv2.countNonZero(value)
                if total_pixels>425:
                    roi_r = roi[x+1]
                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value= value.rstrip()
                    value=value.replace('\n',' ')
                    check_box_dict[roi_r[3]]=value
    else:
        roi = [(72, 728), (104, 760), 'text', 'check_number']
        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
        value= value.rstrip() 
        if value=='4.':
            #print('type 2')
            roi=[[(102, 540), (142, 580), 'check_box', 'check_box_1'], [(142, 542), (1777, 571), 'text', '1'], [(102, 591), (142, 628), 'check_box', 'check_box_2'], [(111, 594), (1780, 665), 'text', '2'], [(102, 671), (142, 711), 'check_box', 'check_box_3'], [(142, 671), (1780, 700), 'text', '3'], [(102, 722), (142, 760), 'check_box', 'check_box_4'], [(142, 726), (1292, 762), 'text', '4'], [(197, 762), (237, 802), 'check_box', 'check_box_4.a'], [(242, 762), (308, 802), 'text', '4.a'], [(357, 762), (397, 802), 'check_box', 'check_box_4.b'], [(397, 765), (502, 802), 'text', '4.b'], [(542, 762), (582, 802), 'check_box', 'check_box_4.c'], [(582, 765), (785, 805), 'text', '4.c'], [(265, 805), (305, 845), 'check_box', 'check_box_4.1'], [(304, 812), (1230, 842), 'text', '4.1'], [(265, 851), (305, 891), 'check_box', 'check_box_4.2'], [(305, 851), (1780, 888), 'text', '4.2'], [(265, 894), (305, 934), 'check_box', 'check_box_4.3'], [(305, 897), (1777, 965), 'text', '4.3'], [(102, 1145), (142, 1185), 'check_box', 'check_box_5'], [(142, 1142), (1777, 1211), 'text', '5'], [(102, 1228), (142, 1268), 'check_box', 'check_box_6'], [(142, 1228), (1777, 1257), 'text', '6'], [(168, 1268), (205, 1308), 'check_box', 'check_box_6.a'], [(205, 1268), (1782, 1297), 'text', '6.a'], [(265, 1311), (305, 1351), 'check_box', 'check_box_6.1'], [(305, 1314), (425, 1351), 'text', '6.1'], [(454, 1311), (494, 1351), 'check_box', 'check_box_6.2'], [(500, 1314), (985, 1351), 'text', '6.2'], [(168, 1357), (205, 1394), 'check_box', 'check_box_6.b'], [(205, 1360), (1757, 1437), 'text', '6.b'], [(102, 1514), (142, 1554), 'check_box', 'check_box_7'], [(120, 1514), (1765, 1577), 'text', '7'], [(102, 1725), (142, 1765), 'check_box', 'check_box_attach.1'], [(142, 1728), (885, 1760), 'text', 'attachments.1'], [(102, 1771), (142, 1808), 'check_box', 'check_box_attach.2'], [(142, 1771), (888, 1814), 'text', 'attachments.2'], [(102, 1834), (142, 1871), 'check_box', 'check_box_attach.3'], [(142, 1837), (894, 1894), 'text', 'attachments.3'], [(102, 1897), (142, 1937), 'check_box', 'check_box_attach.4'], [(142, 1900), (902, 1977), 'text', 'attachments.4'], [(1025, 1725), (1062, 1765), 'check_box', 'check_box_attach.5'], [(1062, 1728), (1725, 1762), 'text', 'attachments.5'], [(1025, 1771), (1062, 1808), 'check_box', 'check_box_attach.6'], [(1065, 1771), (1734, 1828), 'text', 'attachments.6'], [(1025, 1834), (1062, 1871), 'check_box', 'check_box_attach.7'], [(1065, 1834), (1740, 1868), 'text', 'attachments.7'], [(1025, 1897), (1065, 1937), 'check_box', 'check_box_attach.8'], [(1065, 1897), (1745, 1940), 'text', 'attachments.8'], [(1025, 1957), (1062, 1997), 'check_box', 'check_box_attach.9'], [(1062, 1960), (1748, 2000), 'text', 'attachments.9']]
            for x,r in enumerate(roi):
                if r[2]=='check_box':
                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                    total_pixels=cv2.countNonZero(value)
                    if total_pixels>425:
                        roi_r = roi[x+1]
                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value= value.rstrip()
                        value=value.replace('\n',' ')
                        check_box_dict[roi_r[3]]=value
        else:
            roi = [(74, 546), (104, 574), 'text', 'check_number']
            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value= value.rstrip() 
            if value=='1.':
                #print('type 3')
                roi=[[(102, 540), (142, 580), 'check_box', 'check_box_1'], [(142, 542), (1785, 571), 'text', '1'], [(106, 606), (146, 646), 'check_box', 'check_box_2'], [(148, 608), (1774, 642), 'text', '2'], [(102, 671), (142, 711), 'check_box', 'check_box_3'], [(142, 671), (1762, 777), 'text', '3'], [(102, 785), (142, 825), 'check_box', 'check_box_4'], [(142, 788), (1777, 828), 'text', '4'], [(197, 825), (237, 865), 'check_box', 'check_box_4.a'], [(240, 828), (311, 865), 'text', '4.a'], [(357, 825), (397, 865), 'check_box', 'check_box_4.b'], [(397, 828), (508, 865), 'text', '4.b'], [(542, 825), (582, 865), 'check_box', 'check_box_4.c'], [(582, 828), (805, 865), 'text', '4.c'], [(265, 868), (305, 908), 'check_box', 'check_box_4.1'], [(305, 874), (1774, 902), 'text', '4.1'], [(265, 914), (305, 954), 'check_box', 'check_box_4.2'], [(305, 917), (1777, 945), 'text', '4.2'], [(265, 957), (305, 997), 'check_box', 'check_box_4.3'], [(305, 957), (1765, 1037), 'text', '4.3'], [(102, 1208), (142, 1248), 'check_box', 'check_box_5'], [(142, 1214), (1768, 1234), 'text', '5'], [(154, 1260), (191, 1300), 'check_box', 'check_box_5.1'], [(197, 1260), (1774, 1320), 'text', '5.1'], [(102, 1405), (142, 1445), 'check_box', 'check_box_6'], [(125, 1405), (1782, 1480), 'text', '6'], [(102, 1620), (142, 1657), 'check_box', 'check_box_attach.1'], [(142, 1622), (882, 1654), 'text', 'attachments.1'], [(102, 1662), (142, 1702), 'check_box', 'check_box_attach.2'], [(142, 1665), (891, 1722), 'text', 'attachments.2'], [(102, 1725), (142, 1765), 'check_box', 'check_box_attach.3'], [(142, 1725), (897, 1791), 'text', 'attachments.3'], [(102, 1788), (142, 1828), 'check_box', 'check_box_attach.4'], [(142, 1794), (900, 1860), 'text', 'attachments.4'], [(1025, 1620), (1065, 1657), 'check_box', 'check_box_attach.5'], [(1065, 1617), (1771, 1648), 'text', 'attachments.5'], [(1025, 1662), (1065, 1702), 'check_box', 'check_box_attach.6'], [(1065, 1665), (1771, 1702), 'text', 'attachments.6'], [(1025, 1725), (1065, 1765), 'check_box', 'check_box_attach.7'], [(1062, 1725), (1737, 1762), 'text', 'attachments.7']]
                for x,r in enumerate(roi):
                    if r[2]=='check_box':
                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                        total_pixels=cv2.countNonZero(value)
                        if total_pixels>425:
                            roi_r = roi[x+1]
                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip()
                            value=value.replace('\n',' ')
                            check_box_dict[roi_r[3]]=value
            else:
                roi=[(52, 552), (86, 586), 'text', 'check_number']
                imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value= value.rstrip() 
                if value=='1.':
                    #print('type 4')
                    roi=[[(87, 544), (127, 587), 'check_box', 'check_box_1'], [(129, 544), (1759, 584), 'text', '1'], [(87, 609), (127, 649), 'check_box', 'check_box_2'], [(128, 606), (1756, 638), 'text', '2'], [(87, 672), (129, 712), 'check_box', 'check_box_3'], [(129, 672), (1759, 689), 'text', '3'], [(177, 714), (214, 752), 'check_box', 'check_box_3.a'], [(219, 717), (277, 752), 'text', '3.a'], [(337, 714), (374, 749), 'check_box', 'check_box_3.b'], [(374, 714), (489, 752), 'text', '3.b'], [(522, 714), (559, 749), 'check_box', 'check_box_3.c'], [(559, 712), (832, 749), 'text', '3.c'], [(247, 759), (284, 794), 'check_box', 'check_box_3.1'], [(284, 757), (1759, 772), 'text', '3.1'], [(247, 802), (284, 839), 'check_box', 'check_box_3.2'], [(284, 804), (1759, 819), 'text', '3.2'], [(247, 847), (284, 884), 'check_box', 'check_box_3.3'], [(284, 844), (1762, 912), 'text', '3.3'], [(87, 1117), (129, 1157), 'check_box', 'check_box_4'], [(129, 1114), (1762, 1187), 'text', '4'], [(89, 1212), (129, 1252), 'check_box', 'check_box_5'], [(129, 1212), (1757, 1229), 'text', '5'], [(149, 1254), (187, 1292), 'check_box', 'check_box_5.a'], [(187, 1257), (1759, 1277), 'text', '5.a'], [(247, 1299), (284, 1337), 'check_box', 'check_box_5.1'], [(287, 1304), (404, 1339), 'text', '5.1'], [(437, 1297), (474, 1334), 'check_box', 'check_box_5.2'], [(479, 1297), (947, 1337), 'text', '5.2'], [(149, 1344), (187, 1382), 'check_box', 'check_box_5.b'], [(189, 1342), (1762, 1399), 'text', '5.b'], [(89, 1499), (129, 1542), 'check_box', 'check_box_6'], [(129, 1499), (1762, 1572), 'text', '6'], [(90, 1818), (124, 1853), 'check_box', 'check_box_attach.1'], [(124, 1818), (881, 1843), 'text', 'attachments.1'], [(90, 1862), (124, 1893), 'check_box', 'check_box_attach.2'], [(124, 1859), (881, 1921), 'text', 'attachments.2'], [(87, 1921), (128, 1962), 'check_box', 'check_box_attach.3'], [(124, 1921), (893, 1984), 'text', 'attachments.3'], [(87, 1984), (124, 2021), 'check_box', 'check_box_attach.4'], [(128, 1984), (896, 2056), 'text', 'attachments.4'], [(1018, 1815), (1056, 1853), 'check_box', 'check_box_attach.5'], [(1056, 1815), (1731, 1853), 'text', 'attachments.5'], [(1018, 1859), (1059, 1899), 'check_box', 'check_box_attach.6'], [(1056, 1859), (1559, 1924), 'text', 'attachments.6'], [(1018, 1921), (1056, 1959), 'check_box', 'check_box_attach.7'], [(1056, 1924), (1578, 1962), 'text', 'attachments.7'], [(1018, 1984), (1056, 2024), 'check_box', 'check_box_attach.8'], [(1056, 1984), (1737, 2040), 'text', 'attachments.8'], [(1018, 2049), (1056, 2087), 'check_box', 'check_box_attach.9'], [(1056, 2049), (1268, 2093), 'text', 'attachments.9']]
                    for x,r in enumerate(roi):
                        if r[2]=='check_box':
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                            value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                            total_pixels=cv2.countNonZero(value)
                            if total_pixels>425:
                                roi_r = roi[x+1]
                                imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                value= value.rstrip()
                                value=value.replace('\n',' ')
                                check_box_dict[roi_r[3]]=value
                else:
                    roi=[(58, 558), (90, 590), 'text', 'check_number']
                    imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value= value.rstrip() 
                    if value=='1.':
                        #print('type 5')
                        roi=[[(846, 204), (1064, 240), 'number', 'app_number'], [(1274, 194), (1664, 236), 'text', 'applicant'], [(846, 288), (1208, 338), 'text', 'examiner'], [(1276, 286), (1446, 336), 'number', 'art_unit']]
                        for x,r in enumerate(roi):
                            imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                            value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                            value= value.rstrip()
                            file[r[3]]=value
                            if r[3]=='app_number':
                                value = value.replace('.',',')
                                file[r[3]]=value
                        roi=[[(89, 552), (129, 592), 'check_box', 'check_box_1'], [(129, 552), (1717, 587), 'text', '1'], [(89, 614), (129, 654), 'check_box', 'check_box_2'], [(132, 614), (1717, 644), 'text', '2'], [(89, 677), (129, 717), 'check_box', 'check_box_3'], [(129, 677), (1722, 694), 'text', '3'], [(89, 739), (129, 777), 'check_box', 'check_box_4'], [(132, 739), (1717, 759), 'text', '4'], [(177, 784), (214, 822), 'check_box', 'check_box_4.a'], [(217, 782), (287, 819), 'text', '4.a'], [(334, 782), (372, 819), 'check_box', 'check_box_4.b'], [(372, 784), (484, 817), 'text', '4.b'], [(517, 782), (552, 817), 'check_box', 'check_box_4.c'], [(554, 782), (789, 819), 'text', '4.c'], [(244, 827), (282, 864), 'check_box', 'check_box_4.1'], [(282, 829), (1724, 842), 'text', '4.1'], [(247, 869), (282, 907), 'check_box', 'check_box_4.2'], [(282, 869), (1722, 894), 'text', '4.2'], [(247, 914), (282, 952), 'check_box', 'check_box_4.3'], [(282, 914), (1714, 984), 'text', '4.3'], [(92, 1184), (132, 1224), 'check_box', 'check_box_5'], [(132, 1182), (1719, 1257), 'text', '5'], [(92, 1277), (132, 1319), 'check_box', 'check_box_6'], [(132, 1279), (1727, 1304), 'text', '6'], [(149, 1322), (187, 1359), 'check_box', 'check_box_6.a'], [(187, 1322), (1732, 1347), 'text', '6.a'], [(247, 1364), (284, 1402), 'check_box', 'check_box_6.1'], [(284, 1367), (399, 1404), 'text', '6.1'], [(432, 1364), (469, 1402), 'check_box', 'check_box_6.2'], [(474, 1367), (907, 1402), 'text', '6.2'], [(149, 1409), (187, 1447), 'check_box', 'check_box_6.b'], [(189, 1409), (1727, 1469), 'text', '6.b'], [(92, 1564), (132, 1607), 'check_box', 'check_box_7'], [(132, 1562), (1729, 1634), 'text', '7'], [(88, 1805), (126, 1844), 'check_box', 'check_box_attach.1'], [(126, 1808), (885, 1838), 'text', 'attachments.1'], [(88, 1849), (126, 1888), 'check_box', 'check_box_attach.2'], [(126, 1849), (894, 1897), 'text', 'attachments.2'], [(88, 1911), (126, 1952), 'check_box', 'check_box_attach.3'], [(126, 1911), (908, 1976), 'text', 'attachments.3'], [(88, 1976), (126, 2011), 'check_box', 'check_box_attach.4'], [(126, 1976), (908, 2064), 'text', 'attachments.4'], [(991, 1799), (1029, 1838), 'check_box', 'check_box_attach.5'], [(1029, 1802), (1714, 1841), 'text', 'attachments.5'], [(991, 1844), (1029, 1885), 'check_box', 'check_box_attach.6'], [(1029, 1849), (1488, 1908), 'text', 'attachments.6'], [(991, 1908), (1026, 1944), 'check_box', 'check_box_attach.7'], [(1029, 1905), (1532, 1947), 'text', 'attachments.7'], [(991, 1970), (1029, 2008), 'check_box', 'check_box_attach.8'], [(1029, 1970), (1726, 2014), 'text', 'attachments.8'], [(991, 2014), (1029, 2052), 'check_box', 'check_box_attach.9'], [(1029, 2017), (1261, 2061), 'text', 'attachments.9']]
                        for x,r in enumerate(roi):
                            if r[2]=='check_box':
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                total_pixels=cv2.countNonZero(value)
                                if total_pixels>380:
                                    roi_r = roi[x+1]
                                    imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                    value= value.rstrip()
                                    value=value.replace('\n',' ')
                                    check_box_dict[roi_r[3]]=value
                    else:
                        roi=[(120, 606), (154, 642), 'text', 'check_number']
                        imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                        value= value.rstrip() 
                        if value=='1.':
                            #print('type 6')
                            roi=[[(904, 266), (1116, 310), 'number', 'app_number'], [(902, 358), (1156, 400), 'text', 'examiner'], [(1332, 272), (1664, 310), 'text', 'applicant'], [(1332, 362), (1448, 402), 'number', 'art_unit']]
                            for x,r in enumerate(roi):
                                imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                value=pytesseract.image_to_string(imgcrop,lang="eng",config='--psm 6')
                                value= value.rstrip()
                                file[r[3]]=value
                                if r[3]=='app_number':
                                    value = value.replace('.',',')
                                    file[r[3]]=value
                            roi=[[(152, 602), (194, 644), 'check_box', 'check_box_1'], [(197, 608), (1023, 644), 'text', '1'], [(152, 641), (194, 682), 'check_box', 'check_box_2'], [(197, 647), (1082, 682), 'text', '2'], [(152, 682), (194, 720), 'check_box', 'check_box_3'], [(199, 682), (1279, 717), 'text', '3'], [(152, 717), (194, 761), 'check_box', 'check_box_4'], [(199, 717), (1299, 764), 'text', '4'], [(238, 758), (273, 791), 'check_box', 'check_box_4.a'], [(276, 758), (352, 794), 'text', '4.a'], [(397, 761), (432, 794), 'check_box', 'check_box_4.b'], [(432, 758), (538, 797), 'text', '4.b'], [(579, 761), (611, 794), 'check_box', 'check_box_4.c'], [(614, 761), (841, 797), 'text', '4.c'], [(305, 799), (341, 832), 'check_box', 'check_box_4.1'], [(341, 799), (1147, 838), 'text', '4.1'], [(305, 838), (341, 876), 'check_box', 'check_box_4.2'], [(341, 838), (1452, 879), 'text', '4.2'], [(305, 879), (344, 917), 'check_box', 'check_box_4.3'], [(344, 882), (1758, 964), 'text', '4.3'], [(149, 997), (194, 1038), 'check_box', 'check_box_5'], [(194, 999), (1567, 1041), 'text', '5'], [(232, 1035), (273, 1079), 'check_box', 'check_box_5.a'], [(273, 1041), (1264, 1079), 'text', '5.a'], [(149, 1076), (194, 1117), 'check_box', 'check_box_6'], [(194, 1079), (1364, 1117), 'text', '6'], [(149, 1244), (194, 1282), 'check_box', 'check_box_7'], [(197, 1244), (1767, 1320), 'text', '7'], [(149, 1344), (194, 1385), 'check_box', 'check_box_8'], [(191, 1347), (785, 1385), 'text', '8'], [(208, 1385), (244, 1420), 'check_box', 'check_box_8.a'], [(249, 1382), (1549, 1420), 'text', '8.a'], [(302, 1423), (338, 1458), 'check_box', 'check_box_8.a.1'], [(341, 1426), (458, 1461), 'text', '8.a.1'], [(488, 1423), (523, 1458), 'check_box', 'check_box_8.a.2'], [(529, 1423), (776, 1464), 'text', '8.a.2'], [(205, 1464), (241, 1502), 'check_box', 'check_box_8.b'], [(247, 1464), (1744, 1505), 'text', '8.b'], [(205, 1505), (244, 1544), 'check_box', 'check_box_8.c'], [(252, 1505), (1758, 1544), 'text', '8.c'], [(149, 1670), (191, 1711), 'check_box', 'check_box_9'], [(191, 1673), (1785, 1747), 'text', '9'], [(132, 1852), (167, 1888), 'check_box', 'attachments.1'], [(167, 1855), (691, 1885), 'text', 'attachments.1'], [(1082, 1855), (1117, 1888), 'check_box', 'check_box_attach.2'], [(1114, 1855), (1744, 1891), 'text', 'attachments.2'], [(132, 1891), (164, 1920), 'check_box', 'check_box_attach.3'], [(167, 1891), (899, 1926), 'text', 'attachments.3'], [(132, 1923), (167, 1955), 'check_box', 'check_box_attach.5'], [(167, 1926), (985, 1967), 'text', 'attachments.5'], [(1082, 1891), (1117, 1923), 'check_box', 'check_box_attach.4'], [(1117, 1891), (1761, 1923), 'text', 'attachments.4'], [(1082, 1923), (1117, 1955), 'check_box', 'check_box_attach.6'], [(1117, 1920), (1767, 1952), 'text', 'attachments.6'], [(132, 1955), (164, 1991), 'check_box', 'check_box_attach.7'], [(167, 1958), (899, 2023), 'text', 'attachments.7'], [(1082, 1958), (1114, 1991), 'check_box', 'check_box_attach.8'], [(1117, 1958), (1779, 1994), 'text', 'attachments.8'], [(1082, 1988), (1117, 2023), 'check_box', 'check_box_attach.9'], [(1117, 1988), (1241, 2026), 'text', 'attachments.9']]
                            for x,r in enumerate(roi):
                                if r[2]=='check_box':
                                    imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                    imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                    value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                    total_pixels=cv2.countNonZero(value)
                                    if total_pixels>360:
                                        roi_r = roi[x+1]
                                        imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                        value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                        value= value.rstrip()
                                        value=value.replace('\n',' ')
                                        check_box_dict[roi_r[3]]=value
                        else:
                            roi=[(96, 482), (114, 512), 'text', 'check_number']
                            imgcrop = img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                            value= value.rstrip() 
                            if value=='1':
                                roi=[[(118, 476), (154, 514), 'check_box', 'check_box_1'], [(156, 480), (1150, 518), 'text', '1'], [(162, 520), (202, 556), 'check_box', 'check_box_1.1'], [(202, 522), (1200, 562), 'text', '1.1'], [(118, 580), (156, 616), 'check_box', 'check_box_2'], [(158, 582), (1756, 650), 'text', '2'], [(120, 666), (156, 702), 'check_box', 'check_box_3'], [(156, 668), (1768, 784), 'text', '3'], [(120, 796), (156, 832), 'check_box', 'check_box_4'], [(156, 796), (1284, 838), 'text', '4'], [(218, 886), (256, 922), 'check_box', 'check_box_4.a'], [(256, 882), (322, 920), 'text', '4.a'], [(374, 886), (410, 920), 'check_box', 'check_box_4.b'], [(412, 888), (522, 924), 'text', '4.b'], [(576, 886), (612, 918), 'check_box', 'check_box_4.c'], [(614, 884), (820, 924), 'text', '4.c'], [(288, 930), (324, 966), 'check_box', 'check_box_4.1'], [(324, 934), (1154, 968), 'text', '4.1'], [(288, 970), (326, 1006), 'check_box', 'check_box_4.2'], [(324, 974), (1436, 1014), 'text', '4.2'], [(286, 1014), (322, 1048), 'check_box', 'check_box_4.3'], [(324, 1014), (1776, 1106), 'text', '4.3'], [(120, 1294), (156, 1332), 'check_box', 'check_box_5'], [(158, 1296), (1124, 1332), 'text', '5'], [(168, 1334), (206, 1372), 'check_box', 'check_box_5.1'], [(212, 1336), (1764, 1402), 'text', '5.1'], [(117, 1488), (154, 1528), 'check_box', 'check_box_6'], [(157, 1488), (1785, 1562), 'text', '6'], [(111, 1642), (151, 1677), 'check_box', 'check_box_attach.1'], [(111, 1685), (148, 1722), 'check_box', 'check_box_attach.2'], [(148, 1642), (788, 1674), 'text', 'attachments.1'], [(151, 1685), (871, 1748), 'text', 'attachments.2'], [(111, 1751), (151, 1785), 'check_box', 'check_box_attach.3'], [(151, 1751), (888, 1820), 'text', 'attachments.3'], [(111, 1811), (148, 1848), 'check_box', 'check_box_attach.4'], [(151, 1817), (897, 1882), 'text', 'attachments.4'], [(1051, 1640), (1091, 1680), 'check_box', 'check_box_attach.5'], [(1091, 1642), (1748, 1674), 'text', 'attachments.5'], [(1051, 1682), (1088, 1722), 'check_box', 'check_box_attach.6'], [(1091, 1688), (1757, 1725), 'text', 'attachments.6'], [(1051, 1745), (1088, 1785), 'check_box', 'check_box_attach.7'], [(1088, 1745), (1348, 1794), 'text', 'attachments.7']]
                                for x,r in enumerate(roi):
                                    if r[2]=='check_box':
                                        imgcrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
                                        imgGray = cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
                                        value=cv2.threshold(imgGray,170,255, cv2.THRESH_BINARY_INV)[1]
                                        total_pixels=cv2.countNonZero(value)
                                        if total_pixels>360:
                                            roi_r = roi[x+1]
                                            imgcrop = img[roi_r[0][1]:roi_r[1][1],roi_r[0][0]:roi_r[1][0]]
                                            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                                            value= value.rstrip()
                                            value=value.replace('\n',' ')
                                            check_box_dict[roi_r[3]]=value
    for i in check_box_dict.values():
        if i=="Examiner's Amendment/Comment":
            file['File_sets']='Set_3'
    #print(check_box_dict)
    file['check_box_dict']=check_box_dict
if section_1_5:
    print('section_1_5 ',section_1_5)
    phrase={}
    img_lst=[*range(img_n,len(page_lst))]
    comp_text=''
    for i in img_lst:
        img= cv2.imread(page_lst[i])
        text = pytesseract.image_to_string(img,lang="eng",config='--psm 6')
        text = text.rstrip()
        comp_text=comp_text+'\n'+text
    #print(comp_text)
    if section_1_0 or section_1_1 or section_1_4:
        pass
    else:
        app_number=re.findall(r'Application/Control Number: (.*\d+).\w',comp_text)
        if app_number:
            app_number=app_number[0]
            file['app_number']=app_number
        art_unit=re.findall(r'Art Unit: (.*\d+)',comp_text)
        if art_unit:
            art_unit=art_unit[0]
            file['art_unit']=art_unit
    phrase_1=''
    phrase_1 = re.findall(r'The terminal disclaimer[\n ]has been recorded',comp_text)
    if phrase_1:
        phrase_1=phrase_1[0]
        phrase_1=phrase_1.replace('\n',' ')
        phrase['phrase_1']=phrase_1
    phrase_2=''
    phrase_2 = re.findall(r'Claims.*are allowed',comp_text)
    if phrase_2:
        phrase_2=phrase_2[0]
        phrase['phrase_2']=phrase_2
    phrase_3=''
    phrase_3 = re.findall(r'statement of reasons for the indication of allowable subject[\n ]matter',comp_text)
    if phrase_3:
        phrase_3=phrase_3[0]
        phrase_3=phrase_3.replace('\n',' ')
        phrase['phrase_3']=phrase_3
    phrase_4=''
    phrase_4 = re.findall(r'examiner’s statement of reasons of allowance',comp_text)
    if phrase_4:
        phrase_4=phrase_4[0]
        phrase['phrase_4']=phrase_4
    phrase_5=''
    phrase_5 = re.findall(r'drawings are acceptable',comp_text)
    if phrase_5:
        phrase_5=phrase_5[0]
        phrase['phrase_5']=phrase_5
    phrase_6=''
    phrase_6 = re.findall(r'Examiner’s amendment to the record appears below',comp_text)
    if phrase_6:
        phrase_6=phrase_6[0]
        phrase['phrase_6']=phrase_6
    phrase_7=''
    phrase_7 = re.findall(r'AMENDMENTS TO THE CLAIMS',comp_text)
    if phrase_7:
        phrase_7=phrase_7[0]
        phrase['phrase_7']=phrase_7
    phrase_8=''
    phrase_8 = re.findall(r'application has been amended',comp_text)
    if phrase_8:
        phrase_8=phrase_8[0]
        phrase['phrase_8']=phrase_8
    phrase_9=''
    phrase_9 = re.findall(r'In the title, please delete title.*[\n ].*insert the title',comp_text)
    if phrase_9:
        phrase_9=phrase_9[0]
        phrase_9=phrase_9.replace('\n',' ')
        phrase['phrase_9']=phrase_9
    phrase_10=''
    phrase_10 = re.findall(r'new title has been entered',comp_text)
    if phrase_10:
        phrase_10=phrase_10[0]
        phrase['phrase_10']=phrase_10
    phrase_11=''
    phrase_11 = re.findall(r'Double Patenting',comp_text)
    if phrase_11:
        phrase_11=phrase_11[0]
        phrase['phrase_11']=phrase_11
    phrase_12=''
    phrase_12 = re.findall(r'terminal disclaimer.*has been approved',comp_text)
    if phrase_12:
        phrase_12=phrase_12[0]
        phrase['phrase_12']=phrase_12
    phrase_13=''
    phrase_13 = re.findall(r'Application was granted Accelerated Examination status',comp_text)
    if phrase_13:
        phrase_13=phrase_13[0]
        phrase['phrase_13']=phrase_13
    phrase_14=''
    phrase_14=re.findall(r'Election/Restrictions',comp_text)
    if phrase_14:
        phrase_14=phrase_14[0]
        phrase['phrase_14']=phrase_14
    phrase_15=''
    phrase_15=re.findall(r'invention II, non-elected without traverse',comp_text)
    if phrase_15:
        phrase_15=phrase_15[0]
        phrase['phrase_15']=phrase_15
    phrase_16=''
    phrase_16=re.findall(r'amend the amendment to the Specification.*',comp_text)
    if phrase_16:
        phrase_16=phrase_16[0]
        phrase['phrase_16']=phrase_16
    phrase_17=''
    phrase_17=re.findall(r'request for continued examination',comp_text)
    if phrase_17:
        phrase_17=phrase_17[0]
        phrase['phrase_17']=phrase_17
    phrase_18=''
    phrase_18=re.findall(r'Continued Examination Under 37 CFR 1.114',comp_text)
    if phrase_18:
        phrase_18=phrase_18[0]
        phrase['phrase_18']=phrase_18
    phrase_19=''
    phrase_19_0=re.findall(r'Amend the title to the following',comp_text)
    phrase_19_1=re.findall(r'''EXAMINER'S AMENDMENT''',comp_text)
    if phrase_19_0 and phrase_19_1:
        phrase_19_0=phrase_19_0[0]
        phrase_19_1=phrase_19_1[0]
        phrase['phrase_19']=phrase_19_1+' '+phrase_19_0
    phrase_20=''
    phrase_20=re.findall(r'Please amend.*Specification',comp_text)
    if phrase_20:
        phrase_20=phrase_20[0]
        phrase['phrase_20']=phrase_20
    phrase_21=''
    phrase_21=re.findall(r'drawings filed.*accepted',comp_text)
    if phrase_21:
        phrase_21=phrase_21[0]
        phrase['phrase_21']=phrase_21
    phrase_22=''
    phrase_22=re.findall(r'abstract has been replaced',comp_text)
    if phrase_22:
        phrase_22=phrase_22[0]
        phrase['phrase_22']=phrase_22
    phrase_23=''
    phrase_23=re.findall(r'applicant’s claim for foreign priority',comp_text)
    if phrase_23:
        phrase_23=phrase_23[0]
        phrase['phrase_23']=phrase_23
    phrase_24=''
    phrase_24=re.findall(r'terminal disclaimer overcomes the double patenting rejections',comp_text)
    if phrase_24:
        phrase_24=phrase_24[0]
        phrase['phrase_24']=phrase_24
    #print(phrase)
    file['phrases']=phrase
print(file)
filen=a.replace('pdf','json')
with open(os.path.join(DOWNLOAD_FOLDER) + "\\" + filen, 'w') as outfile:
    json.dump(file, outfile)
s3.meta.client.upload_file( os.path.join(DOWNLOAD_FOLDER) + "\\" + filen, my_bucket, s3_dir+'/'+filen)
end=time.time()
tot=end-start
print('time taken: {:.2f} Seconds'.format(tot))
total_time=total_time+tot
total_time=total_time/3600
print('Total time taken: {:.2f} Hrs.'.format(total_time))