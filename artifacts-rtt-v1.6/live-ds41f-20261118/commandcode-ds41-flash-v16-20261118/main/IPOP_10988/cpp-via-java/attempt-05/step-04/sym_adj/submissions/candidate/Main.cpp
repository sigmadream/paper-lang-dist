#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    if (!(cin >> s)) return 0;

    bool valid = true;
    for (int i = 0; i < (int)s.length() / 2; i++) {
        if (s[i] != s[s.length() - 1 - i]) {
            valid = false;
            break;
        }
    }

    cout << (valid ? 1 : 0) << '\n';
    return 0;
}