import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def plot(data, title):
	plot.i +=1
	plt.subplot(2, 2, plot.i) #where to plot the image
	plt.imshow(data) #Display the data
	plt.gray() #set background color
	plt.title(title) #set the title of each image

# When filling the accumulator array we split the circle into 8 equal parts, and keep increasing the value if x and y lies within these
# 8 parts, if they do we increase them by one and then check if there are more than 90 points in the accumulator array of each of these
# 8 parts thus resulting in us finding the circles
def fill_accumulatorArray(orignalX,originalY,radius, height, width, accumulatorArray):
	x = radius
	y=0
	checkNext = 1-x  
	while(y<x):
		# Part 1
		if(x + orignalX<height and y + originalY<width):
			accumulatorArray[ x + orignalX,y + originalY,radius]+=1; 
		# Part 2
		if(y + orignalX<height and x + originalY<width):
			accumulatorArray[ y + orignalX,x + originalY,radius]+=1;
		# Part 3
		if(-y + orignalX<height and x + originalY<width):
			accumulatorArray[-y + orignalX,x + originalY,radius]+=1;
		# Part 4
		if(-x + orignalX<height and y + originalY<width):
			accumulatorArray[-x + orignalX,y + originalY,radius]+=1;
		# Part 5
		if(-x + orignalX<height and -y + originalY<width):
			accumulatorArray[-x + orignalX,-y + originalY,radius]+=1;
		# Part 6
		if(-y + orignalX<height and -x + originalY<width):
			accumulatorArray[-y + orignalX,-x + originalY,radius]+=1;
		# Part 7
		if(y + orignalX<height and -x + originalY<width):
			accumulatorArray[ y + orignalX,-x + originalY,radius]+=1;
		# Part 8
		if(x + orignalX<height and -y + originalY<width):
			accumulatorArray[ x + orignalX,-y + originalY,radius]+=1;
		y+=1
		if(checkNext<=0):
			checkNext += 2 * y + 1
		else:
			x=x-1;
			checkNext += 2 * (y - x) + 1

#Applying canny edge detection to the image to find a threshold value
def cannyImageSelection():
	for x in range(0, 200, 5):
		for y in range(0, 200, 10):
			edge_image = cv2.Canny(blur_image, x, y)
			matplotlib.image.imsave('cannyedge_image' + str(x) + '_' + str(y) + '.png', edge_image)
plot.i = 0

def main():
	#convert the image into an array
	image = cv2.imread('input.jpg', 1)
	# Make a copy for outputting the final image with detected circles
	output = image.copy()
	data = np.array(image)

	#plot the original image
	plot(data, 'original')

	#Apply Gausian Filer of 3x3 kernel to remove noise
	blur_image = cv2.GaussianBlur(image,(3,3),0)
	data = np.array(blur_image)
	#plot the blurred image
	plot(data, 'Gaussian Blur Image')
	matplotlib.image.imsave('blurred_image.png', blur_image)

	#From the images formed above we find that the best suitable threshold is 75, 150
	edge_image = cv2.Canny(blur_image, 75, 150)
	data = np.array(edge_image)
	plot(data, 'Canny Edge Image')

	# Get dimensions image and set radius = 100
	height, width = edge_image.shape
	radius = 150
	#print(height)
	#print(width)

	# Set definitions of the accumulator array
	accumulatorArray = np.zeros(((height, width, radius)))
	filterArray = np.zeros((30, 30, radius))
	filterArray[:,:,:] = 1
	
	# Finding the edges and circles by filling the accumulator array
	edges = np.where(edge_image==255)
	for i in xrange(0, len(edges[0])):
		x = edges[0][i]
		y = edges[1][i]
		for r in xrange(20, 70):
			fill_accumulatorArray(x, y, r, height, width, accumulatorArray)

	i=0 #initiating iterator for i
	j=0 #initiating iterator for j
	#Plotting the found circles back onto the image
	while(i<height-30):
		while(j<width-30):
			filterArray=accumulatorArray[i:i+30,j:j+30,:]*filterArray
			maxPoint = np.where(filterArray==filterArray.max())
			maxPointZero = maxPoint[0]       
			maxPointOne = maxPoint[1]
			maxPointTwo = maxPoint[2]
			maxPointOne=maxPointOne+j
			maxPointZero=maxPointZero+i
			if(filterArray.max()>90):
				cv2.circle(output,(maxPointOne,maxPointZero),maxPointTwo,(255,0,0),2)
			j=j+30
			filterArray[:,:,:]=1
		
		j=0
		i=i+30
		
	matplotlib.image.imsave('Output.png', output)
	plot(output, 'Output Image')
	plt.show()

main()