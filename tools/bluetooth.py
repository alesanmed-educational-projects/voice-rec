import time
import serial

def run(q, bluetooth):
	command_start = '['
	command_end = ']'

	command_pending = 0;
	command = "";
	bluetooth.flushInput();
	while 1:
		bytesToRead = bluetooth.inWaiting()
		if bytesToRead > 0:
			char = bluetooth.read(1).decode('utf-8')
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