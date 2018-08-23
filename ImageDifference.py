import cv2
import math
import numpy as np
import sys
from sklearn.cluster import KMeans

if __name__ == "__main__":
	pic1 = str(sys.argv[1])
	pic2 = str(sys.argv[2])
	nClusters = int(sys.argv[3])

# find difference between two images and
# store that as a new image file
img1 = cv2.imread(pic1)
img2 = cv2.imread(pic2)
imgDif = img1 - img2

# get image width and height
height, width = imgDif.shape[:2]

# go through every pixel and check if it is
# not black, if so, push it's coordinates
# into a list for k-means clustering
points = list()
for x in range(0, width):
	for y in range(0, height):
		if (imgDif[y, x] != [0, 0, 0]).all():
			points.append((x, y))

# CLUSTER!
kmeans = KMeans(n_clusters=nClusters)
kmeans.fit(points)

# Iterate through each point in the cluster, 
# and estimate an elipse that covers the 
# cluster
for i in range(nClusters):
	# get edge points
	left = None
	right = None
	up = None
	down = None
	for j in range(len(points)):
		if kmeans.labels_[j] == i:
			# point is left of center
			if points[j][0] < kmeans.cluster_centers_[i][0]:
				if left is None:
					left = points[j]
				else:
					if points[j][0] < left[0]:
						left = points[j]
			# point is right of center
			elif points[j][0] > kmeans.cluster_centers_[i][0]:
				if right is None:
					right = points[j]
				else:
					if points[j][0] > right[0]:
						right = points[j]

			# point is up of center
			if points[j][1] < kmeans.cluster_centers_[i][1]:
				if up is None:
					up = points[j]
				else:
					if points[j][1] < up[1]:
						up = points[j]
			# point is down of center
			elif points[j][1] > kmeans.cluster_centers_[i][1]:
				if down is None:
					down = points[j]
				else:
					if points[j][1] > down[1]:
						down = points[j]

	tl = (left[0], up[1])
	tr = (right[0], up[1])
	bl = (left[0], down[1])
	br = (right[0], down[1])

	cv2.line(imgDif, (math.floor(tl[0]), math.floor(tl[1])),
		(math.floor(tr[0]), math.floor(tr[1])), (255, 255, 255), 4)

	cv2.line(imgDif, (math.floor(tr[0]), math.floor(tr[1])),
		(math.floor(br[0]), math.floor(br[1])), (255, 255, 255), 4)

	cv2.line(imgDif, (math.floor(br[0]), math.floor(br[1])),
		(math.floor(bl[0]), math.floor(bl[1])), (255, 255, 255), 4)

	cv2.line(imgDif, (math.floor(bl[0]), math.floor(bl[1])),
		(math.floor(tl[0]), math.floor(tl[1])), (255, 255, 255), 4)

	# if right is higher than left, average
	# with up point, recalculate
	#if right[1] < left[1]:
	#	right = ((right[0] + up[0]) / 2, (right[1] + up[1]) / 2)
	#	left = ((left[0] + down[0]) / 2, (left[1] + down[1]) / 2)

	# if left is higher than right, average
	# with down point, recalculate
	#elif right[1] > left[1]:
	#	right = ((right[0] + down[0]) / 2, (right[1] + down[1]) / 2)
	#	left = ((left[0] + up[0]) / 2, (left[1] + up[1]) / 2)

	# get x radius of ellipse
	#dx = abs(left[0] - right[0])
	#dy = abs(left[1] - right[1])
	#rx = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)) - 20

	# get angle between left and right
	# points in degress
	#angle = math.degrees(math.atan2(dy, dx))

	# angle adjustments
	#if right[1] < left[1]:
	#	angle -= 45

	# get ry
	# find all points on the verticle axis
	# and find the distance between the
	# edges and then tilt that distance 
	# by a complementary angle to the theta
	#dy = 0
	#p = None
	#for j in range(len(points)):
	#	if kmeans.labels_[j] == i:
	#		if math.floor(points[j][0]) == math.floor(kmeans.cluster_centers_[i][0]): 
	#			if (abs(kmeans.cluster_centers_[i][1] - points[j][1]) > dy):
	#				dy = abs(kmeans.cluster_centers_[i][1] - points[j][1])
	#				p = points[j]

	#theta = angle
	#ry = (dy / math.cos(theta))
	#ry = 30
	
	#cv2.line(imgDif, (math.floor(right[0]), math.floor(right[1])),
	#	(math.floor(left[0]), math.floor(left[1])), (255, 255, 255), 4)

	# draw ellipse
	#cv2.ellipse(imgDif, (math.floor(kmeans.cluster_centers_[i][0]), math.floor(kmeans.cluster_centers_[i][1])),
	#	(math.floor(abs(rx)), math.floor(abs(ry))), angle, 0, 360, (255, 255, 255), 2)

# output JSON data
# check for solutions JSON file to append
# to, if not exists, create one.


cv2.imshow('imgDif', imgDif)
cv2.waitKey(0)
cv2.destroyAllWindows()