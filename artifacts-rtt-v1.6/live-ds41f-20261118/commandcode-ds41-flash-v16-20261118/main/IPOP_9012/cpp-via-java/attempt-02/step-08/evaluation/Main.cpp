#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;

    while (T-- > 0) {
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

        cout << (valid ? "YES\n" : "NO\n");
    }

    return 0;
}