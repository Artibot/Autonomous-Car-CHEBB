import sys
sys.path.append('../Dependencies')
sys.path.append('./Predict')
import pygame

from steering import Steering
from motor import Motor
from time import sleep
from predict import Predict



#import config

pygame.init()
pygame.joystick.init()

prediction = Predict("VGG16_RealImg_Adagrad_150x2.EP74-0.62-0.04.h5", 150, 150)

DrivingMotor = Motor(388)

SteeringWheel = Steering(298)
SteeringWheel.Run()

axis = 0
stop = 0
autoMode = 0
joystick_pressed = 0	


steer_enhancer = 2
	
while stop == 0:
	pygame.event.get()

	if pygame.joystick.get_count() == 1: # 1
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
			try:
				axis = prediction.predict_angle(steer_enhancer)
				
			except:
				axis = 0
			print(axis)
			SteeringWheel.set_angle(axis) # Sets the steering angle to the wheels
			DrivingMotor.Run(1)
		else:
			#manual override
			axis = Joystick.get_axis(0)
			start = Joystick.get_button(7)
			if start:
				SteeringWheel.set_angle(axis)
			DrivingMotor.Run(start)
		
		del Joystick
	sleep(0.001)

		
		

SteeringWheel.Stop()
del SteeringWheel
del DrivingMotor

