#pragma once

#include <string>
#include <fstream>
#include <atomic>


class OutputStructure {

    public:

        float gain;
        std::atomic<uint64_t> truePositives;
        std::atomic<uint64_t> falsePositives;
        std::atomic<uint64_t> falseNegatives;
        std::atomic<uint64_t> notCorrectedAndShouldnt;
        std::atomic<uint64_t> notCorrectedButShould;
        std::atomic<uint64_t> notAligned;
        std::atomic<uint64_t> wrongCorrection;
        std::atomic<uint64_t> nReadsProcessed;

        OutputStructure();

        // Export results in an output file
        void exportResults(std::ofstream& outputFile);

        // Computes gain
        void computeGain();
};
