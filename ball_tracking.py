from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time

KNOWN_WIDTH=7.0
def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth
focal = 403.66667374320656

greenLower = (20, 100, 100)
greenUpper = (30, 255, 255)
# if a video path was not supplied, grab the reference
# to the webcam

vs = VideoStream(src=0).start()

time.sleep(2.0)

while True:
	# grab the current frame
	frame = vs.read()
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

			inches = distance_to_camera(KNOWN_WIDTH,focal,radius*2)
			w=frame.shape[1]
			orientation=""
			if(w/2 - radius < center[0] and w/2 + radius > center[0]):
				orientation = "center"
			elif(w/2 > center[0]):
				orientation = "left"
			else:
				orientation = "right"
			string = "%.2f inches " % (inches)
			string+=orientation
			cv2.putText(frame, string,
			(frame.shape[1] - 500, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
			2.0, (0, 255, 0), 3)
			print(orientation)

			
			

			print(str(inches) + " inches")
	# update the points queue
	cv2.imshow("Frame", frame)

	key = cv2.waitKey(1) & 0xFF

	if key == ord('q'):
		break
    
vs.stop()

cv2.destroyAllWindows()
