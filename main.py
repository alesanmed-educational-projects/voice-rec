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

    return proc

def run_barcode(q, bluetooth):
    barcode.run()

def run_voice(q, bluetooth):
    result = record.run()
    if result == -1:
        q.put(-1)

def run_serial(q, bluetooth):
    bluetooth_read.run(bluetooth, q=q)


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

def send_command(command, bluetooth):
	bluetooth.write(command.encode('utf-8') + b'\n')

def send_cart(cart, BARCODE_FILEPATH, PRODUCT_FILEPATH, PENDING_PATH, bluetooth):
    print("Requested cart: {0}".format(cart))
    if cart == 'last':
        send_last_cart(BARCODE_FILEPATH, PRODUCT_FILEPATH, bluetooth);
        os.unlink(PENDING_PATH)

def terminate_proc(proc):
    for p in proc:
        p.terminate()

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

if __name__ == '__main__':
    BARCODE_FILEPATH = 'barcodes.json'
    PRODUCT_FILEPATH = 'products.json'
    PENDING_PATH = '.pending'
    
    bluetooth = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    
    while True:
        if not os.path.exists(PENDING_PATH):
            touch(PENDING_PATH)
            if os.path.exists(BARCODE_FILEPATH):
                os.remove(BARCODE_FILEPATH)
            
            if os.path.exists(PRODUCT_FILEPATH):
                os.remove(PRODUCT_FILEPATH)
        
        q = Queue(1)
        proc = runInParallel(q, bluetooth, run_voice, run_barcode, run_serial)
        
        while 1:
            print("System Ready")
            data = q.get()
            
            print(data)
            if data == -1:
                terminate_proc(proc)
                send_command('get_last_cart', bluetooth)
                break
            elif "get" in data.split()[0]:
                print("GET command received")
                terminate_proc(proc)
                cart = data.split()[1]
                send_cart(cart, BARCODE_FILEPATH, PRODUCT_FILEPATH, PENDING_PATH, bluetooth)
                break
