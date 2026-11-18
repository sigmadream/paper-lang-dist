#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    if (!getline(cin, s)) return 0;
    int b = 0, e = (int)s.size();
    while (e > 0 && (s[e-1]=='\r' || s[e-1]=='\n' || s[e-1]==' ' || s[e-1]=='\t')) e--;
    while (b < e && (s[b]==' ' || s[b]=='\t' || s[b]=='\r' || s[b]=='\n')) b++;
    string t = s.substr(b, e - b);
    bool valid = true;
    for (size_t i = 0; i < t.size()/2; i++) {
        if (t[i] != t[t.size()-1-i]) { valid = false; break; }
    }
    cout << (valid ? 1 : 0) << "\n";
    return 0;
}