import numpy as np
from skimage import io
from PIL import Image
import cv2

shift = np.matrix([[0.0,-1.0,0.0],[-1.0,3.0,0.0],[0.0,-1.0,0.0]])

img = io.imread('/Users/chosenone/Desktop/pocs-18frame.tif')
arr = img

#img = Image.open('/Users/chosenone/Desktop/pocs-18frame.tif')
#img.convert('YCbCr')
#arr = np.array(img)
for i in range(3):
	arr[:,:,i] = cv2.filter2D(arr[:,:,i], -1, shift)

io.imsave('/Users/chosenone/Desktop/sharpen.tif',arr)

#result = Image.fromarray(arr, mode='RGB')
#result.convert('RGB')
#result.save('/Users/chosenone/Desktop/sharpen.tif')

