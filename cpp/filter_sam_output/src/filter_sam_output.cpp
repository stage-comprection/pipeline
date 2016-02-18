#include "./utils/src/utils.h"

#include <iostream>

using namespace std;

int main (int argc, char *argv[]) {

    if (argc < 2){
        cout<< "    Error: not enough argument, exiting"<<endl;
        return -1;
    }

    string outputFilePath = argv[1];

    ofstream output;
    output.open(outputFilePath);

    char line[5000];
    string splittedLine;
    int size;

    while(cin.getline(line, 5000)){

        splittedLine = split(line); // Split function is in utils, splits by '\t' by default
        output << splittedLine[0] <<"\t";

        /* SAM output organisation (only relevant fields):
         * 0. Identifier / name of the aligned read
         * 1. Flag for read features  (only used for revComp)
         * 2. Identifier / name of the reference sequence on which the read aligns ( = '*' if no alignment)
         * 3. Starting position of the read on the reference sequence (1-based offset)
         * 9. Read sequence
         */

        if (splittedLine[2] != "*"){

            output << splittedLine[2]<< "\t" << splittedLine[3] << "\t";
            size = static_cast<int>(splittedLine[9].size());
            output << size << "\t";

            if (size >= 16 and size < 32 ){
                output << "1" << "\n";
            } else {
                output << "0" << "\n";
            }

        } else {
            output << "not_aligned\n";
        }

    }

  return 0;
}
