import sys
sys.path.append('../Dependencies')
sys.path.append('./Predict')
import pygame

from steering import Steering
from motor import Motor
from time import sleep
from capture import Capture



#import config

pygame.init()
pygame.joystick.init()


DrivingMotor = Motor(388)

SteeringWheel = Steering(298)
SteeringWheel.Run()

axis = 0
stop = 0
autoMode = 1
joystick_pressed = 0	
i = 0

steer_enhancer = 2
cap = Capture()
	
while stop == 0:
	pygame.event.get()

	if pygame.joystick.get_count() == 1: # 1
		Joystick = pygame.joystick.Joystick(0)
		Joystick.init()
		
		if Joystick.get_button(6) == 0:
			joystick_pressed = 0
			
		autoMode = Joystick.get_button(6)
		stop = Joystick.get_button(0)
			#manual override
		axis = Joystick.get_axis(0)
		start = Joystick.get_button(7)
		if start:
			SteeringWheel.set_angle(axis)
			if autoMode:
				i = i + 1
				if i % 10 == 0:
					 cap.capture(angle = axis*5, fram = int(i/10))
		DrivingMotor.Run(start)
		
		del Joystick
	sleep(0.001)

		
		

SteeringWheel.Stop()
del SteeringWheel
del DrivingMotor

