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
        } else {
            return false;
        }
    }
    return balance == 0;
}

int main() {
    std::string tLine;
    if (!std::getline(std::cin, tLine)) return 0;

    int t = std::stoi(tLine);
    for (int i = 0; i < t; ++i) {
        std::string s;
        if (!std::getline(std::cin, s)) break;
        std::cout << (isValid(s) ? "YES" : "NO") << '\n';
    }
    return 0;
}