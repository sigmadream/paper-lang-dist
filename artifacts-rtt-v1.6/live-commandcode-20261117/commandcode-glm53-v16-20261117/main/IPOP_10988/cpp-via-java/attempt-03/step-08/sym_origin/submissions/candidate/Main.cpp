#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    // trim whitespace
    size_t b = s.find_first_not_of(" \t\r\n");
    size_t e = s.find_last_not_of(" \t\r\n");
    if (b == string::npos) s = "";
    else s = s.substr(b, e - b + 1);
    bool valid = true;
    size_t len = s.size();
    for (size_t i = 0; i < len / 2; i++) {
        if (s[i] != s[len - 1 - i]) { valid = false; break; }
    }
    cout << (valid ? 1 : 0) << "\n";
    return 0;
}