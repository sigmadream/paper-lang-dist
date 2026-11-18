#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!(cin >> first)) return 0;

    int t = stoi(first);

    for (int i = 1; i <= t; ++i) {
        string s;
        if (!(cin >> s)) s = "";

        int balance = 0;
        bool valid = true;

        for (char ch : s) {
            if (ch == '(') {
                ++balance;
            } else {
                --balance;
            }

            if (balance < 0) {
                valid = false;
                break;
            }
        }

        if (balance != 0) valid = false;

        cout << (valid ? "YES" : "NO") << '\n';
    }

    return 0;
}