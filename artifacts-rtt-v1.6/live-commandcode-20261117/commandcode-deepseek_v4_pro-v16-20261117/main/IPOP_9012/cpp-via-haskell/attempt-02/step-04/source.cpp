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
        }
    }
    return bal == 0;
}

int main() {
    int t;
    if (!(std::cin >> t)) return 0;
    for (int i = 0; i < t; ++i) {
        std::string s;
        if (!(std::cin >> s)) break;
        std::cout << (isValid(s) ? "YES" : "NO") << '\n';
    }
    return 0;
}