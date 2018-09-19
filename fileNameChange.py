import os
import math

path = os.getcwd()
filenames = os.listdir(path)

sorted(filenames)

counter = 0
for count, filename in enumerate(sorted(filenames), start=1): # iterate through all files, alphabetically
    if (str(filename)[0] != '.'): # ignore hidden files
        if (str(filename)[len(str(filename)) - 1] == 'g'): #ignore non png/jpg
            if ('original' in str(filename)): # original
                os.rename(filename, str(math.floor(counter / 3)) + '_original.jpg')
                counter += 1
            elif ('edited' in str(filename)): # edited
                os.rename(filename, str(math.floor(counter / 3)) + '_edited.jpg')
                counter += 1
            elif ('answers' in str(filename)): # answers
                os.rename(filename, str(math.floor(counter / 3)) + '_answers.png')
                counter += 1
