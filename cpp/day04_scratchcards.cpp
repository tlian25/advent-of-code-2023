// Day 4. Scratchcards
// https://adventofcode.com/2023/day/4
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>

using namespace std;

struct ScratchCard {
    int n;
    set<int> winningnums;
    set<int> mynums;
};

void print_card(ScratchCard* card) {
    cout << "Card: " << card->n << endl << "Winning Nums: ";
    for (auto n : card->winningnums) {
        cout << n << ' ';
    }
    cout << endl;
    cout << "My Nums: ";
    for (auto n : card->mynums) {
        cout << n << ' ';
    }
    cout << endl;
}


set<int> parse_nums(string s, string delimiter = " ") {
    set<int> res;
    size_t pos = 0;
    string next;
    while ((pos = s.find(delimiter)) != string::npos) {
        next = s.substr(0, pos);
        if (next.length() != 0) {
            res.insert(stoi(next));
        }
        s.erase(0, pos + delimiter.length());
    }
    // last item
    if (s.length() > 0) res.insert(stoi(s));
    return res;
}





auto read_input() {
    string filename = "../inputs/day04_input.txt";
    cout << "Input file: " << filename << endl;
    string line;
    vector<ScratchCard*> cards;
    ifstream input(filename);
    while (getline(input, line)) {
        ScratchCard* c = new ScratchCard();
        int idx0 = line.find(" ");
        int idx1 = line.find(':');
        int idx2 = line.find('|');
        c->n = stoi(line.substr(idx0+1, idx1-idx0));
        c->winningnums = parse_nums(line.substr(idx1+2, idx2-idx1-2));
        c->mynums = parse_nums(line.substr(idx2+2));
        cards.push_back(c);
    }
    input.close();
    return cards;
}


int get_wins(ScratchCard* card) {
    set<int> wins;
    set_intersection(card->mynums.begin(), card->mynums.end(),
                    card->winningnums.begin(), card->winningnums.end(),
                    inserter(wins, wins.begin()));
    return wins.size();
}

int score_card(ScratchCard* card) {
    int wins = get_wins(card);
    if (wins == 0) return 0;
    return pow(2, wins-1);
}


auto part1() {
    vector<ScratchCard*> cards = read_input();

    int score = 0;
    for (ScratchCard* card : cards) {
        int s = score_card(card);
        // print_card(card);
        // cout << s << endl;
        score += s;
    }
    return score;
}


auto part2() {
    vector<ScratchCard*> cards = read_input();
    vector<int> counts;
    for (int i=0; i<cards.size(); i++) {
        counts.push_back(1);
    }

    ScratchCard* card;
    int wins;
    int currcount;
    int totalcount = 0;
    for (int i=0; i<cards.size(); i++) {

        card = cards[i];
        currcount = counts[i];
        wins = get_wins(card);

        // Add current count
        totalcount += currcount;

        // increase cards
        for (int j=0; j<wins; j++) {
            counts[i+j+1] += currcount;
        }
    }

    return totalcount;
}


int main() {
    auto p1 = part1();
    cout << "Part 1: " << p1 << endl;

    cout << "--------------" << endl;

    auto p2 = part2();
    cout << "Part 2: " << p2 << endl;
}