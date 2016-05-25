import numpy as np
import RPi.GPIO as GPIO
import time

import tools.transcript as transcript
import tools.record as record

from scipy.io.wavfile import write

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

out = np.empty((48000*10, 1))

print("Empieza")
while True:
	GPIO.wait_for_edge(23, GPIO.FALLING)
	record.run(out)
	GPIO.wait_for_edge(23, GPIO.RISING)
	record.stop()
	write("product.wav", 48000, out)
