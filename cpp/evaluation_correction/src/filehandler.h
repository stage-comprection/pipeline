#pragma once

#include "utils.h"
#include "read.h"

#include <dirent.h>


class FileHandler{

    public:

        std::string readsSet;
        std::string reference;

        // Paths to useful folders
        std::string pathToReadsFolder;
        std::string pathToReferenceFolder;
        std::string pathToOutputFolder;

        // Paths to files
        std::string readsFilePath;
        std::string correctedFilePath;
        std::string referenceFilePath;
        std::string alignmentFilePath;
        std::string outputFilePath;

        // File streams
        std::ifstream originalReadsFile;
        std::ifstream correctedReadsFile;
        std::ifstream alignmentFile;
        std::ifstream referenceFile;
        std::ofstream outputFile;

        // Global parameters
        uint nLinesInCorrectedReads;
        uint nFilesForSplitting;
        uint readLength;
        uint nThreadsForExt;

        // Reference genome
        std::vector<std::string> referenceGenome;

        // Default constructor
        FileHandler();

        // Standard constructor
        void updateSettings(std::string& readsSetName, std::string& referenceName);

        // Creates temporary files to store reads
        std::vector<std::ofstream> createTempFiles(std::string& name);

        // Splits original reads into a number of files (defined in settings)
        void splitOriginalReadsFiles();

        // Splits corrected reads into a number of files (defined in settings)
        void splitCorrectedReadsFiles();

        // Splits reference sequence of reads into a number of files (defined in settings)
        void splitReferenceReadsFiles();

        // Gets read length from original reads file
        void getReadLength();

        // Gets number of lines for a read from corrected reads file
        void getLinesInCorrectedReads();

        // Skips alignment header lines
        std::string skipAlignmentHeaderLines();

        // Loads reference genome in memory
        void getReferenceGenome();

        // Cleanup all the temporary files at the end of the program (all temporary files start with 'temp')
        void cleanupTempFiles();

        // Extracts the read's sequence from the reference file, using the position given by the SAM output
        std::string getReferenceSequence(const int& seqNumber, const int& position, const uint revComp);

        // Reconstructs read vector from temporary files
        std::vector<Read> getReadsFromTempFiles(const uint batchNumber);

};
