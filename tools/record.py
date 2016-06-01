from ctypes import *
from contextlib import contextmanager

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

import json
import RPi.GPIO as GPIO
import os
import pyaudio
import pygame
import time
import tools.transcript as transcript
import wave
import tools.text2int as text2int
import sys
 
def run():
    FILEPATH = 'products.json'
    FORMAT = pyaudio.paInt16
    RATE = 44100
    CHUNK = 9216
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "product.wav"
     
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.FALLING)
    GPIO.add_event_detect(24, GPIO.RISING)
    
    pygame.mixer.init()
    pygame.mixer.music.load('alert.wav')   
    
    with noalsaerr():
        audio = pyaudio.PyAudio()

    for i in range(audio.get_device_count()):
        device = audio.get_device_info_by_index(i)

        if "usb" in device['name'].lower():
            INDEX = i
            CHANNELS = device['maxInputChannels']
            print("Device: {0}".format(INDEX))
            break
    while True:
        print("Listo")
        while not GPIO.event_detected(23):
            pass
        
        pygame.mixer.music.play() 
        while pygame.mixer.music.get_busy() == True:
                continue
            
        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
        t = time.time()
        print("Comienza a hablar")
        frames = []
         
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if GPIO.event_detected(24):
                if time.time() - t < 1:
                    print("Parando")
                    audio.terminate()
                    return -1
                break
            try:
                data = stream.read(CHUNK)
            except:
                pass
            frames.append(data)
        print("finished recording")
         
        # stop Recording
        stream.stop_stream()
        stream.close()
         
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        
        product = transcript.run()
        
        if product is not None:
            product = product.split()
            
            try:
                product_index = product.index('product')
            except:
                return
            
            quantity_present = True
            try:
                quantity_index = product.index('amount')
            except:
                quantity = 1
                quantity_index = sys.maxsize
                quantity_present = False
            
            if product_index < quantity_index:
                product_name =" ".join(product[product_index + 1:quantity_index])
                if quantity_present:
                    quantity = text2int.run(" ".join(product[quantity_index + 1:]))
            else:
                product_name = product[product_index + 1:]
                quantity = text2int.run(" ".join(product[quantity_index + 1:product_index]))
            
            print(product_name)
            print(quantity)
            
            if os.path.exists(FILEPATH):
                with open(FILEPATH, 'r') as outfile:
                    products = json.load(outfile)['products']
            else:
                products = {}
                
            products[product_name] = quantity
        
            with open(FILEPATH, 'w') as outfile:
                json.dump({'products': products }, outfile)
            
if __name__ == "__main__":
    run()
