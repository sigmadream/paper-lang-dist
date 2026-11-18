#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    string line;

    if (!(cin >> T)) return 0;
    getline(cin, line);

    for (int i = 0; i < T; ++i) {
        string s;
        if (!getline(cin, s)) break;

        if (!s.empty() && s.back() == '\r') s.pop_back();

        int bal = 0;
        bool ok = true;

        for (char c : s) {
            if (c == '(') {
                ++bal;
            } else if (c == ')') {
                if (bal == 0) {
                    ok = false;
                } else {
                    --bal;
                }
            }
        }

        if (bal != 0) ok = false;

        cout << (ok ? "YES" : "NO") << '\n';
    }

    return 0;
}