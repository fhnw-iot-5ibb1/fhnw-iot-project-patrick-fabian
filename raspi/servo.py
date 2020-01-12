import pigpio
import Utils

class Servo:

    def __init__(self, pin, min, max):
        self.servo_pin = pin
        self.min = min
        self.max = max
        self.gpio = pigpio.pi()
        self.gpio.set_servo_pulsewidth(self.servo_pin, 1500)

    def set_pulsewidth(self, pulsewidth):
        self.gpio.set_servo_pulsewidth(self.servo_pin, Utils.translate(pulsewidth, self.min, self.max, 500, 2350))
