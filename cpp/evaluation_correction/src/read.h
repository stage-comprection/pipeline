#pragma once

#include "outputstructure.h"

#include <string>

class Read{

    public:

        std::string identifier;
        std::string originalSequence;
        std::string correctedSequence;
        std::string referenceSequence;

        // Comparison operator used for sorting
        bool operator < (const Read& read) const{
            return(stoi(identifier) < stoi(read.identifier));
        }

        Read();
        void analyze(OutputStructure& output);

};
