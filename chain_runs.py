import os

readsFile = 'SRR959239.fasta'
refFile = 'ecoli_k12.fasta'
tempFiles = 20


abundanceBcalm = 10
kmerBcalm = [15, 21, 25, 31]


def start_run(readsFile, refFile, tempFiles, abundanceBcalm, kmerBcalm):

    os.system('./run_pipeline.py' +
              ' -i ' + readsFile +
              ' -f ' + refFile +
              ' --abundanceBcalm ' + str(abundanceBcalm) +
              ' --tempFiles ' + str(tempFiles) +
              ' --kmerBcalm ' + str(kmerBcalm)
              )


for k in kmerBcalm:
    start_run(readsFile, refFile, tempFiles, abundanceBcalm, k)
