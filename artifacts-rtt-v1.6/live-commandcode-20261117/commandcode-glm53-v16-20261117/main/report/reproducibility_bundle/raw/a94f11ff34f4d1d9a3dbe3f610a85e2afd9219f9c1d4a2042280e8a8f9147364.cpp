#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    if (!getline(cin, s)) return 0;
    while (!s.empty() && (s.back() == '\r' || s.back() == '\n' || s.back() == ' ' || s.back() == '\t')) s.pop_back();
    size_t b = 0;
    while (b < s.size() && (s[b] == ' ' || s[b] == '\t' || s[b] == '\r' || s[b] == '\n')) b++;
    s = s.substr(b);
    bool valid = true;
    for (size_t i = 0; i < s.size() / 2; i++) {
        if (s[i] != s[s.size() - 1 - i]) { valid = false; break; }
    }
    cout << (valid ? 1 : 0) << "\n";
    return 0;
}