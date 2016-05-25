import time
import numpy as np
import sounddevice as sd
import tools.transcript as transcript

from scipy.io.wavfile import write

import RPi.GPIO as GPIO

sd.default.device = 4
fs = 48000
duration = 10  # seconds

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(24, GPIO.RISING)

while True:
    myrecording = np.zeros((0, 2))
    
    GPIO.wait_for_edge(23, GPIO.FALLING)
    with sd.InputStream(channels=2) as in_stream:
        t = time.time()
        while time.time() - t <= duration and not GPIO.event_detected(24):
            myrecording = np.append(myrecording, in_stream.read(384)[0], axis=0)
        
    write('product.wav', fs, myrecording)
    print(transcript.run())
        