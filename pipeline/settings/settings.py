"""
Merges settings values from command-line arguments and default user settings
into a settings dictionary (using a chainmap) and updates output path.

Organisation of the settings dictionary (with const name in brackets):

settings:

    - general (GENERAL):
        - outputPath (OUTPUT_PATH) = path to output directory
        - correction (CORRECTION) = correction tool
        - correctedFile (CORRECTED_FILE) = corrected file name
        - settingsFile (SETTINGS_FILE) = settings file name
        - savePath (SAVE_PATH) = path to save directory
        - nThreads (N_THREADS) = number of available threads
        - evaluationMode (EVALUATION) = bool (True: only evaluation)
        - cleanup (CLEANUP_MODE) = 1: All but bowtie 2: All 3: Restore data bk
        - nReadsToAdd (N_READS_TO_ADD) = make a small test file of size n

    - data (DATA):
        - readsPath (READS_PATH) = path to reads directory
        - refPath (REF_PATH) = path to reference directory
        - readsFile (READS_FILE) = name of reads file
        - refFile (REF_FILE) = name of reference file

    - bowtie (BOWTIE):
        - path (PATH) = path to directory containing bowtie binary
        - output_file (OUTPUT_FILE) = name of output file for bowtie
        - nMismatches (N_MISMATCHES) = number of allowed mismatches

    - bloocoo (BLOOCOO):
        - path (PATH) = path to directory containing bloocoo binary
        - kmerSize (KMER_SIZE) = kmer size for bloocoo
        - abundanceThreshold (ABUNDANCE) = abundance threshold for a good kmer

    - musket (MUSKET):
        - path (PATH) = path to directory containing musket binary
        - kmerSize (KMER_SIZE) = kmer size for musket

    - dbg_correction (DBG_CORRECTION):
        - path (PATH) = path to directory containing dbg_correction binary
        - kmerSizeBcalm (KMER_SIZE_BCALM) = size of kmer for bcalm
        - kmerSizeBgreat (KMER_SIZE_BGREAT) = size of kmer for bgreat
        - abundanceThresholdBcalm (ABUNDANCE_BCALM) = abundance bcalm
        - abundanceThresholdBgreat (ABUNDANCE_BGREAT) = abundance bgreat
        - settingsFile (SETTINGS_FILE) = name of settings file (.ini)
        - pathToBcalm (BCALM_PATH) = path to bcalm binary
        - pathToBgreat (BGREAT_PATH) = path to bgreat binary

    - evaluation (EVALUATION):
        - path (PATH) = path to directory containing evaluation binary
        - settingsFile (SETTINGS_FILE) = name of settings file (.ini)
        - nTempFiles (N_TEMP_FILES) = n temp files (memory management)

    - format_reads (FORMAT_READS):
        - path (PATH) = path to format reads binary

    - bowtie_parser (BOWTIE_PARSER):
        - path (PATH) = path to bowtie parser binary

"""

from .const import *
from . import command_line
from . import user_defined
from . import defaults
from collections import ChainMap
import os


def merge_settings_sources():
    """
    Merges command line settings with default settings (from settings.py)
    Priority is given to command line values.
    Merged values are stored in settings dictionary
    """
    settings = dict()
    for key in defaults.settings:
        if key in command_line.settings.keys():
            if key in user_defined.settings.keys():
                settings[key] = ChainMap({},
                                         command_line.settings[key],
                                         user_defined.settings[key],
                                         defaults.settings[key])
            else:
                settings[key] = ChainMap({},
                                         command_line.settings[key],
                                         defaults.settings[key])
        else:
            if key in user_defined.settings.keys():
                settings[key] = ChainMap({},
                                         user_defined.settings[key],
                                         defaults.settings[key])
            else:
                settings[key] = ChainMap({},
                                         defaults.settings[key])

    return settings


def update_output_path():
    """
    Updates output path with the new directory name
    Format : READSFILE_CORRECTION_PARAMETERS_COUNT
    """

    outputDir = settings[GENERAL][OUTPUT_PATH]
    baseFileName = settings[DATA][READS_FILE].replace('.fasta', '')
    outputDir += (baseFileName +
                  '_' + settings[GENERAL][CORRECTION])

    if settings[GENERAL][CORRECTION] == 'dbg_correction':

        outputDir += '_' + str(settings[DBG_CORRECTION][KMER_SIZE_BCALM])
        outputDir += '_' + str(settings[DBG_CORRECTION][ABUNDANCE_BCALM])
        outputDir += '_' + str(settings[DBG_CORRECTION][KMER_SIZE_BGREAT])
        outputDir += '_' + str(settings[DBG_CORRECTION][ABUNDANCE_BGREAT])

    elif settings[GENERAL][CORRECTION] == 'bloocoo':
        outputDir += '_' + str(settings[BLOOCOO][KMER_SIZE])
        outputDir += '_' + str(settings[BLOOCOO][ABUNDANCE])

    elif settings[GENERAL][CORRECTION] == 'musket':
        outputDir += '_' + str(settings[MUSKET][KMER_SIZE])

    count = 0
    # while os.path.isdir(outputDir + '_' + str(count)):
    #     count += 1

    outputDir += '_' + str(count)
    outputDir += '/'
    settings[GENERAL][OUTPUT_PATH] = outputDir


settings = merge_settings_sources()
update_output_path()
