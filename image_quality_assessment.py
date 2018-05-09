# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 11:28
# @Author  : Jiahui Zhang
# @Email   : zjiahui96@gmail.com
# @File    : image_quality_assessment.py
# @Software: PyCharm

import numpy as np
import math
from PIL import Image
from image_pretreatment import *
from estimation_shift import *
from skimage.measure import compare_ssim
import cv2


#############################
# 计算图像的峰值信噪比（PSNR） #
#############################
def getPSNR(source, detect):
    # images = remove_shift(source, detect)
    # source = images[0]
    # detect = images[1]
    source = source.convert('YCbCr')
    detect = detect.convert('YCbCr')
    src = np.array(source)
    src1 = src[:, :, 0]
    src2 = src[:, :, 1]
    src3 = src[:, :, 2]
    det = np.array(detect)
    det1 = det[:, :, 0]
    det2 = det[:, :, 1]
    det3 = det[:, :, 2]
    y = src1 - det1
    cb = src2 - det2
    cr = src3 - det3
    msey = y * y
    msecb = cb * cb
    msecr = cr * cr
    sum = msey.sum() + msecb.sum() + msecr.sum()
    mse = sum / (src.shape[0] * src.shape[1] * 3)

    val = 255

    psnr = 10 * math.log10((val ^ 2) / mse)

    print("PSNR: {}".format(psnr))
    print("MSE: {}".format(mse))

    return psnr, mse

# def remove_shift(source, detect):
#     image = []
#     result = []
#     result.append(source)
#     image.append(rgb2gray(source))
#     image.append(rgb2gray(detect))
#     shift = estimate_shift(image, 15)
#     print(shift)
#     temp_detect = np.array(detect)
#     for i in range(temp_detect.shape[2]):
#         print(int(round(shift[1,0])))
#         print(int(round(shift[1,1])))
#         temp_detect[:,:,i] = np.roll(temp_detect[:,:,i], int(round(shift[1,0])), 0)
#         temp_detect[:,:,i] = np.roll(temp_detect[:,:,i], int(round(shift[1,1])), 1)
#     result_detect = Image.fromarray(temp_detect, mode='RGB')
#     result.append(result_detect)
#
#     images = []
#     images.append(rgb2gray(source))
#     images.append(rgb2gray(result_detect))
#     print(estimate_shift(images,15))
#
#     return result


#############################
# 计算图像的结构相似性（SSIM） #
#############################
def getSSIM(source, detect):
    # 加载两张输入的图片
    src = np.array(source)
    det = np.array(detect)

    # 将两张输入的图像转化为灰度图
    graySrc = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    grayDet = cv2.cvtColor(det, cv2.COLOR_RGB2GRAY)

    # 计算两张图片之间的结构相似性
    (score, diff) = compare_ssim(graySrc, grayDet, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    # print("DIFF: {}".format(diff))

    return score

###########################
# 图像质量评估记录及写入文件 #
###########################
def image_assessment(source, detect):
    record_file = open('image_assessment_result.txt', "a")
    psnr, mse = getPSNR(source, detect)
    ssim = getSSIM(source, detect)
    record_file.write("\nPSNR: {}\n".format(psnr))
    record_file.write("MSE: {}\n".format(mse))
    record_file.write("SSIM: {}\n".format(ssim))