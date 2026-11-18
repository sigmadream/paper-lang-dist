#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, int s, int m, int e, vector<pair<int,int>>& out) {
    if (n == 1) { out.push_back({s, e}); return; }
    hanoi(n - 1, s, e, m, out);
    out.push_back({s, e});
    hanoi(n - 1, m, s, e, out);
}

int main() {
    string input;
    getline(cin, input);
    string digits;
    for (char c : input) { if (isdigit((unsigned char)c)) digits += c; else break; }
    int n = stoi(digits);
    cout << ((1LL << n) - 1) << "\n";
    vector<pair<int,int>> moves;
    hanoi(n, 1, 2, 3, moves);
    string out;
    for (auto& [a, b] : moves) {
        out += to_string(a);
        out += ' ';
        out += to_string(b);
        out += '\n';
    }
    fputs(out.c_str(), stdout);
    return 0;
}