from twisted.internet import reactor 

from sysfs.gpio import GPIOController 
from sysfs.gpio import GPIOinDireection as Direction
from sysfs.gpio import GPIOinEdge as Edge

import time

GPIOController().available_pins =[388]
print "started"

led_pin = GPIOController().alloc_pin(388, Direction.OUTPUT)

while 1:
	led_pin.set() #Sets pin to high
	time.sleep(0.3)
	led_pin.reset() # Sets pin to low
	time.sleep(0.3)