import os

readsFile = ['SRR959239.fasta']
refFile = ['ecoli_k12.fasta']
correction = ['dbg_correction']
abundance = [3,5,7,9,11]
kmerSize = [27,31]
tempFiles = 20


def start_run(reads, ref, c, temp, a, k):

    command = ('./run_pipeline.py' +
               ' -i ' + reads +
               ' -f ' + ref +
               ' -c ' + c +
	       ' -u T ' +
               ' --tempFiles ' + str(temp)
               )

    if c == 'dbg_correction':
        command += ' --abundance ' + str(a)
        command += ' --kmerSize ' + str(k)

    os.system(command)

for read in readsFile:
    for ref in refFile:
        for c in correction:
	    if c == 'dbg_correction':
		    for a in abundance:
		        for k in kmerSize:
		            start_run(read, ref, c, tempFiles, a, k)
	    else:
		start_run(read, ref, c, tempFiles, a, k)
