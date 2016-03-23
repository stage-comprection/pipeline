"""
Main settings file for the pipeline.
Settings will have the value initialized in this file if there are not
overriden by command-line arguments.
Settings are stored in a dictionary which will later be merged with another
dictionary containing command-line updated settings.
"""

import os

# General pipeline parameters
general = {'baseDir': os.getcwd(),
           'outputPath': '/home/rferon/project/output/',
           'correction': 'dbg_correction',
           'correctedFile': 'corrected_',
           'alignerIndexFile': 'aligner_index_',
           'alignerFile': 'aligner_',
           'settingsFile': 'settings.txt',
           'savePath': '/home/rferon/project/output/save/',
           'nThreads': 6,
           'evaluationMode': False,
           'cleanup': 'T',
           'fullCleanup': 'F',
           'restoreFiles': 'F',
           'saveCorrected': 'F',
           'nReadsToAdd': 0,
           'kmerSize': 31,
           'abundance': 5,
           }


# Data parameters
data = {'readsPath': '/home/rferon/project/data/reads/',
        'refPath': '/home/rferon/project/data/references/',
        'readsFile': 'SRR959239.fasta',
        'refFile': 'ecoli_k12.fasta'}


# Bowtie parameters
bowtie = {'path': general['baseDir'] + '/ext/bowtie/',
          'nMismatches': 3}

# Bowtie2 parameters
bowtie2 = {'path': general['baseDir'] + '/ext/bowtie2/',
           'mode': 'fast'}


# BWA parameters
bwa = {'path': general['baseDir'] + '/ext/bwa/'}


# Bloocoo parameters
bloocoo = {'path': general['baseDir'] + '/ext/bloocoo/'}


# Musket parameters
musket = {'path': general['baseDir'] + '/ext/musket/'}


# DBG correction parameters
dbg_correction = {'path': general['baseDir'] + '/binaries/',
                  'settingsFile': 'correction_settings.ini',
                  'pathToBcalm': general['baseDir'] + '/ext/bcalm/',
                  'pathToBgreat': general['baseDir'] + '/ext/bgreat/',
                  'aligner': 'bowtie'}


# Evaluation parameters
evaluation = {'path': general['baseDir'] + '/binaries/',
              'settingsFile': 'evaluation_settings.ini',
              'nTempFiles': 20}


# Format reads utility
format_reads = {'path': general['baseDir'] + '/binaries/'}


# Bowtie Parser utility
bowtie_parser = {'path': general['baseDir'] + '/binaries/'}


# Generates default settings dictionary
settings = {'general': general,
            'data': data,
            'bowtie': bowtie,
            'bowtie2': bowtie2,
            'bwa': bwa,
            'bloocoo': bloocoo,
            'musket': musket,
            'dbg_correction': dbg_correction,
            'evaluation': evaluation,
            'format_reads': format_reads,
            'bowtie_parser': bowtie_parser
            }
