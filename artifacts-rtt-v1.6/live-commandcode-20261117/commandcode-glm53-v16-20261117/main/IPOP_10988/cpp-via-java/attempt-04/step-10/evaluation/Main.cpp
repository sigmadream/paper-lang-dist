#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    size_t end = s.size();
    while (end > 0) {
        char c = s[end - 1];
        if (c == '\n' || c == '\r' || c == ' ' || c == '\t') end--;
        else break;
    }
    bool valid = true;
    size_t len = end;
    for (size_t i = 0; i < len / 2; i++) {
        if (s[i] != s[end - 1 - i]) { valid = false; break; }
    }
    cout << (valid ? 1 : 0) << "\n";
    return 0;
}