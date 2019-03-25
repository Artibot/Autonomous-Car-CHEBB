from time import sleep

class servo:

    pin = 0
    dir = ''

    def __init__(self, pin, dir = '/sys/class/gpio/'):
        self.pin = pin
        self.__export_pin(dir)

    def __export_pin(self, dir):
        f = open(dir + "export", "w+")
        f.write("%d", self.pin)
        f.close()
        self.dir = dir + "gpio" + pin + "/"
        f = open(self.dir + "direction", "w+")
        f.write("out")
        f.close()

    def __set__value(self, value):
        f = open(self.dir + "value", "w+")
        f.write(value)
        f.close()

    def set__pwm(self, ratio):
        high_time = 0.002
        self.__set__value(1)
        sleep(high_time)
        self.__set__value(0)
        sleep(0.05-high_time)


motor = servo(388)
while True:
    motor.set__pwm(1)

