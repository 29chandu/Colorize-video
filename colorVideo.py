# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 16:29:56 2018

@author: fury29
"""

import Algorithmia
import PIL.Image
import io
from tkinter import filedialog
from tkinter import *
import os
import cv2


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
# Chose the directory from which images need to be converted
#root.videoDirectoryToBeConverted =  filedialog.askdirectory(initialdir = os.getcwd(), title = "Select directory of images to be converted")
unconvertedVideo = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select video to be converted")
root.outputDirectory = filedialog.askdirectory(initialdir = os.getcwd(), title = "Select directory to save converted images").replace("/",'\\') + '\\' + "Converted images"
root.destroy()

if not os.path.isdir(root.outputDirectory):
    os.mkdir(root.outputDirectory)
    
frames = os.getcwd() + '\\frames'
if not os.path.isdir(frames):
    os.mkdir(frames)
    
vidcap = cv2.VideoCapture(unconvertedVideo)
success,image = vidcap.read()
fps = vidcap.get(cv2.CAP_PROP_FPS)
print('Frames per second value = ', str(fps), end='')
frameCount = int(input('Number of frames need to be extracted per second: '))
print()

if frameCount <= fps:    
    extractFrame = fps//frameCount
else:
    extractFrame = fps

count = 0
imageNumber = 1
while success:
    if count%extractFrame == 0:
        cv2.imwrite( frames + '\\' + "frame-%05d.png" % imageNumber, image)     # save frame as JPEG file      
        imageNumber += 1
    success,image = vidcap.read()
    #print('Read a new frame: ', success)
    count += 1
    
    
f = open('api_key.txt')
apiKey = f.readline()
client = Algorithmia.client(apiKey[:-1])

inputDir = client.dir("data://.my/inputs")
if not inputDir.exists():
    inputDir.create()

outputDir = client.dir("data://.my/outputs")
if not outputDir.exists():
    outputDir.create()

for imageName in os.listdir('frames'):
    if imageName.endswith('.png'):    
        imageFullPath = 'frames' + '\\' + imageName
        print(imageName)
        try:
            colorizeImage(imageFullPath, imageName)
        except:
            print()
            print(imageName + ' is missing')
            break
    else:
        continue
    
force = True
if outputDir.exists():
    outputDir.delete(force)
    
if inputDir.exists():
    inputDir.delete(force)

print('Converion successful')
