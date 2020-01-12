import pigpio

class Buzzer:

    def __init__(self, pin):
        self.buzzerPin = pin
        self.gpio = pigpio.pi()

    def turn_on(self):
        self.gpio.write(self.buzzerPin, 1)

    def turn_off(self):
        self.gpio.write(self.buzzerPin, 0)