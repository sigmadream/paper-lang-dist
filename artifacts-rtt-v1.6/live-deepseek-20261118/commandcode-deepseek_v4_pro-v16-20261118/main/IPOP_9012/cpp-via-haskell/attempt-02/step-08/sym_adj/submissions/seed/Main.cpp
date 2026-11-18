#include <iostream>
#include <string>

bool isBalanced(const std::string& s) {
    int bal = 0;
    for (char c : s) {
        if (c == '(') {
            ++bal;
        } else if (c == ')') {
            if (bal > 0) --bal;
            else return false;
        } else {
            return false;
        }
    }
    return bal == 0;
}

int main() {
    std::string tStr;
    if (!(std::cin >> tStr)) return 0;

    int T;
    try {
        std::size_t pos;
        T = std::stoi(tStr, &pos);
        if (pos != tStr.size()) return 0;
    } catch (...) {
        return 0;
    }

    for (int i = 0; i < T; ++i) {
        std::string s;
        if (!(std::cin >> s)) break;
        std::cout << (isBalanced(s) ? "YES" : "NO") << '\n';
    }
    return 0;
}