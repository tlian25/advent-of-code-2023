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



auto part1() {


    return 1;
}


auto part2() {


    return 2;
}


int main() {
    auto p1 = part1();
    cout << "Part 1: " << p1 << endl;

    cout << "--------------" << endl;

    auto p2 = part2();
    cout << "Part 2: " << p2 << endl;
}