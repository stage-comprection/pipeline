#pragma once

#include "filehandler.h"
#include "outputstructure.h"

#include <thread>

class Master {

    public:

        // Object storing values to output later
        OutputStructure output;

        // Object in charge of file operations
        FileHandler fileHandler;

        // Number of threads allowed
        uint nThreads;

        // Constructor
        Master();
        Master(std::string& settingsFilePath);

        // Loads small read files in memory, compares original/corrected/reference sequences and increments counters accordingly
        void processOneBatch(uint batchNumber);

        // Calculate the gain obtained after correction, using the number of True Positives, False Positives and False Negatives
        void computeMetrics();

        // Reads settings from configuration file
        std::vector<std::string> readSettingsFile(std::string& settingsFilePath);

    private:


};
