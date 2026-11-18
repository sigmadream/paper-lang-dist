#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;

    string line;
    getline(cin, line);

    while (T--) {
        string s;
        getline(cin, s);

        int balance = 0;
        bool ok = true;

        for (char c : s) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                if (balance <= 0) {
                    ok = false;
                    break;
                }
                --balance;
            }
        }

        if (ok && balance == 0) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }

    return 0;
}