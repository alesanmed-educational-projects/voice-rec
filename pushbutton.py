import RPi.GPIO as GPIO
import time

import tools.speech as speech
import tools.record as record

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

prev_state = -1

while True:
	input_state = GPIO.input(23)
	
	if prev_state == -1:
		print("Empiesa")
		prev_state = input_state

	if prev_state == 0 and input_state == 1:
		record.run(10)
	if prev_state == 1 and input_state == 0:
		record.stop()
	
	prev_state = input_state
