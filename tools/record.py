import sounddevice as sd
from scipy.io.wavfile import write

def run(duration):
	sd.default.device = 2;
	fs = 48000;
	duration = duration; # seconds
	myrecording = sd.rec(duration * fs, samplerate=fs, channels=1);

	write('product.wav', fs, myrecording);

def stop():
	sd.stop();
