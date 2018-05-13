import numpy as np
import scipy.ndimage
from skimage import io
from PIL import Image

img = io.imread('/Users/chosenone/Desktop/made/baby/img1.tif')
img_x = img[:,:,0]
img_y = img[:,:,1]
img_z = img[:,:,2]

zoom_x = scipy.ndimage.zoom(img_x, 2, order=2)
zoom_y = scipy.ndimage.zoom(img_y, 2, order=2)
zoom_z = scipy.ndimage.zoom(img_z, 2, order=2)

result = np.zeros((zoom_x.shape[0],zoom_x.shape[1], 3), 'uint8')

result[:,:,0] = zoom_x
result[:,:,1] = zoom_y
result[:,:,2] = zoom_z

io.imsave('/Users/chosenone/Desktop/zoom.tif',result)
