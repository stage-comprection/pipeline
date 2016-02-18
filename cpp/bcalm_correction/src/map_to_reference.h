#pragma once
#include "./utils/src/utils.h"
#include "settings.h"

// Loads reference genome in memory as a vector of sequences. Identifiers are not stored because the reference file is processed before and sequence names are
// set to the order of the sequence (first sequence is >0, second is >1 ...)
std::vector<std::string> getReferenceGenome(std::ifstream& referenceFile);

// Returns sequence from a reference based on parameters obtained in the SAM output file (reference sequence number and position on this sequence).
std::string getReferenceSequence(std::vector<std::string>& referenceGenome, const int& seqNumber, const int& position, int& readLength, const uint revComp);

// Extracts information from the alignment SAM output file, gets corrected reads sequence from the DB graph (the reference genome here) and stores these corrected
// reads in an output file.
int getReadsFromReference(SettingsStructure& settings);

