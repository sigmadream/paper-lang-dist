#include <bits/stdc++.h>
using namespace std;

static bool isSpace(char c) {
    return c == ' ' || c == '\t' || c == '\r' || c == '\n';
}

static string trim(const string& s) {
    size_t a = 0, e = s.size();
    while (a < e && isSpace(s[a])) a++;
    while (e > a && isSpace(s[e - 1])) e--;
    return s.substr(a, e - a);
}

int main() {
    string s, t;
    if (!getline(cin, s)) s = "";
    if (!getline(cin, t)) t = "";
    s = trim(s);
    t = trim(t);
    int counts[26] = {0};
    for (char c : s) counts[c - 'a']++;
    for (char c : t) counts[c - 'a']--;
    for (int x : counts) {
        if (x != 0) {
            cout << 0 << "\n";
            return 0;
        }
    }
    cout << 1 << "\n";
    return 0;
}