import cv2
import math
import numpy as np
from sklearn.cluster import KMeans

# Change these to be entered in terminal before runtime
pic1 = 'cook1.jpg' 
pic2 = 'cook2.jpg'
nClusters = 5
# - - - - - - - - - - - - - - - - - - - - - - - - - - -

# find difference between to images and
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
	left = None
	right = None
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

	# get euclidean distance between two edge points
	pdx = abs(left[0] - right[0])
	pdy = abs(left[1] - right[1])
	pd = math.sqrt(math.pow(pdx, 2) + math.pow(pdy, 2)) - 30

	# get angle between the two points in degress
	angle = math.degrees(math.atan2(pdy, pdx))

	# adjustments????
	if right[1] < left[1]:
		angle += 135
	
	# draw ellipse
	cv2.ellipse(imgDif, (math.floor(kmeans.cluster_centers_[i][0]), math.floor(kmeans.cluster_centers_[i][1])),
		(math.floor(pd), 30), angle, 0, 360, (255, 255, 255), 2)





cv2.imshow('imgDif', imgDif)
cv2.waitKey(0)
cv2.destroyAllWindows()