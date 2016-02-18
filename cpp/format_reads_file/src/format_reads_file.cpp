#include <stdio.h>
#include <string>
#include <fstream>
#include <iostream>


using namespace std;

void formatReadsFile(string& readsFilePath){

    ifstream readsFile;
    string originalreadsFile = readsFilePath + ".backup";
    readsFile.open(originalreadsFile.c_str());

    ofstream formattedReadsFile;
    formattedReadsFile.open(readsFilePath.c_str());

    string line;
    bool start = false;
    uint count = 0;

    while(getline(readsFile, line)){

        if(line[0] == '>'){

            if (!start){

                formattedReadsFile << '>' + to_string(count) + '\n';
                start = true;

            }else {

                formattedReadsFile << "\n>" + to_string(count) + '\n';

            }

            ++count;

        }else {

            formattedReadsFile << line;
        }
    }

    readsFile.close();
    formattedReadsFile.close();
}



int main(int argc, char *argv[]){

    if (argc < 2){
        cout<<"\nError : not enough arguments, exiting...\n";
        return -1;
    }

    string fileName = argv[1];
    string readsFilePath = "/home/rferon/project/data/reads/" + fileName;
    formatReadsFile(readsFilePath);
    return 0;
}

