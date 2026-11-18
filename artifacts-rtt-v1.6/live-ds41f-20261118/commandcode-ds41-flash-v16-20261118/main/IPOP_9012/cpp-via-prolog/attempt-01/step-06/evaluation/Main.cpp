#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    while (T--) {
        string s;
        getline(cin, s);

        int balance = 0;
        bool ok = true;

        for (char c : s) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                if (balance == 0) {
                    ok = false;
                    break;
                }
                --balance;
            }
        }

        if (balance != 0) ok = false;

        cout << (ok ? "YES" : "NO") << '\n';
    }

    return 0;
}