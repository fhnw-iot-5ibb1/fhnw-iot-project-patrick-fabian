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
        
        self.i = 0

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
        
    def show_text(self, text):
        self.i = (self.i + 1) % (len(text) + 4)
        self.display.show(f"    {text}    "[self.i:self.i+4])

    def temp(self):
        t = self.sensor_service.get_temp()
        print(f"temp: {t}")
        self.display.show(f"{str(round(t))[-2:]}*C")

        # next state
        self.cycle_display()
        self.test_for_alarm()

    def hum(self):
        h = self.sensor_service.get_hum()
        print(f"hum: {h}")
        self.display.show(f"h {str(round(h))[-2:]}")

        # next state
        self.cycle_display()
        self.test_for_alarm()

    def co2(self):
        co2 = self.sensor_service.get_co2()
        print(f"co2: {co2}")
        self.display.show(f"{co2:4}")

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
service = thingSpeakService.ThingSpeakService()

dummy = Dummy()
SM = StateMachine(button=button, display=disp, sensor_service=service)
while True:
    SM.run()
