import json
import os.path
import os
import sys
import re

def run():
    sys.stdin = open(0)
    while (True):
        filepath = 'barcodes.json'

        if os.path.exists(filepath):
            with open(filepath, 'r') as outfile:
                barcodes = json.load(outfile)['barcodes']
        else:
            barcodes = {}

        barcode = input()
        if barcode:
            barcode = re.sub("[^0-9]", "", barcode)
            if barcode in barcodes.keys():
                quantity = barcodes[barcode]
                barcodes[barcode] = quantity + 1
            else:
                barcodes[barcode] = 1

        with open(filepath, 'w') as outfile:
            json.dump({'barcodes': barcodes }, outfile)


if __name__ == "__main__":
    run()
