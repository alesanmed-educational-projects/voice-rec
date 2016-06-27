import time
import serial

def run(bluetooth, q=None):
	command_start = '['
	command_end = ']'

	command_pending = 0;
	command = "";
	bluetooth.flushInput();
	print("Bluetooth over Serial Port [OK]")
	while 1:
		bytesToRead = bluetooth.inWaiting()
		if bytesToRead > 0:
			char = bluetooth.read(1).decode('utf-8')
			if command_pending == 0 and char == command_start:
				command_pending = 1
			elif command_pending == 0 and char != command_start:
				continue
			elif command_pending == 1 and char == command_end:
				if q is not None:
					q.put(command)
				command = ""
				command_pending = 0
			elif command_pending == 1 and char != command_end:
				command += char

if __name__ == "__main__":
	bluetooth = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

	run(bluetooth)