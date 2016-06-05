import time
import serial


ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
      )

string = "";
ser.flushInput();
while 1:
	bytesToRead = ser.inWaiting()
	if bytesToRead > 0:
		print("Bytes: " + str(bytesToRead))
		char = ser.read(1).decode('utf-8')
		string += char
		if char == ']':
			print(string);
			string = "";
			print("\n");
	else:
		print("None", end="\r")
