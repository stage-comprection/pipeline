"""
Parser for command-line arguments
Check settings.py for a description of each parameter
"""

import argparse


def formatParser(dictionary):
    """
    Check if some arguments were not entered (value = None)
    so they don't override default settings (in settings.py)
    """

    general = dict()
    data = dict()
    dbg_correction = dict()
    evaluation = dict()

    o_dict = {'general': general,
              'data': data,
              'dbg_correction': dbg_correction,
              'evaluation': evaluation
              }

    for k, v in dictionary.items():
        if v is not None:
            temp = k.split('.')
            o_dict[temp[0]][temp[1]] = v

    return o_dict


# Initialize parser
parser = argparse.ArgumentParser(description='Process pipeline''s arguments')

parser.add_argument('--readsfile', '-i', dest='data.readsFile',
                    help='Name of the reads file')

parser.add_argument('--reffile', '-f', dest='data.refFile',
                    help='Name of the reference file')

parser.add_argument('--readspath', dest='data.readsPath',
                    help='Path to the reads directory')

parser.add_argument('--refpath', dest='data.refPath',
                    help='Path to the references directory')

parser.add_argument('--outputpath', '-o', dest='general.outputPath',
                    help='Path to the output directory')

parser.add_argument('--threads', '-t', dest='general.nThreads',
                    help='Number of threasd to use')

parser.add_argument('--evaluationOnly', '-e', dest='general.evaluationMode',
                    help='Perform evaluation only (T / F)')

parser.add_argument('--cleanup', '-u', dest='general.cleanup',
                    help='Cleanup mode (T / F) - remove corrected file')

parser.add_argument('--fullCleanup', dest='general.fullCleanup',
                    help='Full cleanup mode (T / F) - remove output dir')

parser.add_argument('--restoreFiles', '-r', dest='general.restoreFiles',
                    help='Restore data files (T / F)')

parser.add_argument('--smallFile', '-s', dest='general.nReadsToAdd',
                    help='Number of reads to add to test file' +
                    ' (if 0, no test file is made)')

parser.add_argument('--correction', '-c', dest='general.correction',
                    help='Correction tool to be used')

parser.add_argument('--kmerSize', dest='general.kmerSize',
                    help='Kmer size to use in correction')

parser.add_argument('--abundance', dest='general.abundance',
                    help='Abundance threshold for correction')

parser.add_argument('--tempFiles', dest='evaluation.nTempFiles',
                    help='Number of temp files to generate for evaluation')


# Get settings values from command line options
cl_input = vars(parser.parse_args())

# Check for None values (so they don't override default settings)
settings = formatParser(cl_input)
