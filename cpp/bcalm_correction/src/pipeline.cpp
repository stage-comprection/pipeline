#include "pipeline.h"

using namespace std;


// Runs bcalm + bglue to obtain DB graph (represented by a list of unitigs)
void getUnitigs(SettingsStructure& settings){

    runBcalm(settings);
    runBglue(settings);

}




// Format bglue output (list of unitigs) : gives each unitig an identifier based on its order of occurrence (first unitig: >0, second unitig: >1 ...)
void formatBglueOutput(SettingsStructure& settings){

    string bglueOutputPath = settings.pathToOutput + "temp_bglue_" + settings.baseFileName;
    string formattedOutputPath = settings.pathToOutput + "temp_formatted_bglue_" + settings.baseFileName;
    ifstream bglueOutput;
    ofstream formattedOutput;

    bglueOutput.open(bglueOutputPath.c_str());
    formattedOutput.open(formattedOutputPath.c_str());

    string line;
    int count=0;

    while(getline(bglueOutput, line)){

        if(line[0] == '>'){
            formattedOutput<<line + to_string(count)<<endl;
            ++count;
        } else formattedOutput<<line<<endl;
    }

    bglueOutput.close();
    formattedOutput.close();

}




// Generates an unique file to store reads unmapped by bgreat (for now they're splitted in two files)
void concatenateFiles(SettingsStructure& settings, vector<string>& inputFileNames, string outputName ){

    // Opens output file
    string concatenatedOutputPath = settings.pathToOutput + outputName + settings.baseFileName + ".fasta";
    ofstream concatenatedOutput;
    concatenatedOutput.open(concatenatedOutputPath.c_str());

    // Opens input files and write them into the output file
    string tempFilePath, line;
    ifstream tempInput;

    for (uint i=0; i<inputFileNames.size(); ++i){

        tempFilePath = settings.pathToOutput + inputFileNames[i] + settings.baseFileName;
        tempInput.open(tempFilePath.c_str());

        while(getline(tempInput, line)){
            concatenatedOutput<<line<<endl;
        }

        tempInput.close();
    }

}




// Cleanup all the temporary files at the end of the program (all temporary files start with 'temp')
void cleanupTempFiles(SettingsStructure& settings){

    // Using standard libray, a directory and its content are represented by pointers with specific types
    DIR* directory =  opendir(settings.pathToOutput.c_str());
    struct dirent* directoryContent;

    if(!directory) return; // Directory not open

    int deletedFlag;
    vector<int> deleted; // Stores deleted state for each file

    // Iterates over directory content and remove each file starting with 'temp'
    while ((directoryContent=readdir(directory))){
        string fileToBeDeleted = settings.pathToOutput + directoryContent->d_name;

        if(fileToBeDeleted.find("temp") != string::npos){
          deletedFlag = remove(fileToBeDeleted.c_str()); // I don't know why my IDE doesn't like my use of remove but it works
          deleted.push_back(deletedFlag);
        }
    }

    closedir(directory);

    int sum = 0;

    for (int n : deleted)
        sum += n;
}




// Pipeline per se, runs all commands and checks if they executed correctly
void getCorrectedReadsFromBcalm(SettingsStructure& settings){

    getUnitigs(settings);

    formatBglueOutput(settings);

    runBgreat(settings);

    vector<string> files {"temp_bgreat_noAlign_", "temp_bgreat_noOverlap_"};
    string outputName = "temp_bgreat_uncorrected_";
    concatenateFiles(settings, files , outputName);

    buildBowtieIndex(settings);

    runBowtie(settings);

    getReadsFromReference(settings);

    vector<string> files2 {"temp_bgreat_corrected_", "temp_bowtie_corrected_"};
    outputName = "corrected_";
    concatenateFiles(settings, files2 , outputName);

    cleanupTempFiles(settings);

}
