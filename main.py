from multiprocessing import Process
import tools.barcode as barcode
import tools.record as record

def runInParallel(*fns):
	proc = []
	for fn in fns:
		p = Process(target=fn)
		p.start()
		proc.append(p)
	for p in proc:
		p.join()

def run_barcode():
	barcode.run()

def run_voice():
	record.run()

if __name__ == '__main__':
	runInParallel(run_barcode, run_voice)