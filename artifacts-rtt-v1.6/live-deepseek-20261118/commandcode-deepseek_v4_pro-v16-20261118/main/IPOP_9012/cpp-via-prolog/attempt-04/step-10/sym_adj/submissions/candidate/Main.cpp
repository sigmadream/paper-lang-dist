#include <iostream>
#include <string>
#include <limits>

bool isValid(const std::string& s) {
    int balance = 0;
    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            if (balance <= 0) return false;
            --balance;
        }
        // 다른 문자는 무시 (문제는 소괄호만 주어짐)
    }
    return balance == 0;
}

int main() {
    int T;
    std::cin >> T;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    for (int i = 0; i < T; ++i) {
        std::string line;
        std::getline(std::cin, line);
        std::cout << (isValid(line) ? "YES" : "NO") << '\n';
    }
    return 0;
}