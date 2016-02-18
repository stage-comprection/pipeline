#include "pipeline.h"

using namespace std;

int main(int argc, char *argv[])
{

    if (argc < 2){
        cout<<"Not enough arguments, exiting..."<<endl;
        return -1;
    }
    // There is only one argument (the base file name, i.e. reads name stripped of '.fasta')

    SettingsStructure settings; // See settings.h for description of the settings structure
    string baseDirectory = argv[1];
    string settingsFilePath = baseDirectory + "/correction_settings.ini";

    settings.loadSettingsFile(settingsFilePath);

    getCorrectedReadsFromBcalm(settings);

    return 0;
}
