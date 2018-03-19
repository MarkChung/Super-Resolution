# -- coding:utf-8 --
import cv2
from numpy import *
import numpy as np
from PIL import Image


# 取出图像中的第 line 信道
def selectimage(img, line):
    result = img[:, :, line]
    return result

# 图像最邻近插值法
def nearestinset(img, factor):
    size = img.shape
    height = size[0]
    width = size[1]

    emptyImage = np.zeros((factor * height, factor * width))

    for i in range(factor * height):
        for j in range(factor * width):
            x = int(i / factor)
            y = int(j / factor)
            emptyImage[i, j] = img[x, y]
    return emptyImage

# 初始化图像
def generateimage(dir):
    img = Image.open(dir)
    img = img.convert('YCbCr')
    temp = np.array(img)
    temp = 1.0 * temp / 255
    size = temp.shape
    for i in range(size[0]):
        for j in range(size[1]):
            for k in range(size[2]):
                temp[i][j][k] = round(temp[i][j][k], 4)
    return temp

# 求二维数组里最大值
def getmax(img):
    maxnum = 0
    for i in range(img.shape[0]):
        if maxnum < max(img[i]):
            maxnum = max(img[i])
    return maxnum

# 求二维数组里最小值
def getmin(img):
    minnum = 0
    for i in range(img.shape[0]):
        if minnum > min(img[i]):
            minnum = min(img[i])
    return minnum

# 迭代反投影算法(IBP)
def IBP(factor):
    delta_est = matrix([[0, 0], [-0.2555, -0.5818], [-0.3909, -0.6848], [-0.5418, -0.1202]])
    phi_est = matrix([[0], [0], [0], [0]])

    img = generateimage('/Users/chosenone/Desktop/image1.tif')

    img1 = selectimage(img, 0)
    cb_temp = selectimage(img, 1)
    cr_temp = selectimage(img, 2)
    im_color1 = nearestinset(cb_temp, factor)
    im_color2 = nearestinset(cr_temp, factor)

    imOrigBig = nearestinset(img1, factor)  # 图像最邻近插值
    # -- end of Movie Variables

    # 初始化
    lamda = 0.01  # 定义迭代反投影算法的步长
    max_iter = 1000  # 迭代次数
    iter = 1  # 当前迭代次数

    # 从估计高分辨率图像开始，用第一幅低分辨率图像的没有采样过的版本作为初始的估计
    X = imOrigBig
    X_prev = X
    E = zeros([1000, 2])

    blur = matrix([[0.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 0.0]])
    blur = blur / sum(blur)

    sharpen = matrix([[0, -0.25, 0], [-0.25, 2, -0.25], [0, -0.25, 0]])

    # 主循环
    while iter < max_iter:

        G = zeros(X.shape)
        for i in range(4):
            tempimage = generateimage('/Users/chosenone/Desktop/image' + str(i + 1) + '.tif')
            tempimage = selectimage(tempimage, 0)

            # circshift() 做运动估计
            temp = roll(X, int(-round(factor * delta_est[i, 0])), 0)
            temp = roll(temp, int(-round(factor * delta_est[i, 1])), 1)

            # imrotate() 做图像旋转
            # temp = transform.rotate(temp, phi_est(i))

            # imfilter() 存疑，可以有更好的方法
            temp = cv2.filter2D(temp, -1, blur)

            temp = temp[::factor, ::factor]  # 图像缩放，每factor个像素点取一个值

            temp = temp - tempimage

            temp = nearestinset(temp, factor)

            temp = cv2.filter2D(temp, -1, sharpen)

            # temp.rotate(-phi_est(i))
            # temp = transform.rotate(temp, -phi_est(i))

            temp = roll(temp, int(round(factor * delta_est[i, 1])), 1)
            temp = roll(temp, int(round(factor * delta_est[i, 0])), 0)
            G = G + temp

        X = X - lamda * G
        if getmin(X) < 0:
            X = X - getmin(X)
            X = X / getmax(X)

        delta = linalg.norm(X_prev - X) / linalg.norm(X)
        E[iter][0] = iter
        E[iter][1] = delta
        if iter > 3:
            if abs(E[iter - 4, 1] - delta) < 1e-5:
                break
        X_prev = X
        iter = iter + 1

    imagesize = X.shape
    height = imagesize[0]
    width = imagesize[1]

    for i in range(height):
        for j in range(width):
            X[i][j] = X[i][j] * 255
            im_color1[i][j] = im_color1[i][j] * 255
            im_color2[i][j] = im_color2[i][j] * 255

    temp_result = zeros((height, width, 3), 'uint8')
    for i in range(height):
        for j in range(width):
            temp_result[i][j][0] = X[i][j]
            temp_result[i][j][1] = im_color1[i][j]
            temp_result[i][j][2] = im_color2[i][j]

    result = Image.fromarray(temp_result, mode='YCbCr')
    result = result.convert('RGB')
    result.save('/Users/chosenone/Desktop/result.tif')

    print ("the " + str(iter) + " accuracy is: " + str(1 - round(delta, 7)))

    return X