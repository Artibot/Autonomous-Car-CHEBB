import sys
sys.path.append('../Dependencies')
sys.path.append('./Predict')
import pygame

from steering import Steering
from motor import Motor
from time import sleep
import numpy as np
import load_graph 

import cv2
import time
from keras.models import load_model
from keras import backend as k
import imageCapture as iCap
#import config

pygame.init()
pygame.joystick.init()

DrivingMotor = Motor(388)

SteeringWheel = Steering(298)
SteeringWheel.Run()

# open cam
#args = iCap.parse_args()

#cap = iCap.open_cam_usb(args.video_dev, args.image_width, args.image_height)
#iCap.open_window(args.image_width, args.image_height)
#iCap.read_cam(cap)
#if not cap.isOpened():

#	sys.exit('Failed to open camera!')

#abc, vid = cap.read()


#model_name = "VGG16_Steering_Weights.EP75-1.09-0.09.h5" # Name of the model that is going to be used for predicting images

# Create an object from MyModel class of #load_graph.py filew
#model1 = load_graph.MyModel(128, 128, model_name) 
autoMode = 0

joystick_pressed = 0		

while 1:
	pygame.event.get()


	if pygame.joystick.get_count() == 1:
		Joystick = pygame.joystick.Joystick(0)
		Joystick.init()
		if Joystick.get_button(6) == 1 and joystick_pressed == 0:
			autoMode = 1 - autoMode
			joystick_pressed = 1
		
		if Joystick.get_button(6) == 0:
			joystick_pressed = 0
			

		stop = Joystick.get_button(0)
		if autoMode:
			#auto predict
			#steering = model1.predictImage(np.array(vid), False) # Get steering angle from camera
			#steering_norm = steering / 5 # Normalizing the steering angle between -1 and 1

			SteeringWheel.set_angle(1) # Sets the steering angle to the wheels
			
		else:
			#manual override
			axis = Joystick.get_axis(0)
			start = Joystick.get_button(7)
			if start:
				SteeringWheel.set_angle(axis)
			DrivingMotor.Run(start)
		
		if stop: 
			break
		del Joystick
	sleep(0.001)
	
		
		

SteeringWheel.Stop()
del SteeringWheel

