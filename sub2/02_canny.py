#canny边缘检测
import cv2

img=cv2.imread('img.jpg',cv2.IMREAD_GRAYSCALE)

cy_img=cv2.Canny(img,90,800)#矩阵，下边缘，上边缘

#展示
cv2.imshow('window',cy_img)
cv2.waitKey(0)
