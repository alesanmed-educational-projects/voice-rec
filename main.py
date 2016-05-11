import datetime
from multiprocessing import Process, Queue
import os
import json
import tools.barcode as barcode
import tools.record as record

def runInParallel(q, *fns):
    
    proc = []
    for fn in fns:
        p = Process(target=fn, args=(q,))
        p.start()
        proc.append(p)
    
    print("Return proc")
    return proc

def run_barcode(q):
    barcode.run()

def run_voice(q):
    result = record.run()
    if result == -1:
        q.put(-1)
        print("Saliendo")

if __name__ == '__main__':
    BARCODE_FILEPATH = 'barcodes.json'
    PRODUCT_FILEPATH = 'products.json'
    
    while True:
        if os.path.exists(BARCODE_FILEPATH):
            os.remove(BARCODE_FILEPATH)
        
        if os.path.exists(PRODUCT_FILEPATH):
            os.remove(PRODUCT_FILEPATH)
        
        q = Queue()
        proc = runInParallel(q, run_voice, run_barcode)
        
        print("While")
        while q.get() != -1:
            print("Mi q es {0}".format(q.get()))
            pass
        
        for p in proc:
            p.terminate()
        
        with open(BARCODE_FILEPATH, 'r') as barcodes:
            with open(PRODUCT_FILEPATH, 'r') as products:
                result = {
                    'products': json.load(products)['products'],
                    'barcodes': json.load(barcodes)['barcodes']
                }
                
                with open('shopping_carts/cart-{0}.json'.format(
                    datetime.datetime.strftime(datetime.datetime.now(), 
                                               '%Y-%m-%d-%H.%M.%S')), 'w') as file:
                    json.dump(result, file)
        
