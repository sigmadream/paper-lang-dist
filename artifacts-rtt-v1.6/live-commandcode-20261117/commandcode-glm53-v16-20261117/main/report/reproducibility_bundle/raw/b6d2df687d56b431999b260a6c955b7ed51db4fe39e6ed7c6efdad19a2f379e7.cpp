#include <bits/stdc++.h>
using namespace std;

static bool isSpace(char c) {
    return c == ' ' || c == '\t' || c == '\r' || c == '\n';
}

static string trim(const string& str) {
    size_t a = 0, z = str.size();
    while (z > a && isSpace(str[z - 1])) z--;
    while (a < z && isSpace(str[a])) a++;
    return str.substr(a, z - a);
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
    bool ok = true;
    for (int x : counts) if (x != 0) { ok = false; break; }
    cout << (ok ? 1 : 0) << "\n";
    return 0;
}