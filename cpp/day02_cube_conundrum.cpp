// Day 2: Cube Conundrum
// https://adventofcode.com/2023/day/2
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>
#include<deque>

using namespace std;

deque<string> splitstring(string s, string delimiter = " ") {
    deque<string> res;
    int l = delimiter.size();
    int end = s.size();
    int p = 0;
    while (p != -1 && p < end) {
        p = s.find(delimiter);
        res.push_back(s.substr(0, p));
        s.erase(0, p+l);
    }
    return res;
}

void printSubgame(unordered_map<string, int>& subgame) {
    for (auto m : subgame) {
        cout << m.first << ": " << m.second << " | ";
    }
    cout << endl;
}


class Game {
public:
    int number;
    deque<string> subgames;
    Game(int number) {
        this->number = number;
    }

    bool hasNextSubgame() {
        return !subgames.empty();
    }

    unordered_map<string, int> getNextSubgame() {
        unordered_map<string, int> game;
        string s = subgames.front();
        subgames.pop_front(); 
        // 3 blue, 1 red
        for (string c : splitstring(s, ", ")) {
            // 3 blue
            deque<string> cc = splitstring(c, " ");
            game[cc[1]] += stoi(cc[0]);
        }
        return game;
    }

    int getNumber() {
        return this->number;
    }
};

auto read_input() {
    string filename = "../inputs/day02_input.txt";
    cout << "Input file: " << filename << endl;
    string line;
    vector<Game*> games;
    ifstream input(filename);
    while (getline(input, line)) {
        int i = line.find(" ");
        int j = line.find(":");
        int num = stoi(line.substr(i, j-i));
        Game* g = new Game(num);
        g->subgames = splitstring(line.substr(j+2), "; ");
        games.push_back(g);
    }
    input.close();
    return games;
}

// Red, green or blue cubes
// secret number of cubes of each color in the bag
// goal is to figure out info about the number of cubes

// Which gamves would be possilbe with
const string RED = "red";
const string BLUE = "blue";
const string GREEN = "green";

unordered_map<string, int> BAG = {
    {RED, 12},
    {GREEN, 13},
    {BLUE, 14}
};


bool isPossible(unordered_map<string, int>& subgame, unordered_map<string, int>& bag) {
    for (auto c : subgame) {
        if (bag.count(c.first) && bag[c.first] >= subgame[c.first]) {
            continue;
        }
        return false;
    }
    return true;
}


int part1() {
    vector<Game*> games = read_input();
    int res = 0;

    for (Game* g : games) {
        bool possible = true;
        while (possible && g->hasNextSubgame()) {
            unordered_map<string, int> subgame = g->getNextSubgame();
            possible = isPossible(subgame, BAG);
        }
        if (possible) res += g->getNumber();
    }
    return res;
}


// fewest number of cubes of each color that could have made the game possible
// power of a set of cubes is equal to number of R, G, B multiplied together
// sum of power for each game

void updateMaxCubes(unordered_map<string, int>& subgame, unordered_map<string, int>& maxCubes) {
    for (auto s : subgame) {
        maxCubes[s.first] = max(maxCubes[s.first], s.second);
    }
}


int part2() {
    vector<Game*> games = read_input();
    int res = 0;
    for (Game* g : games) {
        unordered_map<string, int> maxCubes = {{RED, 0}, {BLUE, 0}, {GREEN, 0}};
        // need to track max of every color type
        while (g->hasNextSubgame()) {
            unordered_map<string, int> subgame = g->getNextSubgame();
            updateMaxCubes(subgame, maxCubes);
        }

        // Take power
        int pow = 1;
        for (auto m : maxCubes) {
            pow *= m.second;
        }
        res += pow;
    }
    return res;
}


int main() {
    auto p1 = part1();
    cout << "Part 1: " << p1 << endl;

    cout << "--------------" << endl;

    auto p2 = part2();
    cout << "Part 2: " << p2 << endl;
}