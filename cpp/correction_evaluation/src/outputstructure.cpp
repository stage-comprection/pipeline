#include "outputstructure.h"

OutputStructure::OutputStructure(){

    this->gain = 0;
    this->truePositives = 0;
    this->falsePositives = 0;
    this->falseNegatives = 0;
    this->notCorrectedAndShouldnt = 0;
    this->notCorrectedButShould = 0;
    this->notAligned = 0;
    this->wrongCorrection = 0;
    this->nReadsProcessed = 0;
}




// Writes results to output file
void OutputStructure::exportResults(std::ofstream& outputFile){

    outputFile<<"Gain\tTruePositives\tFalsePositives\tFalseNegatives\tNotCorrectedButShould\tNotCorrectedAndShouldnt\tNotAligned\tReadsProcessed\n";
    outputFile<<this->gain<<"\t"<<this->truePositives<<"\t"<<this->falsePositives<<"\t"<<this->falseNegatives<<"\t"
              <<this->notCorrectedButShould<<"\t"<<this->notCorrectedAndShouldnt<<"\t"<<this->notAligned<<"\t"<<this->nReadsProcessed<<std::endl;
    outputFile.close();
}




// Gain formula (TP-FP)/(TP+FN)
void OutputStructure::computeGain(){

    this->gain = ((float) this->truePositives - (float) this->falsePositives) / ((float) this->truePositives + (float) this->falseNegatives + (float) this->notCorrectedButShould);

}
