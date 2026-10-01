#include <iostream>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (!(cin >> t)) {
        return 0;
    }

    while (t--) {
        string s;
        if (!(cin >> s)) {
            break;
        }
        int bal = 0;
        bool valid = true;
        for (char c : s) {
            if (c == '(') {
                bal++;
            } else if (c == ')') {
                bal--;
            }
            if (bal < 0) {
                valid = false;
                break;
            }
        }
        if (bal != 0) {
            valid = false;
        }
        cout << (valid ? "YES" : "NO") << "\n";
    }

    return 0;
}
