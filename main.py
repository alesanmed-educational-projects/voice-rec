import datetime
from multiprocessing import Process, Queue
import os
import json
import tools.barcode as barcode
import tools.record as record
import tools.bluetooth as bluetooth_read
import serial

def runInParallel(q, bluetooth, *fns):
    
    proc = []
    for fn in fns:
        p = Process(target=fn, args=(q, bluetooth))
        p.start()
        proc.append(p)
    
    print("Return proc")
    return proc

def run_barcode(q, bluetooth):
    barcode.run()

def run_voice(q, bluetooth):
    result = record.run()
    if result == -1:
        q.put([-1])
        print("Saliendo")

def run_serial(q, bluetooth):
    bluetooth_read.run(q, bluetooth)


def send_last_cart(BARCODE_FILEPATH, PRODUCT_FILEPATH, bluetooth):
    result = {}
        
    if os.path.exists(BARCODE_FILEPATH):
        with open(BARCODE_FILEPATH, 'r') as barcodes:
            result['barcodes'] = json.load(barcodes)['barcodes']
    
    if os.path.exists(PRODUCT_FILEPATH):
        with open(PRODUCT_FILEPATH, 'r') as products:
            result['products'] = json.load(products)['products']

    timestamp = datetime.datetime.strftime(datetime.datetime.now(), 
                                   '%Y-%m-%d-%H.%M.%S')
    with open('shopping_carts/cart-{0}.json'.format(timestamp), 'w') as file:
        json.dump(result, file)
    
    with open('shopping_carts/cart-{0}.json'.format(timestamp), 'rb') as file:
        for line in file.readlines():
            print(line)
            bluetooth.write(line + b'\n')

if __name__ == '__main__':
    BARCODE_FILEPATH = 'barcodes.json'
    PRODUCT_FILEPATH = 'products.json'
    
    bluetooth = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    
    while True:
        if os.path.exists(BARCODE_FILEPATH):
            os.remove(BARCODE_FILEPATH)
        
        if os.path.exists(PRODUCT_FILEPATH):
            os.remove(PRODUCT_FILEPATH)
        
        q = Queue(1)
        proc = runInParallel(q, bluetooth, run_voice, run_barcode, run_serial)
        
        data = q.get()
        
        print(data)
        if data != -1:
            continue
        
        for p in proc:
            p.terminate()

        send_last_cart(BARCODE_FILEPATH, PRODUCT_FILEPATH, bluetooth);
