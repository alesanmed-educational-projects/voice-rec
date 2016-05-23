import sounddevice as sd
from scipy.io.wavfile import write

def run(duration):
	fs = 48000
	duration = duration  # seconds
	myrecording = sd.rec(duration * fs, samplerate=fs, channels=2, blocking=True);

	write('product.wav', fs, myrecording)
