# -*- coding: utf-8 -*-

from time import time
import button
import thingSpeakService
import buzzer
import servo
import rotation
import led
from grove import grove_4_digit_display

THING_SPEAK_CHANNEL = 935198
THING_SPEAK_API_KEY = '81SYGRV7PHQU25C8'

class StateMachine():
    def __init__(self, button, display, sensor_service, buzzer, rotation_sensor, servo, led):
        self.button = button
        self.display = display
        self.sensor_service = sensor_service
        self.buzzer = buzzer
        self.rotation_sensor = rotation_sensor
        self.servo = servo
        self.led = led

        self.state = self.co2
        self.old_state = self.state
        self.state_change_time = 0
        self.cycle_display_delay = 5
        self.co2_threshold = 2000
        self.alarm_muted = False
        
        self.i = 0
        self.last_rotation = 0
        self.last_rotation_time = 0
        self.rotation_delay = 5

    def run(self):
        if self.state != self.old_state:
          self.old_state = self.state
          self.state_change_time = time()
        
        # display co2 measurement with servo
        co2 = self.sensor_service.get_co2()
        self.servo.set_pulsewidth(co2)
        
        # show with led if over threshold
        if co2 > self.co2_threshold:
          self.led.turn_on()
        else:
          self.led.turn_off()
        
        # run state
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
        elif self.button.was_pressed() or time() - self.state_change_time > self.cycle_display_delay:
            self.state = states[(states.index(self.state) + 1) % len(states)]
        self.button.reset()
        
    def show_text(self, text):
        self.i = (self.i + 1) % (len(text) + 4)
        self.display.show(f"    {text}    "[self.i:self.i+4])
        
    def show_co2(self, co2=None):
        if co2 is None:
          co2 = self.sensor_service.get_co2()
        # print(f"co2: {co2}")
        co2str = f"{co2:4}"
        self.display.show(co2str[-4:])

    def temp(self):
        t = self.sensor_service.get_temp()
        # print(f"temp: {t}")
        self.display.show(f"{str(round(t))[-2:]:2}*C")

        # next state
        self.cycle_display()
        self.test_for_alarm()

    def hum(self):
        h = self.sensor_service.get_hum()
        # print(f"hum: {h}")
        self.display.show(f"h {str(round(h))[-2:]:2}")

        # next state
        self.cycle_display()
        self.test_for_alarm()

    def co2(self):
        self.show_co2()

        # next state
        self.cycle_display()
        self.test_for_alarm()

    def set_co2_threshold(self):
        rotation_co2 = round(self.rotation_sensor.get_translated_value() / 50) * 50
        current_time = time()
        if rotation_co2 != self.last_rotation:
          self.last_rotation = rotation_co2
          self.last_rotation_time = current_time
        
        self.show_co2(rotation_co2)
        self.co2_threshold = rotation_co2

        # next state
        if current_time - self.last_rotation_time > self.rotation_delay or self.button.was_pressed():
          self.state = self.co2
          self.last_rotation = -1

    def alarm(self):
        self.show_co2()
        self.buzzer.turn_on()

        # next state
        if self.button.was_pressed():
            self.state = self.co2
            self.buzzer.turn_off()
        if self.sensor_service.get_co2() < self.co2_threshold:
            self.alarm_muted = True
            self.state = self.co2
            self.buzzer.turn_off()

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
        
    def get(self):
        return 1500
        
    def turn_on(self):
        print("UUUUIIIIIIIUUUUUUIIII")
    
    def turn_off(self):
        pass

    def get_co2(self):
        return self.co2

disp = grove_4_digit_display.Grove(16, 17, brightness=grove_4_digit_display.BRIGHT_HIGHEST)
button = button.Button(pin=5, double_press_threshold=0.4)
service = thingSpeakService.ThingSpeakService(channel=THING_SPEAK_CHANNEL, api_key=THING_SPEAK_API_KEY)
buzzer = buzzer.Buzzer(12)
servo = servo.Servo(pin=18, min=0, max=5000)
rot_sensor = rotation.RotationSensor(pin=4, min=0, max=5000)
led_actuator = led.Led(6)

dummy = Dummy()
SM = StateMachine(button=button, display=disp, sensor_service=service, buzzer=buzzer, rotation_sensor=rot_sensor, servo=servo, led=led_actuator)
try:
  while True:
      SM.run()
except KeyboardInterrupt:
  disp.show("    ")
