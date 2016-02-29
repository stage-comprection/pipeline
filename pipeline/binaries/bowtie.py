"""
Functions to generate an index for bowtie and align a set of reads with bowtie.
Bowtie is run with following parameters:
 - k: 1 (only one alignment is kept)
 - best mode (only the best alignment is kept)
 - input files: fasta (-f flag)
 - v: set by user in pipeline's settings (number of mismatches allowed in
      alignment)
 - p: set by user in pipeline's settings (number of threads)
"""

from ..settings import *
import os


# Generates and index for bowtie from a reference file
def bowtie_index(settings):

    os.system(
              settings[BOWTIE][PATH] +
              'bowtie-build --quiet ' +
              settings[DATA][REF_PATH] +
              settings[DATA][REF_FILE] +
              ' ' +
              settings[GENERAL][OUTPUT_PATH] +
              settings[BOWTIE][INDEX_FILE] +
              settings[DATA][READS_FILE].replace('.fasta', '')
              )


# Aligns a set of reads on a reference using bowtie
def bowtie(settings):

    # Runs bowtie binary with parameters from the pipeline's settings
    if not os.path.isfile(settings[GENERAL][OUTPUT_PATH] +
                          settings[BOWTIE][OUTPUT_FILE] +
                          settings[DATA][READS_FILE].replace('.fasta', '')):
        os.system(
                  settings[BOWTIE][PATH] +
                  'bowtie -f -k 1 --best -v ' +
                  str(settings[BOWTIE][N_MISMATCHES]) +
                  ' -p ' +
                  str(settings[GENERAL][N_THREADS]) +
                  ' ' +
                  settings[GENERAL][OUTPUT_PATH] +
                  settings[BOWTIE][INDEX_FILE] +
                  settings[DATA][READS_FILE].replace('.fasta', '') +
                  ' ' +
                  settings[DATA][READS_PATH] +
                  settings[DATA][READS_FILE] +
                  ' --sam-nohead --sam-nosq -S | ' +
                  settings[BOWTIE_PARSER][PATH] +
                  "bowtie_to_reads " +
                  settings[DATA][REF_PATH] +
                  settings[DATA][REF_FILE] +
                  " true " +
                  settings[GENERAL][OUTPUT_PATH] +
                  settings[BOWTIE][OUTPUT_FILE] +
                  settings[DATA][READS_FILE].replace('.fasta', '')
                  )
    else:
        print('\n    Found a SAM output file, skipping alignment' +
              '(use --cleanup 2 or 3 to generate a new alignment file)')
