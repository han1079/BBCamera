import numpy as np
from scipy.misc import imread, imsave, imresize
import cv2
import matplotlib.image as mpimg
from PIL import Image
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 170;
 
# Filter by Area.
params.filterByArea = True
params.minArea = 250
 
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 1
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.7
 
# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.5
params.maxInertiaRatio = 1
 
# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else : 
    detector = cv2.SimpleBlobDetector_create(params)


#Green Search space dictated as bright various hues of green.

lower_green = (45, 100, 50)
upper_green = (75, 255, 255)

#Create and name a class camera that stores captured camera information from DEVICE 0
camera = cv2.VideoCapture(0);

def process_image(frame):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# define range of blue color in HSV
	lower_blue = np.array([115,50,50])
	upper_blue = np.array([130,255,255])

	# define range of red color in HSV
	lower_red = np.array([0,160,120])
	upper_red = np.array([10,255,255])

	# Thresholding
	bluemask = cv2.inRange(hsv, lower_blue, upper_blue)
	redmask = cv2.inRange(hsv, lower_red, upper_red)
	grmask = cv2.inRange(hsv, lower_green, upper_green)

	# Bitwise-AND mask and original image
	#res = cv2.bitwise_and(frame,frame, mask= mask)

	cv2.imshow('frame',frame)
	cv2.imshow('mask',bluemask)
	cv2.imshow('grmask',grmask)
	#cv2.imshow('res',res)

	return {'blue':bluemask, 'red':redmask}

while(True):
#Capture a single frame from the captured frame
	aframe = cv2.imread("./greenball.jpg",0)
	print(aframe)
#	(grabbed,aframe) = camera.read()
	frame = np.array(aframe, dtype=np.uint8)

	# Process the frame using the process_image() function
	processedimgs = process_image(frame)

	nvimg_blue = cv2.cvtColor(processedimgs['blue'], cv2.COLOR_GRAY2BGR)
	nvimg_red = cv2.cvtColor(processedimgs['red'], cv2.COLOR_GRAY2BGR)

	height, width, depth = nvimg_red.shape

	red = cv2.split(nvimg_red)[0]
	blue = cv2.split(nvimg_blue)[2]
	green = np.zeros((height, width), np.uint8)

	output_array = cv2.merge([blue, green, red])


# 	temp = cv2.resize(aframe, (160,120), "INTER_NEAREST")

# 	frame = cv2.blur(temp, (20,20))
	
# 	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# #	H,S,V = cv2.split(hsv)
# #	row = H.shape[0]
# #	cols = H.shape[1]

# 	mask = cv2.inRange(hsv, lowerGreen, upperGreen)
# 	output = frame.copy()
# 	img = cv2.blur(mask, (10,10))

# #	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.2,100)

# 	if circles is not None:
# 	# convert the (x, y) coordinates and radius of the circles to integers
# 		circles = np.round(circles[0, :]).astype("int")
	 
# 		# loop over the (x, y) coordinates and radius of the circles
# 		for (x, y, r) in circles:
# 			# draw the circle in the output image, then draw a rectangle
# 			# corresponding to the center of the circle
# 			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
# 			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
# #	placeholder = frame

# #	keypoints = detector.detect(mask)

# #	keyframe = cv2.drawKeypoints(mask,keypoints,np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# 	cv2.imshow('tralovtich', output)

# #	print(frame[row/2, cols/2, :])

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

camera.release()
cv2.destroyAllWindows()
