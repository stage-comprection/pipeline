"""
Functions to correct a set of reads using the bcalm correction pipeline.
Parameters are given using a .ini file instead of command-line arguments.
"""

from ..settings import *
import os


def generate_settings_file(settings):
    """
    Generates an .ini file used by the DBG correction pipeline to initialize
    parameter values.
    """

    pathToSettingsFile = (settings[GENERAL][OUTPUT_PATH] +
                          settings[DBG_CORRECTION][SETTINGS_FILE])

    with open(pathToSettingsFile, 'w') as o:

        o.write("outputPath=" +
                settings[GENERAL][OUTPUT_PATH] + "\n")
        o.write("baseFileName=" +
                settings[DATA][READS_FILE].replace('.fasta', '') + "\n")
        o.write("bcalmPath=" +
                settings[DBG_CORRECTION][BCALM_PATH] + "\n")
        o.write("bowtiePath=" +
                settings[BOWTIE][PATH] + "\n")
        o.write("bowtie2Path=" +
                settings[BOWTIE2][PATH] + "\n")
        o.write("bwaPath=" +
                settings[BWA][PATH] + "\n")
        o.write("bgreatPath=" +
                settings[DBG_CORRECTION][BGREAT_PATH] + "\n")
        o.write("bowtieParserPath=" +
                settings[BOWTIE_PARSER][PATH] + "\n")
        o.write("readsPath=" +
                settings[DATA][READS_PATH] + "\n")
        o.write("readsFile=" +
                settings[DATA][READS_FILE] + "\n")
        o.write("kmerSize=" +
                str(settings[GENERAL][KMER_SIZE]) + "\n")
        o.write("abundance=" +
                str(settings[GENERAL][ABUNDANCE]) + "\n")
        o.write("nThreads=" +
                str(settings[GENERAL][N_THREADS]) + "\n")
        o.write("nMismatchesBowtie=" +
                str(settings[BOWTIE][N_MISMATCHES]) + "\n")
        o.write("aligner=" +
                str(settings[DBG_CORRECTION][ALIGNER]) + "\n")


def dbg_correction(settings):
    """ Corrects original reads using dbg_correction """

    # Generates the settings file used by dbg_correction
    generate_settings_file(settings)

    # Runs dbg_correction binary
    os.system(settings[DBG_CORRECTION][PATH] +
              'dbg_correction ' +
              settings[GENERAL][OUTPUT_PATH])
