import cv2
img=cv2.imread('img.jpg',cv2.IMREAD_GRAYSCALE)#文件名，标志位（灰度图，写0一样）
print(type(img))#矩阵
print(img.shape)#矩阵大小（像素点为矩阵的一个量# ）

# #展示
# cv2.imshow('window',img)#窗体名，图片
#
# if(cv2.waitKey(0)==ord('q')):
#     cv2.destroyAllWindows()#关闭窗口

# #阻塞1k ms，0为永久阻塞
# k=cv2.waitKey(0)#输入一个值后退出
cv2.imwrite('img_g.jpg',img)#保存，写入文件(写入图片格式)