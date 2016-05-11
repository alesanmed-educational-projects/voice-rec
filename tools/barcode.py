import json
import os.path
import os
import sys

def run():
	sys.stdin = open(0)
	while (True):
		filepath = 'barcodes.json'

		if os.path.exists(filepath):
			with open(filepath, 'r') as outfile:
				barcodes = json.load(outfile)['barcodes']
		else:
			barcodes = []

		barcode = input()
		if barcode:
			barcodes.append(barcode)
			print(barcode)

		with open(filepath, 'w') as outfile:
			json.dump({'barcodes': barcodes }, outfile)


if __name__ == "__main__":
	run()
