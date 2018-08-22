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

	# get x radius of ellipse
	dx = abs(left[0] - right[0])
	dy = abs(left[1] - right[1])
	rx = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)) - 30

	# get angle between left and right points in degress
	angle = math.degrees(math.atan2(dy, dx))

	# angle adjustments
	if right[1] < left[1]:
		angle += 135

	# get ry
	# iterate through every point, and compare its
	# angle in relation to the center point. Find the 
	# two furthest points on the line that is
	# perpendicular to the angle created from the left
	# and right points. Measure this distance to get ry.
	for j in range(len(points)):
		if kmeans.labels_[j] == i:
			tx = points[j][0] # point x
			ty = points[j][1] # point y
			cx = kmeans.cluster_centers_[i][0] # center x
			cy = kmeans.cluster_centers_[i][1] # center y
			dx = abs(tx - cx) # distance between x coordinates
			dy = abs(ty - cy) # distance between y coordinates
			an = math.floor(math.degrees(math.atan2(dy, dx))) # angle
			
			perpAn = math.floor(math.floor(angle) - an)
			print(str(perpAn) + "\n" + str(math.floor(angle)) + "\n")
			if perpAn % 90 <= 10: #and abs(perpAn - angle) > 10:
				cv2.line(imgDif, (math.floor(tx), math.floor(ty)), (math.floor(cx), math.floor(cy)), (255, 255, 255), 1)

	ry = 40;
	
	# draw ellipse
	cv2.ellipse(imgDif, (math.floor(kmeans.cluster_centers_[i][0]), math.floor(kmeans.cluster_centers_[i][1])),
		(math.floor(rx), math.floor(ry)), angle, 0, 360, (255, 255, 255), 2)

# output JSON data
# check for solutions JSON file to append
# to, if not exists, create one.


cv2.imshow('imgDif', imgDif)
cv2.waitKey(0)
cv2.destroyAllWindows()