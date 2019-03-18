import numpy as np
import os
import sys
import glob
import argparse
import random
from PIL import Image


filepath = "frame_000030_st_0,3026959_th_0,3.jpg"

path = 'C:\\Users\\Chrisander\\Desktop\\untitled\\data\\'
image = Image.open(filepath)
x_trainTest = np.array(image)
#print("X_train")
#print(x_trainTest)
#basename = "frame_000271_st_-0,2323141_th_0,3"
#basename = "frame_000271_st_-0.2323141_th_0.3"
#
# print("basename")
# print(filepath)
#f = basename[:-4]
#f = basename
# f = filepath[:-4]
# f = f.replace(',', '.')
# print("f[:-4]")
# print(f)
# f = f.split('_')
# print("'_'")
# print(f)
#
# steering = float(f[3])
# throttle = float(f[5])
#
# print("steering")
# print(steering)
#
# print("throttle")
# print(throttle)
#
# data = {'steering':steering, 'throttle':throttle }
# print("data")
# print(data)
#
# steering2 = data["steering"]
# throttle2 = data["throttle"]
#
# print("steering2")
# print(steering2)
#
# print("throttle2")
# print(throttle2)
# controls = steering2
# y_train = np.array(controls)
# print("heaheahasadasd", (y_train))

# def hei(x_train, y_train):
#     a = x_train
#     b = y_train
#     yield a, b
#
# print(hei(x_trainTest, y_train))

#x_images = np.array()
#y_images = np.array()
x_images = []
y_labels = []
i = 0

def createGenerator():
    for name in glob.glob1(path, '*jpg'):
        path2 = os.path.join(path, name)
        xImage = Image.open(path2)
        xImage = np.array(xImage)
        steering = name[:-4]
        print(steering)
        steering = steering.replace(',', '.')
        print(steering)
        steering = steering.split('_')
        print(steering)
        steering = float(steering[3])
        print(steering)
        x_images.append(xImage)
        y_labels.append(steering)
        #x_images[i] = [xImage]
        #y_images[i] = [steering]
        #length = len(x_images)
        #print(length)
        #print(y_images)
        #print(y_labels)

    x_train = np.array(x_images)
    y_train = np.array(y_labels)
    yield x_train, y_train

myGenerator = createGenerator()

for i in myGenerator:
    print(i)


x = np.array(([1,2],[3,4]))

print('Array x:')
print(x)
print('\n')
y = np.expand_dims(x, axis = 0)

print('Array y:')
print(y)
print('\n')
