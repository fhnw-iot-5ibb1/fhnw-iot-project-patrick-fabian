import Utils
from grove.grove_rotary_angle_sensor import GroveRotaryAngleSensor

class RotationSensor:

    def __init__(self, pin, min, max):
        self.rot_pin = pin
        self.min = min
        self.max = max
        self.sensor = GroveRotaryAngleSensor(self.rot_pin)

    def get_translated_value(self):
        return Utils.translate(self.sensor.value, 0, 999, self.min, self.max)

    def get_raw_value(self):
        return self.sensor.value