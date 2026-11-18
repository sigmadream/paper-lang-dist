#include <iostream>
#include <string>
using namespace std;

bool valid(const string& s) {
    int balance = 0;
    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else {
            if (balance == 0) return false;
            --balance;
        }
    }
    return balance == 0;
}

int main() {
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        string s;
        cin >> s;
        cout << (valid(s) ? "YES" : "NO") << '\n';
    }
    return 0;
}