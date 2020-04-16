# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:33:08 2020

@author(s): Casey & Aarjav
"""


import numpy as np
import cv2
import os
import shutil
import re
import json

"""variable definitions"""
photo_array = []
tag_array = []
exclude = []
include_only = []
num_face = []
directory = os.path.dirname(os.path.abspath(__file__))
#this is where your hashtag name goes (source directory should be named hashtag)
hashtag_name = "puertorican"
source = directory + "/" + hashtag_name + "/"
#this is where your destination directory goes for processed images
destination = directory + "/images_2"
#this is the location of the json file
jsonFile = directory + "/" + hashtag_name + "/" + hashtag_name + ".json"


"""function returns JSON file contents"""
def openJSON(fileName):
    with open(fileName,'r',encoding='utf-8') as j:
        return json.load(j)
        print('JSON Successfully Loaded')

"""populate tags_array with filename and tag list"""
def mkTagArr(json_data):
    for x in range (0, len(json_data['GraphImages'])):
        url = json_data['GraphImages'][x]['display_url']
        for y in range (6,8):    
            picName = re.split('[/?]', url)[y]
            if picName.endswith(".jpg"):
                tags = json_data['GraphImages'][x]['tags']
                tag_array.append([picName, tags])
            else:
                continue
              
"""
computer vision stuff we need to flush through :)
TODO: parse based on included and excluded hashtags
"""
def compVis(pic):
    image = hashtag_name + "/" + pic
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(image)
    if isinstance(img, np.ndarray):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        numFaces = len(faces)
        print("image name ", pic, " number of faces= ", numFaces)
        return(numFaces)
    else:
        print("image name ", pic, " not available in directory")
        print(type(img))       
        

"""copy file to new directory if there is one face in the picture
!Enter your source and destination in variable definitions above"""
            
def copyPic(origDir):
    for x in range (0, len(origDir)):
        if compVis(origDir[x][0]) == 1:
            fileSrc = source + origDir[x][0]
            fileDest = destination
            shutil.copy(fileSrc, fileDest)
            print(origDir[x][0], "copied successfully")
        else:
            print(origDir[x][0], "not copied")
            
        
"""
Main function
"""
def main():
    mkTagArr(openJSON(jsonFile))
    print(tag_array)
    compVis(tag_array[6][0])
    print(tag_array[4][0])
    print(len(tag_array))
    copyPic(tag_array)


if __name__== "__main__":
    main()
