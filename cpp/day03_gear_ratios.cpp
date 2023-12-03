// Day 3: Gear Ratios
// https://adventofcode.com/2023/day/3
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>
#include<tuple>
#include<map>

using namespace std;


char SPACE = '.';
char GEAR = '*';

auto read_input() {
    string filename = "../inputs/day03_input.txt";
    cout << "Input file: " << filename << endl;
    string line;
    vector<vector<char>> grid;
    ifstream input(filename);
    while (getline(input, line)) {

        vector<char> row;
        for (char c : line) {
            row.push_back(c);
        }
        row.push_back(SPACE); // add extra space to mark end of line for parsing
        grid.push_back(row);
    }
    input.close();
    return grid;
}


bool is_digit(char c) {
    return c >= '0' && c <= '9';
}


bool is_symbol(char c) {
    return c != SPACE && !is_digit(c);
}


vector<tuple<int, int, int>> find_numbers(vector<vector<char>>& grid) {
    vector<tuple<int, int, int>> nums;
    vector<char> n;
    int row = -1;
    int col = -1;

    for (int r=0; r<grid.size(); r++) {
        for (int c=0; c<grid[0].size(); c++) {
            // cout << r << ' ' << c << ' ' << grid[r][c] << endl;
            if (!is_digit(grid[r][c])) {
                if (!n.empty()) {
                    int num = stoi(string(n.begin(), n.end()));
                    // cout << "Num: " << num << endl;
                    nums.push_back(tuple(num, row, col));
                    // reset
                    n.clear();
                    row = -1;
                    col = -1;
                }
            } else {
                n.push_back(grid[r][c]);
                // Track start
                if (row == -1) row = r;
                if (col == -1) col = c;
            }
        }
    }
    return nums;
};


vector<pair<int, int>> DIRS = {
    make_pair(1,0),
    make_pair(-1,0),
    make_pair(0,1),
    make_pair(0,-1),
    make_pair(1,1),
    make_pair(1,-1),
    make_pair(-1,1),
    make_pair(-1,-1)
};


bool search_symbol(int r, int c, vector<vector<char>>& grid) {
    while (is_digit(grid[r][c])) {
        // search in all 8 directions
        for (auto d : DIRS) {
            int nr = r + d.first;
            int nc = c + d.second;
            if (nr >= 0 && nr < grid.size() && nc >= 0 && nc < grid[0].size()) {
                if (is_symbol(grid[nr][nc])) return true;
            }
        }
        c++;
    }
    return false;
}


pair<vector<int>, vector<int>> find_parts(vector<tuple<int, int, int>>& nums, vector<vector<char>>& grid) {
    vector<int> parts = {};
    vector<int> nonparts = {};

    for (auto t : nums) {
        int n = get<0>(t);
        int r = get<1>(t);
        int c = get<2>(t);
        // search to the right and see if any surrounding is a symbol
        if (search_symbol(r, c, grid)) {
            parts.push_back(n);
        } else {
            nonparts.push_back(n);
        }
    }
    return make_pair(parts, nonparts);
}


auto part1() {
    auto grid = read_input();
    auto nums = find_numbers(grid);
    auto split = find_parts(nums, grid);
    vector<int> parts = split.first;
    vector<int> nonparts = split.second;

    int res = 0;
    for (int p : parts) {
        res += p;
    }

    return res;
}


pair<int, int> search_gear(int r, int c, vector<vector<char>>& grid) {
    while (is_digit(grid[r][c])) {
        // search in all 8 directions
        for (auto d : DIRS) {
            int nr = r + d.first;
            int nc = c + d.second;
            if (nr >= 0 && nr < grid.size() && nc >= 0 && nc < grid[0].size()) {
                if (grid[nr][nc] == GEAR) return make_pair(nr, nc);
            }
        }
        c++;
    }
    return make_pair(-1, -1);
}



map<pair<int, int>, vector<int>> find_gear_ratios(vector<tuple<int, int, int>>& nums, vector<vector<char>>& grid) {
    map<pair<int, int>, vector<int>> gears;
    pair<int, int> gear;

    for (auto t : nums) {
        int n = get<0>(t);
        int r = get<1>(t);
        int c = get<2>(t);
        // search to the right and see if any surrounding is a symbol
        gear = search_gear(r, c, grid);
        if (gear.first != -1) {
            gears[gear].push_back(n);
        }
    }
    return gears;
}


auto part2() {
    auto grid = read_input();
    auto nums = find_numbers(grid);
    auto gears = find_gear_ratios(nums, grid);

    int res = 0;
    for (auto g : gears) {
        if (g.second.size() == 2) {
            res += g.second[0] * g.second[1];
        }
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