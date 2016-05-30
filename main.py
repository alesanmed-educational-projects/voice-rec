from multiprocessing import Process, Queue
import os
import tools.barcode as barcode
import tools.record as record

def runInParallel(q, *fns):
    
    proc = []
    for fn in fns:
        p = Process(target=fn, args=(q,))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()
    
    return proc

def run_barcode():
    barcode.run()

def run_voice(q):
    result = record.run()
    if result == -1:
        q.put(-1)

if __name__ == '__main__':
    BARCODE_FILEPATH = 'barcodes.json'
    PRODUCT_FILEPATH = 'products.json'
    
    while True:
        if os.path.exists(BARCODE_FILEPATH):
            os.remove(BARCODE_FILEPATH)
        
        if os.path.exists(PRODUCT_FILEPATH):
            os.remove(PRODUCT_FILEPATH)
        
        q = Queue()
        proc = runInParallel(q, run_barcode, run_voice)
        first = False
        
        while q.get() != -1:
            pass
        
        # Proceso de mandar cosas
        
        for p in proc:
            p.terminate()