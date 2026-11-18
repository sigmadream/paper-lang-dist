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
    int T;
    if (!(std::cin >> T)) return 0;
    std::string s;
    for (int i = 0; i < T; ++i) {
        std::cin >> s;
        std::cout << (isBalanced(s) ? "YES" : "NO") << '\n';
    }
    return 0;
}