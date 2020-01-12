import pigpio

class Led:

    def __init__(self, pin):
        self.ledPin = pin
        self.gpio = pigpio.pi()

    def turn_on(self):
        self.gpio.write(self.ledPin, 1)

    def turn_off(self):
        self.gpio.write(self.ledPin, 0)