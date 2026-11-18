#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    if (!getline(cin, s)) s = "";
    if (!getline(cin, t)) t = "";
    // trim
    auto trim = [](const string& str) {
        size_t a = str.find_first_not_of(" \t\r\n");
        size_t z = str.find_last_not_of(" \t\r\n");
        if (a == string::npos) return string("");
        return str.substr(a, z - a + 1);
    };
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