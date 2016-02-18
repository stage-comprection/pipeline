"""
Main settings file for the pipeline.
Settings will have the value initialized in this file if there are not
overriden by command-line arguments.
Settings are stored in a dictionary which will later be merged with another
dictionary containing command-line updated settings.
"""


# General pipeline parameters
general = {'outputPath': '/home/rferon/project/output/',
           'correction': 'bcalm',
           'correctedFile': 'corrected_',
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
bowtie = {'path': './binaries/',
          'output_file': 'bowtie_',
          'nMismatches': 3}


# Bloocoo parameters
bloocoo = {'path': './binaries/',
           'kmerSize': 31,
           'abundanceThreshold': 5}


# Musket parameters
musket = {'path': './binaries/',
          'kmerSize': 31}


# Bcalm correction parameters
dbg_correction = {'path': './binaries/',
                  'kmerSizeBcalm': 31,
                  'kmerSizeBgreat': 31,
                  'abundanceThresholdBcalm': 5,
                  'abundanceThresholdBgreat': 5,
                  'settingsFile': 'correction_settings.ini',
                  'pathToBcalm': '',
                  'pathToBgreat': ''}


# Evaluation parameters
evaluation = {'path': './binaries/',
              'settingsFile': 'evaluation_settings.ini',
              'nTempFiles': 20}


# Format reads utility
format_reads = {'path': './binaries/'}


# Generates default settings dictionary
settings = {'general': general,
            'data': data,
            'bowtie': bowtie,
            'bloocoo': bloocoo,
            'musket': musket,
            'dbg_correction': dbg_correction,
            'evaluation': evaluation,
            'format_reads': format_reads
            }
