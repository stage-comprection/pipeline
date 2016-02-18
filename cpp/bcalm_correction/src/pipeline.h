#pragma once

#include "run_binaries.h"
#include "map_to_reference.h"

#include <iostream>
#include <fstream>
#include <dirent.h>




// Runs bcalm + bglue to obtain DB graph (represented by a list of unitigs)
void getUnitigs(SettingsStructure& settings);

// Format bglue output (list of unitigs) : gives each unitig an identifier based on its order of occurrence (first unitig: >0, second unitig: >1 ...)
void formatBglueOutput(SettingsStructure& settings);

// Generates an unique file to store reads unmapped by bgreat (for now they're splitted in two files)
void concatenateFiles(SettingsStructure& settings, std::vector<std::string>& inputFileNames, std::string outputName );

// Cleanup all the temporary files at the end of the program (all temporary files start with 'temp')
void cleanupTempFiles(SettingsStructure& settings);

// Pipeline per se, runs all commands and checks if they executed correctly
void getCorrectedReadsFromBcalm(SettingsStructure& settings);

