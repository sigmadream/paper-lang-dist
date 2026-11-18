#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;

    while (T--) {
        string s;
        cin >> s;

        int balance = 0;
        bool valid = !s.empty();

        for (char c : s) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                if (balance == 0) {
                    valid = false;
                    break;
                }
                --balance;
            } else {
                valid = false;
                break;
            }
        }

        if (balance != 0) valid = false;

        cout << (valid ? "YES" : "NO") << '\n';
    }

    return 0;
}