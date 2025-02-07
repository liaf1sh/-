import cv2
import numpy as np

roi_img=cv2.imread('edges_img.jpg',cv2.IMREAD_GRAYSCALE)

mask1=np.zeros_like(roi_img)#数组
#感兴趣的区域
#掩码
mask=cv2.fillPoly(mask1,np.array([[[0,368],[240,210],[300,210],[640,368]]]),color=255)#数组，坐标，掩码值
# cv2.imshow('mask',mask)
# cv2.waitKey(0)

#布尔运算
mask_roi=cv2.bitwise_and(roi_img,mask)#原图，掩码
cv2.imshow('0',mask_roi)
cv2.waitKey(0)