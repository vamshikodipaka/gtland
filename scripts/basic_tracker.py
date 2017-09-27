#!/usr/bin python

# Imports
import os, sys, glob
import argparse
from collections import deque
import numpy as np
import cv2
import imutils

# placeholder function
def nothing(x):
    pass

CALIB_MODE = False

# Argument parser
ap = argparse.ArgumentParser()
ap.add_argument ("-v", "--video",  help = "path to the (optional) video file")
ap.add_argument ("-b", "--buffer", type = int, default = 64, help = "max buffer size")
ap.add_argument ("-c", "--calibration", help = "start in calibration mode")
args = vars(ap.parse_args())

# The default values are for the postits
cv2.namedWindow('Color Range')
cv2.createTrackbar('Blue Low',  'Color Range', 12, 255,  nothing)
cv2.createTrackbar('Green Low', 'Color Range', 45, 255,  nothing)
cv2.createTrackbar('Red Low',   'Color Range', 100, 255, nothing)
cv2.createTrackbar('Blue High', 'Color Range', 41, 255,  nothing)
cv2.createTrackbar('Green High','Color Range', 202, 255, nothing)
cv2.createTrackbar('Red High',  'Color Range', 255, 255, nothing)

color_low  = np.array([0, 0, 0])
color_high = np.array([250, 105, 50])
pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam, do calibration only in this case
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
    if args.get("calibration", False):
        CALIB_MODE = True
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    (grabbed, frame) = camera.read()

    # end of the video
    if args.get("video") and not grabbed:
        break

    frame   = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv     = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Blobs
    mask = cv2.inRange(hsv, color_low, color_high)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)    

    # Show trackbars and find their position
    # use them to set new threshold
    cv2.imshow("Color Range", mask)
    bl = cv2.getTrackbarPos("Blue Low",  "Color Range")    
    gl = cv2.getTrackbarPos("Green Low", "Color Range")
    rl = cv2.getTrackbarPos("Red Low",   "Color Range")
    bh = cv2.getTrackbarPos("Blue High", "Color Range")
    gh = cv2.getTrackbarPos("Green High","Color Range")
    rh = cv2.getTrackbarPos("Red High",  "Color Range")
    color_low = np.array([bl, gl, rl])
    color_high= np.array([bh, gh, rh])

	# contouring and (x, y) center of the blob
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
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
 
	# update the points queue
    pts.appendleft(center)
    	# loop over the set of tracked points
    for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()