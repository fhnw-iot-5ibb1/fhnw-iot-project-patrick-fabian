import time
import subprocess
from grove import grove_4_digit_display

ip = subprocess.check_output("hostname -I | cut -d\" \" -f1", shell=True)
ip = "   IP " + ip.decode("utf-8")

disp = grove_4_digit_display.Grove(16, 17, brightness=grove_4_digit_display.BRIGHT_HIGHEST)

while True:
	for i in range(len(ip)):
		disp.show(ip[i:i+4])
		time.sleep(0.2)

