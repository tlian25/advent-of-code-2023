// Day 1: Trebuchet?!
// https://adventofcode.com/2023/day/1
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>
#include<string>

using namespace std;

auto read_input() {
    string filename = "../inputs/day01_input.txt";
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

// combine first digit and last digit to form a single two digit number

pair<int, int> first_and_last_digit(string s) {
    int first = -1;
    int last = -1;
    for (char c : s) {
        if (c >= '0' and c <= '9') {
            if (first == -1) {
                first = c - '0';
            }
            last = c - '0';
        }
    }
    return make_pair(first, last);
}

int part1() {
    vector<string> lines = read_input();

    int sum = 0;
    for (string s : lines) {
        pair<int, int> digits = first_and_last_digit(s);
        sum += digits.first * 10 + digits.second;
    }
    return sum;
}


unordered_map<string, int> word2int = {
    {"zero", 0},
    {"one", 1},
    {"two", 2},
    {"three", 3},
    {"four", 4},
    {"five", 5},
    {"six", 6},
    {"seven", 7},
    {"eight", 8},
    {"nine", 9}
};

pair<int, int> first_and_last_digit_words(string s) {
    int first = -1;
    int last = -1;
    string ss;
    char c;
    for (int i=0; i<s.length(); i++) {
        // check first if digit
        c = s[i];
        if (c >= '0' and c <= '9') {
            if (first == -1) {
                first = c - '0';
            }
            last = c - '0';
        }
        // else see if is a start of a word
        // check for substring with next 5 chars
        for (int j=1; j<6; j++) {
            ss = s.substr(i, j);
            if (word2int.count(ss)) {
                // cout << ss << endl;
                if (first == -1) {
                    first = word2int[ss];
                }
                last = word2int[ss];
            }
        }
    }
    return make_pair(first, last);
}


int part2() {

    vector<string> lines = read_input();

    int sum = 0;
    for (string s : lines) {
        pair<int, int> digits = first_and_last_digit_words(s);
        sum += digits.first * 10 + digits.second;
    }
    return sum;
}


int main() {
    auto p1 = part1();
    cout << "Part 1: " << p1 << endl;

    cout << "--------------" << endl;

    auto p2 = part2();
    cout << "Part 2: " << p2 << endl;
}