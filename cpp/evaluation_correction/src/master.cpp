#include "master.h"

//#include <errno.h>

using namespace std;


// Default constructor
Master::Master(){

}




// Standard constructor to use (reads settings from configuration file)
Master::Master(string& settingsFilePath){

    this->fileHandler = FileHandler();
    vector<string> settings = readSettingsFile(settingsFilePath);
    this->fileHandler.updateSettings(settings[0], settings[1]);
}




// Calculates the gain obtained after correction, using the number of True Positives, False Positives and False Negatives
void Master::computeMetrics(){

    // Loads reference genome in memory
    this->fileHandler.getReferenceGenome();

    // Gets original, corrected and reference sequences and stores them in temporary files (assigns one thread to each process)
    thread splitOriginal(&FileHandler::splitOriginalReadsFiles, &this->fileHandler);
    thread splitCorrected(&FileHandler::splitCorrectedReadsFiles, &this->fileHandler);
    thread splitReference(&FileHandler::splitReferenceReadsFiles, &this->fileHandler);

    // Synchronizes threads:
    splitOriginal.join();
    splitCorrected.join();
    splitReference.join();

    uint threadNumber = 0;
    vector<thread> threads;

    while (threadNumber < this->fileHandler.nFilesForSplitting){

        threads.resize(0);

        for (uint j=0; j<this->nThreads; ++j){

            threads.push_back(thread(&Master::processOneBatch, this, threadNumber));
            ++threadNumber;
        }

        for(auto &t : threads){
             t.join();
        }
    }

    this->fileHandler.cleanupTempFiles();

    this->output.computeGain();
    this->output.exportResults(this->fileHandler.outputFile);
}




// Loads small read files in memory, compares original/corrected/reference sequences and increments counters accordingly
void Master::processOneBatch(uint batchNumber){

    vector<Read> reads = this->fileHandler.getReadsFromTempFiles(batchNumber);

    for (uint i=0; i<reads.size(); ++i){

        reads[i].analyze(this->output);
    }
}




// Reads settings from configuration file
vector<string> Master::readSettingsFile(string& settingsFilePath){

    ifstream settingsFile;
    settingsFile.open(settingsFilePath);

    string line, key, value;
    vector<string> splittedLine, output;

    string tempReadSet = "null", tempReference = "null";

    while(getline(settingsFile, line)){

        splittedLine = split(line, "=");
        key = splittedLine[0];
        value = splittedLine[1];

        if (key =="nThreads"){
            this->nThreads = stoi(value);
        }
        else if (key =="readsFolderPath"){
            this->fileHandler.pathToReadsFolder = value;
        }
        else if (key =="referenceFolderPath"){
            this->fileHandler.pathToReferenceFolder = value;
        }
        else if (key =="outputFolderPath"){
            this->fileHandler.pathToOutputFolder = value;
        }
        else if (key =="nTempFiles"){
            this->fileHandler.nFilesForSplitting = stoi(value);
        }
        else if (key =="readSet"){
            tempReadSet = value;
        }
        else if (key =="reference"){
            tempReference = value;
        }

    }

    settingsFile.close();

    if (tempReadSet != "null"){
        output.push_back(tempReadSet);
    } else {
        cout<<"\n     Error: cannot find read set name in settings file, exiting... \n";
    }

    if (tempReadSet != "null"){
        output.push_back(tempReference);
    } else {
        cout<<"\n     Error: cannot find read set name in settings file, exiting... \n";
    }



    return output;
}
