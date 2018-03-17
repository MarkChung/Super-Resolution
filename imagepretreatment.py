from skimage import io
from numpy import *

ImageNumer = 4
Image = []
for i in range(ImageNumer):
    Image[i+1] = io.imread('/Users/chosenone/Desktop/image' + str(i+1) + '.tif')
