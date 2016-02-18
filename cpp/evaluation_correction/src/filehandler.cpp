#include "filehandler.h"

using namespace std;

// Default constructor for FileHandler class
FileHandler::FileHandler(){

    //
    this->readsSet = "";
    this->reference = "";

    // Initializes paths to useful folders
    this->pathToReadsFolder = "/home/rferon/project/data/reads/";
    this->pathToReferenceFolder = "/home/rferon/project/data/references/";
    this->pathToOutputFolder = "/home/rferon/project/output/SRR959239";

    // Initializes paths to files
    this->readsFilePath = "";
    this->correctedFilePath = "";
    this->referenceFilePath = "";
    this->alignmentFilePath = "";
    this->outputFilePath = "";

    // Global parameters
    this->nFilesForSplitting = 100;
    this->readLength = 100;
    this->nLinesInCorrectedReads = 1;

}




// Gives value to most settings in FileHandler
void FileHandler::updateSettings(string& readsSetName, string& referenceName){

    this->readsSet = readsSetName.erase(readsSetName.size()-6, 6); // ".fasta" has length 6
    this->reference = referenceName;

    // Initializes paths to files
    this->readsFilePath = pathToReadsFolder + readsSet + ".fasta";
    this->correctedFilePath = pathToOutputFolder + "corrected_" + readsSet + ".fasta";
    this->referenceFilePath = pathToReferenceFolder + reference;
    this->alignmentFilePath = pathToOutputFolder + "bowtie_" + readsSet;
    this->outputFilePath = pathToOutputFolder + "gain_" + readsSet;

    // Opens files
    this->originalReadsFile.open(readsFilePath.c_str());
    this->originalReadsFile.open(readsFilePath.c_str());
    this->correctedReadsFile.open(correctedFilePath.c_str());
    this->referenceFile.open(referenceFilePath.c_str());
    this->alignmentFile.open(alignmentFilePath.c_str());
    this->outputFile.open(outputFilePath.c_str());

    // Global parameters
    this->getReadLength();
    this->getLinesInCorrectedReads();

}




// Gets read length from original reads file
void FileHandler::getReadLength(){

    string line;

    resetFileIndex(this->originalReadsFile);

    // Skips header line for the first read (ID)
    getline(this->originalReadsFile, line);
    // Original reads are on one line, I formatted them this way before (in the pipeline)
    getline(this->originalReadsFile, line);

    this->readLength = (uint)line.size();
}




// Gets number of lines for a read from corrected reads file
void FileHandler::getLinesInCorrectedReads(){

    // Corrected reads can be splitted in several lines depending on the program used... We count how many lines for one read.
    string line;
    resetFileIndex(this->correctedReadsFile);
    getline(this->correctedReadsFile, line);

    this->nLinesInCorrectedReads = 0;

    // Counts how many lines are needed for a read.
    do{
        getline(this->correctedReadsFile, line);
        ++this->nLinesInCorrectedReads;
    } while (line[0] not_eq '>');

    --this->nLinesInCorrectedReads; // We counted one more line than necessary (the line with '>')
}




// Skips alignment header lines
string FileHandler::skipAlignmentHeaderLines(){

    string line;

    do{
        getline(this->alignmentFile, line);
    }while (line[0] == '@'); // SAM files sometimes have a bunch of header lines starting with '@'

    return line;
}




// Loads reference genome in memory
void FileHandler::getReferenceGenome(){

    string line;

    while(getline(this->referenceFile, line)){

        // Reference and reads files were processed to have their occurrence order as identifier, therefore no need to store identifier
        if (line[0] not_eq '>'){
            this->referenceGenome.push_back(line);
        }

    }
}




// Cleanup all the temporary files at the end of the program (all temporary files start with 'temp')
void FileHandler::cleanupTempFiles(){

    // Using standard libray, a directory and its content are represented by pointers with specific types
    DIR* directory =  opendir(this->pathToOutputFolder.c_str());
    struct dirent* directoryContent;

    if(!directory) return; // Directory not open

    int deletedFlag;
    vector<int> deleted; // Stores deleted state for each file

    // Iterates over directory content and remove each file starting with 'temp'
    while ((directoryContent=readdir(directory))){
        string fileToBeDeleted = this->pathToOutputFolder + directoryContent->d_name;

        if(fileToBeDeleted.find("temp") != string::npos){
          deletedFlag = remove(fileToBeDeleted.c_str()); // I don't know why my IDE doesn't like my use of remove but it works
          deleted.push_back(deletedFlag);
        }
    }

    closedir(directory);

    int sum = 0;

    for (int n : deleted)
        sum += n;

    if (sum > 0){
        cout<<" Warning: some temporary files were not deleted ... \n\n";
    }
}




// Creates temporary files to store reads
vector<ofstream> FileHandler::createTempFiles(string& name){

    ofstream tempStream;
    string fileName;
    vector<ofstream> streams;

    for(uint i=0; i<this->nFilesForSplitting; ++i){

        fileName = this->pathToOutputFolder + "temp_" + name + "_" + to_string(i) + ".txt";
        tempStream.open(fileName.c_str());
        streams.push_back(move(tempStream));
    }

    return streams;
}




// Splits original reads into a number of files (defined in master)
void FileHandler::splitOriginalReadsFiles(){

    string name = "original";
    vector<ofstream> files = this->createTempFiles(name);

    resetFileIndex(this->originalReadsFile);

    string line;
    int readNumber = 0, fileNumber = 0;

    while(getline(this->originalReadsFile, line)){

        if(line[0]=='>'){
            readNumber = stoi(line.substr(1, line.length()));
            fileNumber = readNumber % this->nFilesForSplitting;
            files[fileNumber]<< line + "\n";
        } else {
            files[fileNumber]<< line + "\n";
        }

    }

    for (uint i=0; i<files.size(); ++i){
        files[i].close();
    }
}




// Splits corrected reads into a number of files (defined in master)
void FileHandler::splitCorrectedReadsFiles(){

    string name = "corrected";
    vector<ofstream> files = this->createTempFiles(name);

    resetFileIndex(this->correctedReadsFile);

    string line;
    int readNumber = 0, fileNumber = 0;

    while(getline(this->correctedReadsFile, line)){

        if(line[0]=='>'){
            readNumber = stoi(line.substr(1, line.length()));
            fileNumber = readNumber % this->nFilesForSplitting;
            files[fileNumber]<< line + "\n";
        } else {
            files[fileNumber]<< line + "\n";
        }

    }

    for (uint i=0; i<files.size(); ++i){
        files[i].close();
    }
}




// Splits reference sequence of reads into a number of files (defined in master)
void FileHandler::splitReferenceReadsFiles(){

    string name = "reference";
    vector<ofstream> files = this->createTempFiles(name);

    resetFileIndex(this->referenceFile);

    int readNumber = 0, fileNumber = 0;
    vector<string> splittedLine;

    string alignmentLine, sequence;

    // Skips alignment header lines
    alignmentLine = this->skipAlignmentHeaderLines();

    do {

        splittedLine = split(alignmentLine);

        readNumber = stoi(splittedLine[0]);

        if (splittedLine[2] not_eq "*"){ // "*" means that alignment was not found for this read

             sequence = this->getReferenceSequence(stoi(splittedLine[2]), stoi(splittedLine[3]), stoi(splittedLine[1]));

         } else {

             sequence = "not_aligned";
         }

        fileNumber = readNumber % this->nFilesForSplitting;
        files[fileNumber]<< ">" + to_string(readNumber) + "\n";
        files[fileNumber]<< sequence + "\n";

    } while (getline(this->alignmentFile, alignmentLine));

    for (uint i=0; i<files.size(); ++i){
        files[i].close();
    }
}




// Extracts the read's sequence from the reference file, using the position given by the SAM output
string FileHandler::getReferenceSequence(const int& seqNumber, const int& position, const uint revComp){

    string referenceRead = this->referenceGenome[seqNumber].substr(position-1, this->readLength);

    // revComp is given by a flag in the SAM output. This flag is set to 16 when the reverse complement was aligned
    if (revComp == 16){
        return reverseComplement(referenceRead);
    }

    return referenceRead;
}




// Reconstructs read vector from temporary files
vector<Read> FileHandler::getReadsFromTempFiles(const uint batchNumber){


    vector<Read> reads;
    ifstream originalReads, correctedReads, referenceReads;
    Read tempRead;
    string line;
    int readNumber = 0;

    originalReads.open(this->pathToOutputFolder + "temp_original_" + to_string(batchNumber) + ".txt");
    correctedReads.open(this->pathToOutputFolder + "temp_corrected_" + to_string(batchNumber) + ".txt");
    referenceReads.open(this->pathToOutputFolder + "temp_reference_" + to_string(batchNumber) + ".txt");

    resetFileIndex(originalReads);
    resetFileIndex(correctedReads);
    resetFileIndex(referenceReads);

    while(getline(originalReads, line)){

        if (line[0] == '>'){
            tempRead.identifier = line.substr(1, line.length());
        } else if (line.size() > 2){
            tempRead.originalSequence = line;
            reads.push_back(tempRead);
        }
    }

    sort(reads.begin(), reads.end());

    while(getline(correctedReads, line)){

        if (line[0] == '>'){

            readNumber = stoi(line.substr(1))/this->nFilesForSplitting;

            // Keeps storing lines until reaching desired value (when reads are splitted in several lines)
            for (uint i=0; i<this->nLinesInCorrectedReads; ++i){

                getline(correctedReads, line);

                // Reads are sorted (since their names have been based on their order) therefore we can directly access a read by its identifier
                reads[readNumber].correctedSequence += line;

            }
        }
    }

    while(getline(referenceReads, line)){

        if (line[0] == '>'){

            readNumber = stoi(line.substr(1,line.length()))/this->nFilesForSplitting;
            getline(referenceReads, line);
            // Reads are sorted (since their names have been based on their order) therefore we can directly access a read by its identifier
            reads[readNumber].referenceSequence += line;
        }

    }

    originalReads.close();
    correctedReads.close();
    referenceReads.close();

    return reads;
}
