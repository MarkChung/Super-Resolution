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

#############################
# 计算图像的峰值信噪比（PSNR） #
#############################
def PSNR(source, detect):

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

    return psnr, mse

img1 = Image.open('/Users/chosenone/Desktop/pocs-18frame.tif')
img2 = Image.open('/Users/chosenone/Desktop/man.tif')

print PSNR(img1, img2)
