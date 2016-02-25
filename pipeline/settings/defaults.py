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
           'settingsFile': 'settings.ini',
           'nThreads': 6,
           'evaluationMode': False,
           'cleanup': 0,
           'nReadsToAdd': 0}


# Data parameters
data = {'readsPath': '/home/rferon/project/data/reads/',
        'refPath': '/home/rferon/project/data/references/',
        'readsFile': 'SRR959239.fasta',
        'refFile': 'ecoli_k12.fasta'}


# Bowtie parameters
bowtie = {'path': general['baseDir'] + '/ext/bowtie/',
          'output_file': 'bowtie_',
          'index_file': 'bowtie_index_',
          'nMismatches': 3}


# Bloocoo parameters
bloocoo = {'path': general['baseDir'] + '/ext/bloocoo/',
           'kmerSize': 31,
           'abundanceThreshold': 5}


# Musket parameters
musket = {'path': general['baseDir'] + '/ext/musket/',
          'kmerSize': 31}


# DBG correction parameters
dbg_correction = {'path': general['baseDir'] + '/binaries/',
                  'kmerSizeBcalm': 31,
                  'kmerSizeBgreat': 31,
                  'abundanceThresholdBcalm': 5,
                  'abundanceThresholdBgreat': 5,
                  'settingsFile': 'correction_settings.ini',
                  'pathToBcalm': general['baseDir'] + '/ext/bcalm/',
                  'pathToBgreat': general['baseDir'] + '/ext/bgreat/'}


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
            'bloocoo': bloocoo,
            'musket': musket,
            'dbg_correction': dbg_correction,
            'evaluation': evaluation,
            'format_reads': format_reads,
            'bowtie_parser': bowtie_parser
            }
