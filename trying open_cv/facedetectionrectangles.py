# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:33:08 2020

@author: Casey
"""


import numpy as np
import cv2
import os


photoArr = []

directory = r'C:\Users\Casey\puertorican'
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        print(os.path.join(directory, filename))
        photoArr.append(filename)
    else:
        continue



image = input('what is the name of your image? ')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


img = cv2.imread(image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
if faces == ():
    print('no face')
else:
    print(faces)


cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(photoArr[0])