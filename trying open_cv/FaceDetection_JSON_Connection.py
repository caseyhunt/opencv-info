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
#this is where your source goes
source = directory + "/puertorican/"
#this is where your destination goes
destination = directory + "/images_2"
#this is the location of the json file
jsonFile = directory + "/puertorican/puertorican.json"


"""function returns JSON file contents"""
def openJSON(fileName):
    with open(fileName,'r',encoding='utf-8') as j:
        return json.load(j)
        print('JSON Successfully Loaded')
        #print(data)
        #print(url)
        
        #print(data['GraphImages'][0]['urls'])
        
def findPicName(dirName, dirLoc):
    url = dirName['GraphImages'][dirLoc]['display_url']
    picName = re.split('[/?]', url)[6]
    print(picName)

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
Gets all image names from specified directory
"""
def get_images_from_directory():
    for filename in os.listdir(source):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            photo_array.append(filename)
        else:
            continue
        
        
        
"""
computer vision stuff we need to flush through :)
TODO: identify only one face
"""
def compVis(pic):
    image = "puertorican/" + pic
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(image)
    if type(img)!='NoneType':
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
        
        
def compVis2(pic):
    image = "puertorican/" + pic
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
Enter your source and destination in variable definitions above"""
def copyToDir(origDir):
    for picture in origDir:
        if compVis(picture) == 1:
            fileSrc = source + picture
            fileDest = destination
            shutil.copy(fileSrc, fileDest)
            print(picture, "copied successfully")
        else:
            print(picture, "not copied")
            
def copyPic(origDir):
    for x in range (0, len(origDir)):
        if compVis2(origDir[x][0]) == 1:
            fileSrc = source + origDir[x][0]
            fileDest = destination
            shutil.copy(fileSrc, fileDest)
            print(origDir[x][0], "copied successfully")
        else:
            print(origDir[x][0], "not copied")

def numFaces(origDir):
    for x in range (0, len(origDir)):
        if origDir[x][0].endswith('.jpg'):
            num_face.append([origDir[x][0], compVis(origDir[x][0])])
        else:
            continue
            
        
"""
Main function
"""
def main():
  
    get_images_from_directory()
    #print(np.array(photo_array))
    #copyToDir(photo_array)
    #openJSON(jsonFile)
    mkTagArr(openJSON(jsonFile))
    print(tag_array)
    compVis2(tag_array[6][0])
    print(tag_array[4][0])
    print(len(tag_array))
    #numFaces(tag_array)
    #print(num_face)
    copyPic(tag_array)
    #findPicName(openJSON(jsonFile), 0)

if __name__== "__main__":
    main()
