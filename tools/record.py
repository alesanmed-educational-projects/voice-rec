import sounddevice as sd
from scipy.io.wavfile import write

def run(out):
	print("Graba")
	sd.default.device = 2;
	fs = 48000;
	duration = 10; # seconds
	sd.rec(duration * fs, samplerate=fs, channels=1, out=out);

def stop():
	print("Para")
	sd.stop();
