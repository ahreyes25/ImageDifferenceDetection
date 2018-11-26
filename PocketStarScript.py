import numpy as np
import imutils
import random
import math
import json
import cv2
import sys
import os

#----------------------------------------------------------------------------------------
# ShapeDetector.detect
def detect(c):
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 3:
        shape = "triangle"
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
    elif len(approx) == 5:
        shape = "pentagon"
    else:
        shape = "circle"
    return shape

#----------------------------------------------------------------------------------------
# Read Folder
if __name__ == "__main__":
    pictureFolder = "/" + str(sys.argv[1]) + "/"

#----------------------------------------------------------------------------------------
# Rename Files
path = os.getcwd()
picturePath = str(path) + pictureFolder
filenames = os.listdir(picturePath)
sorted(filenames)
counter = 0

# iterate through all files, alphabetically
for count, filename in enumerate(sorted(filenames), start=1):
    # ignore hidden files
    if (str(filename)[0] != '.'):
        #ignore non png/jpg
        if (str(filename)[len(str(filename)) - 1] == 'g'):

            print("Renaming " + str(filename) + "...")

            # rename original files
            if ('original' in str(filename)):
                os.rename(str(picturePath) + str(filename), str(picturePath) +
                    str(str(math.floor(counter / 3)) + '_original.jpg'))

                counter += 1
            # rename edited files
            elif ('edited' in str(filename)):
                os.rename(str(picturePath) + str(filename), str(picturePath) +
                    str(str(math.floor(counter / 3)) + '_edited.jpg'))

                counter += 1
            # rename answers files
            elif ('answers' in str(filename)): 
                os.rename(str(picturePath) + str(filename), str(picturePath) +
                    str(str(math.floor(counter / 3)) + '_answers.png'))

                counter += 1

            print("Finished!")

#----------------------------------------------------------------------------------------
# Convert Images To Black
filenames = os.listdir(picturePath)
sorted(filenames)

# iterate through all files
for count, filename in enumerate(sorted(filenames), start=1):
    # ignore hidden files
    if (str(filename)[0] != '.'):
        # ignore non png/jpg
        if (str(filename)[len(str(filename)) - 1] == 'g'):
            # get answers file
            if 'answers' in str(filename):
                print("Converting " + str(filename) + " to black...")

                img = cv2.imread(str(picturePath) + str(filename), -1)

                # get image width and height
                height, width = img.shape[:2]

                inShape = False

                # remove strange green blocks that surround shapes
                for x in range(0, width):
                    for y in range(0, height):
                        if img[y, x][3] == 0:
                            img[y, x] = [255, 255, 255, 0]

                # recolor background to black
                for x in range(0, width):
                    for y in range(0, height):
                        if inShape:
                            if img[y, x][3] == 0:
                                img[y, x] = [0, 255, 0, 0]
                        else:
                            if img[y, x][3] == 0:
                                img[y, x] = [0, 0, 0, 255]

                # save picture
                cv2.imwrite(str(picturePath) + str(filename), img)
                print("Finished!")

#----------------------------------------------------------------------------------------
# Shape Detection
filenames = os.listdir(picturePath)
sorted(filenames)

# iterate through all files
for count, filename in enumerate(sorted(filenames), start=1):
    # ignore hidden files
    if (str(filename)[0] != '.'):
        # ignore non png/jpg
        if (str(filename)[len(str(filename)) - 1] == 'g'):
            # get answers file
            if 'answers' in str(filename):

                print("Calculating " + str(filename) + " shapes...")

                #------------------------------------------------------------------------
                # Check old JSON first to get size - aka: current game level
                if os.path.exists('./pictureData.json'):
                    with open('./pictureData.json') as file:
                        oldData = json.load(file)
                    currentLevel = len(oldData) + 1
                else:
                    currentLevel = 1

                #------------------------------------------------------------------------
                # Create dictionary object to hold JSON
                data = {}
                data['level_' + str(currentLevel)] = {}

                #------------------------------------------------------------------------
                # resize image
                img = cv2.imread(str(picturePath) + str(filename))

                #------------------------------------------------------------------------
                # get image width and height
                height, width = img.shape[:2]

                if height > width:
                    resized = imutils.resize(img, width = 300)
                else:
                    resized = imutils.resize(img, height = 300)

                ratio = img.shape[0] / float(resized.shape[0])

                #------------------------------------------------------------------------
                # convert image to a more manageble color state
                gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

                #------------------------------------------------------------------------
                # compute contours
                contours = cv2.findContours(thresh.copy(), 
                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if imutils.is_cv2():
                    contours = contours[0]
                else:
                    contours = contours[1]

                #------------------------------------------------------------------------
                # shape and data computation
                currentShape = 0
                clusters = []

                for cont in contours:
                    moment = cv2.moments(cont)
                    cX = int((moment["m10"] / moment["m00"]) * ratio)
                    cY = int((moment["m01"] / moment["m00"]) * ratio)
                    shape = detect(cont)

                    cont = cont.astype("float") * ratio
                    cont = cont.astype("int")

                    # close fitting bounding box
                    if shape == "rectangle" or shape == "square" or shape == "pentagon":
                        rect = cv2.minAreaRect(cont)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        rectArea = rect[1][0] * rect[1][1]
                        shapeCenter = rect[0]

                    #close fitting bounding ellipse
                    elif shape == "circle" or shape == "ellipse":
                        ellipse = cv2.fitEllipse(cont)
                        shapeCenter = ellipse[0]
                    
                    #--------------------------------------------------------------------
                    # format data for JSON output
                    drawPoints = []
                    divisor = math.floor(len(cont) / 36)
                    index = 0
                    for c in cont:
                        if divisor > 0:
                            if index % divisor == 0:
                                value = []
                                drawPoints.append({
                                    'x': str(c[0][0]),
                                    'y': str(c[0][1])
                                })
                        else:
                            value = []
                            drawPoints.append({
                                'x': str(c[0][0]),
                                'y': str(c[0][1])
                            })  
                        
                    # JSON data for Rectangles
                    if shape == "rectangle" or shape == "square" or shape == "pentagon":
                        cornerPoints = []
                        for p in box:
                            cornerPoints.append({
                                'x': str(p[0]),
                                'y': str(p[1])
                            })

                        clusters.append({
                            'shape': str(shape),
                            #'center_x': str(int(shapeCenter[0])),
                            #'center_y': str(int(shapeCenter[1])), 
                            'width': str(int(rect[1][0])),
                            'height': str(int(rect[1][1])),
                            #'theta': str(int(rect[2])),
                            'points': cornerPoints,
                        })

                    # JSON data for ellipse
                    elif shape == "circle" or shape == "ellipse":
                        clusters.append({
                            'shape': str(shape),
                            'center_x': str(int(shapeCenter[0])),
                            'center_y': str(int(shapeCenter[1])), 
                            'width': str(int(ellipse[1][0])),
                            'height': str(int(ellipse[1][1])),
                            'theta': str(int(ellipse[2])),
                            'points': drawPoints
                        })

                    currentShape += 1

                # store data in JSON
                data['level_' + str(currentLevel)] = {
                    'clusters': clusters
                }

                #------------------------------------------------------------------------
                # store orientation based off of picture width and height
                if width > height:
                    data['level_' + str(currentLevel)]['orientation'] = 'horizontal'
                else:
                    data['level_' + str(currentLevel)]['orientation'] = 'vertical'

                #------------------------------------------------------------------------
                # write to JSON file
                # append to old JSON file
                if os.path.exists('./pictureData.json'):
                    with open('./pictureData.json') as file:
                        oldData = json.load(file)
                    oldData.update(data)

                    with open('./pictureData.json', 'w') as file:
                        json.dump(oldData, file)

                #------------------------------------------------------------------------
                # create new JSON file
                else:       
                    with open('./pictureData.json', 'w') as file:
                        json.dump(data, file)

                print("Finished!")