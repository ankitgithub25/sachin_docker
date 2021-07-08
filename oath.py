#!/usr/bin/env python3
import re
import pytesseract
import cv2 
import numpy as np
import sys 
from pdf2image import convert_from_path 
import os 
import time
import math
import json
import boto3
s3 = boto3.resource('s3')
my_bucket = 'bb-bot-test'
s3_dir=sys.argv[1]
a=sys.argv[2]
bad_char='''[!,*)@#%(&$_;:?^«+>~|—]'''
def rotateImage(image, angle):
    row,col,dim = image.shape
    center=tuple(np.array([row,col])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col,row))
    return new_image
pytesseract.pytesseract.tesseract_cmd=r'Tesseract-OCR\tesseract.exe'
DOWNLOAD_FOLDER = 'downloads'
print(a)
path_file = os.path.join(DOWNLOAD_FOLDER, a)
file={}
start=time.time()
page = convert_from_path(path_file,dpi=220,poppler_path=r'poppler-0.68.0\bin')
filename = "last_page.jpg"
filename = os.path.join(DOWNLOAD_FOLDER, filename)
page[-1].save(filename, 'JPEG')
b=1
while not file:
    img=cv2.imread(filename)
    blur = cv2.GaussianBlur(img,(5,3), 1)
    mask=cv2.inRange(blur,(0,0,0),(150,150,150))
    img = 255 - mask
    cv2.imwrite(filename, img)
    img=cv2.imread(filename)
    img_before=cv2.imread(filename)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
    angles = []
    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img_before, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    median_angle = np.median(angles)
    if median_angle !=0:
        print('Rotating image to {} degree to correct it.'.format(median_angle))
        img = rotateImage(img, median_angle)
    method = cv2.TM_CCOEFF_NORMED
    large_image=img
    legal_lst=['legal.jpg','legal1.jpg','legal2.jpg','legal3.jpg','legal4.jpg','legal5.jpg','legal6.jpg','legal7.jpg',
              'legal8.jpg','legal9.jpg','legal10.jpg','legal11.jpg']
    for l in legal_lst:
        small_image = cv2.imread('static'+'\\'+l)
        w, h = small_image.shape[0], small_image.shape[1]
        res = cv2.matchTemplate(small_image, large_image, method)
        threshold = 0.6
        loc = np.where( res >= threshold)
        x_lst=[]
        y_lst=[]
        pt=False
        for pt in zip(*loc[::-1]):
            x_lst.append(pt[0])
            y_lst.append(pt[1])
        if pt:
            most_x=max(set(x_lst), key=x_lst.count)
            most_y=max(set(y_lst), key=y_lst.count)
            pt=(most_x, most_y)
            #print('match found')
            #print(pt[0], pt[1] ,pt[0] + h, pt[1] + w)
            x1=pt[0]+124
            y1=pt[1]+51
            x2=pt[0] + h+380
            y2=pt[1] + w+81
            roi=[(x1,y1),(x2,y2)]
            #print(x1,y1,x2,y2)
            imgcrop=img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            value=re.sub(bad_char,"",value)
            value=value.replace(']','')
            value=value.strip()
            file['inventor_1']=value
            break
    if not file:
        small_image = cv2.imread('static'+'\\'+'german_first_inventor.jpg')
        w, h = small_image.shape[0], small_image.shape[1]
        res = cv2.matchTemplate(small_image, large_image, method)
        threshold = 0.6
        loc = np.where( res >= threshold)
        pt=False
        for pt in zip(*loc[::-1]):
            #print(pt, ' : pt')
            break
        if pt:
            #print('match found')
            #print(pt[0], pt[1] ,pt[0] + h, pt[1] + w)
            x1=pt[0]+4
            y1=pt[1]+55
            x2=pt[0] + h+363
            y2=pt[1] + w+118
            roi=[(x1,y1),(x2,y2)]
            imgcrop=img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
            value=pytesseract.image_to_string(imgcrop, config='--psm 6')
            value=value.rstrip()
            value=re.sub(bad_char,"",value)
            value=value.strip()
            file['inventor_1']=value
            small_image = cv2.imread('german_second_inventor.jpg')
            w, h = small_image.shape[0], small_image.shape[1]
            res = cv2.matchTemplate(small_image, large_image, method)
            threshold = 0.6
            loc = np.where( res >= threshold)
            pt=False
            for pt in zip(*loc[::-1]):
                #print(pt, ' : pt')
                break
            if pt:
                #print('match found')
                #print(pt[0], pt[1] ,pt[0] + h, pt[1] + w)
                x1=pt[0]
                y1=pt[1]+56
                x2=pt[0] + h+312
                y2=pt[1] + w+118
                roi=[(x1,y1),(x2,y2)]
                imgcrop=img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                value=re.sub(bad_char,"",value)
                value=value.strip()
                file['inventor_2']=value
        else:
            small_image = cv2.imread('static'+'\\'+'name_inventor.jpg')
            w, h = small_image.shape[0], small_image.shape[1]
            res = cv2.matchTemplate(small_image, large_image, method)
            threshold = 0.8
            loc = np.where( res >= threshold)
            counter=1
            pt_lst=[]
            for pt in zip(*loc[::-1]):
                pt_lst.append(pt)
            for t, pt in enumerate(pt_lst):
                ch=False
                if t==0:
                    ch=True
                else:
                    if (pt_lst[t-1][1]+100)<pt[1]:
                        ch=True
                if ch:
                    #print('match found')
                    #print(pt[0], pt[1] ,pt[0] + h, pt[1] + w)
                    x1=pt[0]+390
                    y1=pt[1]-7
                    x2=pt[0] + h+1019
                    y2=pt[1] + w-15
                    roi=[(x1,y1),(x2,y2)]
                    imgcrop=img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    value=re.sub(bad_char,"",value)
                    value=value.strip()
                    name='inventor'+'_'+str(counter)
                    file[name]=value
                    counter=counter+1
        if not file:
            small_image = cv2.imread('static'+'\\'+'full_name.jpg')
            w, h = small_image.shape[0], small_image.shape[1]
            res = cv2.matchTemplate(small_image, large_image, method)
            threshold = 0.6
            loc = np.where( res >= threshold)
            counter=1
            pt_lst=[]
            for pt in zip(*loc[::-1]):
                pt_lst.append(pt)
            for t, pt in enumerate(pt_lst):
                ch=False
                if t==0:
                    ch=True
                else:
                    if (pt_lst[t-1][1]+100)<pt[1]:
                        ch=True
                if ch:
                    #print('Match Found')
                    x1=pt[0]+18
                    y1=pt[1]+63
                    x2=pt[0] + h+1182
                    y2=pt[1] + w+55
                    roi=[(x1,y1),(x2,y2)]
                    imgcrop=img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                    value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                    value=value.rstrip()
                    value=re.sub(bad_char,"",value)
                    value=value.strip()
                    name='inventor'+'_'+str(counter)
                    file[name]=value
                    counter=counter+1
        if not file:
            small_image = cv2.imread('static'+'\\'+'no_auth.jpg')
            w, h = small_image.shape[0], small_image.shape[1]
            res = cv2.matchTemplate(small_image, large_image, method)
            threshold = 0.6
            loc = np.where( res >= threshold)
            pt=False
            for pt in zip(*loc[::-1]):
                #print(pt, ' : pt')
                break
            if pt:
                #print('match found')
                #print(pt[0], pt[1] ,pt[0] + h, pt[1] + w)
                x1=pt[0]+517
                y1=pt[1]+193
                x2=pt[0] + h-277
                y2=pt[1] + w+167
                roi=[(x1,y1),(x2,y2)]
                imgcrop=img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                value=re.sub(bad_char,"",value)
                value=value.strip()
                file['inventor_1']=value
        if not file:
            small_image = cv2.imread('static'+'\\'+'no_auth_legal.jpg')
            w, h = small_image.shape[0], small_image.shape[1]
            res = cv2.matchTemplate(small_image, large_image, method)
            threshold = 0.6
            loc = np.where( res >= threshold)
            pt=False
            for pt in zip(*loc[::-1]):
                #print(pt, ' : pt')
                break
            if pt:
                #print('match found')
                #print(pt[0], pt[1] ,pt[0] + h, pt[1] + w)
                x1=pt[0]
                y1=pt[1]+220
                x2=pt[0] + h
                y2=pt[1] + w+220
                roi=[(x1,y1),(x2,y2)]
                imgcrop=img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                value=re.sub(bad_char,"",value)
                value=value.strip()
                file['inventor_1']=value
        if not file:
            small_image = cv2.imread('static'+'\\'+'no_auth1.jpg')
            w, h = small_image.shape[0], small_image.shape[1]
            res = cv2.matchTemplate(small_image, large_image, method)
            threshold = 0.6
            loc = np.where( res >= threshold)
            pt=False
            for pt in zip(*loc[::-1]):
                #print(pt, ' : pt')
                break
            if pt:
                #print('match found')
                #print(pt[0], pt[1] ,pt[0] + h, pt[1] + w)
                x1=pt[0]-383
                y1=pt[1]+823
                x2=pt[0] + h-340
                y2=pt[1] + w+840
                roi=[(x1,y1),(x2,y2)]
                imgcrop=img[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
                value=pytesseract.image_to_string(imgcrop, config='--psm 6')
                value=value.rstrip()
                value=re.sub(bad_char,"",value)
                value=value.strip()
                file['inventor_1']=value
    if file or b==2:
        break
    else:
        path_file = os.path.join(DOWNLOAD_FOLDER, a)
        page = convert_from_path(path_file,dpi=220,poppler_path=r'C:\poppler-0.68.0\bin')
        page[-2].save(filename, 'JPEG')
        b=b+1
print(file)
filen=a.replace('pdf','json')
with open(os.path.join(DOWNLOAD_FOLDER) + "\\" + filen, 'w') as outfile:
    json.dump(file, outfile)
s3.meta.client.upload_file( os.path.join(DOWNLOAD_FOLDER) + "\\" + filen, my_bucket, s3_dir+'/'+filen)
end=time.time()
tot=end-start
print('Total time taken {} seconds'.format(tot))