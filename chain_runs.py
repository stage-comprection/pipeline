import os

readsFile = 'SRR959239.fasta'
refFile = 'ecoli_k12.fasta'
tempFiles = 20


abundance = 10
kmerSize = [15, 21, 25, 31]


def start_run(readsFile, refFile, tempFiles, abundanceBcalm, kmerSize):

    os.system('./run_pipeline.py' +
              ' -i ' + readsFile +
              ' -f ' + refFile +
              ' --abundance ' + str(abundance) +
              ' --tempFiles ' + str(tempFiles) +
              ' --kmerSize ' + str(kmerSize)
              )


for k in kmerSize:
    start_run(readsFile, refFile, tempFiles, abundance, k)
