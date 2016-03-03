"""
Functions to correct a set of reads using bloocoo.
Bloocoo is run with following parameters:
 - high-recall mode
 - kmer-size: set by user in pipeline's settings
 - abundance: set by user in pipeline's settings
 - nb-cores: set by user in pipeline's settings
"""

from ..settings import *
import os


# Corrects original reads using bloocoo
def bloocoo(settings):

    # Runs bloocoo binary with parameters from the pipeline's settings
    os.system(
              settings[BLOOCOO][PATH] +
              'Bloocoo -high-recall -file ' +
              settings[DATA][READS_PATH] +
              settings[DATA][READS_FILE] +
              ' -kmer-size ' +
              str(settings[GENERAL][KMER_SIZE]) +
              ' -abundance ' +
              str(settings[GENERAL][ABUNDANCE]) +
              ' nb-cores ' +
              str(settings[GENERAL][N_THREADS]) +
              ' -out ' +
              settings[GENERAL][OUTPUT_PATH] +
              settings[GENERAL][CORRECTED_FILE] +
              settings[DATA][READS_FILE]
              )
