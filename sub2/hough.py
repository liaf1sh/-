# import cv2
# import numpy as np
# # from Tools.scripts.generate_stdlib_module_names import list_setup_extensions
# #
# # import isqcurvefit
# # from isqcurvefit import least_square_fit
#
#
# #斜率
# def calculate_slope(line):
#     x1,y1,x2,y2=line[0]
#     return (y2-y1)/(x2-x1)
#
# img = cv2.imread('masked_edge_img.jpg',cv2.IMREAD_GRAYSCALE)
#
# #获取线
# #霍夫变换 矩阵，距离r，theta精度，累加阈值，最短阈值，统一线两点最大长度
# lines=cv2.HoughLinesP(img,1,np.pi/180,15,minLineLength=40,maxLineGap=20)
# #列表，离散的
#
# #斜率》0左车道，《0右车道
# leftline=[line for line in lines if calculate_slope(line)>0]
# rightline=[line for line in lines if calculate_slope(line)<0]
#
#
# #离群值过滤
# #删除斜率不一致的线
# #列表，误差值
# def sub_line(lines,threshold):
#     #all斜率
#     slopes=[calculate_slope(line)for line in lines]
#     # print(slopes)
#
#     while len(lines)>0:
#         #平均值mean()
#         mean = np.mean(slopes)
#         # print(mean)
#         #算出每个斜率与平均值的差值，绝对值abs()
#         diff=[abs(s-mean) for s in slopes]
#         # print(diff)
#         #diff中最大的差值的元素位置，返回最大值argmax()
#         idx=np.argmax(diff)
#         # print(idx)
#         # print(diff[idx])
#
#         if diff[idx]>threshold:
#             #删除s里和l里
#             slopes.pop(idx)
#             lines.pop(idx)
#         else:
#             break
#         return lines
#
# #删除前
# print('before filter:')
# print('left lines number=')
# print(len(leftline))
# print('right lines number=')
# print(len(rightline))
#
# sub_line(leftline, threshold=0.2)
# sub_line(rightline, threshold=0.2)
#
# #删除后
# print('after filter:')
# print('left lines number=')
# print(len(leftline))
# print('right lines number=')
# print(len(rightline))
# print('-----------------------------------------------------')
# #opencv两点对为直线
#
# # 将lines中所有线段拟合成一条
# def least_square_fit(lines):
#     #取出所有坐标点，ravel()高维数组转一维
#     xc=np.ravel([[line[0][0],line[0][2]]for line in lines])
#     yc=np.ravel([[line[0][1],line[0][3]]for line in lines])
#     #直线拟合, 多项式系数，多项式拟合坐标，坐标，阶数
#     poly=np.polyfit(xc,yc,deg=1)
#     #多项式系数计算直线的两点，用于唯一确定这条直线
#     point1=(np.min(xc),np.polyval(poly,np.min(xc)))
#     point2=(np.max(xc),np.polyval(poly,np.max(xc)))
#     return np.array([point1,point2],dtype=int)
#
# print('left line')
# print(least_square_fit(leftline))
# print('right line')
# print(least_square_fit(rightline))
# print('-----------------------------------------------------')
# ll=least_square_fit(leftline)
# rl=least_square_fit(rightline)
#
# img=cv2.imread('img.jpg',cv2.IMREAD_COLOR)
# #line()不可读入集合
# cv2.line(img,tuple(ll[0]),tuple(ll[1]),color=(255,0,255),thickness=5)
# cv2.line(img,tuple(rl[0]),tuple(rl[1]),color=(0,0,255),thickness=5)
# cv2.imshow('wd',img)
# cv2.waitKey(0)
#
