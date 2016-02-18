#include "read.h"

#include <iostream>

using namespace std;


// Constructor for Read object
Read::Read(){

    identifier = "";
    originalSequence = "";
    correctedSequence = "";
    referenceSequence = "";

}




// Compares two reads and returns the positions of difference between thoses reads
void Read::analyze(OutputStructure& output){

    // In case something was removed during correction or the reference is smaller/bigger...
    uint minimumLength = min(this->originalSequence.size(), this->referenceSequence.size());
    minimumLength = min(minimumLength, (uint) this->correctedSequence.size());

    /* How are values computed:
     * If base is corrected and correction is right (same as reference), true positive
     * If base is corrected but correction is wrong (not the reference), false positive
     * If base is not corrected but original is different from reference, false negative
     */

    if (this->referenceSequence == "not_aligned"){

        ++output.notAligned;

    } else {

        for (uint i=0; i<minimumLength; ++i){

            if (this->originalSequence[i] != this->referenceSequence[i]){

                if (this->correctedSequence != "not_corrected"){

                    if (this->correctedSequence[i] == this->referenceSequence[i]){

                        ++output.truePositives;

                    } else if (this->correctedSequence[i] != this->originalSequence[i]){

                        ++output.wrongCorrection;

                    } else {

                        ++output.falseNegatives;
                    }

                } else {

                    ++output.notCorrectedButShould;
                }

            } else if (this->correctedSequence != "not_corrected"){

                if (this->correctedSequence[i] != this->originalSequence[i]){

                    ++output.falsePositives;
                }

            } else {

                ++output.notCorrectedAndShouldnt;
            }

        }
    }

    ++output.nReadsProcessed;

}
