#include <iostream>
#include <string>

bool valid(const std::string& s) {
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
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t;
    if (!(std::cin >> t)) return 0;

    while (t--) {
        std::string s;
        std::cin >> s;
        std::cout << (valid(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}