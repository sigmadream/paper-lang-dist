#include <iostream>
#include <string>
#include <vector>

std::string check(const std::string& s) {
    int balance = 0;
    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            if (balance == 0) {
                return "NO";
            }
            --balance;
        }
    }
    return balance == 0 ? "YES" : "NO";
}

int main() {
    int t;
    if (!(std::cin >> t)) return 0;

    for (int i = 0; i < t; ++i) {
        std::string s;
        std::cin >> s;
        std::cout << check(s) << '\n';
    }

    return 0;
}