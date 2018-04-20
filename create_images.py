# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 14:14
# @Author  : Jiahui Zhang
# @Email   : zjiahui96@gmail.com
# @File    : create_images.py
# @Software: PyCharm

from PIL import Image
import numpy as np
from image_pretreatment import *
from skimage import exposure
import scipy.ndimage
import cv2

#################################
# 用高分辨率图像构造序列低分辨率图像 #
#################################
def generate(image, factor, imagenumber):

    shift = np.zeros((imagenumber, 2))
    for i in range(1, imagenumber):
        shift[i, 0] = random.randint(0, 4)
        shift[i, 1] = random.randint(0, 4)

    result = []

    img = np.array(image)
    img = img * 1.0
    size = img.shape
    height = int(size[0] / factor)
    width = int(size[1] / factor)

    emptyimage = np.zeros((height,width,size[2]),'uint8')
    for i in range(size[2]):
        img[:,:,i] = 1.0 * img[:,:,i] / 255
        tempimage = create_images(img[:,:,i], factor, shift, imagenumber)
        if getmax(tempimage) > 1:
            tempimage = tempimage / getmax(tempimage)
        tempimage = tempimage * 255
        emptyimage[:,:,i] = tempimage

    singleresult = Image.fromarray(emptyimage, mode='RGB')
    singleresult.save('/Users/chosenone/Desktop/made/man/image'+str(i+1)+'.tif')
    result.append(singleresult)



def create_images(image, factor, delta, imagenumber):

    shift = np.zeros((imagenumber, 2))
    for i in range(1, imagenumber):
        shift[i, 0] = random.randint(0, 4)
        shift[i, 1] = random.randint(0, 4)

    img = np.array(image)
    img = img * 1.0
    size = img.shape
    height = int(size[0] / factor)
    width = int(size[1] / factor)
    result = []

    def widthoverflow(num):
        if (num >= (factor * width - 2)):
            return factor * width - 2
        else:
            return num

    def heightoverflow(num):
        if (num >= (factor * height - 2)):
            return factor * height - 2
        else:
            return num

    for num in range(imagenumber):
        emptyimage = np.zeros((height, width, 3),'uint8')
        x = int(shift[num][0])
        x1 = shift[num][0] - x
        y = int(shift[num][1])
        y1 = shift[num][1] - y
        sum = 0
        for m1 in range(height):
            for m2 in range(width):
                for n2 in range(factor * m2, factor * (m2 + 1) - 1):
                    for n1 in range(factor * m1, factor * (m1 + 1) - 1):
                        sum = sum + img[heightoverflow(n1 + x), widthoverflow(n2 + y)] * (1 - x1) * (1 - y1) + img[
                            heightoverflow(n1 + x + 1), widthoverflow(n2 + y + 1)] * x1 * y1 + \
                              img[heightoverflow(n1 + x), widthoverflow(n2 + y + 1)] * (1 - x1) * y1 + img[
                                  heightoverflow(n1 + x + 1), widthoverflow(n2 + y)] * x1 * (1 - y1)
                sum[0] = float(sum[0]) / factor / factor
                sum[1] = float(sum[1]) / factor / factor
                sum[2] = float(sum[2]) / factor / factor
                emptyimage[m1, m2] = sum
        # emptyimage = exposure.adjust_gamma(emptyimage, 0.4)
        temp = Image.fromarray(emptyimage, mode='RGB')
        # temp = temp.convert('RGB')
        temp.save('/Users/chosenone/Desktop/made/man/img' + str(num + 1) + '.tif')
        result.append(temp)



    return result
