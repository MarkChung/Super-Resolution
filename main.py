from iteratedbackprojection import *

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
    im_result = IBP(Images, 2)