#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    // strip trailing whitespace/newline
    while (!s.empty() && (s.back() == '\n' || s.back() == '\r' || s.back() == ' ')) s.pop_back();
    if (s.empty()) return 0;
    string r = s;
    reverse(r.begin(), r.end());
    cout << (s == r ? 1 : 0) << "\n";
    return 0;
}