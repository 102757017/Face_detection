# -*- coding: UTF-8 -*-
import cv2
from PIL import Image
import os
import numpy as np


os.chdir(os.path.dirname(__file__))
classfier = cv2.CascadeClassifier("opencv-haarcascade_frontalface_alt2.xml")
img = cv2.imdecode(np.fromfile('example.png', dtype=np.uint8), 1)
faceRects = classfier.detectMultiScale(img, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))  # 读取脸部位置

if len(faceRects) > 0:  # 大于0则检测到人脸
    for faceRect in faceRects:  # 单独框出每一张人脸
        x, y, w, h = faceRect
        #绘制矩阵框，(0,0,255)是颜色
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255),1) #12
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()