#!/usr/bin/env python
import pigpio
from grove import grove_4_digit_display, grove_led, grove_slide_potentiometer

servo_pin = 18
buzzer_pin = 12
button_pin = A2

disp = grove_4_digit_display.Grove(16,17, brightness=grove_4_digit_display.BRIGHT_HIGHEST)
poti = grove_slide_potentiometer.Grove(A0)
led = grove_led.Grove(5)


