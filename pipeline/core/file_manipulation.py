"""
Functions used by the pipeline to perform file manipulation:
 - cleanup generated files (cleanup_files)
 - create output directory (create_output_directory)
 - generate a small reads file (generate_small_reads_file)
 - format the original reads file (format_reads_file)
 - format the reference file (format_reference_file)
 - restore the reads file from backup (restore_reads_file)
 - restore the reference file from backup (restore_reference_file)
"""

from ..settings import *
import os
import shutil


# Cleanup pipeline's files (reads and reference):
def cleanup_files(settings):

    if settings[GENERAL][CLEANUP_MODE] == 'T':
        restore_reference_file(settings)
        restore_reads_file(settings)


# Creates the output directory
def create_output_directory(settings):

    os.makedirs(settings[GENERAL][OUTPUT_PATH])


# Creates a reads file which is a subset of the original reads file
def generate_small_reads_file(settings):

    size = settings[GENERAL][N_READS_TO_ADD]
    name = 'test_' + str(settings[GENERAL][N_READS_TO_ADD]) + '.fasta'
    with open(settings[DATA][REF_PATH] + settings[DATA][READS_FILE]) as f:
        with open(settings[DATA][READS_PATH] + name, 'w') as g:
            for i in range(2*size):
                print(i)
                g.write(f.readline())


# Formats the original reads file in the following format :
# - Read ID : number of the read (by occurence)
# - Sequence one one line regardless of size
def format_reads_file(settings):

    if not os.path.isfile(settings[DATA][READS_PATH] +
                          settings[DATA][READS_FILE] +
                          '.backup'):

        os.rename(settings[DATA][READS_PATH] +
                  settings[DATA][READS_FILE],
                  settings[DATA][READS_PATH] +
                  settings[DATA][READS_FILE] +
                  '.backup')

    os.system(settings[FORMAT_READS][PATH] +
              'format_reads_file ' +
              settings[DATA][READS_PATH] +
              settings[DATA][READS_FILE])


# Formats the reference file with '0' as ID and sequence on one line
def format_reference_file(settings):

    if not os.path.isfile(settings[DATA][REF_PATH] +
                          settings[DATA][REF_FILE] +
                          '.backup'):

        os.rename(settings[DATA][REF_PATH] +
                  settings[DATA][REF_FILE],
                  settings[DATA][REF_PATH] +
                  settings[DATA][REF_FILE] +
                  '.backup')

        with open(settings[DATA][REF_PATH] +
                  settings[DATA][REF_FILE] +
                  '.backup') as f:
            with open(settings[DATA][REF_PATH] +
                      settings[DATA][REF_FILE], 'w') as o:
                f.readline()
                o.write(">0\n")
                for line in f:
                    o.write(line.strip())


# Restores reads file from backup
def restore_reads_file(settings):

    if os.path.isfile(settings[DATA][READS_PATH] +
                      settings[DATA][READS_FILE] +
                      '.backup'):
        if os.path.isfile(settings[DATA][READS_PATH] +
                          settings[DATA][READS_FILE]):

            os.remove(settings[DATA][READS_PATH] +
                      settings[DATA][READS_FILE])

        os.rename(settings[DATA][READS_PATH] +
                  settings[DATA][READS_FILE] +
                  '.backup',
                  settings[DATA][READS_PATH] +
                  settings[DATA][READS_FILE])


# Restores reference file from backup
def restore_reference_file(settings):

    if os.path.isfile(settings[DATA][REF_PATH] +
                      settings[DATA][REF_FILE] +
                      '.backup'):

        if os.path.isfile(settings[DATA][REF_PATH] +
                          settings[DATA][REF_FILE]):

            os.remove(settings[DATA][REF_PATH] +
                      settings[DATA][REF_FILE])

        os.rename(settings[DATA][REF_PATH] +
                  settings[DATA][REF_FILE] +
                  '.backup',
                  settings[DATA][REF_PATH] +
                  settings[DATA][REF_FILE])


# Generates a stats file
def generate_stats_file(settings):

    bgreat = open(settings[GENERAL][OUTPUT_PATH] +
                  'logs_bgreat.txt')
    bowtie = open(settings[GENERAL][OUTPUT_PATH] +
                  'logs_bowtie.txt')
    output = open(settings[GENERAL][OUTPUT_PATH] +
                  'correction_stats.txt', 'w')

    for line in bgreat:
        if line.startswith('Number of unitig'):
            nUnitigs = line.split(': ')[1].strip('\n')
        elif line.startswith('Read'):
            nReads = line.split(' : ')[1].strip('\n')
        elif line.startswith('No Overlap'):
            nNotOverlap = line.split(' : ')[1].split(' ')[0].strip('\n')
        elif line.startswith('Got Overlap'):
            nOverlap = line.split(' : ')[1].split(' ')[0].strip('\n')
        elif line.startswith('Overlap and Aligned'):
            nOverlapAligned = line.split(' : ')[1].split(' ')[0].strip('\n')
        elif line.startswith('Overlap but no aligne'):
            nOverlapNotAligned = line.split(' : ')[1].split(' ')[0].strip('\n')

    for line in bowtie:
        if line.startswith('# reads with at least one reported'):
            nAligned = line.split(': ')[1].split(' ')[0].strip('\n')
        elif line.startswith('# reads that failed to align'):
            nUnaligned = line.split(': ')[1].split(' ')[0].strip('\n')

    output.write('nUnitigs' + '\t' + 'nReads' + '\t' + 'nNotOverlap' + '\t' +
                 'nOverlap' + '\t' + 'nOverlapAligned' + '\t' +
                 'nOverlapNotAligned' + '\t' + 'nAligned' + '\t' +
                 'nUnaligned' + '\n')
    output.write(nUnitigs + '\t' + nReads + '\t' + nNotOverlap + '\t' +
                 nOverlap + '\t' + nOverlapAligned + '\t' +
                 nOverlapNotAligned + '\t' + nAligned + '\t' + nUnaligned)

    output.close()
    bgreat.close()
    bowtie.close()


# Prints a copy of all settings in a file
def print_settings_file(settings):

    with open(settings[GENERAL][OUTPUT_PATH] +
              settings[GENERAL][SETTINGS_FILE], 'w') as o:
        for key1, value1 in settings.items():
            o.write('[' + key1 + ']\n')
            for key2, value2 in value1.items():
                try:
                    o.write(key2 + ': ' + value2 + '\n')
                except TypeError:
                    o.write(key2 + ': ' + str(value2) + '\n')
            o.write('\n')


# Saves a copy of important files at the end of the run
def save_pipeline_output(settings):

    saveDir = (settings[GENERAL][SAVE_PATH])
    baseFileName = settings[DATA][READS_FILE].replace('.fasta', '')
    saveDir += (baseFileName +
                '_' + settings[GENERAL][CORRECTION])

    if settings[GENERAL][CORRECTION] in ['dbg_correction', 'bloocoo']:

        saveDir += '_' + str(settings[GENERAL][KMER_SIZE])
        saveDir += '_' + str(settings[GENERAL][ABUNDANCE])

    elif settings[GENERAL][CORRECTION] == 'musket':
        saveDir += '_' + str(settings[GENERAL][KMER_SIZE])

    count = 1
    while os.path.isdir(saveDir + '_' + str(count)):
        count += 1

    saveDir += '_' + str(count)
    saveDir += '/'

    os.makedirs(saveDir)

    try:
        shutil.copy(settings[GENERAL][OUTPUT_PATH] +
                    settings[GENERAL][CORRECTED_FILE] +
                    settings[DATA][READS_FILE],
                    saveDir +
                    settings[GENERAL][CORRECTED_FILE] +
                    settings[DATA][READS_FILE])
    except FileNotFoundError:
        pass

    try:
        shutil.copy(settings[GENERAL][OUTPUT_PATH] +
                    settings[GENERAL][SETTINGS_FILE],
                    saveDir +
                    settings[GENERAL][SETTINGS_FILE])
    except FileNotFoundError:
        pass

    try:
        shutil.copy(settings[GENERAL][OUTPUT_PATH] +
                    'logs_bowtie.txt',
                    saveDir +
                    'logs_bowtie.txt')
    except FileNotFoundError:
        pass

    try:
        shutil.copy(settings[GENERAL][OUTPUT_PATH] +
                    'logs_bcalm.txt',
                    saveDir +
                    'logs_bcalm.txt')
    except FileNotFoundError:
        pass
    try:
        shutil.copy(settings[GENERAL][OUTPUT_PATH] +
                    'logs_bglue.txt',
                    saveDir +
                    'logs_bglue.txt')
    except FileNotFoundError:
        pass

    try:
        shutil.copy(settings[GENERAL][OUTPUT_PATH] +
                    'logs_bgreat.txt',
                    saveDir +
                    'logs_bgreat.txt')
    except FileNotFoundError:
        pass

    try:
        shutil.copy(settings[GENERAL][OUTPUT_PATH] +
                    'logs_bowtie_index.txt',
                    saveDir +
                    'logs_bowtie_index.txt')
    except FileNotFoundError:
        pass

    try:
        shutil.copy(settings[GENERAL][OUTPUT_PATH] +
                    'gain_' +
                    settings[DATA][READS_FILE].replace('.fasta', ''),
                    saveDir +
                    'evaluation_results.txt')
    except FileNotFoundError:
        pass

    try:
        shutil.copy(settings[GENERAL][OUTPUT_PATH] +
                    'correction_stats.txt',
                    saveDir +
                    'correction_stats.txt')
    except FileNotFoundError:
        pass
