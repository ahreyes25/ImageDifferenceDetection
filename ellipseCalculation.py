
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
