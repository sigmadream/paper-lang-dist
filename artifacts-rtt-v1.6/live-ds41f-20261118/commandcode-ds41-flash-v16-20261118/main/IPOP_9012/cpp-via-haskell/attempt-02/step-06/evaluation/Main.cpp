#include <iostream>
#include <string>

bool valid(const std::string& s) {
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
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t;
    if (!(std::cin >> t)) return 0;

    for (int i = 0; i < t; ++i) {
        std::string s;
        std::cin >> s;
        std::cout << (valid(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}