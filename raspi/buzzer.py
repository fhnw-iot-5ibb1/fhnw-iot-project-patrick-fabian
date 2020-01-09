import pigpio

class Buzzer:

    def __init__(self):
        self.buzzerPin = 12
        self.gpio = pigpio.pi()

    def turn_on(self):
        self.gpio.write(self.buzzerPin, 1)

    def turn_off(self):
        self.gpio.write(self.buzzerPin, 0)