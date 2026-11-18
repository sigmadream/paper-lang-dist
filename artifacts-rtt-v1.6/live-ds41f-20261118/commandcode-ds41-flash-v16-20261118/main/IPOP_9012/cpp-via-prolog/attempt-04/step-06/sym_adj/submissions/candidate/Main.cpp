#include <iostream>
#include <string>
#include <cctype>

static std::string trim(const std::string& s) {
    size_t start = 0;
    while (start < s.size() && std::isspace(static_cast<unsigned char>(s[start]))) {
        ++start;
    }
    size_t end = s.size();
    while (end > start && std::isspace(static_cast<unsigned char>(s[end - 1]))) {
        --end;
    }
    return s.substr(start, end - start);
}

static bool validParens(const std::string& s) {
    int balance = 0;
    for (unsigned char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            if (balance > 0) {
                --balance;
            } else {
                return false;
            }
        }
    }
    return balance == 0;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) {
        return 0;
    }
    std::string dummy;
    std::getline(std::cin, dummy);

    for (int i = 0; i < T; ++i) {
        std::string line;
        if (!std::getline(std::cin, line)) {
            break;
        }
        line = trim(line);
        std::cout << (validParens(line) ? "YES" : "NO") << '\n';
    }

    return 0;
}