"""
Functions to evaluate the results of correction using the evaluation pipeline.
Parameters are given using a .ini file instead of command-line arguments.
"""

from ..settings import *
import os


# Generates an .ini file used by the evaluation pipeline to initialize
# parameter values.
def generate_settings_file(settings):

    pathToSettingsFile = (settings[GENERAL][OUTPUT_PATH] +
                          settings[EVALUATION][SETTINGS_FILE])

    with open(pathToSettingsFile, 'w') as o:

        o.write("outputFolderPath=" +
                settings[GENERAL][OUTPUT_PATH] + "\n")
        o.write("readsFolderPath=" +
                settings[DATA][READS_PATH] + "\n")
        o.write("referenceFolderPath=" +
                settings[DATA][REF_PATH] + "\n")
        o.write("readSet=" +
                settings[DATA][READS_FILE] + "\n")
        o.write("reference=" +
                settings[DATA][REF_FILE] + "\n")
        o.write("nThreads=" +
                str(settings[GENERAL][N_THREADS]) + "\n")
        o.write("nTempFiles=" +
                str(settings[EVALUATION][N_TEMP_FILES]) + "\n")


# Evaluates the results of correction using the evaluation pipeline
def evaluation(settings):

    # Generates the settings file used by the evaluation pipeline
    generate_settings_file(settings)

    # Runs evaluation_correction binary
    os.system(settings[EVALUATION][PATH] + 'evaluation_correction ' +
              settings[GENERAL][OUTPUT_PATH])
