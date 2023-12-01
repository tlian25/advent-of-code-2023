// Day
// https://adventofcode.com/2023/day/
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>

using namespace std;

auto read_input() {
    string filename = "../inputs/day00_input.txt";
    cout << "Input file: " << filename << endl;
    string line;
    vector<string> lines;
    ifstream input(filename);
    while (getline(input, line)) {
        lines.push_back(line);
    }
    input.close();
    return lines;
}



void part1() {

}


void part2() {

}


int main() {
    part1();
    part2();
}