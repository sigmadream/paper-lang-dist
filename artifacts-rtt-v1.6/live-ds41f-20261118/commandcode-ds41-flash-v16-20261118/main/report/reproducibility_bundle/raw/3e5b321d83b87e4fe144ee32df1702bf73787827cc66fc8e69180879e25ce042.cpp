#include <iostream>
#include <string>

bool isValid(const std::string& s) {
    int balance = 0;
    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            if (balance <= 0) return false;
            --balance;
        } else {
            return false;
        }
    }
    return balance == 0;
}

int main() {
    int t;
    if (!(std::cin >> t)) return 0;

    for (int i = 0; i < t; ++i) {
        std::string s;
        std::cin >> s;
        std::cout << (isValid(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}