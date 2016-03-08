import os

readsFile = ['SRR065390.fasta']
refFile = ['celegans.fasta']
correction = ['dbg_correction', 'bloocoo', 'musket']
abundance = [15]
kmerSize = [31]
tempFiles = 20


def start_run(reads, ref, c, temp, a, k):

    command = ('./run_pipeline.py' +
               ' -i ' + reads +
               ' -f ' + ref +
               ' -c ' + c +
               ' --tempFiles ' + str(temp)
               )

    if c == 'dbg_correction':
        command += ' --abundance ' + str(a)
        command += ' --kmerSize ' + str(k)

    os.system(command)

for read in readsFile:
    for ref in refFile:
        for c in correction:
            for a in abundance:
                for k in kmerSize:
                    start_run(read, ref, c, tempFiles, a, k)
