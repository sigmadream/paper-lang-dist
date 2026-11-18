#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    int t = stoi(line);
    string out;
    for (int i = 0; i < t; i++) {
        string s;
        if (!getline(cin, s)) break;
        // trim
        size_t b = s.find_first_not_of(" \t\r\n");
        size_t e = s.find_last_not_of(" \t\r\n");
        if (b == string::npos) s.clear();
        else s = s.substr(b, e - b + 1);
        int bal = 0;
        bool valid = true;
        for (char c : s) {
            if (c == '(') bal++;
            else bal--;
            if (bal < 0) { valid = false; break; }
        }
        if (bal != 0) valid = false;
        out += valid ? "YES" : "NO";
        out += '\n';
    }
    cout << out;
    return 0;
}