#include <iostream>
#include <string>
using namespace std;

bool isValid(const string& s) {
    int balance = 0;
    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            if (balance == 0) return false;
            --balance;
        } else {
            return false;
        }
    }
    return balance == 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (!(cin >> t)) return 0;

    for (int i = 0; i < t; ++i) {
        string s;
        cin >> s;
        cout << (isValid(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}