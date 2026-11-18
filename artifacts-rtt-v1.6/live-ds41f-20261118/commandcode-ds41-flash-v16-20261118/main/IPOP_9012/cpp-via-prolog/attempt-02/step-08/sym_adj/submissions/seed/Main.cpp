#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;

    string dummy;
    getline(cin, dummy);

    for (int i = 0; i < T; ++i) {
        string s;
        if (!getline(cin, s)) break;

        int balance = 0;
        bool ok = true;

        for (char c : s) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                if (balance > 0) {
                    --balance;
                } else {
                    ok = false;
                    break;
                }
            }
        }

        if (ok && balance == 0)
            cout << "YES\n";
        else
            cout << "NO\n";
    }

    return 0;
}