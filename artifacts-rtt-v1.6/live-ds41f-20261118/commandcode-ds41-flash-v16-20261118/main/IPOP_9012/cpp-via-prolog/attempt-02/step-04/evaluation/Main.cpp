#include <iostream>
#include <string>
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