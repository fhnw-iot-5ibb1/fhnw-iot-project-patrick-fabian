
# servo_test.py - Test functionality of SG90 Micro Servo
#
# Written By: David Such

import pigpio

servo_pin = 18
pulsewidth = 1500     # Should be the centre for a SG90

# setup
pi = pigpio.pi()
pi.set_servo_pulsewidth(servo_pin, pulsewidth)

try:
    while True:
        pulsewidth = int(input("Enter Duty Cycle (Left = 500 to Right = 2500):"))
        pi.set_servo_pulsewidth(servo_pin, pulsewidth)
            
except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
finally:
    print("Cleaning up GPIO...")
    pi.stop()
