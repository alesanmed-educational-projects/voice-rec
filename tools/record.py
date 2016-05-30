import RPi.GPIO as GPIO
import pyaudio
import pygame
import time
import wave
 
def record():
    INDEX = 0
    FORMAT = pyaudio.paInt16
    RATE = 44100
    CHUNK = 1024
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
    while not GPIO.event_detected(23):
        pass
    
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    
    pygame.mixer.music.play() 
    while pygame.mixer.music.get_busy() == True:
            continue
    
    t = time.time()
    print("Comienza a hablar")
    frames = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        if GPIO.event_detected(24):
            if time.time() - t < 1:
                return -1
            break
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
     
     
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