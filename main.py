#!/usr/bin/env python3
from subprocess import call
import sys
import os
import json
import boto3
import errno
import shutil
s3 = boto3.resource('s3')
bucket = 'bb-bot-test'
s3_dir=sys.argv[1]
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)
my_bucket = s3.Bucket(bucket)
for file in my_bucket.objects.filter(Prefix=s3_dir):
    try:
        path1, filename = os.path.split(file.key)
        try:
            os.makedirs(root_dir + path1)
        except Exception as err:
            pass
        my_bucket.download_file(file.key, os.path.join(DOWNLOAD_FOLDER, filename))
    except Exception as err:
        print(err)
office_action=['CTAV','CTEQ','CTFR','CTNF','CTRS']
for a in os.listdir(DOWNLOAD_FOLDER):
    if a.endswith('.pdf'):
        if 'oath' in a:
            call(['python', 'oath.py', s3_dir, a])
        elif 'ads' in a:
            call(['python', 'ads.py', s3_dir, a])
        elif 'noa' in a:
            call(['python', 'noa.py', s3_dir, a])
        elif list(filter(lambda x:x in a, office_action)):
            call(['python', 'office.py', s3_dir, a])
        else:
            print(a, ' :Unable to understand this file.')
for filename in os.listdir(DOWNLOAD_FOLDER):
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    try:
        shutil.rmtree(filepath)
    except OSError:
        os.remove(filepath)