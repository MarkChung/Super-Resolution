# -*- coding: utf-8 -*-
# @Time    : 2018/3/19 10:32
# @Author  : Jiahui Zhang
# @Email   : zjiahui96@gmail.com
# @File    : iteratedbackprojection.py
# @Software: PyCharm

from imagepretreatment import *
import cv2
from numpy import *
import numpy as np
from PIL import Image
from skimage import transform


# 迭代反投影算法(IBP)
def IBP(images, delta_est, factor):
    phi_est = matrix([[0], [0], [0], [0]])

    img = images[0]
    img = generateimage(img)

    # img1 = img
    img1 = selectimageline(img, 0)
    cb_temp = selectimageline(img, 1)
    cr_temp = selectimageline(img, 2)
    # 图像最邻近插值
    im_color1 = nearestinsert(cb_temp, factor)
    im_color2 = nearestinsert(cr_temp, factor)
    imOrigBig = nearestinsert(img1, factor)

    # 双线性插值
    # im_color1 = doublelinearinsert(cb_temp, factor)
    # im_color2 = doublelinearinsert(cr_temp, factor)
    # imOrigBig = doublelinearinsert(img1, factor)

    # 双三次插值
    # im_color1 = double3insert(cb_temp, factor)
    # im_color2 = double3insert(cr_temp, factor)
    # imOrigBig = double3insert(img1, factor)

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
            tempimage = generateimage(images[i])
            tempimage = selectimageline(tempimage, 0)

            # circshift() 做运动估计
            temp = roll(X, int(-round(factor * delta_est[i, 0])), 0)
            temp = roll(temp, int(-round(factor * delta_est[i, 1])), 1)

            # imrotate() 做图像旋转
            # temp = transform.rotate(temp, phi_est(i))

            # imfilter() 存疑，可以有更好的方法
            temp = cv2.filter2D(temp, -1, blur)

            temp = temp[::factor, ::factor]  # 图像缩放，每factor个像素点取一个值

            temp = temp - tempimage

            temp = nearestinsert(temp, factor)    # 最邻近插值
            # temp = doublelinearinsert(temp, factor)  # 双线性插值
            # temp = double3insert(temp, factor)      #双三次插值

            # temp = cv2.filter2D(temp, -1, sharpen)

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

    # result = Image.fromarray(temp_result, mode='L')

    print ("the " + str(iter) + " accuracy is: " + str(1 - round(delta, 7)))

    return result
