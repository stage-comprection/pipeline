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


# def cleanup_files(settings):
#     """
#     Cleanup pipeline's files (reads and reference)
#     """

#     if settings[GENERAL][CLEANUP_MODE] == 'T':
#         restore_data_file(settings, 'reference')
#         restore_reads_file(settings, 'reads')


def cleanup_files(settings):
    """ Cleanup pipeline's files (reads and reference) """

    if settings[GENERAL][RESTORE_FILES] == 'T':
        restore_data_file(settings, 'reference')
        restore_data_file(settings, 'reads')

    if settings[GENERAL][CLEANUP_MODE] == 'T':

        if os.path.isfile(settings[GENERAL][OUTPUT_PATH] +
                          settings[GENERAL][CORRECTED_FILE] +
                          settings[DATA][READS_FILE]):

            os.remove(settings[GENERAL][OUTPUT_PATH] +
                      settings[GENERAL][CORRECTED_FILE] +
                      settings[DATA][READS_FILE])

    if settings[GENERAL][FULL_CLEANUP] == 'T':
        if os.path.isdir(settings[GENERAL][OUTPUT_PATH]):
            shutil.rmtree(settings[GENERAL][OUTPUT_PATH])


def create_output_directory(settings):
    """ Creates the output directory """

    if not os.path.isdir(settings[GENERAL][OUTPUT_PATH]):
        os.makedirs(settings[GENERAL][OUTPUT_PATH])

    else:
        print(' (skipped)')


def generate_small_reads_file(settings):
    """ Creates a reads file which is a subset of the original reads file """

    size = settings[GENERAL][N_READS_TO_ADD]
    name = 'test_' + str(settings[GENERAL][N_READS_TO_ADD]) + '.fasta'
    with open(settings[DATA][REF_PATH] + settings[DATA][READS_FILE]) as f:
        with open(settings[DATA][READS_PATH] + name, 'w') as g:
            for i in range(2*size):
                print(i)
                g.write(f.readline())


def format_data_file(settings, f):
    """
    Formats the original reads file in the following format :
      - Read ID : number of the read (by occurence)
      - Sequence one one line regardless of size
    Formats the reference file with '0' as ID and sequence on one line
    """

    if f == 'reads':
        filePath = READS_PATH
        fileName = READS_FILE
        keepN = 'F'
    elif f == 'reference':
        filePath = REF_PATH
        fileName = REF_FILE
        keepN = 'T'
    else:
        print('Invalid file to be formatted')

    if settings[GENERAL][RESTORE_FILES] == 'T':

        if not os.path.isfile(settings[DATA][filePath] +
                              settings[DATA][fileName] +
                              '.backup'):

            os.rename(settings[DATA][filePath] +
                      settings[DATA][fileName],
                      settings[DATA][filePath] +
                      settings[DATA][fileName] +
                      '.backup')

        os.system(settings[FORMAT_READS][PATH] +
                  'format_reads_file ' +
                  settings[DATA][filePath] +
                  settings[DATA][fileName] +
                  ' ' +
                  keepN)

    else:

        if not os.path.isfile(settings[DATA][filePath] +
                              settings[DATA][fileName] +
                              '.backup'):

            os.rename(settings[DATA][filePath] +
                      settings[DATA][fileName],
                      settings[DATA][filePath] +
                      settings[DATA][fileName] +
                      '.backup')

        if not os.path.isfile(settings[DATA][filePath] +
                              settings[DATA][fileName]):

            os.system(settings[FORMAT_READS][PATH] +
                      'format_reads_file ' +
                      settings[DATA][filePath] +
                      settings[DATA][fileName] +
                      ' ' +
                      keepN)

        else:
            print(' (skipped)')


def restore_data_file(settings, f):
    """ Restores a data file from backup """

    if f == 'reads':
        filePath = READS_PATH
        fileName = READS_FILE
    elif f == 'reference':
        filePath = REF_PATH
        fileName = REF_FILE
    else:
        print('Invalid file to be formatted')

    if os.path.isfile(settings[DATA][filePath] +
                      settings[DATA][fileName] +
                      '.backup'):
        if os.path.isfile(settings[DATA][filePath] +
                          settings[DATA][fileName]):

            os.remove(settings[DATA][filePath] +
                      settings[DATA][fileName])

        os.rename(settings[DATA][filePath] +
                  settings[DATA][fileName] +
                  '.backup',
                  settings[DATA][filePath] +
                  settings[DATA][fileName])


def generate_stats_file(settings):
    """
    Generates a stats file for correction step (when using dbg correction)
    """

    bgreat = open(settings[GENERAL][OUTPUT_PATH] +
                  'logs_bgreat.txt')
    bowtie = open(settings[GENERAL][OUTPUT_PATH] +
                  'logs_bowtie.txt')
    output = open(settings[GENERAL][OUTPUT_PATH] +
                  'correction_stats.txt', 'w')

    nReads = -1
    nNotOverlap = -1
    nOverlap = -1
    nOverlapAligned = -1
    nOverlapNotAligned = -1
    nAligned = -1
    nUnaligned = -1

    for line in bgreat:
        if line.startswith('Reads :'):
            nReads = line.split(' : ')[1].strip('\n')
        elif line.startswith('No overlap'):
            nNotOverlap = line.split(' : ')[1].split(' ')[0].strip('\n')
        elif line.startswith('Got overlap'):
            nOverlap = line.split(' : ')[1].split(' ')[0].strip('\n')
        elif line.startswith('Overlap and aligned'):
            nOverlapAligned = line.split(' : ')[1].split(' ')[0].strip('\n')
        elif line.startswith('Overlap but not aligned'):
            nOverlapNotAligned = line.split(' : ')[1].split(' ')[0].strip('\n')

    for line in bowtie:
        if line.startswith('# reads with at least one reported'):
            nAligned = line.split(': ')[1].split(' ')[0].strip('\n')
        elif line.startswith('# reads that failed to align'):
            nUnaligned = line.split(': ')[1].split(' ')[0].strip('\n')

    output.write('nReads' + '\t' + 'nNotOverlap' + '\t' +
                 'nOverlap' + '\t' + 'nOverlapAligned' + '\t' +
                 'nOverlapNotAligned' + '\t' + 'nAligned' + '\t' +
                 'nUnaligned' + '\n')
    output.write(nReads + '\t' + nNotOverlap + '\t' +
                 nOverlap + '\t' + nOverlapAligned + '\t' +
                 nOverlapNotAligned + '\t' + nAligned + '\t' + nUnaligned)

    output.close()
    bgreat.close()
    bowtie.close()


def print_settings_file(settings):
    """ Prints a copy of all settings in a file to be saved """

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


def save_pipeline_output(settings):
    """
    Saves a copy of important files at the end of the run and
    remove the output directory (necessary on the cluster because of
    space constraints)
    """

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

    if settings[GENERAL][SAVE_CORRECTED] == 'T':
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

    # shutil.rmtree(settings[GENERAL][OUTPUT_PATH])
