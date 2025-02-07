import cv2
import numpy as np

# from hough import leftline


#灰度化，高斯滤波，canny变换，边缘提取
def getedge(colorimg,gaussian_ksize=5,gaussian_sigmax=1,canny_threshold1=50,canny_threshold2=100):
    gaussian=cv2.GaussianBlur(colorimg,(gaussian_ksize,gaussian_ksize),gaussian_sigmax)
    grayimg=cv2.cvtColor(gaussian,cv2.COLOR_RGB2GRAY)
    edgeimg=cv2.Canny(grayimg,canny_threshold1,canny_threshold2)
    return edgeimg

#划区域，掩膜
def roi(grayimg):
    poly_pts = np.array([[[0, 368], [300, 210], [340, 210], [640, 368]]])
    #数组
    mask = np.zeros_like(grayimg)
    #掩码
    mask = cv2.fillPoly(mask, pts=poly_pts, color=255)
    #原图，掩码
    img_mask = cv2.bitwise_and(grayimg, mask)
    return img_mask

#获取线段
def getline(edgeimg):
    #计算斜率
    def calculate_slope(line):
        x1, y1, x2, y2 = line[0]
        return (y2 - y1) / (x2 - x1)

    #离群值过滤
    # 删除斜率不一致的线
    # 列表，误差值
    def sub_line(lines, threshold=0.2):
        # all斜率
        slopes = [calculate_slope(line) for line in lines]
        # print(slopes)
        while len(lines) > 0:
            # 平均值mean()
            mean = np.mean(slopes)
            # print(mean)
            # 算出每个斜率与平均值的差值，绝对值abs()
            diff = [abs(s - mean) for s in slopes]
            # print(diff)
            # diff中最大的差值的元素位置，返回最大值argmax()
            idx = np.argmax(diff)
            # print(idx)
            # print(diff[idx])
            if diff[idx] > threshold:
                # 删除s里和l里
                slopes.pop(idx)
                lines.pop(idx)
            else:
                break
        return lines

    #最小二乘拟合
    # 将lines中所有线段拟合成一条
    def least_square_fit(lines):
        # 取出所有坐标点，ravel()高维数组转一维
        xc = np.ravel([[line[0][0], line[0][2]] for line in lines])
        yc = np.ravel([[line[0][1], line[0][3]] for line in lines])
        # 直线拟合, 多项式系数，多项式拟合坐标，坐标，阶数
        poly = np.polyfit(xc, yc, deg=1)
        # 多项式系数计算直线的两点，用于唯一确定这条直线
        point1 = (np.min(xc), np.polyval(poly, np.min(xc)))
        point2 = (np.max(xc), np.polyval(poly, np.max(xc)))
        return np.array([point1, point2], dtype=int)

    #霍夫变换 矩阵，距离r，theta精度，累加阈值，最短阈值，统一线两点最大长度
    lines=cv2.HoughLinesP(edgeimg,1,np.pi/180,15,minLineLength=40,maxLineGap=20)
    #列表，离散的
    #斜率》0左车道，《0右车道
    leftline=[line for line in lines if calculate_slope(line)>0]
    rightline=[line for line in lines if calculate_slope(line)<0]

    #提出离群线段，迭代一下
    leftline=sub_line(leftline)
    rightline=sub_line(rightline)

    return least_square_fit(leftline),least_square_fit(rightline)

#画线
def draw(img,lines):
    #lines: 两条线段: [np.array([[xmin1, ymin1], [xmax1, ymax1]]),
    # np.array([[xmin2, ymin2], [xmax2, ymax2]])]
    leftline,rightline=lines
    #line()需将array转为tuple
    cv2.line(img, tuple(leftline[0]), tuple(leftline[1]), color=(255, 200, 255),thickness=5)
    cv2.line(img, tuple(rightline[0]), tuple(rightline[1]), color=(0, 255, 255), thickness=5)


#彩图显示车道线
def showline(colorimg):
    edgeimg=getedge(colorimg)
    maskgratimg=roi(edgeimg)
    lines=getline(maskgratimg)
    draw(colorimg,lines)
    return colorimg

#读视频流，文件名
capture=cv2.VideoCapture('video.mp4')
while True:
    #读取帧
    #是否关闭，帧图像(数组)
    ret,frame=capture.read()
    farme=showline(frame)
    cv2.imshow('win',farme)
    cv2.waitKey(10)