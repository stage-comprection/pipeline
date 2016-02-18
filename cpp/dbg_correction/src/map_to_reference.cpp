#include "map_to_reference.h"

using namespace std;


// Loads reference genome in memory as a vector of sequences. Identifiers are not stored because the reference file is processed before and sequence names are
// set to the order of the sequence (first sequence is >0, second is >1 ...)
vector<string> getReferenceGenome(ifstream& referenceFile){

    string line;
    vector<string> referenceGenome;

    while(getline(referenceFile, line)){

        if (line[0] not_eq '>'){
            referenceGenome.push_back(line);
        }

    }

    return referenceGenome;
}




// Returns sequence from a reference based on parameters obtained in the SAM output file (reference sequence number and position on this sequence).
string getReferenceSequence(vector<string>& referenceGenome, const int& seqNumber, const int& position, int& readLength, const uint revComp){

    string referenceRead = referenceGenome[seqNumber].substr(position-1, readLength);

    if (revComp == 16){ // SAM file has a flag set to 16 when reverse complement was aligned (not entirely true, maybe need to check that later)
        return reverseComplement(referenceRead);
    }

    return referenceRead;
}




// Extracts information from the alignment SAM output file, gets corrected reads sequence from the DB graph (the reference genome here) and stores these corrected
// reads in an output file.
int getReadsFromReference(SettingsStructure& settings){

    // Opens all required files
    ifstream alignmentFile, referenceGenomeFile;
    ofstream correctedReadsFile;

    alignmentFile.open(settings.pathToOutput + "temp_aligned_" + settings.baseFileName);
    correctedReadsFile.open(settings.pathToOutput + "temp_bowtie_corrected_" + settings.baseFileName);

    string pathToReferenceGenome = settings.pathToOutput + "temp_formatted_bglue_" + settings.baseFileName;

    referenceGenomeFile.open(pathToReferenceGenome.c_str());

    vector<string> referenceGenome = getReferenceGenome(referenceGenomeFile); // Loads reference genome in memory (DB graph contigs here)
    string line;

    // Skip SAM header lines - starting with a '@'
    while(getline(alignmentFile, line)){

        if (alignmentFile.peek() != '@'){
            break;
        }

    }

    vector<string> splittedLine;
    string correctedSequence, name;

    // Reads through the alignment SAM output file and for each line (i.e. each read) gets the corrected sequence from the reference (DB graph contigs)
    // if the read has been aligned. Otherwise read will be marked as 'not_corrected'. Results are stored in output file.
    while(getline(alignmentFile, line)){

        splittedLine = split(line); // Split function is in utils, splits by '\t' by default
        name = splittedLine[0];
        int size = static_cast<int>(splittedLine[9].size());

        if (splittedLine[2] != "*"){ // If "*" the read hasn't been aligned, therefore it's marked as 'not_corrected'
            correctedSequence = getReferenceSequence(referenceGenome, stoi(splittedLine[2]), stoi(splittedLine[3]), size, stoi(splittedLine[1]));
            correctedReadsFile<<">" + name + "\n" + correctedSequence + "\n";
        } else{
            correctedReadsFile<<">" + name + "\n" + "not_corrected" + "\n";
        }

    }

    alignmentFile.close();
    correctedReadsFile.close();

    return 0;
}


