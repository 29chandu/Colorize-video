# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 07:21:59 2018

@author: fury29
"""

import Algorithmia
import PIL.Image
import io
from tkinter import filedialog
from tkinter import *
import os

def colorizeImage(imageFullPath, imageName):

    print('    Uploading...')
    client.file("data://.my/inputs/" + imageName).putFile(imageFullPath)

    input = {
	  "image": "data://.my/inputs/" + imageName,
	  "location": "data://.my/outputs/" + imageName
      }
    algo = client.algo('deeplearning/ColorfulImageColorization/1.1.13')
    print('    Converting...')
    algo.pipe(input).result

    print('    Downloading...')
    imageBytes = client.file("data://.my/outputs/" + imageName).getBytes()
    image = PIL.Image.open(io.BytesIO(imageBytes))
    image.save(root.outputDirectory + '\\' + imageName.split('.')[0] + '.png')
    print()

root = Tk()
root.outputDirectory = filedialog.askdirectory(initialdir = os.getcwd(), title = "Select directory to save converted images").replace("/",'\\') + '\\' + "Converted images"
root.destroy()

frameNumber = input('Enter the frame number to start conversion from: ')

f = open('api_key.txt')
apiKey = f.readline()
client = Algorithmia.client(apiKey[:-1])

inputDir = client.dir("data://.my/inputs")
if not inputDir.exists():
    inputDir.create()

outputDir = client.dir("data://.my/outputs")
if not outputDir.exists():
    outputDir.create()


skippedFrames = []
for imageName in os.listdir('frames'):
    if imageName.endswith('.png') and int(imageName[6:-4]) >= int(frameNumber):    
        imageFullPath = 'frames' + '\\' + imageName
        print(imageName)
        try:
            colorizeImage(imageFullPath, imageName)
        except:
            print()
            print(imageName + ' is missing')
            skippedFrames.append((imageFullPath, imageName));
            continue
    else:
        continue
    
print()
print('Working on skipped frames')
for i in skippedFrames:
    imageFullPath, imageName = i
    print(imageName)
    try:
        colorizeImage(imageFullPath, imageName)
    except:
        print()
        print(imageName + ' is missing from skipped frames')
        continue