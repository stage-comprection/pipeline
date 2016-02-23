"""
Merges settings values from command-line arguments and default user settings
into a settings dictionary (using a chainmap) and updates output path.

Organisation of the settings dictionary (with const name in brackets):

settings:

    - general (GENERAL):
        - outputPath (OUTPUT_PATH) = path to output directory
        - correction (CORRECTION) = correction tool
        - correctedFile (CORRECTED_FILE) = corrected file name
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

from . import command_line
from .const import *
from . import defaults
from collections import ChainMap


# Merges command line settings with default settings (from settings.py)
# Priority is given to command line values.
# The merged values are stored in settings dictionary
settings = dict()
for key in defaults.settings:
    if key in command_line.settings.keys():
        settings[key] = ChainMap({},
                                 command_line.settings[key],
                                 defaults.settings[key])
    else:
        settings[key] = ChainMap({},
                                 defaults.settings[key])

# Updates output path with the original reads file's name
settings[GENERAL][OUTPUT_PATH] += settings[DATA][READS_FILE].replace('.fasta',
                                                                     '') + '/'
