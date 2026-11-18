#include <iostream>
#include <string>

bool isBalanced(const std::string& str) {
    int balance = 0;
    for (char c : str) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            --balance;
            if (balance < 0) {
                return false;
            }
        } else {
            return false;
        }
    }
    return balance == 0;
}

int main() {
    int T;
    std::cin >> T;
    for (int i = 0; i < T; ++i) {
        std::string s;
        std::cin >> s;
        std::cout << (isBalanced(s) ? "YES" : "NO") << '\n';
    }
    return 0;
}