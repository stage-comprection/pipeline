"""
Functions to correct a set of reads using the bcalm correction pipeline.
Parameters are given using a .ini file instead of command-line arguments.
"""

from ..settings import *
import os


# Generates an .ini file used by the DBG correction pipeline to initialize
# parameter values.
def generate_settings_file(settings):

    pathToSettingsFile = (settings[GENERAL][OUTPUT_PATH] +
                          settings[DBG_CORRECTION][SETTINGS_FILE])

    with open(pathToSettingsFile, 'w') as o:

        o.write("outputPath=" +
                settings[GENERAL][OUTPUT_PATH] + "\n")
        o.write("readsPath=" +
                settings[DATA][READS_PATH] + "\n")
        o.write("bcalmPath=" +
                settings[DBG_CORRECTION][BCALM_PATH] + "\n")
        o.write("bowtiePath=" +
                settings[BOWTIE][PATH] + "\n")
        o.write("bgreatPath=" +
                settings[DBG_CORRECTION][BGREAT_PATH] + "\n")
        o.write("readsFile=" +
                settings[DATA][READS_FILE] + "\n")
        o.write("kmerSizeBgreat=" +
                str(settings[DBG_CORRECTION][KMER_SIZE_BGREAT]) + "\n")
        o.write("kmerSizeBcalm=" +
                str(settings[DBG_CORRECTION][KMER_SIZE_BCALM]) + "\n")
        o.write("abundanceBcalm=" +
                str(settings[DBG_CORRECTION][ABUNDANCE_BCALM]) + "\n")
        o.write("abundanceBgreat=" +
                str(settings[DBG_CORRECTION][ABUNDANCE_BGREAT]) + "\n")
        o.write("nThreads=" +
                str(settings[GENERAL][N_THREADS]) + "\n")
        o.write("nMismatchesBowtie=" +
                str(settings[BOWTIE][N_MISMATCHES]) + "\n")


# Corrects original reads using dbg_correction
def dbg_correction(settings):

    # Generates the settings file used by dbg_correction
    generate_settings_file(settings)

    # Runs dbg_correction binary
    os.system(settings[DBG_CORRECTION][PATH] + 'dbg_correction ')
