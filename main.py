from multiprocessing import Process, Queue
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
    first = True
    while True:
        if first:
            q = Queue() 
            proc = runInParallel(q, run_barcode, run_voice)
            first = False
        
        print(q.get())