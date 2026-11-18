#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    string s;
    ostringstream out;
    while (t-- > 0) {
        if (!(cin >> s)) break;
        int bal = 0;
        bool valid = true;
        for (char c : s) {
            if (c == '(') bal++;
            else bal--;
            if (bal < 0) { valid = false; break; }
        }
        if (bal != 0) valid = false;
        out << (valid ? "YES" : "NO") << '\n';
    }
    cout << out.str();
    return 0;
}