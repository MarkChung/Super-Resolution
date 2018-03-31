import numpy as np
from PIL import Image

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

    for i in range(factor*height):
        for j in range(factor*width):
            x = int(i / factor)
            y = int(j / factor)
            p = (i + 0.0) / factor - x
            q = (j + 0.0) / factor - y
            x = int(x) - 2
            y = int(y) - 2
            A = np.array([[S(1+p), S(p), S(1-p), S(2-p)]])

            if x >= 1 and x <= (factor*height - 3) and y >= 1 and y <= (factor*width - 3):
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
                emptyImage[i,j] = round(blue, 4)

    return emptyImage

if __name__ == '__main__':
    img = Image.open('/Users/chosenone/Desktop/img1_1.tif')
    img = generateimage(img)
    arr = np.array(img)
    line0 = arr[:,:,0]
    line1 = arr[:,:,1]
    line2 = arr[:,:,2]
    line0 = double3insert(line0, 2)
    line1 = double3insert(line1, 2)
    line2 = double3insert(line2, 2)
    empty = np.zeros((1024,768,3),'uint8')
    for i in range(1024):
        for j in range(768):
            line0[i][j] = line0[i][j] * 255
            line1[i][j] = line1[i][j] * 255
            line2[i][j] = line2[i][j] * 255
    for i in range(1024):
        for j in range(768):
            empty[i][j][0] = line0[i][j]
            empty[i][j][1] = line1[i][j]
            empty[i][j][2] = line2[i][j]

    result = Image.fromarray(empty, mode='YCbCr')
    result = result.convert('RGB')
    result.save('/Users/chosenone/Desktop/once3insert.tif')