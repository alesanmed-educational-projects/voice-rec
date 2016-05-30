import json
import os.path

def run():
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

	with open('barcodes.json', 'w') as outfile:
		json.dump({'barcodes': barcodes }, outfile)