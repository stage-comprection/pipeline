"""
Main script for evaluating correction.
Manage settings and launch the pipeline.
"""

from settings import *
import core


# Generates a test read file of size N if specified by user

def run():

    if int(settings[GENERAL][N_READS_TO_ADD]) > 0:

        core.generate_small_reads_file(settings)

        settings[DATA][READS_FILE] = ('test_' +
                                      settings[GENERAL][N_READS_TO_ADD] +
                                      '.fasta')

        settings[GENERAL][CLEANUP_MODE] = 2

    # Runs pipeline
    core.evaluation_pipeline(settings)
