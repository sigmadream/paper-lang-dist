#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    string s;
    for (char c : line) {
        if (c >= 'a' && c <= 'z') s += c;
        else break;
    }
    if (s.empty()) return 0;
    string r(s.rbegin(), s.rend());
    cout << (s == r ? "1" : "0") << "\n";
    return 0;
}