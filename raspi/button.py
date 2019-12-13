# -*- coding: utf-8 -*-

from grove.grove_button import GroveButton
import time
import sys

class Button():
    def __init__(self, pin, double_press_threshold):
        """
        @param pin [int] Raspberry pi BCM pin
        @param double_press_threshold [float] max delay in seconds between button pressed that count as a double press
        """
        self.pin = pin
        self.double_press_threshold = double_press_threshold

        self.pressed = False
        self.double_pressed = False
        self.last_event = 0

        self.button = GroveButton(pin)
        self.button.on_press = self._on_press

    def _on_press(self, t):
        current_time = time.time()
        delta = current_time - self.last_event
        self.last_event = current_time
        self.pressed = True
        if delta < self.double_press_threshold:
            self.double_pressed = True

    def was_pressed(self):
        state = self.pressed
        self.pressed = False
        return state

    def was_double_pressed(self):
        state = self.double_pressed
        self.double_pressed = False
        return state

    def reset(self):
        self.pressed = False
        self.double_pressed = False

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Argument Button Pin required")
  else:
    button = Button(int(sys.argv[1]), 0.4)
    while(True):
      if button.was_double_pressed():
        print("double-press")
      elif button.was_pressed():
        print("pressed")
      button.reset()
      time.sleep(0.001)
