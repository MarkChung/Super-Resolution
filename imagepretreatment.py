# -- coding: utf-8 --

from numpy import *
import numpy as np
import math
import cv2

from PIL import Image


# 取出图像中的第 line 信道
def selectimageline(img, line):
    result = img[:, :, line]
    return result


# 图像最邻近插值法
def nearestinsert(img, factor):
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


# 图像双线性插值法
def doublelinearinsert(img, factor):
    size = img.shape
    height = size[0]
    width = size[1]

    emptyImage = np.zeros((factor * height, factor * width))

    for i in range(factor * height):
        for j in range(factor * width):
            x = int(i / factor)
            y = int(j / factor)
            p = (i + 0.0) / factor - x
            q = (j + 0.0) / factor - y
            x = int(x) - 1
            y = int(y) - 1
            if x + 1 < (factor * height) and y + 1 < (factor * width):
                value = img[x, y] * (1 - p) * (1 - q) + img[x, y + 1] * q * (1 - p) + img[x + 1, y] * (1 - q) * p + img[
                    x + 1, y + 1] * p * q
            emptyImage[i, j] = round(value, 4)
    return emptyImage


# 图像双三次插值法

def S(x):
    x = np.abs(x)
    if 0 <= x < 1:
        return 1 - 2 * x * x + x * x * x
    if 1 <= x < 2:
        return 4 - 8 * x + 5 * x * x - x * x * x
    else:
        return 0


def double3insert(img, factor):
    size = img.shape
    height = size[0]
    width = size[1]
    emptyImage = np.zeros((factor * height, factor * width))

    for i in range(factor * height):
        for j in range(factor * width):
            x = int(i / factor)
            y = int(j / factor)
            p = (i + 0.0) / factor - x
            q = (j + 0.0) / factor - y
            x = int(x) - 2
            y = int(y) - 2
            A = np.array([[S(1 + p), S(p), S(1 - p), S(2 - p)]])

            if x >= 1 and x <= (factor * height - 3) and y >= 1 and y <= (factor * width - 3):
                B = np.array([
                    [img[x - 1, y - 1], img[x - 1, y],
                     img[x - 1, y + 1],
                     img[x - 1, y + 1]],
                    [img[x, y - 1], img[x, y],
                     img[x, y + 1], img[x, y + 2]],
                    [img[x + 1, y - 1], img[x + 1, y],
                     img[x + 1, y + 1], img[x + 1, y + 2]],
                    [img[x + 2, y - 1], img[x + 2, y],
                     img[x + 2, y + 1], img[x + 2, y + 1]],

                ])
                C = np.array([
                    [S(1 + q)],
                    [S(q)],
                    [S(1 - q)],
                    [S(2 - q)]
                ])
                blue = np.dot(np.dot(A, B), C)[0, 0]

                def adjust(value):
                    if value > 1.0:
                        value = 1.0
                    elif value < 0:
                        value = 0.0
                    return value

                blue = adjust(blue)
                emptyImage[i, j] = round(blue, 4)

    return emptyImage


# 初始化图像
def generateimage(img):
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


# 图像的灰度化
def rgb2gray(image):
    img = generateimage(image)
    img = selectimageline(img, 0)

    return img
