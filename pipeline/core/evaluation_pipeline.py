"""
Pipeline to evaluate correction.
Formats original reads and reference files, corrects them with specificed
correction tool and evaluate the correction process.
Pipeline's details:
 - Cleanup files if necessary / specified
 - Create specific output directory
 - Format reference file for easier use
 - Format reads file for easier use
 - Corrects reads
 - Align original reads with bowtie (necessary for evaluation)
 - Evaluate corrected reads (using another pipeline implemented in c++)
"""

from ..settings import *
from . import file_manipulation as fm
from .. import binaries
import os


def evaluation_pipeline(settings):

    # In evaluation mode, the pipeline doesn't perform correction
    if not settings[GENERAL][EVALUATION_MODE]:

        # Cleanup files generated by the pipeline if necessary (several modes)
        print('\n - Cleaning up (mode : ',
              settings[GENERAL][CLEANUP_MODE], ')')
        fm.cleanup_files(settings)

        # Creates output directory if not already created
        print('\n\n - Creating output directory')
        fm.create_output_directory(settings)

        # Formats reference file for easier use
        if int(settings[GENERAL][CLEANUP_MODE]) > 2:
            print('\n\n - Formatting reference file (',
                  settings[DATA][REF_FILE], ')')
            fm.format_reference_file(settings)

        # Formats reads file for easier use
        if int(settings[GENERAL][CLEANUP_MODE]) > 2:
            print('\n\n - Formatting reads file (',
                  settings[DATA][READS_FILE], ')')
            fm.format_reads_file(settings)

        # Corrects reads file after checking if a corrected file already exists
        if not os.path.isfile(settings[GENERAL][OUTPUT_PATH] +
                              settings[GENERAL][CORRECTED_FILE] +
                              settings[DATA][READS_FILE]):
            print('\n\n - Correcting reads file with ',
                  settings[GENERAL][CORRECTION])
            if settings[GENERAL][CORRECTION] == 'musket':
                binaries.musket(settings)
            elif settings[GENERAL][CORRECTION] == 'bloocoo':
                binaries.bloocoo(settings)
            elif settings[GENERAL][CORRECTION] == 'dbg_correction':
                binaries.dbg_correction(settings)
        else:
            print('\n\n - Found a corrected reads file, skipping correction')

        # Generates an index from the reference for alignemnt with bowtie
        print('\n\n - Generating bowtie index')
        binaries.bowtie_index(settings)

        # Aligns reads on reference using bowtie
        print('\n\n - Running bowtie on original reads')
        binaries.bowtie(settings)

        print('\n\n')

    # Evaluates correction results with the evaluation pipeline
    print(' - Evaluating correction\n\n')
    binaries.evaluation(settings)

    # Writes a copy of all settings in a file
    fm.print_settings_file(settings)

    # Saves important files into another directory
    fm.save_pipeline_output(settings)
