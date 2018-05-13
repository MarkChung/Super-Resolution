from skimage import io

for i in range(4):
	img = io.imread('/Users/chosenone/Desktop/made/yuan/img'+str(i+1)+'.tif')
	io.imsave('/Users/chosenone/Desktop/img'+str(i+1)+'.jpg',img)

