#include<set>
#include<string>

using namespace std;

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