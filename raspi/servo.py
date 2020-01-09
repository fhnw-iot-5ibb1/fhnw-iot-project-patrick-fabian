import pigpio

class Servo:

    def __init__(self):
        self.servo_pin = 18
        self.gpio = pigpio.pi()
        self.gpio.set_servo_pulsewidth(self.servo_pin, 1500)

    def set_pulsewidth(self, pulsewidth):
        self.pgio.set_servo_pulsewidth(self.servo_pin, self.translate(pulsewidth, 0, 5000, 500, 2450))

    # credits go to stackoverflow (https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another)
    def translate(self, value, fromMin, fromMax, toMin, toMax):
        # Figure out how 'wide' each range is
        fromSpan = fromMax - fromMin
        toSpan = toMax - toMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - fromMin) / float(fromSpan)

        # Convert the 0-1 range into a value in the right range.
        return toMin + (valueScaled * toSpan)