"""
Functions to correct a set of reads using musket.
Musket is run with following parameters:
 - inorder flag (outputs corrected reads in same order as original reads)
 - k: set by user in pipeline's settings (kmer size)
 - number of expected kmers : 300,000,000 (don't really know...)
 - p: set by user in pipeline's settings (number of threads)
"""

from ..settings import *
import os


# Corrects original reads using musket
def musket(settings):

    # Runs musket binary with parameters from the pipeline's settings
    os.system(
              settings[MUSKET][PATH] +
              'musket -k ' +
              str(settings[GENERAL][KMER_SIZE]) +
              ' 300000000 -p ' +
              str(settings[GENERAL][N_THREADS]) +
              ' -inorder ' +
              settings[DATA][READS_PATH] +
              settings[DATA][READS_FILE] +
              ' -o ' +
              settings[GENERAL][OUTPUT_PATH] +
              settings[GENERAL][CORRECTED_FILE] +
              settings[DATA][READS_FILE]
              )
