// Day 5: If You Give a Seed a Fertilizer
// https://adventofcode.com/2023/day/5
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>
#include<map>

using namespace std;

class Mapping {
public:
    string src;
    string dst;
    vector<pair<long, long>> src_ranges; 
    map<pair<long, long>, long> dst_ranges;
    Mapping(string src, string dst) {
        this->src = src;
        this->dst = dst;
        src_ranges = {};
        dst_ranges = {};
    }

    string get_src() {
        return this->src;
    }

    string get_dst() {
        return this->dst;
    }

    void add_range(long src_start, long dst_start, long length) {
        long src_end = src_start + length - 1;
        this->src_ranges.push_back(make_pair(src_start, src_end));
        sort(this->src_ranges.begin(), this->src_ranges.end());
        this->dst_ranges[make_pair(src_start, src_end)] = dst_start;
    }

    long get_mapping(long src) {
        pair<long, long> range = this->binary_search(src); 
        if (range.first != -1) {
            long diff = src - range.first;
            return this->dst_ranges[range] + diff;
        }
        return src;
    }

    pair<long, long> binary_search(long src) {
        int i = 0;
        int j = this->src_ranges.size();
        int m;

        while (i < j) {
            m = (i+j) / 2;
            if (this->src_ranges[m].first > src) {
                j = m;
            } else {
                i = m+1;
            }
        }

        pair<long, long> range = this->src_ranges[j-1];
        if (range.first <= src && src <= range.second) {
            return range;
        }
        return make_pair(-1, -1);
    }
};


vector<string> split_string(string s, string delimiter = " ") {
    vector<string> res;
    size_t pos = 0;
    string next;
    while ((pos = s.find(delimiter)) != string::npos) {
        next = s.substr(0, pos);
        if (next.length() != 0) {
            res.push_back(next);
        }
        s.erase(0, pos + delimiter.length());
    }
    // last item
    if (s.length() > 0) res.push_back(s);
    return res;
}


vector<long> parse_seeds(string line) {
    vector<long> res;
    vector<string> split = split_string(line);
    for (int i = 1; i < split.size(); i++) {
        res.push_back(stol(split[i]));
    }
    return res;
}


pair<string, string> parse_mapping_name(string line) {
    int i1 = line.find('-');
    int i2 = line.find('-', i1+1);
    int i3 = line.find(' ');
    return make_pair(line.substr(0, i1), line.substr(i2+1, i3-i2-1));
}

tuple<long, long, long> parse_mapping(string line) {
    vector<string> nums = split_string(line);
    return make_tuple(stol(nums[0]), stol(nums[1]), stol(nums[2]));
}



auto read_input() {
    string filename = "../inputs/day05_input.txt";
    cout << "Input file: " << filename << endl;
    string line;
    ifstream input(filename);

    // First line
    getline(input, line);
    vector<long> seeds = parse_seeds(line);

    Mapping* currmap;
    unordered_map<string, Mapping*> mappings;

    while (getline(input, line)) {
        if (line.find("map") != string::npos) {
            pair<string, string> mapnames = parse_mapping_name(line);
            currmap = new Mapping(mapnames.first, mapnames.second);
            mappings[mapnames.first] = currmap;
        } else if (line != "") {
            tuple<long, long, long> nums = parse_mapping(line);
            currmap->add_range(get<0>(nums), get<1>(nums), get<2>(nums));
        }
    }
    input.close();
    return make_pair(seeds, mappings);
}


long get_location(long seed, unordered_map<string, Mapping*>& mappings) {
    string src = "seed";
    long curr = seed;
    Mapping* currmap;
    while (src != "location") {
        cout << curr << endl;
        Mapping* currmap = mappings[src];
        curr = currmap->get_mapping(curr);
        src = currmap->get_dst();
    }
    return curr;
}


auto part1() {
    auto r = read_input();
    vector<long> seeds = r.first;
    unordered_map<string, Mapping*> mappings = r.second;

    long minloc = LONG_MAX;
    for (long seed : seeds) {
        cout << "Seed " << seed << endl;
        minloc = min(minloc, get_location(seed, mappings));
    }
    return minloc;
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