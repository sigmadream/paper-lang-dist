#include <iostream>
#include <string>

bool isValid(const std::string& s) {
    int balance = 0;
    for (char ch : s) {
        if (ch == '(') {
            ++balance;
        } else if (ch == ')') {
            if (balance == 0) return false;
            --balance;
        } else {
            return false;
        }
    }
    return balance == 0;
}

int main() {
    std::string line;
    std::getline(std::cin, line);
    int t = std::stoi(line);
    for (int i = 0; i < t; ++i) {
        std::string s;
        std::getline(std::cin, s);
        std::cout << (isValid(s) ? "YES" : "NO") << '\n';
    }
    return 0;
}