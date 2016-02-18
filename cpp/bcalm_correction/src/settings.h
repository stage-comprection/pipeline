#pragma once

#include "./utils/src/utils.h"

#include <fstream>
#include <iostream>

struct SettingsStructure{

    std::string pathToProject = "/home/rferon/project/";
    std::string pathToOutput = pathToProject + "output/";
    std::string pathToReads = pathToProject + "data/reads/";
    std::string pathToBcalm = pathToProject + "code/bcalm/build/";
    std::string pathToBowtie = pathToProject + "tools/bowtie/" ;
    std::string pathToBgreat = pathToProject + "code/BGREAT/";
    std::string baseFileName = "";
    uint kmerSize_bcalm = 31;
    uint kmerSize_bgreat = 31;
    uint abundanceThreshold_bcalm = 5;
    uint abundanceThreshold_bgreat = 5;
    uint nCores = 6;
    uint nAllowedMismatchesForBowtie = 3;
    uint readLength = 98;

    // Loads settings from settings file
    void loadSettingsFile(std::string& settingsFilePath);

};
