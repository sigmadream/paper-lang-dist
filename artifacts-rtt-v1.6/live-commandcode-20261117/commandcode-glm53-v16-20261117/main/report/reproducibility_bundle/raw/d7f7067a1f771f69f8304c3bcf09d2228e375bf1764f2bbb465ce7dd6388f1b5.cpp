#include <bits/stdc++.h>
using namespace std;

int main() {
    string m;
    if (!getline(cin, m)) return 0;
    string s;
    for (char c : m) {
        if (c >= 'a' && c <= 'z') s += c;
        else break;
    }
    if (!s.empty()) {
        string r = s;
        reverse(r.begin(), r.end());
        cout << (s == r ? "1" : "0") << "\n";
    }
    return 0;
}