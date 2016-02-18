#include "run_binaries.h"

using namespace std;


// Runs bgreat to align reads on multiple unitigs
void runBgreat(SettingsStructure& settings){

    cout<<endl<<"Running Bgreat ... "<<endl;

    // All stdout is collected and stored in a log file (doesn't really work in practice...)
    string logFilePath = settings.pathToOutput + "logs_bgreat.txt";
    FILE* logsOpen = freopen(logFilePath.c_str(), "w", stdout);
    if (logsOpen == NULL) return; // If problem with opening logs file, abort

    // Initializes command to run bgreat in correction mode (-c) with desired path and parameters
    string command = settings.pathToBgreat + "bgreat -r " + settings.pathToReads + settings.baseFileName + ".fasta -k " + to_string(settings.kmerSize_bgreat) +
                     " -g " + settings.pathToOutput + "temp_formatted_bglue_" + settings.baseFileName + " -m " + to_string(settings.abundanceThreshold_bgreat) +
                     " -c -t " + to_string(settings.nCores) + " -f " + settings.pathToOutput + "temp_bgreat_corrected_" + settings.baseFileName + " -o " +
                     settings.pathToOutput + "temp_bgreat_noOverlap_" + settings.baseFileName + " -a " + settings.pathToOutput + "temp_bgreat_noAlign_" +
                     settings.baseFileName;

    // Runs command and stores state
    system(command.c_str());

    fclose(logsOpen);
}




// Builds bowtie index from reference genome (DB graph unitigs)
void buildBowtieIndex(SettingsStructure& settings){

    cout<<endl<<"Building bowtie index ... "<<endl;

    // All stdout is collected and stored in a log file (doesn't really work in practice...)
    string logFilePath = settings.pathToOutput + "logs_bowtie_index.txt";
    FILE* logsOpen = freopen(logFilePath.c_str(), "w", stdout);
    if (logsOpen == NULL) return; // If problem with opening logs file, abort

    // Initializes command to build the bowtie index - see bowtie manual
    string command = settings.pathToBowtie + "bowtie-build " + settings.pathToOutput + "temp_formatted_bglue_" + settings.baseFileName + " " +
                     settings.pathToOutput + "temp_index_" + settings.baseFileName;

    // Runs command and stores state
    system(command.c_str());

    fclose(logsOpen);
}




// Runs bowtie to align reads on DB graph unitigs
void runBowtie(SettingsStructure& settings){

    cout<<endl<<"Running bowtie ... "<<endl;

    // All stdout is collected and stored in a log file (doesn't really work in practice...)
    string logFilePath = settings.pathToOutput + "logs_bowtie.txt";
    FILE* logsOpen = freopen(logFilePath.c_str(), "w", stdout);
    if (logsOpen == NULL) return; // If problem with opening logs file, abort

    // Initializes command to run bowtie with desired parameters and input/output files
    string command = settings.pathToBowtie + "bowtie -f -k 1 --best -v " + to_string(settings.nAllowedMismatchesForBowtie) + " -p " +
                     to_string(settings.nCores) + " " + settings.pathToOutput + "temp_index_" + settings.baseFileName + " " +
                     settings.pathToOutput + "temp_bgreat_uncorrected_" + settings.baseFileName + ".fasta -S " + settings.pathToOutput + "temp_aligned_" +
                     settings.baseFileName + " --sam-nosq";

    // Runs command and stores state
    system(command.c_str());

    fclose(logsOpen);
}




// Runs Bcalm to generate DB graph from original reads
void runBcalm(SettingsStructure& settings){

    cout<<endl<<"Running Bcalm ... "<<endl;

    // All stdout is collected and stored in a log file (doesn't really work in practice...)
    string logFilePath = settings.pathToOutput + "logs_bcalm.txt";
    FILE* logsOpen = freopen(logFilePath.c_str(), "w", stdout);
    if (logsOpen == NULL) return; // If problem with opening logs file, abort

    // Initializes command to run bcalm on original reads with desired input/output files
    string command = settings.pathToBcalm + "bcalm -in " + settings.pathToReads + settings.baseFileName + ".fasta -k " + to_string(settings.kmerSize_bcalm) +
                     " -abundance " + to_string(settings.abundanceThreshold_bcalm) + " -out " + settings.pathToOutput + "temp_bcalm_" +
                     settings.baseFileName + " -verbose 0 -nb-cores " + to_string(settings.nCores);

    // Runs command and stores state
    system(command.c_str());

    fclose(logsOpen);
}




// Runs Bglue to generate unitigs from Bcalm output
void runBglue(SettingsStructure& settings){

    cout<<endl<<"Running Bglue... "<<endl;

    // All stdout is collected and stored in a log file (doesn't really work in practice...)
    string logFilePath = settings.pathToOutput + "logs_bglue.txt";
    FILE* logsOpen = freopen(logFilePath.c_str(), "w", stdout);
    if (logsOpen == NULL) return; // If problem with opening logs file, abort

    // Initializes command to run bglue on bcalm output with desired input/output files
    string command = settings.pathToBcalm + "bglue -in " + settings.pathToOutput + "temp_bcalm_" + settings.baseFileName + ".h5 -verbose 0 -k " +
                     to_string(settings.kmerSize_bcalm) + " -nb-cores " + to_string(settings.nCores) + " -out " + settings.pathToOutput +
                     "temp_bglue_" + settings.baseFileName;

    // Runs command and stores state
    system(command.c_str());


    fclose(logsOpen);

}
