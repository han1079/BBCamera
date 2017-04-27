import numpy as np
import cv2
import imutils

class contourFinder:

	def __init__(self):
		self.name = 'BallFondlers 2 IN 3D'
		self.camerica = cv2.VideoCapture(0)
		self.frame = []
		self.hsv = []
		self.mask = []
		self.center = (0,0)
		self.blur = 0
		self.upperBound = (77, 255, 255)
		self.lowerBound = (28, 86, 6)
		self.contours

	def captureImage(self):
		[grabbed, self.frame] =  self.camerica.read()
		return self.frame

	def hsvAndBlur(self):
		frame = imutils.resize(self.frame, width = 600)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		if self.blur > 0:
			self.hsv = cv2.blur(hsv, (self.blur,self.blur))
		else:
			self.hsv = hsv
		return self.hsv

	def maskAndBlur(self):
		print(self.upperBound)
		mask = cv2.inRange(self.hsv, self.lowerBound, self.upperBound)

		if self.blur > 0:	
			output = cv2.blur(mask, (self.blur,self.blur))
			output = cv2.erode(output, None, iterations = 2)
			self.mask = cv2.dilate(output, None, iterations=1)
		else:
			print("Not Blurring")
			output = cv2.erode(mask, None, iterations = 2)
			output = cv2.dilate(output, None, iterations=2)
			self.mask = output
		return self.mask

	def findContour(self):
		contours = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		if len(contours) > 0:
			self.contours = max(contours, key = cv2.contourArea)
			M = cv2.moments(self.contours)

			if M["m00"] != 0:
				self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			else:
				print("MASS IS ZERO NYKKA. WTF IS YOUR CONTOUR???")
				return self.contours
		else:
			print("No Contours Found Motherfucker.")
			return 0

		return self.center

	def drawOnFrame(self):
		cv2.rectangle(self.frame, (self.center[0] - 5, self.center[1] - 5), (self.center[0] + 5, self.center[1] + 5), (0, 128, 255), -1)

	def endingThisShit(self):
		self.camerica.release()
		cv2.destroyAllWindows()

# if __name__ == '__main__':
#     """ main """
letsDoThis = contourFinder()

while(True):
	frame = letsDoThis.captureImage()

	shrunkenHSV = letsDoThis.hsvAndBlur()

	erodedMask = letsDoThis.maskAndBlur()

	centerpiece = letsDoThis.findContour()

	print(letsDoThis.contours)

	letsDoThis.drawOnFrame()

	cv2.imshow("Label", frame)
	cv2.imshow("shrunkenHSV", shrunkenHSV)
	cv2.imshow("erodedMask", erodedMask)

	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
letsDoThis.endingThisShit()

