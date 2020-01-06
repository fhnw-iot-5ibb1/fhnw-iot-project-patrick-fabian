# -*- coding: utf-8 -*-

import time
import button
import thingSpeakService
from grove import grove_4_digit_display

class StateMachine():
    def __init__(self, button, display, sensor_service):
        self.button = button
        self.display = display
        self.sensor_service = sensor_service

        self.state = self.co2
        self.co2_threshold = 2000
        self.alarm_muted = False

    def run(self):
        self.state()

    def test_for_alarm(self):
        if self.sensor_service.get_co2() > self.co2_threshold:
            if not self.alarm_muted:
                self.alarm_muted = True
                self.state = self.alarm
        else:
            self.alarm_muted = False

    def cycle_display(self):
        states = [self.temp, self.hum, self.co2]
        if self.button.was_double_pressed():
            self.state = self.set_co2_threshold
        elif self.button.was_pressed():
            self.state = states[(states.index(self.state) + 1) % len(states)]
        self.button.reset()

    def temp(self):
        print("temp")

        # next state
        self.cycle_display()
        self.test_for_alarm()

    def hum(self):
        print("hum")

        # next state
        self.cycle_display()
        self.test_for_alarm()

    def co2(self):
        print("co2")

        # next state
        self.cycle_display()
        self.test_for_alarm()

    def set_co2_threshold(self):
        print("set co2 threshold")

        # next state
        self.state = self.co2

    def alarm(self):
        print("alarm")

        # next state
        if self.button.was_pressed():
            self.state = self.co2
        if self.sensor_service.get_co2() < self.co2_threshold:
            self.alarm_muted = True
            self.state = self.co2

class Dummy():
    def __init__(self):
        self.pressed = False
        self.double_pressed = False
        self.co2 = 1800

    def was_double_pressed(self):
        state = self.double_pressed
        self.double_pressed = False
        return state

    def was_pressed(self):
        state = self.pressed
        self.pressed = False
        return state
        
    def reset(self):
        pass

    def get_co2(self):
        return self.co2

disp = grove_4_digit_display.Grove(16, 17, brightness=grove_4_digit_display.BRIGHT_HIGHEST)
button = button.Button(pin=5, double_press_threshold=0.4)

dummy = Dummy()
SM = StateMachine(button=dummy, display=dummy, sensor_service=dummy)
while True:
    SM.run()
    time.sleep(0.5)
    inp = int(input("1 => press; 2 => double_pressed: "))

    if inp == 2:
        dummy.double_pressed = True
    elif inp == 1:
        dummy.pressed = True
    elif inp > 100:
        dummy.co2 = inp


