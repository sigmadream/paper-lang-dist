#include <iostream>
#include <string>

bool isValid(const std::string& s) {
    int balance = 0;
    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            --balance;
            if (balance < 0) return false;
        }
    }
    return balance == 0;
}

int main() {
    int T;
    std::cin >> T;
    std::cin.ignore(); // consume newline after T
    std::string line;
    for (int i = 0; i < T; ++i) {
        std::getline(std::cin, line);
        if (!std::cin) break; // handle EOF
        std::cout << (isValid(line) ? "YES" : "NO") << '\n';
    }
    return 0;
}