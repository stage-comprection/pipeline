"""
Parser for settings.ini file
The settings.ini file is made and provided by the user to override defaults
settings.
This module implements functions to parse this file into a dictionary mergeable
with other settings dictionaries
Settings.ini has the following structure:

[category1]
key1: value1
key2: value2

[category2]
...
"""

import re
import os


def to_bool(s):

    """
    Converts a string to a bool
    """

    acceptable = ['TRUE', 'True', 'true', 'T', 't', 'Y', 'y', '1']

    if s in acceptable:
        return True
    else:
        return False


def settings_parser(filePath):

    """
    Gets all user defined settings from settings.ini file
    Converts to int or bool when necessary
    """

    # Regex for each type of line to be parsed (category, key)
    regex_category = re.compile(r'\[(.+)\]$')
    regex_key = re.compile(r'([^:]+)+: (.+)$')

    settings = {'general': dict(),
                'data': dict(),
                'bowtie': dict(),
                'bloocoo': dict(),
                'musket': dict(),
                'dbg_correction': dict(),
                'evaluation': dict(),
                'format_reads': dict(),
                'bowtie_parser': dict()
                }

    category = ''

    int_values = ['nTempFiles',
                  'nReadsToAdd',
                  'nThreads',
                  'kmerSize',
                  'abundanceThreshold',
                  'nMismatches',
                  'abundanceBcalm'
                  'abundanceBgreat',
                  'kmerSizeBcalm',
                  'kmerSizeBgreat']

    bool_values = ['cleanup',
                   'evaluationMode']

    # Parsing of all lines in the file and conversion when necessary
    with open(filePath) as f:
        for line in f:
            cat = re.match(regex_category, line)
            if cat:
                category = cat.group(1)
            else:
                l = re.match(regex_key, line)
                if l:
                    key = l.group(1)
                    value = l.group(2)
                    if key in int_values:
                        value = int(value)
                    elif key in bool_values:
                        value = to_bool(value)
                    settings[category][key] = value

    return settings


iniFilePath = "settings.ini"

if not os.path.isfile(iniFilePath):
    print('    Warning: no settings.ini file found - defaults settings will' +
          ' be used.')
else:
    settings = settings_parser(iniFilePath)
