import pigpio
import Utils

class Servo:

    def __init__(self):
        self.servo_pin = 18
        self.gpio = pigpio.pi()
        self.gpio.set_servo_pulsewidth(self.servo_pin, 1500)

    def set_pulsewidth(self, pulsewidth):
        self.gpio.set_servo_pulsewidth(self.servo_pin, Utils.translate(pulsewidth, 0, 5000, 500, 2350))
