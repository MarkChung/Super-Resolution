# -*- coding: utf-8 -*-
# @Time    : 2018/3/20 11:20
# @Author  : Jiahui Zhang
# @Email   : zjiahui96@gmail.com
# @File    : main.py
# @Software: PyCharm

from iteratedbackprojection import *
from estimation_shift import *
from createimages import *
import time


def selectImage(imageNumber):
    list = []
    # img1 = Image.open('image/image1.tif')
    img1 = Image.open('/Users/chosenone/Desktop/made/img1.tif')
    list.append(img1)

    for i in range(1, imageNumber):
        # tempImage = Image.open('image/image'+str(i+1)+'.tif')
        tempImage = Image.open('/Users/chosenone/Desktop/made/img' + str(i + 1) + '.tif')
        if (img1.size == tempImage.size):
            list.append(tempImage)
        else:
            print ('Size Error: Image ' + str(i) + ' is not the same size as image 0')

    return list


if __name__ == '__main__':
    start = time.clock()

    # 构造LR图像
    # sourceimage = Image.open('image/test/img1_1.tif')
    # Images = create_images(sourceimage, 2, 8)

    Images = selectImage(8)     #加载已有LR图像
    grayImages = []
    for i in range(len(Images)):
        grayImages.append(rgb2gray(Images[i]))
    delta_est = np.matrix(estimate_shift(grayImages, 15))
    im_result = IBP(Images, delta_est, 2)
    im_result.save('/Users/chosenone/Desktop/result.tif')

    end = time.clock()
    print 'Run Time: ' + str(end - start)
