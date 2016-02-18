#pragma once

#include "settings.h"


// Runs bgreat to align reads on multiple unitigs
void runBgreat(SettingsStructure& settings);

// Builds bowtie index from reference genome (DB graph unitigs)
void buildBowtieIndex(SettingsStructure& settings);

// Runs bowtie to align reads on DB graph unitigs
void runBowtie(SettingsStructure& settings);

// Runs Bcalm to generate DB graph from original reads
void runBcalm(SettingsStructure& settings);

// Runs Bglue to generate unitigs from Bcalm output
void runBglue(SettingsStructure& settings);

