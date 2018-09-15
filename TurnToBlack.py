import cv2
import sys

if __name__ == "__main__":
	pic1 = str(sys.argv[1])

img1 = cv2.imread(pic1)

height, width = imgDif.shape[:2]

for x in range(0, width):
	for y in range(0, height):
		if (imgDif[y, x] == [255, 255, 255]).all():
			imgDif[y, x] = [0, 0, 0]

cv2.imshow('img1', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()