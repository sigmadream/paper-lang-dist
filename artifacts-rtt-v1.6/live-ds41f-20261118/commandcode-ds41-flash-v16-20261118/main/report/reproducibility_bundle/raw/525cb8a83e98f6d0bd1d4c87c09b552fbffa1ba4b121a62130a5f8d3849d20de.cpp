#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!getline(cin, first)) return 0;

    first.erase(remove(first.begin(), first.end(), '\r'), first.end());

    int T = stoi(first);

    for (int i = 0; i < T; ++i) {
        string line;
        if (!getline(cin, line)) break;

        line.erase(remove(line.begin(), line.end(), '\r'), line.end());

        int balance = 0;
        bool ok = true;

        for (char c : line) {
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