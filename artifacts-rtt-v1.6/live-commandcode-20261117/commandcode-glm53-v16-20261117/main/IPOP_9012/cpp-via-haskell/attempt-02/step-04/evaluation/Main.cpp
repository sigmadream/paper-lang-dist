#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    if (!(cin >> t)) return 0;
    string s;
    for (int i = 0; i < t; i++) {
        cin >> s;
        int b = 0;
        bool ok = true;
        for (char c : s) {
            if (c == '(') b++;
            else b--;
            if (b < 0) { ok = false; break; }
        }
        cout << (ok && b == 0 ? "YES" : "NO") << "\n";
    }
    return 0;
}