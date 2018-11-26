How To Use PocketStarScript.py

Steps:
1.	Place PocketStarScript.py file with all of the picture folders.

	For Example:
		./dir ls:
			./pictureSet1 			<-- this is a folder holding pictures and solutions
			./pictureSet2			<-- this is a folder holding pictures and solutions
			./pictureSet3			<-- this is a folder holding pictures and solutions
			readme.txt
			PocketStarScript.py 	<-- the python script

2. 	Open up terminal/cmd and make sure you have python installed along
	with all of the libraries used in this script...
		import numpy
		import imutils
		import random
		import math
		import json
		import cv2
		import sys
		import os

3. 	Inside the terminal, naviagte to the directory that contains all
	of the pictures and the python script listed above

4.	Run the python script by typing the command listed below
		python PocketStarScript.py {directoryName}

	Replace {directoryName} with the name of the folder of pictures
	that you want to run the python script on. For example...
		python PocketStarScript.py pictureSet1

5. 	After the script has finished running, you should have a file
	called pictureData.json
	This file will contain all of the json data for the solutions

6.	You can run this script on multiple folders, and the JSON data
	will be appended to the preexisting pictureData.json file. If this
	file does not exist, it will be created. If it does exist, the 
	data will be added to it.