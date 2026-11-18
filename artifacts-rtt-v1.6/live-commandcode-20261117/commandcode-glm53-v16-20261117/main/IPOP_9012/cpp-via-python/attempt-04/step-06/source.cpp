#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    string s;
    for (int i = 0; i < t; ++i) {
        cin >> s;
        int bal = 0;
        bool valid = true;
        for (char c : s) {
            if (c == '(') ++bal;
            else --bal;
            if (bal < 0) { valid = false; break; }
        }
        if (bal != 0) valid = false;
        cout << (valid ? "YES" : "NO") << "\n";
    }
    return 0;
}