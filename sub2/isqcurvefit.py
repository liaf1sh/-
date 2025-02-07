#最小二乘拟合
import cv2
import numpy as np
import hough

#opencv两点对为直线

# 将lines中所有线段拟合成一条
def least_square_fit(lines):
    #取出所有坐标点，ravel()高维数组转一维
    xc=np.ravel([[line[0][0],line[0][2]]for line in lines])
    yc=np.ravel([[line[0][1],line[0][3]]for line in lines])
    #直线拟合, 多项式系数，多项式拟合坐标，坐标，阶数
    poly=np.polyfit(xc,yc,deg=1)
    #多项式系数计算直线的两点，用于唯一确定这条直线
    point1=(np.min(xc),np.polyval(poly,np.min(xc)))
    point2=(np.max(xc),np.polyval(poly,np.max(xc)))
    return np.array([point1,point2],dtype=int)