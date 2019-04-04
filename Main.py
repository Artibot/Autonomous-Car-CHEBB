import sys
	sys.path.append('../Dependencies')
import pygame
from steering import Steering

pygame.init()
pygame.joystick.init()

Joystick = pygame.joystick.Joystick(0)
Joystick.init()

SteeringWheel = Steering(388)
SteeringWheel.Run()

while 1:
	autoMode = Joystick.get_button(6)
	if autoMode:
		#auto predict
		
	else:
		#manual override
		axis = Joystick.get_axis(0)
		start = Joystick.get_button(7)
		if start:
			SteeringWheel.set_angle(axis)
		sleep(0.0001)
		stop = Joystick.get_button(0)
		if stop:
			break
			
SteeringWheel.Stop()
del SteeringWheel
del Joystick
