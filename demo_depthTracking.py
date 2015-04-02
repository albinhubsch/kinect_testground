#!/usr/bin/env python
# from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import freenect
import cv2
import frame_convert
import numpy as np

# 
position = (0, 0) 	# Circle position
precision = 10 		# Amount of pixels to skip each step
threshold = 20 		# Threshold for depth pixels
oldMinVal = 255		# 

while True:

	# Reset these params every at every frame catch
	meanX = 0
	MeanY = 0
	count = 0
	minVal = 255

	# Get depth and try to normalize it
	depth = frame_convert.pretty_depth(freenect.sync_get_depth()[0])

	# Loop through pixels and find the closest ones, Calculate thier mean position
	for y in xrange(0, len(depth), precision):
		for x in xrange(0, len(depth[0]), precision):
			if depth[y][x] < minVal:
				minVal = depth[y][x]

			if depth[y][x] < oldMinVal + threshold:
				meanX = meanX + x
				MeanY = MeanY + y
				count = count + 1

	# Set previous frame threshold value to new min value
	oldMinVal = minVal

	# Create a black image
	img = np.zeros((480,640,3), np.uint8)

	# If any pixels found update circle position to mean position
	if count is 0:
		position = (0, 0)
	else:
		position = (640-meanX/count, MeanY/count)

	# Draw circle
	cv2.circle(img, position, 5, (100, 200, 40), 10, 8, 0)
	cv2.imshow('Stream', img)

	# Print depth img
	cv2.imshow('Depth', depth)

	# Listen for ESC key, leave loop if pressed
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()