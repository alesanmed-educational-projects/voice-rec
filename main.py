import time
import numpy as np
import sounddevice as sd
import tools.transcript as transcript
import pygame

from scipy.io.wavfile import write

import RPi.GPIO as GPIO

sd.default.device = 2
channels = sd.query_devices()[sd.default.device[0]]['max_input_channels']
fs = 48000
duration = 10  # seconds

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23, GPIO.FALLING)
GPIO.add_event_detect(24, GPIO.RISING)

pygame.mixer.init()
pygame.mixer.music.load('alert.wav')

while True:
    myrecording = np.zeros((0, channels))
    
    print("Listo")
    while not GPIO.event_detected(23):
        pass


    with sd.InputStream(channels=channels) as in_stream:
        while in_stream.read_available < 384:
                pass
        print("Comienza a hablar")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

        t = time.time()
        while time.time() - t <= duration and not GPIO.event_detected(24):
            myrecording = np.append(myrecording, in_stream.read(384)[0], axis=0)
        
        in_stream.stop()

    write('product.wav', fs, myrecording)
    print(transcript.run())
