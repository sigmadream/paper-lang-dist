#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;

    for (int i = 0; i < T; ++i) {
        string s;
        cin >> s;

        int balance = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
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

        if (i > 0) cout << '\n';
        cout << (valid ? "YES" : "NO");
    }

    return 0;
}