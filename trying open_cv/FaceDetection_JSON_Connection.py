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
filtered_array = []
num_face = []
directory = os.path.dirname(os.path.abspath(__file__))

#this is where you define must include/must exclude hashtag criteria
exclude = ['highfidelity', 'makeup']
#any must_include criteria will be required simultaneously. a photo must have all criteria.
include = []
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

"""populate tags_array with filename and tag list, get filename from url in JSON file"""
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

"""function to compare two arrays, reject if any item in arrayReject are present"""           
def parseArrRej(arrayIn, arrayReject):
    if arrayReject == []:
        print('no exclusion criteria')
    else:
            for x in range (0, len(arrayReject)):
                try: 
                    arrayIn.index(arrayReject[x])
                    print("present")
                    return True
                except:
                    print("not present")

"""function to compare two arrays, reject if all items in arrayInclude aren't present"""
def parseArrInc(arrayIn, arrayInclude):
    if arrayInclude == []:
        print('no inclusion criteria')
    else:
            for x in range(0, len(arrayInclude)):
                try:
                    arrayIn.index(arrayInclude[x])
                    print("present")
                except:
                    print("not present")
                    return False


"""use result of array comparision to create an array containing images we want to use"""
def mkFilteredArr(arrToFilter, excArray, incArray):
    for x in range(0,len(arrToFilter)):
        if parseArrRej(arrToFilter[x][1], excArray)!=True and parseArrInc(arrToFilter[x][1], incArray)!=False:
            filtered_array.append(arrToFilter[x][0])
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
        if compVis(origDir[x]) == 1:
            fileSrc = source + origDir[x]
            fileDest = destination
            shutil.copy(fileSrc, fileDest)
            print(origDir[x], "copied successfully")
        else:
            print(origDir[x], "not copied, not one face")
            
        
"""
Main function
"""
def main():
    mkTagArr(openJSON(jsonFile))
    mkFilteredArr(tag_array, exclude, include)
    print(filtered_array)
    copyPic(filtered_array)

if __name__== "__main__":
    main()
