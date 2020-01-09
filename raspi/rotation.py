import Utils
from grove.grove_rotary_angle_sensor import GroveRotaryAngleSensor

class Servo:

    def __init__(self):
        self.rot_pin = 4
        self.sensor = GroveRotaryAngleSensor(self.rot_pin)

    def get_raw_value(self):
        return Utils.translate(self.sensor.value, 0, 999, 0, 5000)

    def get_translated_value(self)
        return self.sensor.value