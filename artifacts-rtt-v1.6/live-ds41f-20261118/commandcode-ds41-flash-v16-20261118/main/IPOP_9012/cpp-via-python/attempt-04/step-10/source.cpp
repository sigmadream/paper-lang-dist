#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (!(cin >> t)) return 0;

    for (int i = 0; i < t; ++i) {
        string s;
        cin >> s;

        int bal = 0;
        bool valid = true;

        for (char ch : s) {
            if (ch == '(') {
                ++bal;
            } else {
                --bal;
            }

            if (bal < 0) {
                valid = false;
                break;
            }
        }

        if (bal != 0) valid = false;

        if (i > 0) cout << '\n';
        cout << (valid ? "YES" : "NO");
    }

    return 0;
}