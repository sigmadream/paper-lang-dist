#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    if (!getline(cin, s)) s = "";
    // trim leading/trailing whitespace
    size_t b = s.find_first_not_of(" \t\r\n");
    size_t e = s.find_last_not_of(" \t\r\n");
    if (b == string::npos) s = "";
    else s = s.substr(b, e - b + 1);
    bool valid = true;
    int len = s.size();
    for (int i = 0; i < len / 2; i++) {
        if (s[i] != s[len - 1 - i]) { valid = false; break; }
    }
    cout << (valid ? 1 : 0) << "\n";
    return 0;
}