from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import signal

#for plotting the various pictures in a grid
def plot(data, title):
	plot.i += 1
	plt.subplot(3,3,plot.i) #where to plot the image
	plt.imshow(data) #Display the data
	plt.gray() #set background color
	plt.title(title) #set title of each image

plot.i = 0 #for iterator purposes

# Function to calculate the zerocrossing
def zero_crossing(image, threshold, requiredThreshold):
	zerocrossing = np.zeros((len(image), len(image[0])))
	for i in range(len(image)-1):
		for j in range(len(image[0]-1)):
			tempList = []
			tempList.append(image[i:i+2, j:j+2])
			maxtimesmin = np.sign(np.amax(tempList))*np.sign(np.amin(tempList))
			maxminusmin = np.amax(tempList)-np.amin(tempList)
			if maxtimesmin<=-1:
				if requiredThreshold==1:
					if(maxminusmin)>=threshold:
						zerocrossing[i][j]=1
				else:
					zerocrossing[i][j] = 1
	return zerocrossing

#convert the image to greyscale
#grey_scaleImage = Image.open('UBCampus.jpg').convert('L')
#grey_scaleImage.save('UBCampus_grey.jpg')

#convert the image into an array
image = Image.open('UBCampus_grey.jpg')
data = np.array(image, dtype=float)

#plot the original picture
plot(data,'original')

# Applying difference of gausian and zero crossing on image
DoG_mask =np.array(([[0, 0, -1, -1, -1, 0, 0],
										 [0, -2, -3, -3, -3, -2, 0],
										 [-1, -3, 5, 5, 5, -3, -1],
										 [-1, -3, 5, 16, 5, -3, -1],
										 [-1, -3, 5, 5, 5, -3, -1],
										 [0, -2, -3, -3, -3, -2, 0],
										 [0, 0, -1, -1, -1, 0, 0]]), np.float32)

DoG_image = signal.convolve2d(data, DoG_mask, mode='full', boundary = 'fill', fillvalue = 0)
plot(DoG_image, 'DoG Image')
#Saving the Image for 1 a)
matplotlib.image.imsave('DoG_image.png', DoG_image)

threshold=700 #this is where you set threshold values

#No Threshold applied to the image
noThresholdDoG = zero_crossing(DoG_image, threshold, 0)
plot(noThresholdDoG, 'DoG No Threshold')
matplotlib.image.imsave('DoG_No_threshold.png', noThresholdDoG)

# Threshold of 700 applied to the image
thresholdToDoG = zero_crossing(DoG_image, threshold, 1)
plot(thresholdToDoG, 'DoG_Threshold '+ str(threshold))
matplotlib.image.imsave('DoG_Threshold'+str(threshold)+'.png', thresholdToDoG)

# Applying Laplacian of Gausian masks and zero crossing
LoG_mask = np.array(([[0, 0, 1, 0, 0],
							[0, 1, 2, 1, 0],
							[1, 2, -16, 2, 1],
							[0, 1, 2, 1, 0],
							[0, 0, 1, 0, 0]]), np.float32)

LoG_image = signal.convolve2d(data, LoG_mask, mode="full", boundary = 'fill', fillvalue = 0)
plot(LoG_image, 'LoG Image')
#Saving the Image for 1 d)
matplotlib.image.imsave('LoG_image.png', LoG_image)

threshold = 200
#No Threshold applied to the image
noThresholdLoG = zero_crossing(LoG_image, threshold, 0)
plot(noThresholdLoG, 'LoG No Threshold')
matplotlib.image.imsave('LoG_No_threshold.png', noThresholdLoG)

# Threshold of 200 applied to the image
thresholdToLoG = zero_crossing(LoG_image, threshold, 1)
plot(thresholdToLoG, 'LoG_Threshold '+ str(threshold))
matplotlib.image.imsave('LoG_Threshold'+str(threshold)+'.png', thresholdToLoG)

#Show the images
plt.show()
