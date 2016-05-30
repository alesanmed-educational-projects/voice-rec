import json
import RPi.GPIO as GPIO
import os
import pyaudio
import pygame
import time
import transcript
import wave
 
def record():
    FILEPATH = 'products.json'
    INDEX = 2
    FORMAT = pyaudio.paInt16
    RATE = 44100
    CHUNK = 8192
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "product.wav"
     
    audio = pyaudio.PyAudio()
    
    CHANNELS = audio.get_device_info_by_index(INDEX)['maxInputChannels']
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.FALLING)
    GPIO.add_event_detect(24, GPIO.RISING)
    
    pygame.mixer.init()
    pygame.mixer.music.load('alert.wav')
    print("Listo")
    
    while True:
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
                    return -1
                break
            try:
                data = stream.read(CHUNK)
            except:
                pass
            frames.append(data)
        print("finished recording")
        print("Chunk: {0}".format(CHUNK)) 
         
        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
         
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        
        product = transcript.run()
    
        if os.path.exists(FILEPATH):
            with open(FILEPATH, 'r') as outfile:
                products = json.load(outfile)['products']
        else:
            products = []
            
        if product is not None:
            products.append(product)
    
        with open(FILEPATH, 'w') as outfile:
            json.dump({'products': products }, outfile)
            
if __name__ == "__main__":
    record()