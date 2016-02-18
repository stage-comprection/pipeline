#ifndef UTILS_H
#define UTILS_H

#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <algorithm>

#define LOGOK fprintf(stderr, "ERR : %s:%i\n", __FILE__, __LINE__);

// Generates a conversion table to compute the reverse complement of a DNA sequence
std::vector<char> generateRevCompTable();

// Creates the table for reverse complement to be used as a global variable
const std::vector<char> revCompTable = generateRevCompTable();

// Splits a string into a vector of strings according to a specified delimiter (default: \t)
std::vector<std::string> split(std::string str, const std::string delimiter="\t");

// Sets back a file line index to 0 (getline will start from the beginning of the file again)
void resetFileIndex(std::ifstream& file);

// Computes the reverse complement of a DNA sequence using an accession table
std::string reverseComplement(const std::string& read);

#endif // UTILS_H
