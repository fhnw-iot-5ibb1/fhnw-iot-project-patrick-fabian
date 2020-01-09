
import time
from grove.grove_rotary_angle_sensor import GroveRotaryAngleSensor

# connect to alalog pin 4(slot A4)
PIN = 4
sensor = GroveRotaryAngleSensor(PIN)
while True:
    print(f'Rotary Value: {sensor.value}')
    time.sleep(.2)
