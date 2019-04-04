import sys
sys.path.append('../Dependencies')
import pygame
from steering import Steering
from time import sleep

pygame.init()
pygame.joystick.init()



SteeringWheel = Steering(388)
SteeringWheel.Run()

while 1:
	pygame.event.get()		

	if pygame.joystick.get_count() == 1:
		Joystick = pygame.joystick.Joystick(0)
		Joystick.init()
		autoMode = Joystick.get_button(6)
		if autoMode:
			#auto predict
			break
		else:
			#manual override
			axis = Joystick.get_axis(0)
			start = Joystick.get_button(7)
			if start:
				SteeringWheel.set_angle(axis)
		
			stop = Joystick.get_button(0)
			if stop:
				break
		sleep(0.001)
		del Joystick
		
SteeringWheel.Stop()
del SteeringWheel

