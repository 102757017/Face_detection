# -*- coding: UTF-8 -*-
import dlib
import cv2
import os
import numpy as np

os.chdir(os.path.dirname(__file__))
# 加载并初始化检测器,经测试使用cpu时速度非常慢，基本不能使用
detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
img = cv2.imdecode(np.fromfile('example.png', dtype=np.uint8), 1)
#参数1表示我们对图像进行向上采样1倍，向上采样图像将使得我们能够检测较小的面孔，但会导致程序使用更多的内存，并运行时间更长
dets = detector(img, 1)
print("Number of faces detected: {}".format(len(dets)))
# 查找脸部位置
for i, face in enumerate(dets):
    # 绘制脸部位置
    cv2.rectangle(img, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 1)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
