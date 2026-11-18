#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    int t = stoi(line);
    string out;
    for (int i = 0; i < t; i++) {
        string s;
        if (!getline(cin, s)) break;
        while (!s.empty() && (s.back() == '\r' || s.back() == ' ' || s.back() == '\n')) s.pop_back();
        size_t b = 0;
        while (b < s.size() && (s[b] == ' ' || s[b] == '\t')) b++;
        s = s.substr(b);
        bool valid = true;
        int bal = 0;
        for (char c : s) {
            if (c == '(') bal++;
            else bal--;
            if (bal < 0) { valid = false; break; }
        }
        if (bal != 0) valid = false;
        out += valid ? "YES\n" : "NO\n";
    }
    cout << out;
    return 0;
}