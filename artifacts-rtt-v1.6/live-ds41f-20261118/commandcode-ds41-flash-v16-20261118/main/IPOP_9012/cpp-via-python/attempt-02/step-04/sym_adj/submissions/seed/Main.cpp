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

        int bal = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
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

        cout << (valid ? "YES" : "NO") << '\n';
    }

    return 0;
}