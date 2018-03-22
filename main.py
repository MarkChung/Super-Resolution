from iteratedbackprojection import *
from estimation_shift import *

def selectImage(imageNumber):
    list = []
    img1 = Image.open('image/image1.tif')
    list.append(img1)

    for i in range(1, imageNumber):
        tempImage = Image.open('image/image'+str(i+1)+'.tif')
        if (img1.size == tempImage.size):
            list.append(tempImage)
        else:
            print ('Size Error: Image ' + str(i) + ' is not the same size as image 0')

    return list

if __name__ == '__main__':
    Images = selectImage(4)
    grayImages = []
    for i in range(len(Images)):
        grayImages.append(rgb2gray(Images[i]))
    delta_est = np.matrix(estimate_shift(grayImages, 25))
    im_result = IBP(Images, delta_est, 2)
    im_result.save('/Users/chosenone/Desktop/result.tif')