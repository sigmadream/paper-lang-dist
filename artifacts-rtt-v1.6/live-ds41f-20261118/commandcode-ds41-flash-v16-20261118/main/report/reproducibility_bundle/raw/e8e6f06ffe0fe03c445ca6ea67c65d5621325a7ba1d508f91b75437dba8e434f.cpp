#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;

    string line;
    getline(cin, line);

    for (int i = 0; i < T; ++i) {
        if (!getline(cin, line)) break;

        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }

        bool ok = true;
        int balance = 0;

        for (char c : line) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                if (balance == 0) {
                    ok = false;
                } else {
                    --balance;
                }
            } else {
                ok = false;
            }
        }

        if (balance != 0) ok = false;

        cout << (ok ? "YES\n" : "NO\n");
    }

    return 0;
}