#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    int end = (int)s.size();
    while (end > 0) {
        char c = s[end - 1];
        if (c == '\n' || c == '\r' || c == ' ' || c == '\t') end--;
        else break;
    }
    bool valid = true;
    int len = end;
    for (int i = 0; i < len / 2; i++) {
        if (s[i] != s[end - 1 - i]) { valid = false; break; }
    }
    cout << (valid ? 1 : 0) << "\n";
    return 0;
}