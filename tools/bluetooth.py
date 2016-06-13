import time
import serial

def run(q):
	ser = serial.Serial(
		port='/dev/ttyAMA0',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
	      )

	command_start = '['
	command_end = ']'

	command_pending = 0;
	command = "";
	ser.flushInput();
	while 1:
		bytesToRead = ser.inWaiting()
		if bytesToRead > 0:
			char = ser.read(1).decode('utf-8')
			if command_pending == 0 and char == '[':
				command_pending == 1
			elif command_pending == 0 and char != '[':
				continue
			elif command_pending == 1 and char == ']':
				q.put(command)
				command = ""
				command_pending = 0
			elif command_pending == 1 and char != ']':
				command += char