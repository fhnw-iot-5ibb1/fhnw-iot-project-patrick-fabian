import pigpio

class Led:

    def __init__(self):
        self.ledPin = 6
        self.gpio = pigpio.pi()

    def turn_on(self):
        self.gpio.write(self.ledPin, 1)

    def turn_off(self):
        self.gpio.write(self.ledPin, 0)