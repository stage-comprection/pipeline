#include "master.h"


// TODO : replace error handling with  cerr << "Error: " << strerror(errno);


using namespace std;

int main(int argc, char *argv[])
{

    // Checks number of arguments
    if(argc < 2){
        cout<<" Error: not enough arguments...\n";
        return -1;
    }

    string baseDirectory = argv[1];
    string settingsFilePath = baseDirectory + "evaluation_settings.ini";

    Master master(settingsFilePath);
    master.computeMetrics();

    cout<<" \n >> Gain = "<<master.output.gain<<"\n\n";

}
