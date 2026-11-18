#include <iostream>
#include <string>

bool check(const std::string& s) {
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
    int T;
    std::cin >> T;
    std::cin.ignore();
    for (int i = 0; i < T; ++i) {
        std::string s;
        std::getline(std::cin, s);
        std::cout << (check(s) ? "YES" : "NO") << '\n';
    }
    return 0;
}