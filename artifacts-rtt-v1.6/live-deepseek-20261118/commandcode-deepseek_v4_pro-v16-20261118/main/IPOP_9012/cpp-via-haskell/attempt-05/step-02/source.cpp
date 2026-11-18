#include <iostream>
#include <string>

bool isValid(const std::string& s) {
    int bal = 0;
    for (char c : s) {
        if (c == '(') {
            ++bal;
        } else if (c == ')') {
            if (bal == 0) return false;
            --bal;
        } else {
            return false;
        }
    }
    return bal == 0;
}

int main() {
    std::string token;
    if (!(std::cin >> token)) {
        return 0;
    }
    int t = 0;
    bool validInt = false;
    try {
        std::size_t pos = 0;
        t = std::stoi(token, &pos);
        if (pos == token.size()) {
            validInt = true;
        }
    } catch (...) {
        validInt = false;
    }
    if (!validInt) {
        return 0;
    }
    for (int i = 0; i < t; ++i) {
        std::string s;
        if (!(std::cin >> s)) {
            break;
        }
        std::cout << (isValid(s) ? "YES" : "NO") << '\n';
    }
    return 0;
}