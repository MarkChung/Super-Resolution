# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 14:14
# @Author  : Jiahui Zhang
# @Email   : zjiahui96@gmail.com
# @File    : createimages.py
# @Software: PyCharm

from PIL import Image
import numpy as np


#################################
# 用高分辨率图像构造序列低分辨率图像 #
#################################
def create_images(image, factor, imagenumber):
    shift = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3], [3, 0],
             [3, 1], [3, 2], [3, 3]]  # 子像素位移量
    # image = image.convert('YCbCr')
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
        emptyimage = np.zeros((height, width, 3), 'uint8')
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
                sum[0] = round(float(sum[0]) / factor / factor)
                sum[1] = round(float(sum[1]) / factor / factor)
                sum[2] = round(float(sum[2]) / factor / factor)
                emptyimage[m1, m2] = sum
        temp = Image.fromarray(emptyimage, mode='RGB')
        # temp = temp.convert('RGB')
        temp.save('/Users/chosenone/Desktop/made/img' + str(num + 1) + '.tif')
        result.append(temp)
    return result
