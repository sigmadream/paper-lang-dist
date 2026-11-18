#include <iostream>
#include <string>

bool isValid(const std::string& s) {
    int balance = 0;
    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            if (balance == 0) return false;
            --balance;
        }
    }
    return balance == 0;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    std::string s;
    for (int i = 0; i < T; ++i) {
        if (!(std::cin >> s)) break;
        std::cout << (isValid(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}